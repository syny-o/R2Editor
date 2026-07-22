import os
from weakref import WeakSet
from PyQt5.QtWidgets import QPlainTextEdit, QToolTip

from text_editor.code_editor import CodeEditor
import text_editor.text_management as text_management

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QTextCursor, QStandardItem, QStandardItemModel, QPalette, QColor


from config.font import font

from text_editor.completer import Completer
from text_editor.text_edit_tooltip_widget import TextEditTooltipWidget
from text_editor.data_manager_widget import DataManagerWidget

from components.text_functions import get_word_under_cursor

from components.syntax_highlighter.i_syntax_highlighter import ISyntaxHighlighter


class TextEdit(CodeEditor):

    font = font

    instances = WeakSet()

    # SIGNAL FOR HANDLING PRESSING MOUSE AT TEXTEDIT
    signal_clicked_on_text_edit = pyqtSignal(object)
    signal_modified_file_content = pyqtSignal(object, bool)
    signal_scroll_position_changed = pyqtSignal(object, int)
    signal_send_outline = pyqtSignal(list)

    
    @classmethod
    def append_child(cls, child):
        cls.instances.add(child)

    @classmethod
    def set_font_to_all_children(cls):
        for ch in cls.instances:
            ch.setFont(cls.font)

    def update_ctrl_pressed(self, is_pressed):
        self.ctrl_pressed = is_pressed


    def __init__(self, main_window, text, file_path, syntax_highlighter: ISyntaxHighlighter):
        super().__init__(text)
        self.main_window = main_window
        self.ctrl_pressed = False

        TextEdit.append_child(self)

        slider = self.verticalScrollBar()
        slider.valueChanged.connect(
            lambda value: self.signal_scroll_position_changed.emit(self, value)
        )


        palette = QPalette()
        palette.setColor(QPalette.HighlightedText, QColor("white"))
        palette.setColor(QPalette.Highlight, QColor("blue"))
        self.setPalette(palette)

        self.file_path = file_path
        self.original_file_content = text
        self.file_was_modified = False


        self.update_syntax_highlighter(syntax_highlighter)

        if self.file_path:
            self.is_read_only = not(os.access(self.file_path, os.W_OK))
        else:
            self.is_read_only = False
        

        # self.font = font
        self.setFont(TextEdit.font)
        


        # DEFINE TEXT EDIT BEHAVIOR
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setTabStopDistance(14)
        self.setMouseTracking(True)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)


        # CONNECT REQUIRED SIGNALS
        self.signal_clicked_on_text_edit.connect(main_window.clicked_on_text_edit)
        self.signal_modified_file_content.connect(main_window.set_tab_modified_icon)
        self.signal_scroll_position_changed.connect(main_window.update_selected_item_in_outline_by_scrollbar)
        self.document().modificationChanged.connect(self._on_modification_changed)
        self.document().setModified(False)
        # self.textChanged.connect(self.main_window.update_outline)

        # self.signal_send_outline.connect(main_window.get_outline)
        # self.cursorPositionChanged.connect(self.send_outline)
        # self.cursorPositionChanged.connect(lambda: print("Hello"))




        # CONNECT COMPLETER - INSTANCE CONFIGURATION
        self.completer = Completer(self.main_window)
        self.completer.setWidget(self)
        self.completer.insert_text.connect(self.insert_completion)
        self.current_model = None




        self.actual_text = ''

        
        self.tooltips = Completer.cond_tooltips
        
        self.scroll_bar = self.verticalScrollBar()

        self.remember_special_char = False

        self.data_manager_widget = DataManagerWidget(self.main_window, self)


    def update_syntax_highlighter(self, syntax_highlighter: ISyntaxHighlighter):
        if self.main_window.app_settings.theme == 'Dark':
            self.syntax_highlighter = syntax_highlighter(self.document(), dark_mode=True)
        else:
            self.syntax_highlighter = syntax_highlighter(self.document(), dark_mode=False)
        

    def mouseMoveEvent(self, event):
        # CREATE INSTANCE OF TEXT CURSOR
        self.viewport().setCursor(Qt.IBeamCursor)
        tc = self.textCursor()
        if tc.selectedText() == '' and self.ctrl_pressed:
            # SAVE CURRENT SCROLLBAR POSITION
            scroll_pos = self.scroll_bar.value()

            # IF THERE IS NO SELECTED TEXT
            isStartOfWord = False
            tc_original_pos = tc.position()
            text_cursor = self.cursorForPosition(event.pos())
            text_cursor.select(QTextCursor.WordUnderCursor)
            if text_cursor.selectedText() == "":
                return

            is_end_of_word = False
            while not is_end_of_word:
                text_cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
                if text_cursor.atEnd() or text_cursor.atBlockEnd():
                    is_end_of_word = True
                if text_cursor.selectedText().endswith((" ", "\n", "\t", "=", ",", '"')):
                    text_cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
                    is_end_of_word = True


            self.setTextCursor(text_cursor)
            word = text_cursor.selectedText().strip()

            # print(f"***{word}***")

            if word in self.tooltips and self.ctrl_pressed:
                content = ""
                
                values_dict = self.tooltips[word]

                if type(values_dict) == str:
                    # self.show_tooltip(values_dict)
                    TextEditTooltipWidget.selected_word = values_dict

                else:
                    
                    for k, v in values_dict.items():
                        ts_content = ""
                        for ts in v:
                            ts_content += f"""
                                <li><font size=3 color=white>{ts}</font></li>
                            """
                        content += f"<font size=4 color=lightblue>{k:}</font><ol>{ts_content}</ol>"
                    
                    # self.show_tooltip(content)
                    
                    TextEditTooltipWidget.selected_word = content

                self.viewport().setCursor(Qt.PointingHandCursor)

            else:
                QToolTip.hideText()
                self.viewport().setCursor(Qt.IBeamCursor)
                TextEditTooltipWidget.selected_word = None
            # SET BACK THE TEXT CURSOR POSITION AND SCROLLBAR POSITION
            tc.setPosition(tc_original_pos)
            self.setTextCursor(tc)
            self.scroll_bar.setValue(scroll_pos)

        super().mouseMoveEvent(event)



    # def mousePressEvent(self, event):
    #     self.signal_clicked_on_text_edit.emit(self)        
    #     return super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        self.signal_clicked_on_text_edit.emit(self) 
        self.completer.completer_tooltip.hide_tooltip()
        if TextEditTooltipWidget.selected_word and self.ctrl_pressed:
            self.show_tooltip(TextEditTooltipWidget.selected_word)

        return super().mouseReleaseEvent(event)        


    def show_tooltip(self, tooltip_text):
        if self.tooltips:
            self.w = TextEditTooltipWidget(self.main_window, self, tooltip_text)


    def show_conditions_in_tooltip(self):
        new_list = [k for k, v in self.tooltips.items() if type(v) is dict]
        content = '<html><body><p align="center">'
        content += f'{"<font size=12 color=lightblue> - </font>".join(sorted(new_list))}'
        content += '</p></body></html>'
        self.show_tooltip(content)


    def is_modified(self):
        return self.document().isModified()


    def _on_modification_changed(self, is_modified):
        self.file_was_modified = is_modified
        self.signal_modified_file_content.emit(self, is_modified)


    def update_completion_context(self):




