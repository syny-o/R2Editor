from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QPushButton

class ComparingWindow(QWidget):
    def __init__(self, parent, my_project_sys_rs_dictionary,
                 my_project_sys_ad_func_dictionary,
                 my_project_sys_ad_tech_dictionary,
                 my_project_dmt_dictionary,
                 another_project_sys_rs_dictionary,
                 another_project_sys_ad_func_dictionary,
                 another_project_sys_ad_tech_dictionary,
                 another_project_dmt_dictionary,
                 my_project_requirements_update_time,
                 another_project_requirements_update_time):
        super().__init__()

        # DEFINE FONT AND WINDOW RESOLUTION
        font = QFont()
        font.setPointSize(9)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.3)
        self.resize(1024, 768)

        # BUTTON LAYOUT
        layout_button = QHBoxLayout()
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)
        export_button = QPushButton('Export')
        layout_button.addWidget(export_button)
        layout_button.addWidget(close_button)
        layout_button.setAlignment(Qt.AlignRight)

        # CREATE WIDGETS AND LAYOUT
        tab_widget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(tab_widget)
        layout.addLayout(layout_button)
        self.setLayout(layout)

        # GET TIMESTAMPS FROM BOTH PROJECTS
        self.timestamp_my_project = my_project_requirements_update_time
        self.timestamp_another_project = another_project_requirements_update_time

        # GET PROJECTS PREFIXES FROM REQUIREMENTS --> CUSTOMER_PROJECT AND SET AS WINDOW TITLE
        self.prefix_my_project = self.get_prefix(my_project_sys_ad_func_dictionary)
        self.prefix_another_project = self.get_prefix(another_project_sys_ad_func_dictionary)
        self.setWindowTitle(self.prefix_my_project + f' ({self.timestamp_my_project})' + ' vs. '
                            + self.prefix_another_project + f' ({self.timestamp_another_project})')

        # COMPARE REQUIREMENTS
        text_sys_rs = self.final_compare(my_project_sys_rs_dictionary, another_project_sys_rs_dictionary)
        text_sys_ad_func = self.final_compare(my_project_sys_ad_func_dictionary, another_project_sys_ad_func_dictionary)
        text_sys_ad_tech = self.final_compare(my_project_sys_ad_tech_dictionary, another_project_sys_ad_tech_dictionary)
        # text_dmt = self.final_compare(my_project_dmt_dictionary, another_project_dmt_dictionary) --> realised that
        # different approach should have been used --> new method dmt_compare has been created
        text_dmt = self.dmt_compare(my_project_dmt_dictionary, another_project_dmt_dictionary)

        # DISPLAY RESULTS IN WIDGETS
        tab_widget.addTab(QTextEdit(text_sys_rs), 'SysRS')
        tab_widget.addTab(QTextEdit(text_sys_ad_func), 'SysAD - Functional Design')
        tab_widget.addTab(QTextEdit(text_sys_ad_tech), 'SysAD - Technical Design')
        tab_widget.addTab(QTextEdit(text_dmt), 'Diagnostic Monitor Table')

        # SET CUSTOM FONT
        for tab_index in range(tab_widget.count()):
            widget = tab_widget.widget(tab_index)
            widget.setFont(font)
            widget.setReadOnly(True)

    def dmt_compare(self, dict_dmt_my_project, dict_dmt_another_project):
        diffs = []
        text = ''
        for r_my, v_my in dict_dmt_my_project.items():
            for r_another, v_another in dict_dmt_another_project.items():
                # compare stripped keys --> (CUS1_PRJ1_)DMT_001 with (CUS2_PRJ2_)DMT_001
                if r_my.split('-')[-1] == r_another.split('-')[-1]: # if DMT_001 == DMT_001
                    if v_my != v_another: # values are different
                        diffs.append(r_my.split('-')[-1])

        if diffs:
            text += self.set_text_color('Following requirements have been changed: ', 'red') + str(diffs)

        else:
            text = 'No differences...'

        return text



    def final_compare(self, dict_my_project, dict_another_project):
        # 1. strip both key values to be same (EPB_CUSTOMER_PROJECT_SysRS12345 --> SysRS12345)
        dict_my_project_stripped = self.strip_requirements_ids(dict_my_project)
        dict_another_project_stripped = self.strip_requirements_ids(dict_another_project)
        # 2. get requirements which are unique for both projects
        requirements_only_in_my_project, requirements_only_in_another_project = \
            self.find_keys_differences(dict_my_project_stripped, dict_another_project_stripped)
        # 3. get requirements which texts differs
        requirements_texts_differences = self.find_values_differences(dict_my_project_stripped,
                                                                      dict_another_project_stripped)
        # 4. create text
        text = self.create_text(requirements_only_in_my_project, requirements_only_in_another_project,
                                requirements_texts_differences)
        if text == '':
            text = 'No differences...'
        return text

    def strip_requirements_ids(self, dictionary):
        """ strip requirements and filter them """
        dictionary_stripped = {}
        for r, v in dictionary.items():
            if v[2] == '04 Approved' and 'HIL' in v[3]:  # include only approved requirements and for HIL
                dictionary_stripped.update({r.split('-')[-1]: v[0]})
        return dictionary_stripped

    def get_prefix(self, dictionary):
        prefix = ''
        for k in dictionary.keys():
            prefix = k.rsplit('-', 1)[0]
            break
        return prefix

    def find_keys_differences(self, dictionary1, dictionary2):
        keys_values_only_dict1 = {}
        keys_values_only_dict2 = {}
        keys_only_dict1 = dictionary1.keys() - dictionary2.keys()
        for k in keys_only_dict1:
            v = dictionary1.get(k)
            keys_values_only_dict1.update({k: v})
        keys_only_dict2 = dictionary2.keys() - dictionary1.keys()
        for k in keys_only_dict2:
            v = dictionary2.get(k)
            keys_values_only_dict2.update({k: v})
        return keys_values_only_dict1, keys_values_only_dict2

    def find_values_differences(self, dictionary1, dictionary2):
        diff_values = []
        for k1, v1 in dictionary1.items():
            for k2, v2 in dictionary2.items():
                if k1 == k2:
                    # remove all whitespaces:
                    v1_new = "".join(v1.split())
                    v2_new = "".join(v2.split())

                    if v1_new.lower() != v2_new.lower():
                        diff_values.append((k1, v1, v2))
                        # d = difflib.Differ()
                        # a_lines = v1_new.splitlines()
                        # b_lines = v2_new.splitlines()
                        # diff = d.compare(a_lines, b_lines)
                        # print('\n'.join(diff))
                        # print(3*'\n')
        return diff_values

    def create_text(self, keys_only_my_project: dict, keys_only_another_project: dict, diff_values: list):
        text = ''
        if len(keys_only_my_project) > 0:
            text += self.set_text_color('FOLLOWING REQUIREMENTS ARE ONLY IN', 'red') + ' ' + \
                    self.set_text_color(self.prefix_my_project + ' (' + self.timestamp_my_project + ')', "red") + ':'
            text += '<br>'
            for k, v in keys_only_my_project.items():
                text += f'<div>{self.set_text_color(self.prefix_my_project + "-" + k, "#66a3ff;")}:</div><div>{v}</div>'
            text += 2 * '<br>'

        if len(keys_only_another_project) > 0:
            text += self.set_text_color('FOLLOWING REQUIREMENTS ARE ONLY IN', 'red') + ' ' + \
                    self.set_text_color(self.prefix_another_project + ' (' + self.timestamp_another_project + ')', 'red') + ':'
            text += '<br>'
            for k, v in keys_only_another_project.items():
                text += f'<div>{self.set_text_color(self.prefix_another_project + "-" + k, "#00cc00;")}:</div><div>{v}</div>'
            text += 2 * '<br>'

        if len(diff_values) > 0:
            text += self.set_text_color('FOLLOWING REQUIREMENTS HAVE DIFFERENT TEXTS: ', 'red')
            text += 2 * '<br>'
            for value in diff_values:
                text += f'{self.set_text_color(self.prefix_my_project + "-" + value[0] + " (" + self.timestamp_my_project  + ")", "#66a3ff;")}<div>{value[1]}</div>'
                text += 2 * '<br>'
                text += f'{self.set_text_color(self.prefix_another_project + "-" + value[0] +  " (" + self.timestamp_another_project + ")", "#00cc00;")}<div>{value[2]}</div>'
                text += 3 * '<br>'

        return text

    def set_text_color(self, text, color):
        return '<span style=" color:' + color + '" >' + text + '</span>'
