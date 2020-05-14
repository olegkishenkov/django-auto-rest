import os
import re

new_version = os.sys.argv[1]

with open('README.md', 'r+') as fh:
    text = fh.read()
    pre_string = r'```python -m pip install --index-url https://test.pypi.org/simple autorest-oleg1248='
    pre_pattern_escaped = re.escape(pre_string).replace(r'\\\\', r'\\')
    pattern = pre_pattern_escaped + r'[a-zA-Z0-9-_.]+```'
    repl = pre_string + new_version + '```'
    text = re.sub(pattern, repl, text, 2)
    fh.seek(0)
    fh.write(text)

with open('setup.py', 'r+') as fh:
    text = fh.read()
    pre_string = r'version="'
    pre_pattern_escaped = re.escape(pre_string).replace(r'\\\\', r'\\')
    pattern = pre_pattern_escaped + r'[a-zA-Z0-9-_.]+"'
    repl = pre_string + '0.0.5"'
    text = re.sub(pattern, repl, text, 2)
    fh.seek(0)
    fh.write(text)

