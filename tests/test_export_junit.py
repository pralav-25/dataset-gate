from xml.etree.ElementTree import fromstring

from dataset_gate.exporters.junit import render


def test_xml_semantics():
    report = {
        "contract": "A&B",
        "summary": {"errors": 1},
        "results": [
            {
                "id": "e",
                "check": "type",
                "severity": "error",
                "passed": False,
                "failed": 1,
                "checked": 3,
                "message": "<bad>",
            },
            {
                "id": "w",
                "check": "type",
                "severity": "warning",
                "passed": False,
                "failed": 1,
                "checked": 3,
                "message": "warn",
            },
        ],
    }
    root = fromstring(render(report))
    assert root.attrib["failures"] == "1"
    assert len(root.findall(".//failure")) == 1 and len(root.findall(".//system-out")) == 1
