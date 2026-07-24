from data_manager.forms.form_doors_inputs import FormDoorsInputs
from data_manager.forms.form_req_data_comparasion import FormReqDataComparasion
from data_manager.nodes.requirement_module import RequirementModule
from data_manager import tree_walker
from dialogs.dialog_message import dialog_message
from doors.doors_connection import DoorsConnection


class DoorsActions:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def open_inputs_form(self, all_modules):
        manager = self.data_manager
        if manager._module_locker.locked_modules:
            dialog_message(
                manager,
                'Requirements are being downloaded from Doors. '
                'Please wait...',
            )
            return

        if not tree_walker.at_least_one_module_is_present(manager.ROOT):
            manager._open_add_requirement_module_form()
            return

        manager.form_doors_inputs = FormDoorsInputs(manager, all_modules)

    def receive_inputs(
        self,
        all_modules,
        app_path,
        database_path,
        user_name,
        password,
    ):
        manager = self.data_manager
        if all_modules:
            for row in range(manager.ROOT.rowCount()):
                node = manager.ROOT.child(row)
                if isinstance(node, RequirementModule):
                    manager._module_locker.lock_module(node)
        else:
            selected_item = manager.MODEL.itemFromIndex(
                manager.TREE.currentIndex()
            )
            if isinstance(selected_item, RequirementModule):
                manager._module_locker.lock_module(selected_item)

        modules = manager._module_locker.locked_modules
        module_paths = [node.path for node in modules]
        columns_names = [node.columns_names for node in modules]
        baselines = [node.current_baseline for node in modules]
        if module_paths and columns_names and baselines:
            self._send_request(
                app_path,
                database_path,
                user_name,
                password,
                module_paths,
                columns_names,
                baselines,
            )

    def receive_data(self, doors_output, timestamp):
        manager = self.data_manager
        comparison_data = {}
        success = True

        error_messages = {
            'Connection Failed': (
                'Connecting to Doors Failed.\n\nPossible reasons:\n'
                '1. Invalid username/password\n'
                '2. Doors client is N/A\n'
                '3. Network issues.'
            ),
            'Doors Application not found': (
                'Doors Application (doors.exe) not found, '
                'check the path in the settings!'
            ),
        }
        if doors_output in error_messages:
            success = False
            dialog_message(manager, error_messages[doors_output])
        else:
            for module in manager._module_locker.locked_modules:
                module_success, message_or_data = (
                    module.receive_data_from_doors(doors_output, timestamp)
                )
                if not module_success:
                    success = False
                    dialog_message(manager, message_or_data)
                    break

                manager.set_project_saved(False)
                if message_or_data:
                    try:
                        comparison_data[module.path] = message_or_data
                    except Exception as exception:
                        dialog_message(manager, str(exception))

        manager._module_locker.unlock_all_modules()
        manager._update_data_summary()
        manager.uiBtnCheckCoverage.setEnabled(True)
        if success:
            manager.form_comparasion = FormReqDataComparasion(comparison_data)

    def _send_request(
        self,
        app_path,
        database_path,
        user_name,
        password,
        module_paths,
        columns_names,
        baselines,
    ):
        manager = self.data_manager
        DoorsConnection(
            manager,
            app_path,
            database_path,
            user_name,
            password,
            module_paths,
            columns_names,
            baselines,
        )
        manager.update_progress_status(True, 'Initialising...')
        manager.uiBtnCheckCoverage.setEnabled(False)