########################################################################################################################
# START COMPLETER
########################################################################################################################

        self.actual_text = self.get_actual_text()
        self.evaluate_actual_text()

########################################################################################################################
# KEYS MANAGEMENT
########################################################################################################################

    def keyReleaseEvent(self, event):
        self.signal_clicked_on_text_edit.emit(self)
        self.update_completion_context()
        if event.key() not in (Qt.Key_Up, Qt.Key_Down):
            self.completer.completer_tooltip.hide_tooltip()
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = False
        return super().keyReleaseEvent(event)

    def _handle_basic_editing_key(self, event):
        key = event.key()

        if key == Qt.Key_Control:
            self.ctrl_pressed = True
            return True

        if key == Qt.Key_Escape:
            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)

        if key == Qt.Key_Return and self.completer.popup().isVisible():
            self.completer.insert_text.emit(self.completer.get_selected())
            return True

        if key == Qt.Key_Return:
            text_management.add_new_line_indent(self)
            return True

        if key == Qt.Key_Backtab:
            text_management.indent_dedent_comment(self, variant='dedent')
            return True

        if key == Qt.Key_Tab:
            text_management.indent_dedent_comment(self, variant='indent')
            return True

        if event.modifiers() & Qt.ShiftModifier and key == Qt.Key_Home:
            text_management.key_shift_home_press(self)
            return True

        if key == Qt.Key_Home:
            text_management.key_home_press(self)
            return True

        if key == Qt.Key_Equal and self.current_model == 'values':
            self.textCursor().insertText('=')
            self.show_popup('')
            return True

        return False

    def _show_completion_for_cursor(self, cursor, empty_prefix_models):
        selected_text = cursor.selectedText()
        if (
            not selected_text
            and (
                not cursor.block().text().strip()
                or self.current_model in empty_prefix_models
            )
        ):
            self.show_popup("")
            return

        special_prefixes = {
            '"': (' "', 2),
            ',': (' ,', 2),
            ')': (' )"', 3),
        }
        for prefix, (replacement, move_left) in special_prefixes.items():
            if selected_text.startswith(prefix):
                self.remember_special_char = True
                cursor.insertText(replacement)
                cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, move_left)
                self.setTextCursor(cursor)
                cursor.select(QTextCursor.WordUnderCursor)
                self.show_popup(cursor.selectedText())
                return

        if selected_text:
            self.show_popup(selected_text)
        else:
            self.completer.popup().hide()

    def _handle_visible_completion(self, event):
        if not self.completer.popup().isVisible():
            return False
        if event.key() in (Qt.Key_Return, Qt.Key_Equal, Qt.Key_Alt):
            return False

        cursor = self.textCursor()
        super().keyPressEvent(event)
        get_word_under_cursor(cursor)
        self._show_completion_for_cursor(cursor, {"values", "pbc_variables"})
        return True

    def _handle_alt_completion(self, event):
        if event.key() != Qt.Key_Alt:
            return False

        if self.completer.popup().isVisible():
            self.completer.popup().hide()
            return False

        cursor = self.textCursor()
        get_word_under_cursor(cursor)
        self._show_completion_for_cursor(
            cursor, {"values", "pbc_variables", "dspace_variables"}
        )
        return True

    def keyPressEvent(self, event):
        QToolTip.hideText()

        if self._handle_basic_editing_key(event):
            return
        if self._handle_visible_completion(event):
            return
        if self._handle_alt_completion(event):
            return

        if event.key() not in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Return):
            self.completer.popup().hide()

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_S:
            self.update_ctrl_pressed(False)

        super().keyPressEvent(event)



