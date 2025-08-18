import pytest
from pathlib import Path


def test_template_file_present():
    tpl = Path("src/lcpi/reporting/templates/optimisation_tank.jinja2")
    assert tpl.exists()


