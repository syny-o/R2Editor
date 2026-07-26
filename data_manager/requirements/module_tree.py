from data_manager.doors.output_parser import (
    parse_module_output,
    parse_requirement,
)
from data_manager.nodes.requirement_node import RequirementNode
from data_manager.requirements.serialization import requirement_module_to_dict
from data_manager.requirements.tree_builder import append_nodes_by_level


def create_tree_from_project_data(module, requirement_data, timestamp):
    module.timestamp = timestamp

    nodes = []
    for item in requirement_data:
        reference = item.get("reference")
        heading = item.get("heading")
        file_references = item.get("file_references")
        is_covered = item.get("is_covered")

        if is_covered is not None and not heading:
            module._coverage_dict.update(
                {reference.lower(): file_references}
            )

        nodes.append(
            RequirementNode(
                module,
                reference,
                heading,
                int(item.get("level")),
                item.get("outlinks"),
                item.get("inlinks"),
                file_references,
                item.get("columns_data"),
                is_covered,
            )
        )

    append_nodes_by_level(module, nodes)


def populate_tree_from_doors(module, doors_output):
    module_data = parse_module_output(doors_output, module.path)
    if module_data is None:
        return

    module.baseline = module_data["baselines"]
    module.attributes = module_data["attributes"]

    nodes = [
        create_requirement_node(module, requirement_text)
        for requirement_text in module_data["requirements"]
    ]
    append_nodes_by_level(module, nodes)


def create_requirement_node(module, requirement_text):
    parsed = parse_requirement(
        requirement_text,
        module.column_number_as_identifier,
    )
    return RequirementNode(
        module,
        parsed["identifier"],
        parsed["heading"],
        parsed["level"],
        parsed["outlinks"],
        parsed["inlinks"],
        None,
        parsed["columns"],
    )


def append_module_to_project_data(module, project_data):
    project_data["REQUIREMENT MODULES"].append(
        requirement_module_to_dict(module)
    )
    return project_data
