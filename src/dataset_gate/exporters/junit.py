"""One test case per rule. Warnings appear in system-out and do not fail CI."""

from xml.etree.ElementTree import Element, SubElement, tostring

EXTENSION = "xml"


def render(report):
    root = Element(
        "testsuite",
        name=report["contract"],
        tests=str(len(report["results"])),
        failures=str(report["summary"]["errors"]),
    )
    for result in report["results"]:
        case = SubElement(root, "testcase", name=result["id"], classname=result["check"])
        if not result["passed"]:
            tag = "failure" if result["severity"] == "error" else "system-out"
            child = SubElement(case, tag)
            child.text = f"{result['failed']}/{result['checked']}: {result['message']}"
    return tostring(root, encoding="unicode", xml_declaration=True) + "\n"