########################################################################################################################
# COMPLETION MANAGEMENT
########################################################################################################################


    def insert_completion(self, completion):
        tc = self.textCursor()
        get_word_under_cursor(tc)
        tc.insertText(completion)

        if self.remember_special_char:
            self.remember_special_char = False
            tc.deleteChar()
        self.setTextCursor(tc)

        self.add_space_to_equal()
        self.complete_special_command()
        if not QToolTip.isVisible():
            self.completer.popup().hide()



    def show_popup(self, completion_prefix):
        self.completer.setCompletionPrefix(completion_prefix)
        cr = self.cursorRect()
        self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0)) # automatically select first popup item
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                    + self.completer.popup().verticalScrollBar().sizeHint().width() + 20)
        self.completer.complete(cr)

    # def focusInEvent(self, event):
    #     if self.completer:
    #         self.completer.setWidget(self)
    #     QPlainTextEdit.focusInEvent(self, event)

########################################################################################################################
# ACTUAL TEXT MANAGEMENT
########################################################################################################################

    def get_actual_text(self):
        if self.textCursor().hasSelection():
            return ""
        pos = self.textCursor().position()
        pos_in_block = self.textCursor().positionInBlock()
        self.moveCursor(QTextCursor.StartOfLine)
        line_text = self.textCursor().block().text()
        actual_text = line_text[:pos_in_block]
        cursor = QTextCursor(self.textCursor())
        cursor.setPosition(pos)
        self.setTextCursor(cursor)
        actual_text = actual_text.split('=')[0]
        actual_text = actual_text.strip()


        return actual_text


    def evaluate_actual_text(self):
        if self.actual_text == 'MonitorVariablesCANape' \
                or self.actual_text == 'MonitorVariablesCanape' \
                or self.actual_text == 'VariableSequence' \
                or self.actual_text == 'CANapeCommand':
            self.switch_to_pbc_variables()
        elif self.actual_text == 'GraphVariables':
            self.switch_to_graph_variables()
        elif self.actual_text == 'MonitorVariables':
            self.switch_to_dspace_variables()
        elif self.completer.cond_model and (self.actual_text in self.completer.cond_dict):
            self.switch_to_values()
        else:
            self.switch_to_conditions()


