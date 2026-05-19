import subprocess
import json
import os

with open('api/report_m4.json', 'r') as f:
    report_data = f.read()

upsk_path = os.path.join('.bin', 'upsk.exe')
cmd = [upsk_path, 'report', report_data, '--json']

result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
if result.returncode != 0:
    exit(1)
