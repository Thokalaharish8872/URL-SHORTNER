import subprocess
import os

os.environ['UPSK_WORKSPACE'] = 'c:/Users/thoka/MyProjects/CAW Assessment'

# Test upsk version
result = subprocess.run(
    ['.bin/upsk.exe', '--version'],
    capture_output=True,
    text=True,
    cwd='c:/Users/thoka/MyProjects/CAW Assessment'
)

with open('test_output.txt', 'w') as f:
    f.write(f"Return code: {result.returncode}\n")
    f.write(f"STDOUT: {result.stdout}\n")
    f.write(f"STDERR: {result.stderr}\n")
