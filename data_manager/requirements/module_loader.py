from data_manager.nodes.requirement_module import RequirementModule


def initialise(data: dict, root_node):
    for module_data in data.get("REQUIREMENT MODULES") or []:
        requirements = module_data.get("requirements")
        path = module_data.get("path")
        if requirements and not path:
            continue

        module = RequirementModule(
            root_node,
            path,
            module_data.get("columns"),
            module_data.get("attributes"),
            module_data.get("baseline"),
            module_data.get("coverage_filter"),
            module_data.get("coverage_dict"),
            module_data.get("update_time"),
            module_data.get("ignore_list"),
            module_data.get("notes"),
            module_data.get("current_baseline"),
            module_data.get("column_number_as_identifier"),
        )

        if requirements:
            module.create_tree_from_requirements_data(
                requirements, module_data.get("update_time")
            )

        root_node.appendRow(module)
        if requirements:
            module.update_icons_according_to_coverage()
