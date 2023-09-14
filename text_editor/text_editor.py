import os
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QToolTip, QStyledItemDelegate, QStyleOptionViewItem, QMessageBox, QApplication, QPushButton, QToolBar, QVBoxLayout, QTextEdit
import importlib
from text_editor.code_editor import QCodeEditor
import text_editor.text_management as text_management

from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QPoint, QModelIndex, QStringListModel, QTimer
from PyQt5.QtGui import QFont, QTextCursor, QStandardItem, QStandardItemModel, QIcon, QPainter, QPixmap, QImage, QScreen

from text_editor.syntax_highlighter import Highlighter

from config.font import font

from text_editor.completer import Completer

from text_editor.tooltips import tooltips

class MyWidget(QWidget):
    selected_word = None
    is_visible = False
    

    def __init__(self, parent, text):
        super().__init__()
        MyWidget.is_visible = True

        TextEdit.shift_pressed = False


        self.setWindowFlags(Qt.Popup)
        
        # self.setWindowOpacity(0.95)
        self.setMaximumSize(1024, 768)
        self.setMinimumSize(640, 480)

        self.resize(*self.calculate_size(text))

        
        

        self.setStyleSheet("color: #edf; background-color: #222; font-size: 14px;")

        btn = QPushButton(QIcon(u"ui/icons/check.png"), "Back")
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.close)

        toolbar = QToolBar()
        toolbar.addWidget(btn)


        # self.te = QTextEdit()
        self.te = QTextEdit()
        self.te.setReadOnly(True)
        l = QVBoxLayout()
        l.addWidget(self.te)
        l.addWidget(toolbar)

        l.setSpacing(20)
        l.setContentsMargins(20, 20, 20, 20)
        
        self.setLayout(l)

        # print(QDesktopWidget.primaryScreen())

        centerPoint = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())
        self.te.append(text)
        self.show()    


    def calculate_size(self, text):
        lines = text.splitlines()
        longest_line = 0
        for line in lines:
            if len(line) > longest_line:
                longest_line = len(line)
        
        if len(lines) < 5:
            return longest_line*5, len(lines) * 300

        return longest_line*5, len(lines) * 30


    def closeEvent(self, e):
        MyWidget.is_visible = False
        return super().closeEvent(e)


