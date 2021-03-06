import os
import re

new_version = os.sys.argv[1]


with open('setup.py', 'r+') as fh:
    text = fh.read()
    pre_string = r'version="'
    pre_pattern_escaped = re.escape(pre_string).replace(r'\\\\', r'\\')
    pattern = pre_pattern_escaped + r'[a-zA-Z0-9-_.]+"'
    repl = pre_string + new_version + '"'
    text = re.sub(pattern, repl, text, 2)
    fh.seek(0)
    fh.write(text)
    print('bumped the version in setup.py:\n{}'.format('\n'.join(re.findall(pattern, text))))

