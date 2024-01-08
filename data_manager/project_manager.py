import json
from pathlib import Path
from typing import Callable
from data_manager.data_manager import DataManager
from PyQt5.QtWidgets import QMainWindow


_MAIN = None
_SETTINGS = None
_DATA_MANAGER = None

_PARAMETERS = {
    "disk_project_path"     : None,
    "json_project_path"     : None,
    "is_project_saved"      : True,
}


# PROPERTY PROVIDED TO DATA MANAGER
def disk_project_path():
    return _PARAMETERS["disk_project_path"]



_listeners = []  # !!! LISTENERS must implement method RECEIVE_PARAMETERS_FROM_PROJECT_MANAGER !!!


# INTERFACE CALLED FROM MAIN WINDOW AT INITIALISATION
def set_listeners(*listeners: object) -> None:
    """ MAIN WINDOW sets these listeners when R2Editor starts --> Main_Window, TreeFileBrowser, Data_Manager, Dashboard """
    global _DATA_MANAGER, _MAIN, _SETTINGS
    _listeners.clear()
    for listener in listeners:
        _listeners.append(listener)
        if isinstance(listener, DataManager):
            _DATA_MANAGER = listener
        if isinstance(listener, QMainWindow):
            _MAIN = listener
            _SETTINGS = _MAIN.app_settings          






# INTERFACE CALLED FROM ALL LISTENERS
def receive_parameters_from_listeners(data: dict) -> None:
    _PARAMETERS.update(data)
    _notify_listeners()






# INTERFACES WITH MAIN WINDOW + DASHBOARD
def open_project(path: Path) -> tuple[bool, str]:
    success, data = _open_json_from_disk(path)

    if not success:  # JSON file has not been loaded at all --> data = Error Message
        return False, data

    _PARAMETERS["json_project_path"] = str(path)    
    _PARAMETERS["is_project_saved"] = True
    
    path = data["disk_project_path"]
    if path is not None and not Path(path).exists():
        _PARAMETERS["disk_project_path"] = None
        _update_recent_projects()
        _send_data_2_data_manager(data)
        _PARAMETERS["is_project_saved"] = False
        _notify_listeners()
        return False, f"Project path [{path}] does not exists!"

    _PARAMETERS["disk_project_path"] = path
    _update_recent_projects()
    _notify_listeners()
    _send_data_2_data_manager(data)
    return True, f"Project {path} loaded."



def save_project() -> tuple[bool, str]:
    if not _PARAMETERS["json_project_path"]:
        return False, "NO JSON PATH"

    data = _receive_data_from_data_manager()
    data["disk_project_path"] = _PARAMETERS["disk_project_path"]

    succes, exception_string = _save_json_2_disk(data)

    if not succes:
        return False, exception_string
    
    _PARAMETERS["is_project_saved"] = True
    _update_recent_projects()
    _notify_listeners()
    return True, "Project Saved"



def save_project_as(new_path: Path) -> Callable:
    _PARAMETERS["json_project_path"] = str(new_path)
    return save_project()



def new_project():
    _DATA_MANAGER.ROOT.removeRows(0, _DATA_MANAGER.ROOT.rowCount())
    _DATA_MANAGER._update_data_summary()    
    _PARAMETERS["disk_project_path"] = None
    _PARAMETERS["is_project_saved"] = True
    _PARAMETERS["json_project_path"] = None
    _notify_listeners()



def is_project_saved() -> bool:
    return _PARAMETERS["is_project_saved"]
    





##################### PRIVATE LOGIC ######################

def _notify_listeners() -> None:
    for listener in _listeners:
        listener.receive_parameters_from_project_manager(_PARAMETERS)


def _open_json_from_disk(path: Path) -> dict:
    try:
        with open(str(path), 'r', encoding='utf8') as f:
            data = json.loads(f.read())    
        return True, data
    except Exception as e:
        return False, str(e)


def _save_json_2_disk(data: dict) -> tuple[bool, str]:
    try:
        with open(_PARAMETERS["json_project_path"], 'w', encoding='utf8') as f:
            f.write(json.dumps(data, indent=2))
        return True, ""
    except Exception as e:
        return False, str(e)              


def _send_data_2_data_manager(data) -> None:
    _DATA_MANAGER.receive_data_from_project_manager(data)    


def _receive_data_from_data_manager() -> dict:
    return _DATA_MANAGER.provide_data_4_project_manager()    


def _update_recent_projects() -> None:
    path = _PARAMETERS["json_project_path"]
    if not _SETTINGS.recent_projects:
        _SETTINGS.recent_projects = [path,]
        return

    if path not in _SETTINGS.recent_projects:
        _SETTINGS.recent_projects.insert(0, path)
    else:
        _SETTINGS.recent_projects.remove(path)
        _SETTINGS.recent_projects.insert(0, path)

    while len(_SETTINGS.recent_projects) > 10:
        _SETTINGS.recent_projects.pop()