class TextEdit(QCodeEditor):

    shift_pressed = False

    font = font

    children = []

    # SIGNAL FOR HANDLING PRESSING MOUSE AT TEXTEDIT
    signal_clicked_on_text_edit = pyqtSignal(object)
    signal_modified_file_content = pyqtSignal(bool)

    
    @classmethod
    def append_child(cls, child):
        cls.children.append(child)

    @classmethod
    def set_font_to_all_children(cls):
        for ch in cls.children:
            ch.setFont(cls.font)


    def __init__(self, main_window=None, text=None, file_path=None):
        super().__init__(text)

        TextEdit.append_child(self)

        self.file_path = file_path
        self.original_file_content = text
        self.file_was_modified = False



        if self.file_path:
            self.is_read_only = not(os.access(self.file_path, os.W_OK))
        else:
            self.is_read_only = False
        
        self.main_window = main_window

        # self.font = font
        self.setFont(TextEdit.font)
        


        # DEFINE TEXT EDIT BEHAVIOR
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setTabStopWidth(14)
        self.setMouseTracking(True)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)


        # CONNECT REQUIRED SIGNALS
        self.signal_clicked_on_text_edit.connect(main_window.clicked_on_text_edit)
        self.signal_modified_file_content.connect(main_window.set_actual_tab_icon)
        self.textChanged.connect(self.text_changed)


        # CONNECT SYNTAX HIGHLIGHTER
        self.highlighter = Highlighter(self.document())

        # CONNECT COMPLETER - INSTANCE CONFIGURATION
        self.completer = Completer()
        self.completer.setWidget(self)
        self.completer.insert_text.connect(self.insert_completion)
        self.current_model = None


        self.actual_text = ''

        
        self.tooltips = Completer.cond_tooltips
        # if  d:= self.completer.cond_dict:
        #     for k, v in d.items():
        #         model_to_unpack = d[k]
        #         values = [model_to_unpack.item(i).text().split()[0] for i in range(model_to_unpack.rowCount())]
                
        #         self.tooltips.update({k: "\n".join(values)})
        #         # print(f"{k} : {v}")
        
        self.scroll_bar = self.verticalScrollBar()
        QToolTip.setFont(font)
        



        self.remember_special_char = False

        # self.setReadOnly(True)

        # self.timer = QTimer()
        # self.timer.start(1000)
        # self.timer.timeout.connect(self.check_file_content_on_disk)

    def check_file_content_on_disk(self):
        if self.main_window.actual_text_edit is self and self.file_path:
            # print(f"Hello from timer: {self.file_path}")
            try:
                with open(self.file_path, 'r') as file_to_open:
                    text_on_disk = file_to_open.read()            
                    if text_on_disk != self.original_file_content:
                        popup = QMessageBox(self)
                        popup.setIcon(QMessageBox.Question)
                        popup.setWindowTitle("R2 Editor")
                        popup.setText("The file has been modified from external source.")
                        popup.setInformativeText("Do you want to reload file?")
                        popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        popup.setDefaultButton(QMessageBox.Yes)
                        answer = popup.exec_()

                        if answer == QMessageBox.Yes:
                            self.setPlainText(text_on_disk)
                            self.original_file_content = text_on_disk
                            self.file_was_modified = False
                            self.signal_modified_file_content.emit(self.file_was_modified)

                        elif answer == QMessageBox.No:
                            self.timer.stop()
                            

            except Exception as e:
                print(str(e))        
        


    # def textUnderCursor(self):
    #     tc = self.textCursor()
    #     isStartOfWord = False
    #     if tc.atStart() or (tc.positionInBlock() == 0):
    #         isStartOfWord = True
    #     while not isStartOfWord:
    #         tc.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
    #         if tc.atStart() or (tc.positionInBlock() == 0):
    #             isStartOfWord = True
    #         elif (tc.selectedText()[0]).isSpace():
    #             isStartOfWord = True
    #     return tc.selectedText()



    def mouseMoveEvent(self, event):
        # self.viewport().setCursor(Qt.ArrowCursor)
        # SAVE CURRENT SCROLLBAR POSITION
        scroll_pos = self.scroll_bar.value()
        # CREATE INSTANCE OF TEXT CURSOR
        tc = self.textCursor()
        # IF THERE IS NO SELECTED TEXT
        isStartOfWord = False

        if tc.selectedText() == '':
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

            if word in self.tooltips and TextEdit.shift_pressed:
                content = ""
                
                values_dict = self.tooltips[word]

                if type(values_dict) == str:
                    # self.show_tooltip(values_dict)
                    MyWidget.selected_word = values_dict

                else:
                    
                    for k, v in values_dict.items():
                        ts_content = ""
                        for ts in v:
                            ts_content += f"""
                                <li><font size=3 color=white>{ts}</font></li>
                            """
                        content += f"<font size=4 color=lightblue>{k:}</font><ol>{ts_content}</ol>"

                    self.viewport().setCursor(Qt.PointingHandCursor)
                    # self.show_tooltip(content)
                    
                    MyWidget.selected_word = content
            else:
                QToolTip.hideText()
                self.viewport().setCursor(Qt.IBeamCursor)
                MyWidget.selected_word = None
            # SET BACK THE TEXT CURSOR POSITION AND SCROLLBAR POSITION
            tc.setPosition(tc_original_pos)
            self.setTextCursor(tc)
            self.scroll_bar.setValue(scroll_pos)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if MyWidget.selected_word and TextEdit.shift_pressed:
            self.show_tooltip(MyWidget.selected_word)
            print(TextEdit.shift_pressed)

        return super().mouseReleaseEvent(event)        


    def show_tooltip(self, tooltip_text):
        if self.tooltips:
            # pos = self.cursorRect(self.textCursor()).bottomRight()
            # pos = self.mapToGlobal(pos)
            # # formated_tooltip_text = f'<html>\n<div style=\"max-width: 1000px;\">{tooltip_text}</div></html>'
            # pos.setX(pos.x()+50)
            # QToolTip.showText(pos, tooltip_text)
            self.w = MyWidget(self, tooltip_text)

    def show_conditions_in_tooltip(self):
        # content = '<div style="width: 2000px;">'
        # content += ", ".join(self.tooltips.keys())
        # content += '</div>'


        # centerPoint = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        # fg = self.frameGeometry()
        # fg.moveCenter(centerPoint)
        # # self.move(fg.topLeft())

        # my_point_x = centerPoint.x()
        # my_point_y = centerPoint.y()

        # tooltip_width = self.main_window.width() - 20
        # tooltip_y_position = self.main_window.height() // 2
        # tool_tip_q_point = self.main_window.pos()
        # tool_tip_q_point.setY(tool_tip_q_point.y() + tooltip_y_position)
        # tool_tip_q_point.setX(tool_tip_q_point.x())
        # content = f"""
        # <html>
        # <table width="{tooltip_width}">
        # <tr>
        #     <td></td>
        # </tr>
        # <tr>
        #     <td>{"<font color=blue> - </font>".join(sorted(self.tooltips.keys()))}</td>
        # </tr>
        # </table>
        # </html>
        # """
        new_list = [k for k, v in self.tooltips.items() if type(v) is dict]
        content = '<html><body><p style="text-align: center" align="center">'
        content += f'{"<font color=blue> - </font>".join(sorted(new_list))}'
        content += '</p></body></html>'
        # QToolTip.showText(QPoint(my_point_x-tooltip_width, my_point_y), content)
        # self.show_tooltip(content)


            


    def mousePressEvent(self, event):
        self.signal_clicked_on_text_edit.emit(self)
        # print(self.viewport().cursor().shape())
        if self.completer.popup.isVisible():
            self.completer.insert_text.emit(self.completer.get_selected())
            return super().mouseReleaseEvent(event)
        
        return super().mousePressEvent(event)


    def mouseReleaseEvent(self, event) -> None:
        if self.completer.popup.isVisible():
            self.completer.insert_text.emit(self.completer.get_selected())
        return super().mouseReleaseEvent(event)


    def is_modified(self):
        return self.toPlainText() != self.original_file_content


    def text_changed(self):
        self.file_was_modified = self.is_modified()
        self.signal_modified_file_content.emit(self.file_was_modified)