########################################################################################################################
# SPECIAL TEXT MANAGEMENT (" = ", MonitorVariables, CANapeCommand, VariableSequence etc.)
########################################################################################################################

    def add_space_to_equal(self):
        tc = self.textCursor()
        line_text = tc.block().text()
        line_text = line_text.rstrip()
        # print(line_text)
        splitted_line_text_list = line_text.split('=')
        # print(splitted_line_text_list)
        if (len(splitted_line_text_list) > 1) \
                and not (line_text.strip().startswith('MonitorVariablesCANape')) \
                and not (line_text.strip().startswith('MonitorVariablesCanape')) \
                and not (line_text.strip().startswith('MonitorVariables')) \
                and not (line_text.strip().startswith('GraphVariables')) \
                and not (line_text.strip().startswith('VariableSequence')) \
                and not (line_text.strip().startswith('CANapeCommand')):

            tc.select(tc.LineUnderCursor)
            tc.removeSelectedText()
            self.insertPlainText(splitted_line_text_list[0].rstrip() + ' = ' + splitted_line_text_list[1].strip())


    def complete_special_command(self):
        tc = self.textCursor()
        line_text = tc.block().text()

        if line_text.strip() == 'MonitorVariablesCANape' or line_text.strip() == 'MonitorVariablesCanape' or line_text.strip() == 'MonitorVariables':
            command = line_text.strip()
            tc.select(tc.LineUnderCursor)
            tc.removeSelectedText()
            self.insertPlainText(line_text + ' = ", 100000, 10"')
            for letter in range(13):
                tc.movePosition(QTextCursor.Left)
            self.setTextCursor(tc)

            # SHOW TOOLTIP / HINT IN CONSOLE
            self.completer.popup().hide()
            # self.show_tooltip(self.tooltips['MonitorVariablesCANape'])



        elif line_text.strip() == 'GraphVariables':
            command = line_text.strip()
            tc.select(tc.LineUnderCursor)
            tc.removeSelectedText()
            self.insertPlainText(line_text + ' = ""')
            for letter in range(1):
                tc.movePosition(QTextCursor.Left)
            self.setTextCursor(tc)

            # SHOW TOOLTIP / HINT IN CONSOLE
            self.completer.popup().hide()
            # self.show_tooltip(self.tooltips['GraphVariables'])


        elif line_text.strip() == 'VariableRisingInRange' \
            or line_text.strip() == 'VariableDroppingInRange' \
            or line_text.strip() == 'VariableRisingChanges' \
            or line_text.strip() == 'VariableDroppingChanges' \
            or line_text.strip() == 'VariableMaxInRange' \
            or line_text.strip() == 'VariableMinInRange':
            command = line_text.strip()
            tc.select(tc.LineUnderCursor)
            tc.removeSelectedText()
            self.insertPlainText(line_text + ' = ""')
            for letter in range(1):
                tc.movePosition(QTextCursor.Left)
            self.setTextCursor(tc)

            # SHOW TOOLTIP / HINT IN CONSOLE
            self.completer.popup().hide()
            # self.show_tooltip(self.tooltips[command])




        elif line_text.strip() == 'CANapeCommand':
            command = line_text.strip()
            tc.select(tc.LineUnderCursor)
            tc.removeSelectedText()
            self.insertPlainText(line_text + ' = "CANape_GetObjectValue()"')
            for letter in range(2):
                tc.movePosition(QTextCursor.Left)
            self.setTextCursor(tc)

            # SHOW TOOLTIP / HINT IN CONSOLE
            self.completer.popup().hide()
            # self.show_tooltip(self.tooltips['CANape_GetObjectValue'])


        elif line_text.strip() == 'VariableSequence':
            command = line_text.strip()
            tc.select(tc.LineUnderCursor)
            tc.removeSelectedText()
            self.insertPlainText(line_text + ' = ""')
            tc.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor)
            self.setTextCursor(tc)

            # SHOW TOOLTIP / HINT IN CONSOLE
            self.completer.popup().hide()
            # self.show_tooltip(self.tooltips['VariableSequence'])



########################################################################################################################
# MODEL MANAGEMENT
########################################################################################################################


    def switch_to_values(self):
        if self.completer.cond_model:
            self.current_model = 'values'
            key = self.actual_text
            # print("key==="+key+"===")
            self.completer.setModel(self.completer.cond_dict.get(key))
        else:
            self.completer.setModel(QStandardItemModel())

    def switch_to_conditions(self):
        self.current_model = 'conditions'
        if self.completer.cond_model:
            self.completer.setModel(self.completer.cond_model)
        else:
            self.completer.setModel(QStandardItemModel())


    def switch_to_pbc_variables(self):
        self.current_model = 'pbc_variables'
        if self.completer.a2l_model:
            self.completer.setModel(self.completer.a2l_model)
        else:
            self.completer.setModel(QStandardItemModel())

    def switch_to_dspace_variables(self):
        self.current_model = 'dspace_variables'
        if self.completer.dspace_model:
            self.completer.setModel(self.completer.dspace_model)
        else:
            self.completer.setModel(QStandardItemModel())

    def switch_to_graph_variables(self):
        variables = text_management.evaluate_data_4_GraphVariables(self)
        variables_model = QStandardItemModel()
        for v in variables:
            item = QStandardItem()
            item.setData(v, Qt.ToolTipRole)
            item.setData(v, Qt.DisplayRole)
            variables_model.appendRow(item)
        self.completer.setModel(variables_model)

    
########################################################################################################################
# ZOOMING (FONT ADJUSTING)
########################################################################################################################


    def font_increase(self):
        point_size = TextEdit.font.pointSize()
        if point_size < 20:
            TextEdit.font.setPointSize(point_size+1)
            TextEdit.set_font_to_all_children()
        return

    def font_decrease(self):
        point_size = TextEdit.font.pointSize()
        if point_size > 6:
            TextEdit.font.setPointSize(point_size-1)
            TextEdit.set_font_to_all_children()
        return        



    def font_reset(self):        
        TextEdit.font.setPointSize(10)         
        TextEdit.set_font_to_all_children()
        return     
