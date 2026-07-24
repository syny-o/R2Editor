from data_manager.view import help_func
from data_manager.view.actions_handler import ActionsHandler


def create_view_actions(view):
    manager = view.DATA_MANAGER
    toolbar = view.uiControlToolbar

    view.action_expand_all_children = help_func.create_action(
        ':/16x16/icons/16x16/cil-expand-down.png',
        'Expand All',
        slot=view.uiDataTreeView.expand_all_children,
        toolbar=None,
    )
    view.action_collapse_all_children = help_func.create_action(
        ':/16x16/icons/16x16/cil-expand-up.png',
        'Collapse All',
        slot=view.uiDataTreeView.collapse_all_children,
        toolbar=None,
    )
    view.action_goto_previous_index = help_func.create_action(
        ':/16x16/icons/16x16/cil-chevron-left.png',
        'Previous',
        slot=view.uiDataTreeView.goto_previous_index,
        toolbar=None,
    )
    view.action_move_up = help_func.create_action(
        ':/16x16/icons/16x16/cil-chevron-top.png',
        'Move Up',
        slot=lambda: manager.move_node(direction='up'),
        shortcut='Ctrl+Up',
        toolbar=toolbar,
    )
    view.action_move_down = help_func.create_action(
        ':/16x16/icons/16x16/cil-chevron-bottom.png',
        'Move Down',
        slot=lambda: manager.move_node(direction='down'),
        shortcut='Ctrl+Down',
        toolbar=toolbar,
    )
    view.action_duplicate = help_func.create_action(
        ':/16x16/icons/16x16/cil-library.png',
        'Duplicate',
        slot=manager.duplicate_node,
        shortcut='Ctrl+D',
        toolbar=toolbar,
    )
    view.action_copy = help_func.create_action(
        ':/16x16/icons/16x16/cil-clone.png',
        'Copy',
        slot=manager.copy_node,
        shortcut='Ctrl+C',
        toolbar=toolbar,
    )
    view.action_paste = help_func.create_action(
        ':/16x16/icons/16x16/cil-plus.png',
        'Paste',
        slot=manager.paste_node,
        shortcut='Ctrl+V',
        toolbar=toolbar,
    )
    view.action_edit = help_func.create_action(
        ':/16x16/icons/16x16/cil-pencil.png',
        'Edit',
        slot=manager.edit_node_request,
        shortcut='F4',
        toolbar=toolbar,
    )
    view.action_remove = help_func.create_action(
        ':/16x16/icons/16x16/cil-x.png',
        'Remove',
        slot=manager.remove_node,
        shortcut='Del',
        toolbar=toolbar,
    )
    view.action_export = help_func.create_action(
        ':/16x16/icons/16x16/cil-save.png',
        'Export',
        slot=manager.tree_2_file,
        shortcut='Ctrl+E',
        toolbar=toolbar,
    )
    view.action_normalise_a2l_file = help_func.create_action(
        ':/16x16/icons/16x16/cil-chart-line.png',
        'Normalise (VDA spec.)',
        slot=manager._normalise_a2l_file,
        toolbar=None,
    )
    view.action_update_module = help_func.create_action(
        ':/16x16/icons/16x16/cil-cloud-download.png',
        'Update',
        slot=lambda: manager._open_form_for_doors_connection_inputs(
            all_modules=False
        ),
        toolbar=None,
    )
    view.action_add_to_ignore_list = help_func.create_action(
        ':/16x16/icons/16x16/cil-task.png',
        'Add To Ignore List',
        slot=manager._add_to_ignore_list,
        toolbar=None,
    )
    view.action_remove_from_ignore_list = help_func.create_action(
        ':/16x16/icons/16x16/cil-external-link.png',
        'Remove From Ignore List',
        slot=manager._remove_from_ignore_list,
        toolbar=None,
    )
    view.action_stop_filtering = help_func.create_action(
        ':/16x16/icons/16x16/cil-x.png',
        'Remove Text Filter',
        slot=view._stop_filtering,
        toolbar=None,
    )

    return ActionsHandler(
        DATA_MANAGER=manager,
        action_expand_all_children=view.action_expand_all_children,
        action_collapse_all_children=view.action_collapse_all_children,
        action_remove_node=view.action_remove,
        action_edit_node=view.action_edit,
        action_duplicate_node=view.action_duplicate,
        action_copy_node=view.action_copy,
        action_paste_node=view.action_paste,
        action_export_node=view.action_export,
        action_move_up_node=view.action_move_up,
        action_move_down_node=view.action_move_down,
        action_normalise_a2l_file=view.action_normalise_a2l_file,
        action_update_module=view.action_update_module,
        action_add_to_ignore_list=view.action_add_to_ignore_list,
        action_remove_from_ignore_list=view.action_remove_from_ignore_list,
        action_stop_filtering=view.action_stop_filtering,
    )