########################################################################################################################
# START COMPLETER
########################################################################################################################

        self.actual_text = self.get_actual_text()
        self.evaluate_actual_text()

########################################################################################################################
# KEYS MANAGEMENT
########################################################################################################################

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            TextEdit.shift_pressed = False
            # QToolTip.hideText()
        return super().keyReleaseEvent(event)
    
    def keyPressEvent(self, event):
        QToolTip.hideText()

        if event.key() == Qt.Key_Control:
            TextEdit.shift_pressed = True
            return

        # if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
        #     self.show_conditions_in_tooltip()
        #     return

        # "ENTER" AFTER POPUP IS VISIBLE
        if event.key() == Qt.Key_Return and self.completer.popup.isVisible():
            self.completer.insert_text.emit(self.completer.get_selected())
            return

        # "ENTER" ONLY
        elif event.key() == Qt.Key_Return:
            text_management.add_new_line_indent(self)
            return

        # "SHIFT" + "TAB" --> DEDENT
        if event.key() == Qt.Key_Backtab:
            text_management.indent_dedent_comment(self, variant='dedent')
            return

        # "TAB" ONLY --> INDENT
        if event.key() == Qt.Key_Tab:
            text_management.indent_dedent_comment(self, variant='indent')
            return

        # "SHIFT" + "HOME" --> STANDARD SHIFT+HOME = SELECT TEXT BEFORE CURSOR
        if event.modifiers() & Qt.ShiftModifier and event.key() == Qt.Key_Home:
            text_management.key_shift_home_press(self)
            return

        # "HOME" ONLY --> MOVE TO START OF LINE OR BEFORE FIRST WORD
        elif event.key() == Qt.Key_Home:
            text_management.key_home_press(self)
            return

        # "=" AFTER CONDITION IS WRITTEN
        if event.key() == Qt.Key_Equal and self.current_model == 'values':
            tc = self.textCursor()
            tc.insertText('=')
            self.show_popup('')
            return

        # "ALT" ONLY
        if event.key() == Qt.Key_Alt:

            tc = self.textCursor()
            tc.select(QTextCursor.WordUnderCursor)




            if tc.selectedText() == "" and tc.block().text().strip() == "" \
            or tc.selectedText() == "" and self.current_model == "values":
                self.show_popup("")
                return

            if tc.selectedText().startswith('"'):
                self.remember_special_char = True
                tc.insertText(' "')
                tc.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 2)
                self.setTextCursor(tc)
                tc.select(QTextCursor.WordUnderCursor)
                self.show_popup(tc.selectedText())
                return

            elif tc.selectedText().startswith(','):
                self.remember_special_char = True
                tc.insertText(' ,')
                tc.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 2)
                self.setTextCursor(tc)
                tc.select(QTextCursor.WordUnderCursor)
                self.show_popup(tc.selectedText())
                return

            elif tc.selectedText().startswith(')'):
                self.remember_special_char = True
                tc.insertText(' )"')
                tc.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 3)
                self.setTextCursor(tc)
                tc.select(QTextCursor.WordUnderCursor)
                self.show_popup(tc.selectedText())
                return


            elif len(tc.selectedText()) > 0:
                self.show_popup(tc.selectedText())
                return
            # elif len(tc.selectedText()) == '':
            #     self.show_popup('')
            #     return
            else:
                self.completer.popup.hide()
                return

        if event.key() not in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Return):
            self.completer.popup.hide()

        # # "CTRL" + "1" --> INSERT CHAPTER
        # if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_1:
        #     text_management.insert_chapter(self)
        #     return

        # # "CTRL" + "2" --> INSERT TEST CASE
        # if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_2:
        #     text_management.insert_testcase(self)
        #     return

        # # "CTRL" + "3" --> INSERT COMMAND
        # if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_3:
        #     text_management.insert_command(self)
        #     return

        # # "CTRL" + "/" --> INSERT COMMENT
        # if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Slash:
        #     text_management.indent_dedent_comment(self, variant='comment')
        #     return

        # # "CTRL" + "r" --> REELOAD TEXT MANAGEMENT MODULE
        # if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_R:
        #     importlib.reload(text_management)
        #     return

        # # "CTRL" + "+" --> INCREASE FONT SIZE
        # if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Plus:            
        #     point_size = TextEdit.font.pointSize()
        #     TextEdit.font.setPointSize(point_size+2)
        #     TextEdit.set_font_to_all_children()
        #     return

        # # "CTRL" + "-" --> DECRASE FONT SIZE
        # if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Minus:            
        #     point_size = TextEdit.font.pointSize()
        #     TextEdit.font.setPointSize(point_size-2)
        #     TextEdit.set_font_to_all_children()          
        #     return

        # # "CTRL" + "0" --> RESET FONT SIZE
        # if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_0:            
        #     TextEdit.font.setPointSize(10)         
        #     TextEdit.set_font_to_all_children()
        #     return                        

        # CALL PARENT KEYPRESS EVENT
        super().keyPressEvent(event)



