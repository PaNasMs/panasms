import importlib.util
from pathlib import Path
import unittest
spec = importlib.util.spec_from_file_location('guard', Path(__file__).with_name('merge-checked.py'))
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class Checks(unittest.TestCase):
    def test_requires_explicit_success(self):
        for conclusion in ('SUCCESS', 'FAILURE', 'CANCELLED', 'SKIPPED', 'NEUTRAL', 'TIMED_OUT', None):
            pr = {'mergeable': 'MERGEABLE', 'statusCheckRollup': [{'__typename': 'CheckRun', 'status': 'COMPLETED', 'conclusion': conclusion}]}
            self.assertEqual(guard.checked(pr), conclusion == 'SUCCESS')
        self.assertFalse(guard.checked({'mergeable': 'MERGEABLE', 'statusCheckRollup': []}))
        self.assertFalse(guard.checked({'mergeable': 'MERGEABLE', 'statusCheckRollup': [{'__typename':'CheckRun','status':'IN_PROGRESS','conclusion':'SUCCESS'}]}))


if __name__ == '__main__':
    unittest.main()
