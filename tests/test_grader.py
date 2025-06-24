import yaml
from pathlib import Path
import pytest

from grader import compute_overall_grade, calculate_final_grade


@pytest.fixture
def rubric_config():
    rubric_path = Path(__file__).resolve().parents[1] / "rubric.yml"
    with open(rubric_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.mark.parametrize(
    "points,expected",
    [
        (28, "A"),
        (24, "B"),
        (23, "C"),
        (18, "D"),
        (5, "E"),
    ],
)
def test_compute_overall_grade(points, expected, rubric_config):
    bands = rubric_config["grade_bands"]
    total_possible = rubric_config["total_points_possible"]
    assert compute_overall_grade(points, bands, total_possible) == expected


def test_calculate_final_grade_mock():
    rubric = {
        "criteria": {
            "c1": {"max_points": 5},
            "c2": {"max_points": 5},
        },
        "grade_bands": {"A": 9, "B": 8, "C": 6, "D": 5, "E": 0},
        "total_points_possible": 10,
    }
    bands_data = {"c1": 5, "c2": 4}
    result = calculate_final_grade(bands_data, 100, rubric)

    assert result["total_points"] == 9
    assert result["overall_grade"] == "A"
    assert result["breakdown"]["c1"] == {"band": 5, "points": 5}
    assert result["breakdown"]["c2"] == {"band": 4, "points": 4}
