import subprocess
import os

os.environ['UPSK_WORKSPACE'] = 'c:/Users/thoka/MyProjects/CAW Assessment'
cwd = 'c:/Users/thoka/MyProjects/CAW Assessment'
upsk_path = os.path.join(cwd, '.bin', 'upsk.exe')

# Read the report JSON
with open('progress/technical-communication/module_01_report.json', 'r') as f:
    report_json = f.read()

# Submit report via stdin
result = subprocess.run(
    [upsk_path, 'report'],
    input=report_json,
    capture_output=True,
    text=True,
    cwd=cwd,
    timeout=60
)

# Write output
with open('final_report_output.txt', 'w') as f:
    f.write(f"Return code: {result.returncode}\n")
    f.write(f"STDOUT:\n{result.stdout}\n")
    f.write(f"STDERR:\n{result.stderr}\n")

# If successful, try to advance
if result.returncode == 0:
    result2 = subprocess.run(
        [upsk_path, 'next', '--summary', 'Completed Module 1 reflection', '--evidence', 'progress/technical-communication/reflection.md'],
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=30
    )
    with open('final_next_output.txt', 'w') as f:
        f.write(f"Return code: {result2.returncode}\n")
        f.write(f"STDOUT:\n{result2.stdout}\n")
        f.write(f"STDERR:\n{result2.stderr}\n")
