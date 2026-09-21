#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser(description='Pin component commits for a stable release; does not create a tag')
p.add_argument('version')
a = p.parse_args()
if not re.fullmatch(r'\d+\.\d+\.\d+', a.version):p.error('Use MAJOR.MINOR.PATCH')
sources = {}
for name, repo in [('backend','backend'),('frontend','frontend'),('files','module-files'),('terminal','module-terminal')]:
    data = json.loads(subprocess.check_output(['gh','api',f'repos/PaNasMs/{repo}/commits/main']))
    sources[name] = data['sha']
Path('release-lock.json').write_text(json.dumps({'version':a.version,'sources':sources},indent=2)+'\n')
print('Review and commit release-lock.json, then tag that commit with v'+a.version)
