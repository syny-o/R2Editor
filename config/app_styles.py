
RGB_BLUE = "58,89,245"
RGB_BLUE_HOVER = "88,99,255"

RGB_RED = "200, 20, 20"
RGB_GREEN = "0, 255, 0"
RGB_BLACK = "20, 20, 20"

RGB_BORDER_LIGHT = "50, 50, 50"
RGB_BORDER_DARK = "100, 100, 100"



THEMES = {

"DARK" : dict(
    RGB_BACKGROUND_0 = "39, 44, 54",
    RGB_BACKGROUND_1 = "33, 37, 43",
    RGB_BACKGROUND_2 = "33, 35, 35",
    RGB_HOVER = RGB_BLUE_HOVER,
    RGB_MAIN = RGB_BLUE,
    RGB_TEXT = "200, 200, 200",
    RGB_BORDER = RGB_BORDER_DARK
),


"LIGHT" : dict(
    RGB_BACKGROUND_2 = "199, 194, 194",
    RGB_BACKGROUND_1 = "233, 233, 243",
    RGB_BACKGROUND_0 = "133, 135, 135",
    RGB_HOVER = RGB_BLUE_HOVER,
    RGB_MAIN = RGB_BLUE,
    RGB_TEXT = "20, 20, 20",
    RGB_BORDER = RGB_BORDER_LIGHT
)


}




