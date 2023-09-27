from PyQt5.QtGui import QTextCursor

def get_word_under_cursor(text_cursor):
    is_end_of_word = False
    is_start_of_word = False
    
    # text_cursor.select(QTextCursor.WordUnderCursor)    
    # while not is_end_of_word:
    #     if text_cursor.atEnd() or text_cursor.atBlockEnd():
    #         is_end_of_word = True
        
    #     text_cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)

    #     if text_cursor.atEnd() or text_cursor.atBlockEnd():
    #         is_end_of_word = True

    #     if text_cursor.selectedText().endswith((" ", "\n", "\t", "=", ",", '"')):
    #         is_end_of_word = True
    #         text_cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
            
    #         break

    # text_cursor.clearSelection()

    while not is_start_of_word:
        if text_cursor.atStart() or text_cursor.atBlockStart():
            is_start_of_word = True
            print("prdel")
        
        
        text_cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)

        if text_cursor.atStart() or text_cursor.atBlockStart():
            is_start_of_word = True
            print("prdel2")

        if text_cursor.selectedText().startswith((" ", "\n", "\t", "=", ",", '"', "(", ")")):
            is_start_of_word = True
            text_cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            print("prdel3")
            break

    print("SelectedText:::" ,text_cursor.selectedText())

    return text_cursor.selectedText()