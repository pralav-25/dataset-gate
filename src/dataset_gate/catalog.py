"""Rule discoverability shared by CLI, API, documentation and contract authors."""

from dataset_gate.rules import catalog


def rule_catalog():
    return [
        {
            "name": spec.name,
            "description": spec.description,
            "column_required": spec.column,
            "parameters": sorted(spec.parameters),
            "required_parameters": list(spec.required),
        }
        for _, spec in sorted(catalog().items())
    ]
