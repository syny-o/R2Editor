STYLES = \
"""
QPushButton{
    background-color: rgb(58, 89, 245);
    color: rgb(200, 200, 200);
    font-size: 16px;
    padding: 12px;
    margin: 5px 0;
}

QPushButton:hover{
    background-color: rgb(95, 180, 255);
}

QLineEdit{
    background-color: rgb(35, 35, 25);
    /*background-image: url(:/16x16/icons/16x16/cil-magnifying-glass.png);
    background-position: left center;
    background-repeat: no-repeat;*/
    padding: 10px;

    margin: 0 5px;
}

QLineEdit QToolButton{
    padding-left: 10px;
    margin-left: 50px;
}

QLineEdit:focus
{
    /*background-color: rgb(58, 89, 245);
    color: rgb(20, 20, 20);*/
    border: 1px solid rgb(58, 89, 205);
}

QComboBox
{
    min-width: 25px;
	padding: 10px;
	border: 1px solid rgb(39, 44, 54);
    background-color: rgb(35, 35, 25);
    selection-background-color: rgb(58, 89, 245);
}

QToolBar QToolButton{
    color: rgb(200, 200, 200);
    font-size: 12px;
    padding: 5px;
    min-width: 40px;
}  

QToolBar QToolButton:hover, QToolBar QToolButton:checked, QToolBar QToolButton:pressed{
    background-color: rgb(95, 180, 255);
}

QToolButton:pressed{
    background-color: rgb(195, 180, 255);
}

QToolBar QToolButton:disabled{
    color: rgb(70, 70, 70);
}

QToolBar{
    
    border: none;
}


"""