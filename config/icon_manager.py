import qtawesome as qta


COLOR_ON = '#4863ff'
COLOR_OFF = '#ddd'
COLOR_DISABLED = '#aaa'
SCALE_FACTOR_MENU_RIGHT = 1.2
SCALE_FACTOR_CONTROL_ACTIONS = 0.7
SCALE_FACTOR_CONTROL_BUTTONS = 1.2
SCALE_FACTOR_CONTRO_SEARCH_BOX = 1.1


def define_icon(icon_name, *, scale_factor, color_off, color_on=COLOR_ON, color_on_active=COLOR_ON, color_disabled=COLOR_DISABLED):
    return qta.icon(icon_name,
                    scale_factor=scale_factor, 
                    color_off=color_off,
                    color_on=color_on,
                    color_on_active=color_on_active,
                    color_disabled=color_disabled)


class IconManager:
    def __init__(self):
        self.ICON_SEARCH_BOX_FIND = define_icon('fa5s.search', scale_factor=SCALE_FACTOR_CONTROL_BUTTONS, color_off=COLOR_ON)
        self.ICON_NODE_REMOVE = define_icon('fa5s.trash-alt', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_EDIT = define_icon('fa5s.edit', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_PASTE = define_icon('fa5s.paste', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_COPY = define_icon('fa5s.copy', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_DUPLICATE = define_icon('fa5s.clone', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_MOVE_UP = define_icon('fa5s.arrow-up', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NODE_MOVE_DOWN = define_icon('fa5s.arrow-down', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_EXPAND_ALL_CHILDREN = define_icon('fa5s.expand-arrows-alt', scale_factor=SCALE_FACTOR_CONTROL_BUTTONS, color_off=COLOR_ON)
        self.ICON_COLLAPSE_ALL_CHILDREN = define_icon('fa5s.compress-arrows-alt', scale_factor=SCALE_FACTOR_CONTROL_BUTTONS, color_off=COLOR_ON)
        self.ICON_PREVIOUS_VIEW = define_icon('fa5s.arrow-left', scale_factor=SCALE_FACTOR_CONTROL_BUTTONS, color_off=COLOR_ON)
        self.ICON_NODE_EXPORT = define_icon('fa5s.file-export', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_NORMALISE_A2L_FILE = define_icon('fa5s.compress', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_UPDATE_MODULE = define_icon('fa5s.sync', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_ADD_TO_IGNORE_LIST = define_icon('fa5s.eye-slash', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)
        self.ICON_REMOVE_FROM_IGNORE_LIST = define_icon('fa5s.eye', scale_factor=SCALE_FACTOR_CONTROL_ACTIONS, color_off=COLOR_ON)


        self.ICON_DATA_MANAGER = qta.icon('fa5s.database',
                                        scale_factor=SCALE_FACTOR_MENU_RIGHT, 
                                        color_off=COLOR_OFF,
                                        color_on=COLOR_ON,
                                        color_on_active=COLOR_ON)
        self.ICON_CODE_EDITOR = qta.icon('fa5s.file-code',
                                        scale_factor=SCALE_FACTOR_MENU_RIGHT, 
                                        color_off=COLOR_OFF,
                                        color_on=COLOR_ON,
                                        color_on_active=COLOR_ON)        
        self.ICON_DASHBOARD = qta.icon('fa5s.home',
                                        scale_factor=SCALE_FACTOR_MENU_RIGHT, 
                                        color_off=COLOR_OFF,
                                        color_on=COLOR_ON,
                                        color_on_active=COLOR_ON)        
        self.ICON_SETTINGS = qta.icon('fa5s.wrench',
                                        scale_factor=SCALE_FACTOR_MENU_RIGHT, 
                                        color_off=COLOR_OFF,
                                        color_on=COLOR_ON,
                                        color_on_active=COLOR_ON)        


        self.ICON_SEARCH_BOX_FIND = qta.icon('fa5s.filter',
                                        offset=(0.1, 0.0),
                                        scale_factor=SCALE_FACTOR_CONTRO_SEARCH_BOX, 
                                        color_off=COLOR_ON,
                                        color_on=COLOR_ON,
                                        color_on_active=COLOR_ON,
                                        color_disabled=COLOR_DISABLED) 



