from pathlib import Path
import os
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/canon_gate.py'


class CanonGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        for name in ['SYSTEM_CONTRACT.md', 'REPO_MAP.md', 'AGENTS_TODO.md']:
            (self.root / name).write_text('fixture\n')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'base')
        self.sha = self.git('rev-parse', 'HEAD').strip()

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, text=True,
                              capture_output=True, check=True).stdout

    def gate(self, base=None, head=None):
        return subprocess.run(['python', str(SCRIPT)], cwd=self.root, text=True,
            capture_output=True, env={**os.environ, 'BASE_SHA': base or self.sha,
                                     'HEAD_SHA': head or self.sha})

    def test_valid_empty_diff_still_checks_files(self):
        self.assertEqual(self.gate().returncode, 0)
        (self.root / 'REPO_MAP.md').unlink()
        self.assertNotEqual(self.gate().returncode, 0)

    def test_unavailable_base_fails(self):
        result = self.gate(base='a' * 40)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('EVIDENCE_UNAVAILABLE', result.stdout)

    def test_unavailable_head_fails(self):
        self.assertNotEqual(self.gate(head='b' * 40).returncode, 0)

    def test_checkout_mismatch_fails(self):
        (self.root / 'new.txt').write_text('new\n')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'next')
        result = self.gate(head=self.sha)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Checkout HEAD does not equal', result.stdout)

    def test_success_does_not_authorize(self):
        result = self.gate()
        self.assertEqual(result.returncode, 0)
        self.assertNotIn('Merge authorized', result.stdout)
        self.assertIn(self.sha, result.stdout)
        self.assertIn('separate requirements', result.stdout)
