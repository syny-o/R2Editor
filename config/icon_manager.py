import qtawesome as qta

COLOR_ON = '#4863ff'
COLOR_OFF = '#ddd'
COLOR_DISABLED = '#aaa'
COLOR_WHITE = '#ddd'
SCALE_FACTOR_MENU_RIGHT = 1.2
SCALE_FACTOR_MENU_LEFT = 1.5
SCALE_FACTOR_CODE_EDITOR = 1.4


SCALE_FACTOR_CONTROL_ACTIONS = 0.7
SCALE_FACTOR_CONTROL_BUTTONS = 1.5
SCALE_FACTOR_CONTRO_SEARCH_BOX = 1.1
SCALE_FACTOR_TITLE_BAR = 1.0


def define_icon(icon_name, *, scale_factor, color_off, color_on=COLOR_ON, color_on_active=COLOR_ON, color_disabled=COLOR_DISABLED):
    return qta.icon(icon_name,
                    scale_factor=scale_factor, 
                    color_off=color_off,
                    color_on=color_on,
                    color_on_active=color_on_active,
                    color_disabled=color_disabled)


class IconManager:
    def __init__(self):

        # MAIN WINDOW - LEFT MENU
        self.ICON_PROJECT_OPEN = define_icon('mdi6.folder-open', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_PROJECT_NEW = define_icon('mdi6.close-box-multiple', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_PROJECT_SAVE = define_icon('mdi6.content-save', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_PROJECT_CLOSE = define_icon('fa5s.times', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_PROJECT_SAVE_AS = define_icon('mdi6.pencil', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_APP_EXIT = define_icon('mdi.power-standby', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_APP_ABOUT = define_icon('fa5s.info-circle', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_APP_HELP = define_icon('fa5s.question-circle', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_MENU = define_icon('mdi.menu', scale_factor=2, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_MENU_CLOSE = define_icon('mdi.close', scale_factor=1.8, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")


        # MAIN WINDOW - RIGHT MENU
        
        self.ICON_DATA_MANAGER = qta.icon('fa5s.database',
                                        scale_factor=SCALE_FACTOR_MENU_RIGHT, 
                                        color_off=COLOR_OFF,
                                        color_on=COLOR_ON,
                                        color_on_active=COLOR_ON)
        self.ICON_CODE_EDITOR = qta.icon('mdi6.application-edit',
                                        scale_factor=SCALE_FACTOR_MENU_RIGHT, 
                                        color_off=COLOR_OFF,
                                        color_on=COLOR_ON,
                                        color_on_active=COLOR_ON)        
        self.ICON_DASHBOARD = qta.icon('fa5s.home',
                                        scale_factor=SCALE_FACTOR_MENU_RIGHT, 
                                        color_off=COLOR_OFF,
                                        color_on=COLOR_ON,
                                        color_on_active=COLOR_ON)        
        self.ICON_SETTINGS = qta.icon('ri.settings-5-fill',
                                        scale_factor=1.6, 
                                        color_off=COLOR_OFF,
                                        color_on=COLOR_ON,
                                        color_on_active=COLOR_ON)   


        # CODE EDITOR
        self.ICON_SAVE_SCRIPT = define_icon('mdi6.content-save', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_SAVE_SCRIPT_AS = define_icon('mdi6.pencil', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_OPEN_SCRIPT = define_icon('mdi6.folder-open', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_NEW_SCRIPT = define_icon('mdi6.file', scale_factor=SCALE_FACTOR_MENU_LEFT, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")

        self.ICON_INSERT_CHAPTER = define_icon('fa5s.book-open', scale_factor=SCALE_FACTOR_CODE_EDITOR, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_INSERT_TESTCASE = define_icon('ph.test-tube-fill', scale_factor=SCALE_FACTOR_CODE_EDITOR, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_INSERT_COMMAND = define_icon('mdi6.code-tags', scale_factor=SCALE_FACTOR_CODE_EDITOR, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_COMMENT_UNCOMMENT = define_icon('mdi6.comment-quote-outline', scale_factor=SCALE_FACTOR_CODE_EDITOR, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")
        self.ICON_FORMAT_CODE = define_icon('mdi6.format-align-right', scale_factor=SCALE_FACTOR_CODE_EDITOR, color_off="#ddd", color_on="#ddd", color_on_active="#ddd")

        self.ICON_ZOOM_IN = define_icon('mdi6.magnify-plus', scale_factor=SCALE_FACTOR_CODE_EDITOR, color_off=COLOR_ON)
        self.ICON_ZOOM_OUT = define_icon('mdi6.magnify-minus', scale_factor=SCALE_FACTOR_CODE_EDITOR, color_off=COLOR_ON)
        self.ICON_ZOOM_RESET = define_icon('mdi6.magnify', scale_factor=SCALE_FACTOR_CODE_EDITOR, color_off=COLOR_ON)

        self.ICON_FILE_LOCKED = qta.icon('fa5s.lock', scale_factor=1, color="red")
        self.ICON_FILE_UNLOCKED = qta.icon('fa5s.unlock', scale_factor=1, color="green")


        # FILE SYSTEM
        self.ICON_DISCONNECT_FOLDER = define_icon('mdi.close', scale_factor=2, color_off="#ddd", color_on="red", color_on_active="red")
        




        
        # DATA MANAGER TREE --> CONTROL BUTTONS
        self.ICON_SEARCH_BOX_FIND = define_icon('fa5s.search', scale_factor=SCALE_FACTOR_CONTROL_BUTTONS, color_off=COLOR_ON)
        self.ICON_NODE_REMOVE = define_icon('fa5s.trash-alt', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_EDIT = define_icon('fa5s.edit', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_PASTE = define_icon('fa5s.paste', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_COPY = define_icon('fa5s.copy', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_DUPLICATE = define_icon('fa5s.clone', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_MOVE_UP = define_icon('fa5s.arrow-up', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_MOVE_DOWN = define_icon('fa5s.arrow-down', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_EXPAND_ALL_CHILDREN = define_icon('mdi.expand-all', scale_factor=SCALE_FACTOR_CONTROL_BUTTONS, color_off=COLOR_ON)
        self.ICON_COLLAPSE_ALL_CHILDREN = define_icon('mdi.collapse-all', scale_factor=SCALE_FACTOR_CONTROL_BUTTONS, color_off=COLOR_ON)
        self.ICON_PREVIOUS_VIEW = define_icon('fa5s.arrow-left', scale_factor=SCALE_FACTOR_CONTROL_BUTTONS, color_off=COLOR_ON)
        self.ICON_NODE_EXPORT = define_icon('fa5s.file-export', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NORMALISE_A2L_FILE = define_icon('fa5s.compress', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_UPDATE_MODULE = define_icon('fa5s.sync', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_ADD_TO_IGNORE_LIST = define_icon('fa5s.eye-slash', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_REMOVE_FROM_IGNORE_LIST = define_icon('fa5s.eye', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)


        self.ICON_SEARCH_BOX_FIND = qta.icon('fa5s.filter',
                                        offset=(0.1, 0.0),
                                        scale_factor=SCALE_FACTOR_CONTRO_SEARCH_BOX, 
                                        color_off=COLOR_ON,
                                        color_on=COLOR_ON,
                                        color_on_active=COLOR_ON,
                                        color_disabled=COLOR_DISABLED) 


        self.ICON_COMBO_All_ITEMS = define_icon('fa.th', scale_factor=1.2, color_off=COLOR_ON)


        # DATA MANAGER TITLE MENU
        self.ICON_NEW_MODULE = define_icon('fa5s.plus', scale_factor=SCALE_FACTOR_TITLE_BAR, color_off=COLOR_WHITE)
        self.ICON_CHECK_COVERAGE = define_icon('fa5s.check-double', scale_factor=SCALE_FACTOR_TITLE_BAR, color_off=COLOR_WHITE)
        self.ICON_CHECK_REPORT = define_icon('fa5s.check-square', scale_factor=SCALE_FACTOR_TITLE_BAR, color_off=COLOR_WHITE)
        self.ICON_UPDATE_REQUIREMENTS = define_icon('fa5s.sync', scale_factor=SCALE_FACTOR_TITLE_BAR, color_off=COLOR_WHITE)
        self.ICON_SET_PROJECT_FOLDER = define_icon('fa5s.folder-open', scale_factor=SCALE_FACTOR_TITLE_BAR, color_off=COLOR_WHITE, color_on=COLOR_WHITE, color_on_active=COLOR_WHITE)

        # DATA MANAGER VARIOUS ICONS
        self.ICON_IGNORED_ITEM = qta.icon('fa5s.eye-slash', scale_factor=0.7, color_off="#cc7a00")
        self.ICON_INLINK = qta.icon('fa5s.arrow-left', scale_factor=0.7, color_off="red")
        self.ICON_OUTLINK = qta.icon('fa5s.arrow-right', scale_factor=0.7, color_off="green")
        self.ICON_SCRIPT_REFERENCE = qta.icon('mdi.file-check', scale_factor=1, color_off="orange")

        
    



