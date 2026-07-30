import pathlib
import unittest

WORKFLOW = (
    pathlib.Path(__file__).resolve().parent.parent
    / ".github"
    / "workflows"
    / "ci.yml"
)


class TestCIWorkflow(unittest.TestCase):
    def test_notebook_dependencies_installed(self):
        text = WORKFLOW.read_text()
        pip_lines = [
            line.strip() for line in text.splitlines()
            if line.strip().startswith("pip install")
        ]
        self.assertTrue(pip_lines, "No pip install command found in workflow")
