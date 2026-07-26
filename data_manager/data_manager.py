from pathlib import Path
from ui.model_editor_ui import Ui_Form
from PyQt5.QtWidgets import QWidget, QShortcut
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QThreadPool
from data_manager.completer_data import send_data_to_completer
from components.module_locker import ModuleLocker
from data_manager.view.widget_view import View
from components.widgets.chart_bar import ChartBar
from config.icon_manager import IconManager
from data_manager.node_actions import NodeActions
from data_manager.doors.actions import DoorsActions
from data_manager.project_data_controller import ProjectDataController
from data_manager.coverage.controller import CoverageController
from data_manager.reference_navigator import ReferenceNavigator
from data_manager.html_report.controller import HtmlReportController
from data_manager.a2l.actions import A2lActions
from data_manager.requirements.module_actions import RequirementModuleActions


class DataManager(QWidget, Ui_Form):

    send_file_path = pyqtSignal(Path)

    def __init__(self, main_window, project_manager):
        super().__init__()
        self.setupUi(self)
        self.uiBtnCheckCoverage.setIcon(IconManager().ICON_CHECK_COVERAGE)
        self.uiBtnCheckHtmlReport.setIcon(IconManager().ICON_CHECK_REPORT)
        self.uiBtnNewModule.setIcon(IconManager().ICON_NEW_MODULE)
        self.uiBtnUpdateRequirements.setIcon(IconManager().ICON_UPDATE_REQUIREMENTS)
        self.uiBtnSetProjectPath.setIcon(IconManager().ICON_SET_PROJECT_FOLDER)


        self.MAIN = main_window
        self.PROJECT_MANAGER = project_manager     
        self.MODEL = QStandardItemModel()
        self.ROOT = self.MODEL.invisibleRootItem()        
        self.ROOT.setData(self, Qt.UserRole)  # add pointer to DataManager instance to be accesseble from child nodes (ReqNode, CondNode, ...)

        self.send_file_path.connect(self.MAIN.document_actions.open_path)

        self.VIEW = View(self, self.MODEL)
        self.ui_layout_tree.addWidget(self.VIEW)
        self.TREE = self.VIEW.uiDataTreeView  # TODO: REFACTOR
        self.node_actions = NodeActions(self)
        self.doors_actions = DoorsActions(self)
        self.project_data_controller = ProjectDataController(self)
        self.coverage_controller = CoverageController(self)
        self.reference_navigator = ReferenceNavigator(self)
        self.html_report_controller = HtmlReportController(self)
        self.a2l_actions = A2lActions(self)
        self.requirement_module_actions = RequirementModuleActions(self)

        self.widget_chart = ChartBar()
        self.ui_layout_data_summary.addWidget(self.widget_chart)

        # self.MODEL.itemChanged.connect(lambda: self.set_project_saved(False))
        self.MODEL.rowsInserted.connect(lambda: self.set_project_saved(False))
        self.MODEL.rowsRemoved.connect(lambda: self.set_project_saved(False))

        # ALL BUTTONS
        self.uiBtnUpdateRequirements.clicked.connect(lambda: self._open_form_for_doors_connection_inputs(all_modules=True))
        self.uiBtnNewModule.clicked.connect(self._open_add_requirement_module_form)
        self.uiBtnCheckCoverage.clicked.connect(self._create_dict_from_scripts_for_coverage_check)
        self.uiBtnCheckHtmlReport.clicked.connect(self.check_HTML_report)
        self.uiBtnSetProjectPath.clicked.connect(self._set_project_path)

        # POINTER TO REQ MODULE(S) WHICH ARE DOWNLOADING
        # self._currently_downloaded_modules = []
        self._module_locker = ModuleLocker()

        # SPECIAL THREAD FOR BROWSING HDD AND GETTING DATA FOR COVERAGE CHECK
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)  

        QShortcut('Ctrl+S', self).activated.connect(
            self.MAIN.project_actions.save
        )


    def goto_index(self, index):
        self.TREE.setCurrentIndex(index)
        self.TREE.scrollTo(index)
        self.TREE.expand(index)
 
     

    @pyqtSlot(bool, str)
    def update_progress_status(self, is_visible, text=''):
        self.MAIN.uiLabelProgressStatus.setText(text) if is_visible else self.MAIN.uiLabelProgressStatus.setText("Ready")
        self.MAIN.uiLabelProgressStatus.setStyleSheet("color: rgb(50, 250, 50);") if is_visible else self.MAIN.uiLabelProgressStatus.setStyleSheet("color: rgb(200, 200, 200);")


    def receive_data_from_drop_or_file_manager(self, data):
        self.project_data_controller.import_files(data)


    ################################################################################################
    #  PROJECT HANDLING
    ################################################################################################

    def _set_project_path(self):
        return self.project_data_controller.choose_project_path()
    

    # @interface --> PROJECT MANAGER
    def set_project_saved(self, is_modified: bool) -> None:
        self.project_data_controller.set_project_saved(is_modified)


    @pyqtSlot(dict)
    def receive_data_from_project_manager(self, data: dict):
        self.project_data_controller.receive_project_data(data)


    @pyqtSlot(dict)
    def receive_parameters_from_project_manager(self, parameters: dict):
        self.project_data_controller.receive_project_parameters(parameters)


    @pyqtSlot(dict)
    def provide_data_4_project_manager(self):
        return self.project_data_controller.provide_project_data()


    #####################################################################################################################################################
    #   ADDING REQUIREMENT MODULE
    #####################################################################################################################################################

    def _open_add_requirement_module_form(self):
        self.requirement_module_actions.open_add_form()

    @pyqtSlot(str, list)
    def receive_data_from_add_req_module_dialog(self, module_path, columns_names):
        self.requirement_module_actions.add_module(
            module_path,
            columns_names,
        )

    #####################################################################################################################################################
    #   CONNECTING AND DOWNLOADING DATA FROM DOORS
    #####################################################################################################################################################        

    def _open_form_for_doors_connection_inputs(self, all_modules: bool) -> None:  # Button Update All Requirements or Update Module Context Menu
        self.doors_actions.open_inputs_form(all_modules)


    @pyqtSlot(bool, str, str, str, str)
    def receive_inputs_from_doors_connection_form(self, all_modules, app_path, database_path, user_name, password):
        self.doors_actions.receive_inputs(
            all_modules,
            app_path,
            database_path,
            user_name,
            password,
        )


    #####################################################################################################################################################
    #   RECEIVING DATA FROM DOORS
    ##################################################################################################################################################### 

    @pyqtSlot(str, str)
    def receive_data_from_doors(self, doors_output: str, timestamp: str):
        self.doors_actions.receive_data(doors_output, timestamp)


    #####################################################################################################################################################
    #   UPDATING COVERAGE BY EDITING SCRIPT IN EDITOR
    #####################################################################################################################################################

    @pyqtSlot(set, str)
    def script_requirement_reference_changed(self, req_references: set[str], script_path: str):
        self.coverage_controller.script_references_changed(
            req_references,
            script_path,
        )


    #####################################################################################################################################################
    #   PHYSICAL COVERAGE CHECK
    #####################################################################################################################################################
    def _create_dict_from_scripts_for_coverage_check(self): # PushButton Check Coverage clicked
        self.coverage_controller.start_physical_check()


    @pyqtSlot(dict)
    def check_coverage(self, file_content_dict: dict):
        self.coverage_controller.apply_physical_check(file_content_dict)



    #####################################################################################################################################################
    #   UPDATE DATA SUMMARY
    #####################################################################################################################################################
    def _update_data_summary(self):        
        self.coverage_controller.update_summary()
    


    ##############################################################################################################################
    # IGNORE LIST:
    ##############################################################################################################################

    def _add_to_ignore_list(self):
        self.coverage_controller.add_selected_to_ignore_list()

    def _remove_from_ignore_list(self):
        self.coverage_controller.remove_selected_from_ignore_list()


    ####################################################################################################################
    # LIST WIDGETS CLICKS/HOVER MANAGEMENT  
    ####################################################################################################################

    def _get_tooltip_from_link(self, link):
        return self.reference_navigator.tooltip_from_link(link)



    def set_tooltip_2_list_widget_item(self, item):
        self.reference_navigator.set_item_tooltip(item)
              

              

    def _doubleclick_on_identifier(self, item):
        self.reference_navigator.go_to_identifier(item)


    def _doubleclick_on_outlink(self, outlink_item):
        self.reference_navigator.follow_outlink(outlink_item)




    def _doubleclick_on_tc_reference(self, list_item_text):
        self.reference_navigator.open_script_reference(list_item_text)




    

    ####################################################################################################################
    # A2L NORMALISATIION:
    ####################################################################################################################
    def _normalise_a2l_file(self):
        self.a2l_actions.normalize_selected_file()


    @pyqtSlot(dict, list, list)
    def a2l_normalisation_finished(self, data_4_report, missing_signals, duplicated_signals):
        self.a2l_actions.show_normalization_report(
            data_4_report,
            missing_signals,
            duplicated_signals,
        )



    ####################################################################################################################
    # ADDING / MODIFYING / REMOVING / EXPORTING NODES DATA:
    ####################################################################################################################


    def tree_2_file(self):
        self.node_actions.export()
        

    def remove_node(self):
        self.node_actions.remove()
        

    def duplicate_node(self):
        self.node_actions.duplicate()

    def copy_node(self):
        self.node_actions.copy()


    def paste_node(self):
        self.node_actions.paste()


    def edit_node_request(self):
        self.node_actions.request_edit()
    
    
    @pyqtSlot()
    def edit_node_response(self):
        self.node_actions.edit_response()


    def move_node(self, direction):
        self.node_actions.move(direction)




    ####################################################################################################################
    # COMPLETER:
    ####################################################################################################################

    def send_data_2_completer(self):
        send_data_to_completer(self.ROOT)
        self._update_data_summary()


    ####################################################################################################################
    # HTML REPORT CHECK:
    ####################################################################################################################
    
    def check_HTML_report(self):
        self.html_report_controller.check_report()

    @pyqtSlot(str)
    def doubleclicked_on_requirement_in_HTML_report_form(self, req_identifier: str):
        self.html_report_controller.go_to_requirement(req_identifier)
