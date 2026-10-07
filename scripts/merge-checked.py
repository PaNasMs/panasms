#!/usr/bin/env python3
"""Merge one PR only after successful checks on its exact current head."""
import argparse
import json
import subprocess


def checked(pr, allowed_skipped=()):
    checks = pr.get('statusCheckRollup') or []
    succeeded = lambda c: c.get('conclusion') == 'SUCCESS' if c.get('__typename') == 'CheckRun' else c.get('state') == 'SUCCESS'
    return any(succeeded(c) for c in checks) and not pr.get('isDraft') and pr.get('mergeable') == 'MERGEABLE' and all(
        (c.get('status') == 'COMPLETED' and (succeeded(c) or (c.get('conclusion') == 'SKIPPED' and c.get('name') in allowed_skipped)))
        if c.get('__typename') == 'CheckRun' else c.get('state') == 'SUCCESS'
        for c in checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo')
    parser.add_argument('pr', type=int)
    parser.add_argument('--allow-skipped-check', action='append', default=[], help='Exact name of a reviewed, intentionally conditional job')
    args = parser.parse_args()
    fields = 'headRefOid,isDraft,mergeable,statusCheckRollup'
    pr = json.loads(subprocess.check_output(['gh', 'pr', 'view', str(args.pr), '--repo', args.repo, '--json', fields]))
    if not checked(pr, args.allow_skipped_check):
        raise SystemExit('Merge refused: every check must explicitly succeed on a mergeable, non-draft PR. Missing, pending, skipped and cancelled checks are not success.')
    subprocess.run(['gh', 'pr', 'merge', str(args.pr), '--repo', args.repo, '--squash', '--match-head-commit', pr['headRefOid']], check=True)


if __name__ == '__main__':
    main()
