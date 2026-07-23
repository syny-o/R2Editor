from PyQt5.QtGui import QRegion, QDrag, QPixmap, QCursor
from PyQt5.QtWidgets import QTabWidget, QTabBar, QTextEdit
from PyQt5.QtCore import Qt, QPoint, QMimeData

from text_editor.text_editor import TextEdit

class Tabs(QTabWidget):

    # signal_tab_inserted = pyqtSignal(int, object)

    def __init__(self, parent, visibility, instance_name):
        super().__init__(parent)
        self.parent = parent
        self.visibility = visibility
        if not self.visibility:
            self.setVisible(False)
        self.instance_name = instance_name
        self.setAcceptDrops(True)
        self.tabBar = self.tabBar()
        self.tabBar.setMouseTracking(True)
        self.tabBar.setCursor(Qt.PointingHandCursor)
        self.indexTab = None
        self.setMovable(True)
        self.setTabsClosable(True)
        # self.setStyleSheet(stylesheet.tabs)
        # self.tabBar.setStyleSheet(stylesheet.tab_bar)



        # self.signal_tab_inserted.connect(parent.tab_has_been_inserted)
        
    def __str__(self):
        return self.instance_name

    def tabInserted(self, index):
        # print('TAB HAS BEEN INSERTED START')
        self.setCurrentIndex(index)
        # print('TAB HAS BEEN INSERTED FINISHED')
        # self.signal_tab_inserted.emit(index, self)


    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton:
            return

        globalPos = self.mapToGlobal(e.pos())
        tabBar = self.tabBar
        posInTab = tabBar.mapFromGlobal(globalPos)
        self.indexTab = tabBar.tabAt(e.pos())
        tabRect = tabBar.tabRect(self.indexTab)

        pixmap = QPixmap(tabRect.size())
        tabBar.render(pixmap,QPoint(),QRegion(tabRect))
        mimeData = QMimeData()
        drag = QDrag(tabBar)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        cursor = QCursor(Qt.OpenHandCursor)
        drag.setHotSpot(e.pos() - posInTab)
        drag.setDragCursor(cursor.pixmap(),Qt.MoveAction)
        dropAction = drag.exec_(Qt.MoveAction)

        ###############################################################################################################
        # Drag Effect - not ideal solution START
        ###############################################################################################################
        if self.parent.right_tabs.count() < 1:
            self.parent.right_tabs.setVisible(False)
        ###############################################################################################################
        # Drag Effect - not ideal solution END
        ###############################################################################################################



    def dragEnterEvent(self, e):
        e.accept()
        if e.source().parentWidget() != self:
            return

        #print(self.indexOf(self.widget(self.indexTab)))
        self.parent.TABINDEX = self.indexOf(self.widget(self.indexTab))

        ###############################################################################################################
        # Drag Effect - not ideal solution START
        ###############################################################################################################
        if self.count() < 2 and not self.visibility:
            self.setVisible(False)
            self.closed_tab = self


        self.parent.right_tabs.setVisible(True)
        if self.parent.right_tabs.count() == 0:
            self.parent.right_tabs.setStyleSheet('background-color: #0080ff')
        ###############################################################################################################
        # Drag Effect - not ideal solution END
        ###############################################################################################################


    def dragLeaveEvent(self,e):
        e.accept()





    def dropEvent(self, e):

        try:
            #print(self.parent.TABINDEX)
            # if e.source().parentWidget() == self:
            #     return

            e.setDropAction(Qt.MoveAction)
            e.accept()
            counter = self.count()

            # if type(e.source().parentWidget()) is TextEdit:
            #     return

            if counter == 0:
                self.addTab(e.source().parentWidget().widget(self.parent.TABINDEX),e.source().tabIcon(self.parent.TABINDEX), e.source().tabText(self.parent.TABINDEX))
            else:
                self.insertTab(counter + 1 ,e.source().parentWidget().widget(self.parent.TABINDEX),e.source().tabIcon(self.parent.TABINDEX), e.source().tabText(self.parent.TABINDEX))

            # self.parent.right_tabs.setStyleSheet('') # NOT NECESSARY CAUSE THE STYLESHEET IS SET VIA PARENT --> UPDATE TITLE

        except Exception as e:
            print(e)

