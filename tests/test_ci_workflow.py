import unittest
from pathlib import Path


WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"


def get_step_run_block(workflow_text: str, step_name: str) -> str:
    lines = workflow_text.splitlines()
    in_step = False
    run_indent = None
    block_lines = []
    for line in lines:
        if line.startswith("- name:") and step_name in line:
            in_step = True
            continue
        if not in_step:
            continue
        # Next step ends the current step block.
        if line.startswith("- name:"):
            break
        if run_indent is None:
            stripped = line.lstrip(" ")
            if stripped.startswith("run:"):
                run_indent = len(line) - len(stripped)
                continue
        else:
            if not line.strip():
                block_lines.append(line)
                continue
            indent = len(line) - len(line.lstrip(" "))
            if indent > run_indent:
                block_lines.append(line)
            else:
                break
    return "\n".join(block_lines)


class TestCiWorkflow(unittest.TestCase):
    def test_docker_login_result_is_tested_in_if_condition(self):
        """Checking $? after a bare pipeline is unreachable.

        GitHub Actions runs shell steps with -e and pipefail by default, so a
        failing docker login would exit the step before the manual $? check.
        The command must be the condition of the if statement instead.
        """
        run_block = get_step_run_block(
            WORKFLOW.read_text(encoding="utf-8"), "Login to NGC"
        )
        self.assertIn("docker login nvcr.io", run_block)
        self.assertNotIn(
            "if [ $? -eq 0 ]",
            run_block,
            "Manual $? check after docker login is unreachable under set -e/pipefail",
        )

