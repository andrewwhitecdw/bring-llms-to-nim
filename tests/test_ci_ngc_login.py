from pathlib import Path


CI_YML = Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'ci.yml'


def test_ngc_login_status_checked_directly():
    content = CI_YML.read_text()
    login_block = content.split('name: Login to NGC', 1)[-1]
    login_block = login_block.split('      - name:', 1)[0]
    assert 'if [ $? -eq 0 ]' not in login_block, (
        'checking $? after a pipeline under set -e/pipefail is unreachable; '
        'use \'if cmd; then ... else ... fi\''
