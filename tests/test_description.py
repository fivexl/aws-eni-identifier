import json

import pytest

import aws_eni_identifier


def json_load(json_path: str):
    with open(json_path) as f:
        return json.load(f)


@pytest.mark.parametrize("description, result", [(test["description"], test["result"]) for test in json_load("./tests/assets/description_only.json")])
def test_description_regexes(description, result):
    assert result == aws_eni_identifier.extract_description_info(description)