########################################################################################################################
# COMPLETION MANAGEMENT
########################################################################################################################


    def insert_completion(self, completion):
        tc = self.textCursor()
        # print(f'***{completion}***')
        tc.movePosition(QTextCursor.StartOfWord)
        tc.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
        tc.insertText(completion)

        if self.remember_special_char:
            self.remember_special_char = False
            tc.deleteChar()
            # tc.movePosition(QTextCursor.Left)
        self.setTextCursor(tc)

        self.add_space_to_equal()
        self.complete_special_command()
        if not QToolTip.isVisible():
            self.completer.popup.hide()



    def show_popup(self, completion_prefix):
        # print(completion_prefix)
        self.completer.setCompletionPrefix(completion_prefix)
        cr = self.cursorRect()
        self.completer.popup.setCurrentIndex(self.completer.completionModel().index(0, 0)) # automatically select first popup item
        cr.setWidth(self.completer.popup.sizeHintForColumn(0)
                    + self.completer.popup.verticalScrollBar().sizeHint().width() + 20)
        self.completer.complete(cr)

    # def focusInEvent(self, event):
    #     if self.completer:
    #         self.completer.setWidget(self)
    #     QPlainTextEdit.focusInEvent(self, event)

########################################################################################################################
# ACTUAL TEXT MANAGEMENT
########################################################################################################################

    def get_actual_text(self):
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
            self.completer.popup.hide()
            self.show_tooltip(self.tooltips['MonitorVariablesCANape'])



        elif line_text.strip() == 'GraphVariables':
            command = line_text.strip()
            tc.select(tc.LineUnderCursor)
            tc.removeSelectedText()
            self.insertPlainText(line_text + ' = ""')
            for letter in range(1):
                tc.movePosition(QTextCursor.Left)
            self.setTextCursor(tc)

            # SHOW TOOLTIP / HINT IN CONSOLE
            self.completer.popup.hide()
            self.show_tooltip(self.tooltips['GraphVariables'])


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
            self.completer.popup.hide()
            self.show_tooltip(self.tooltips[command])




        elif line_text.strip() == 'CANapeCommand':
            command = line_text.strip()
            tc.select(tc.LineUnderCursor)
            tc.removeSelectedText()
            self.insertPlainText(line_text + ' = "CANape_GetObjectValue()"')
            for letter in range(2):
                tc.movePosition(QTextCursor.Left)
            self.setTextCursor(tc)

            # SHOW TOOLTIP / HINT IN CONSOLE
            self.completer.popup.hide()
            self.show_tooltip(self.tooltips['CANape_GetObjectValue'])


        elif line_text.strip() == 'VariableSequence':
            command = line_text.strip()
            tc.select(tc.LineUnderCursor)
            tc.removeSelectedText()
            self.insertPlainText(line_text + ' = ""')
            tc.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor)
            self.setTextCursor(tc)

            # SHOW TOOLTIP / HINT IN CONSOLE
            self.completer.popup.hide()
            self.show_tooltip(self.tooltips['VariableSequence'])



########################################################################################################################
# MODEL MANAGEMENT
########################################################################################################################


    def switch_to_values(self):
        if self.completer.cond_model:
            self.current_model = 'values'
            key = self.actual_text
            print("key==="+key+"===")
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
