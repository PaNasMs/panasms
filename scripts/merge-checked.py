#!/usr/bin/env python3
"""Merge one PR only after successful checks on its exact current head."""
import argparse
import json
import subprocess


def checked(pr):
    checks = pr.get('statusCheckRollup') or []
    return bool(checks) and not pr.get('isDraft') and pr.get('mergeable') == 'MERGEABLE' and all(
        (c.get('status') == 'COMPLETED' and c.get('conclusion') == 'SUCCESS')
        if c.get('__typename') == 'CheckRun' else c.get('state') == 'SUCCESS'
        for c in checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo')
    parser.add_argument('pr', type=int)
    args = parser.parse_args()
    fields = 'headRefOid,isDraft,mergeable,statusCheckRollup'
    pr = json.loads(subprocess.check_output(['gh', 'pr', 'view', str(args.pr), '--repo', args.repo, '--json', fields]))
    if not checked(pr):
        raise SystemExit('Merge refused: every check must explicitly succeed on a mergeable, non-draft PR. Missing, pending, skipped and cancelled checks are not success.')
    subprocess.run(['gh', 'pr', 'merge', str(args.pr), '--repo', args.repo, '--squash', '--match-head-commit', pr['headRefOid']], check=True)


if __name__ == '__main__':
    main()
