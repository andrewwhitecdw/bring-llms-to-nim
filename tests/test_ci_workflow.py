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
            if line.strip().startswith("pip install ipykernel")
        ]
        self.assertTrue(pip_lines, "No notebook dependency install command found in workflow")
        installs = " ".join(pip_lines)
        self.assertIn("papermill", installs)
        self.assertIn("nbconvert", installs)