STYLES = \
"""

QWidget {
    border:none;
    color: rgb(RGB_TEXT);

}

#uiFrameFileSystem #uiFrameFileSystemTitleBar{
    background-color: rgb(RGB_BACKGROUND_0);
    border-bottom: 1px solid rgb(RGB_BORDER);
    border-right: 1px solid rgb(RGB_BORDER);
    
}


#uiFrameFileSystem QToolButton{
    border: 1px solid rgb(RGB_BACKGROUND_0);
    color: rgb(200, 200, 200);

}


#uiFrameFileSystem QToolButton:hover{
    border: 1px solid rgb(200, 0, 0);
}

#uiFrameFileSystem QTreeView{
    background-color: rgb(RGB_BACKGROUND_2);
    /*background-color: rgb(220, 220, 220);*/
    padding: 10px;
    font-size: 13px;
    border: 1px solid rgb(RGB_BORDER);
}



QSplitter #objNameFrameOutline{
    background-color: rgb(RGB_BACKGROUND_0);
}

QSplitter #objNameFrameOutline QLabel{
    padding: 5px;   
    font-weight: bold;
}

QSplitter QTreeWidget{
    background-color: rgb(RGB_BACKGROUND_2);
    border: 1px solid rgb(RGB_BORDER);
    padding: 10px;
    font-size: 13px;
    selection-background-color: rgb(170,170,170);
    /*selection-color: rgb(250, 250, 250);*/
}

QSplitter QTreeWidget::item:hover, #uiFrameFileSystem QTreeView::item:hover{
    background-color: rgb(170,170,170);
    color: rgb(20, 20, 20);
}




#uiFrameTitleBar, #uiFrameEditorTitleBar{
    background-color: rgb(RGB_BACKGROUND_0);
    border-bottom: 1px solid rgb(RGB_BORDER);
    border-left: 1px solid rgb(RGB_BORDER);
    border-right: 1px solid rgb(RGB_BORDER);
    margin-right: 2px;
    max-height: 35px;
    
}

#uiFrameTitleBar{
    margin-left: 2px;
}


#uiFrameTitleBar QPushButton, #uiFrameEditorTitleBar QPushButton{
    padding: 10px;
    color: rgb(200, 200, 200);
}

#uiFrameEditorTitleBar QPushButton:checked{
    background-color: rgb(RGB_HOVER);
}


#uiFrameLeftMenu{
    background-color: rgb(RGB_MAIN);    
}    


#uiFrameLeftMenu QPushButton{
    background-color: rgb(RGB_MAIN);
    border-left: 28px solid rgb(RGB_MAIN);
	background-position: left center;
    background-repeat: no-repeat;
	text-align: left;
    color: rgb(200, 200, 200);   
}

#uiFrameLeftMenu QPushButton::hover{
    background-color: rgb(RGB_HOVER); 
    border-left: 28px solid rgb(RGB_HOVER); 
	
}


#uiFrameRightMenu{
    background-color: rgb(RGB_BACKGROUND_0);
    padding: 0;
}

#uiFrameRightMenu QFrame{
	background-color: rgb(RGB_BACKGROUND_0);
	padding-top: 37px;
}
#uiFrameRightMenu QPushButton {	
	border: none;
	border-left: 25px solid rgb(RGB_BACKGROUND_0);
    border-right: 5px solid rgb(RGB_BACKGROUND_0);
	color: red;
	text-align: left;

}
#uiFrameRightMenu QPushButton:hover {
	background-color: rgb(RGB_HOVER);
	border-left: 25px solid rgb(RGB_HOVER);
    border-right: 5px solid rgb(RGB_HOVER);
}
#uiFrameRightMenu QPushButton:pressed {	
	background-color: rgb(RGB_BACKGROUND_1);
	border-left: 25px solid rgb(RGB_BACKGROUND_1);
    border-right: 5px solid rgb(RGB_BACKGROUND_1);
}
#uiFrameRightMenu QPushButton:checked {	
	background-color: rgb(RGB_BACKGROUND_1);
	border-left: 25px solid rgb(RGB_BACKGROUND_1);
	border-right: 5px solid rgb(RGB_MAIN);
}






QPushButton:hover{
    background-color: rgb(RGB_MAIN);
}

QLineEdit{
    background-color: rgb(RGB_BACKGROUND_2);
    padding: 9px;
    margin: 0 5px;
    border: 1px solid rgb(RGB_BORDER);
    border-radius: 3px;
}


QLineEdit:focus
{
    border-color: rgb(RGB_MAIN);
}

QComboBox
{
	padding: 8px;
	border: 1px solid rgb(RGB_BORDER);
    background-color: rgb(RGB_BACKGROUND_2);
    selection-background-color: rgb(RGB_MAIN);
    border-radius: 3px;
    margin:0;
    margin-right: 2px;
}








/* ############### QTreeView ################## */

/*
QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {
        border-image: none;
        image: url(:/16x16/icons/16x16/cil-plus.png);
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings  {
        border-image: none;
        image: url(:/16x16/icons/16x16/cil-minus.png);
}
*/




/* ############### QTabs ################## */



QTabWidget::pane:top
{
    border: none;
    
}






QTabBar::close-button
{
    border-image: url(./ui/icons/24x24/cil-x.png);   
    background: transparent;
}

QTabBar::close-button:hover
{
    border-image: url(./ui/icons/close.png);    
}


QTabBar::tab:top
{
    color: #eff0f1;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #76797c;
    border-top: 0.1ex solid #76797c;
    /*background-color: #31363b;*/
    padding: 1.5ex;
    padding: 2.5ex;
    min-width: 50px;
    border-top-left-radius: 0.2ex;
    border-top-right-radius: 0.2ex;
    border-bottom: 3px solid #31363b;
    background-color: rgb(RGB_BACKGROUND_0);
    border-right: 1px solid rgb(RGB_BORDER);
}

QTabBar::tab:top:selected
{
    color: #eff0f1;
    background-color: #54575B;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #76797c;
    border-top-left-radius: 0.2ex;
    border-top-right-radius: 0.2ex;
    border-bottom: 3px solid #31363b;

}





/* ############### QMenu ################## */


QMenu{
    background-color: rgb(RGB_BACKGROUND_2);
    color: rgb(RGB_TEXT);
    padding: 0.5ex;
    padding-left: 1ex;
    opacity: 200;
}

QMenu QPixmap{
    padding: 2ex 5ex;
}


QMenu::item{
    padding: 4ex 10ex;
    color: rgb(RGB_TEXT);
    font-style: bold;
}

QMenu::item:selected{
    background-color: rgba(0,50,150,100);
}

QMenu::item:disabled{
    color: rgb(100,100,100);
}


/* ############### QScrollbar ################## */

QScrollBar:horizontal
{
    background-color: #2A2929;
    margin: 1.5ex 0.3ex 1.5ex 0.3ex;
    border: 0.1ex transparent #2A2929;
    border-radius: 0.4ex;
    min-height: 2ex;
}

QScrollBar::handle:horizontal
{
    min-width: 0.5ex;
    border-radius: 0.4ex;
    background-color: rgb(RGB_MAIN);
    
}

QScrollBar::handle:horizontal:hover
{
    background-color: rgb(RGB_HOVER);
}

QScrollBar::sub-line:horizontal:hover,
QScrollBar::sub-line:horizontal:on
{
    border-image: url(./ui/icons/24x24/cil-x.png); 
    width: 1ex;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal,
QScrollBar::up-arrow:horizontal,
QScrollBar::down-arrow:horizontal
{
    background: none;
}


QScrollBar:vertical
{
    background-color: #2A2929;
    width: 8px;
    margin: 1.5ex 0.3ex 1.5ex 0.3ex;
    border: 0.1ex transparent #2A2929;
    border-radius: 0.4ex;
}

QScrollBar::handle:vertical
{
    min-height: 0.5ex;
    border-radius: 0.4ex;
    width: 5px;
    background-color: rgb(RGB_MAIN);
}

QScrollBar::handle:vertical:hover
{
    background-color: rgb(RGB_HOVER);
}

QScrollBar::sub-line:horizontal,
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:vertical,
QScrollBar::add-line:vertical
{
    height: 0ex;
    width: 0ex;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
{
    background: none;
}


#uiFrameData, #uiFrameDataSummary{
    background-color: rgb(RGB_BACKGROUND_1);
}

#uiFrameDataSummary QPushButton{
    padding: 8px;
    /*border: 1px solid rgb(RGB_BORDER);*/
    background-color: rgb(RGB_BACKGROUND_2);
    border-radius: 3px;
}

#uiFrameDataSummary QPushButton:hover{
    background-color: rgb(RGB_HOVER);
}

#uiFrameDataSummary QLabel{
    color: rgb(120, 120, 120);
    font-size: 14px;    
    text-transform: uppercase;
    padding-left: 5px;
}



QSplitterHandle:hover {} 
QSplitter::handle:horizontal:hover {background-color:rgb(RGB_HOVER);}
QSplitter::handle:vertical:hover {background-color:rgb(RGB_HOVER);}

QSplitterHandle {} 
QSplitter::handle:horizontal {
    /*image: url(:/20x20/icons/20x20/cil-options.png);*/
    background-color: rgb(RGB_BORDER);
    border-top: 60ex solid rgb(RGB_BACKGROUND_1);
    border-bottom: 60ex solid rgb(RGB_BACKGROUND_1);
     }

QSplitter::handle:vertical {
    background-color: rgb(RGB_BORDER);
    
     }     





#uiFrameControlTree QPushButton{
    background-color: transparent;
    background-color: rgb(RGB_BACKGROUND_2);
    border-radius: 3px;
    border: 1px solid rgb(RGB_BORDER);
    padding: 10px;
} 

#uiFrameControlTree QToolButton{
    font-size: 12px;
}

#uiFrameControlTree QLineEdit QToolButton{
    padding: 5px;
    margin: 5px;
}

 #uiFrameControlTree{
    background-color: rgb(RGB_BACKGROUND_2);
    border: 1px solid rgb(RGB_BORDER);
    border-radius: 3px;
}

#uiFrameControlTree QPushButton:disabled, #uiFrameControlTree QToolButton:disabled{
    color: rgb(120,120,120); 
}

#uiFrameControlTree QTreeView{
    background-color: rgb(RGB_BACKGROUND_1);
    border: 1px solid rgb(RGB_BORDER);  
    font-size: 13px; 
    selection-background-color: rgb(170,170,170);
}

#uiFrameControlTree QTreeView::item:hover, #uiFrameControlTree QTreeView::item:selected{
    background-color: rgb(170,170,170);
    color: rgb(20, 20, 20);
}

#uiFrameControlTree QPushButton, #uiFrameControlTree QLineEdit, #uiFrameControlTree QComboBox{
    border-color: rgb(RGB_MAIN);
    border-color: rgb(RGB_BORDER);
    font-size: 14px;
}

#uiFrameControlTree QLineEdit:focus, #uiFrameControlTree QComboBox:focus, #uiFrameControlTree QPushButton:hover, #uiFrameControlTree QToolButton:hover{
    background-color: rgb(200, 200, 250);
    color: rgb(20, 20, 20);
}




QToolBar QToolButton{
    font-size: 14px;
    padding: 5px;
    min-width: 40px;
}  

/*QToolBar QToolButton:hover, QToolBar QToolButton:checked, QToolBar QToolButton:pressed{
    background-color: rgb(RGB_HOVER);
}*/








#uiDashboardFrameLeft #uiLabelLogo{
    font-size: 72px;
    color: rgb(RGB_MAIN);
}

#uiDashboardFrameLeft, #uiDashboardFrameLeft QListWidget{
	background-color: rgb(RGB_BACKGROUND_2);
	border: none;
    padding: 10px 20px;
}


#uiDashboardFrameLeft QListWidget::item{
    padding: 5px;
}

#uiDashboardFrameLeft QLabel, #uiDashboardFrameRight QLabel{
	padding: 7 17;
}QListView


#uiDashboardFrameRight{
	background-color: rgb(RGB_BACKGROUND_1);
	border: none;
}

#uiDashboardFrameRight QToolButton{
	color: rgb(RGB_MAIN);    
}

#uiDashboardFrameRight QToolButton:hover{
	color: rgb(RGB_TEXT);
}



QToolTip{
    padding: 10px;
    border: 0.5px solid rgb(RGB_BORDER);
    background-color: rgb(RGB_BACKGROUND_1);
    color: rgb(RGB_TEXT);
}


QListView{
    border: 0.5px solid rgb(RGB_BORDER);
    background-color: rgb(RGB_BACKGROUND_2);
    color: #eff0f1;
    color: rgb(RGB_TEXT);
    padding: 0.5ex;
    opacity: 200;

}

QListView::item{
    padding-right: 1px;
    color: rgb(RGB_TEXT);
}

QListWidget, QTextEdit{
    background-color: rgb(RGB_BACKGROUND_2);
    padding: 10px;
    margin: 0 5px;
    border: 1px solid rgb(RGB_BORDER)
}   

QListWidget::item{
    max-height: 20px;
}



QDialog{
    border: 1px solid rgb(RGB_BORDER);
    background-color: rgb(RGB_BACKGROUND_1);
}



QSplitter{
    background-color: rgb(RGB_BACKGROUND_1);
}

TextEdit{
    background-color: rgb(RGB_BACKGROUND_1);


}



#uiSplitterDataManager{
    background-color: rgb(RGB_BACKGROUND_2);
    background-color: rgb(RGB_BACKGROUND_1);
}



NotificationWidget{
    background-color: rgb(RGB_MAIN);
    color: rgb(200, 200, 200);
}

NotificationWidget QLabel{
    color: rgb(200, 200, 200);
}

QDialog QPushButton{
    background-color: rgb(RGB_BACKGROUND_2);
    padding: 10px 25px;
    margin: 2px;
}

#uiFrameFormWidget{
    background-color: rgb(RGB_BACKGROUND_2);
    border: 1px solid rgb(RGB_BORDER);
}

#uiFrameFormWidget *{
    font-size: 13px;
}

#uiFrameFormWidget QPushButton{
    color: rgb(200, 200, 200);
}

QListWidget{
    padding: 0;
}

QListWidget::item:hover{
    background-color: rgb(RGB_MAIN);
}


TextEditTooltipWidget{
    background-color: rgb(RGB_BACKGROUND_0);
    color: rgb(RGB_TEXT);
}

TextEditTooltipWidget QTextEdit{
    background-color: rgb(RGB_BACKGROUND_0);
    color: rgb(RGB_TEXT);
    border: none;
    font-size: 14px;
}

TextEditTooltipWidget QPushButton{
    font-size: 14px;
    padding: 10px;
    background-color: rgb(RGB_MAIN);
    color: rgb(200, 200, 200);
}

TextEditTooltipWidget QPushButton:hover{
    background-color: rgb(RGB_HOVER);

}

#uiFrameFindReplace {
    background-color: rgb(RGB_BACKGROUND_0);
    border-right: 1.5px solid rgb(RGB_BACKGROUND_1);
    color: rgb(200, 200, 200);
}

#uiFrameFindReplace QWidget{
    padding: 10px;
    color:white;
}

#uiFrameFindReplace QPushButton{
	padding: 5 15;
	background-color: rgb(RGB_BACKGROUND_2);
    color:white;
}

#uiFrameFindReplace QPushButton:hover, #uiFrameFindReplace QPushButton:checked{
    background-color: rgb(RGB_HOVER);
}

#uiFrameFindReplace QLineEdit{
	padding: 5;
	border: 1px solid transparent;
    background-color: rgb(RGB_BACKGROUND_2);
    color:white;
}


/* TABBAR SCROLLBAR - ARROWS */
QTabBar::scroller { /* the width of the scroll buttons */
    width: 40px;
}

QTabBar QToolButton { /* the scroll buttons are tool buttons */
    width: 15px;
    border-width: 2px;
    background-color: rgb(0, 0, 0);
}

#completer_tooltip{

    background-color: rgb(RGB_BACKGROUND_2);
    font-size: 14px;
}

#completer_tooltip QListWidget{
    background-color: rgb(RGB_BACKGROUND_2);
    border: none;
    color: rgb(RGB_TEXT);
    padding: 0.5ex;
    opacity: 200;
}





"""


def switch_theme(theme_key):
    theme = THEMES[theme_key]
    new_styles = STYLES
    for key, value in theme.items():
        new_styles = new_styles.replace(key, value)
    return new_styles


# STYLES = switch_theme(LIGHT)