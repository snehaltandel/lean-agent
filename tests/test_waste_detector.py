"""Unit tests for the WasteDetector tool."""
from app.tools.waste_detector import WasteDetector


def test_detects_multiple_wastes():
    tool = WasteDetector()
    output = tool.run(
        {
            "process_description": "Team members wait for approvals causing delay and extra motion \
when walking to the manager, leading to rework on manual forms.",
        }
    )

    categories = {waste["category"] for waste in output["wastes"]}
    assert {"waiting", "motion", "overprocessing"}.issubset(categories)
    assert "quick win" not in output["summary"].lower()


def test_handles_no_waste_case():
    tool = WasteDetector()
    output = tool.run({"process_description": "The automated pipeline runs smoothly."})
    assert output["wastes"] == []
    assert "no obvious wastes" in output["summary"].lower()
