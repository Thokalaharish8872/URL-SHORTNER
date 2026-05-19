import subprocess
import os
import json
import traceback
from datetime import datetime

os.environ['UPSK_WORKSPACE'] = 'c:/Users/thoka/MyProjects/CAW Assessment'
cwd = 'c:/Users/thoka/MyProjects/CAW Assessment'
upsk_path = os.path.join(cwd, '.bin', 'upsk.exe')

output = []
output.append(f"Timestamp: {datetime.now().isoformat()}")

try:
    # Read the report JSON
    with open('progress/technical-communication/module_01_report.json', 'r') as f:
        report_json = f.read()
    output.append("Read report JSON successfully")
    output.append(f"JSON length: {len(report_json)} chars")
    output.append(f"Has events: {'events' in report_json}")
    
    # Step 1: Submit report via stdin
    output.append("\n=== Step 1: upsk report ===")
    result = subprocess.run(
        [upsk_path, 'report'],
        input=report_json,
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=30
    )
    output.append(f"Return code: {result.returncode}")
    output.append(f"STDOUT: {result.stdout}")
    output.append(f"STDERR: {result.stderr}")
    
    # Step 2: Try upsk next to advance
    output.append("\n=== Step 2: upsk next ===")
    result2 = subprocess.run(
        [upsk_path, 'next', '--summary', 'Completed Module 1 reflection', '--evidence', 'progress/technical-communication/reflection.md'],
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=30
    )
    output.append(f"Return code: {result2.returncode}")
    output.append(f"STDOUT: {result2.stdout}")
    output.append(f"STDERR: {result2.stderr}")
    
except Exception as e:
    output.append(f"ERROR: {e}")
    output.append(traceback.format_exc())

with open('new_result.txt', 'w') as f:
    f.write('\n'.join(output))
