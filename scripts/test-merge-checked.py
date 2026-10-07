import importlib.util
from pathlib import Path
import unittest
spec = importlib.util.spec_from_file_location('guard', Path(__file__).with_name('merge-checked.py'))
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class Checks(unittest.TestCase):
    def test_conditional_release_is_explicit_and_never_allows_cancellation(self):
        success = {'__typename':'CheckRun','name':'build','status':'COMPLETED','conclusion':'SUCCESS'}
        optional = {'__typename':'CheckRun','name':'release','status':'COMPLETED','conclusion':'SKIPPED'}
        pr = {'mergeable':'MERGEABLE','statusCheckRollup':[success, optional]}
        self.assertFalse(guard.checked(pr))
        self.assertTrue(guard.checked(pr, ['release']))
        optional['conclusion'] = 'CANCELLED'
        self.assertFalse(guard.checked(pr, ['release']))
        optional['conclusion'] = 'SKIPPED'
        pr['statusCheckRollup'] = [optional]
        self.assertFalse(guard.checked(pr, ['release']))

    def test_requires_explicit_success(self):
        for conclusion in ('SUCCESS', 'FAILURE', 'CANCELLED', 'SKIPPED', 'NEUTRAL', 'TIMED_OUT', None):
            pr = {'mergeable': 'MERGEABLE', 'statusCheckRollup': [{'__typename': 'CheckRun', 'status': 'COMPLETED', 'conclusion': conclusion}]}
            self.assertEqual(guard.checked(pr), conclusion == 'SUCCESS')
        self.assertFalse(guard.checked({'mergeable': 'MERGEABLE', 'statusCheckRollup': []}))
        self.assertFalse(guard.checked({'mergeable': 'MERGEABLE', 'statusCheckRollup': [{'__typename':'CheckRun','status':'IN_PROGRESS','conclusion':'SUCCESS'}]}))


if __name__ == '__main__':
    unittest.main()
