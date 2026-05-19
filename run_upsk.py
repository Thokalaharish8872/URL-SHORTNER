import subprocess
import os
import sys
import traceback

try:
    os.environ['UPSK_WORKSPACE'] = 'c:/Users/thoka/MyProjects/CAW Assessment'
    cwd = 'c:/Users/thoka/MyProjects/CAW Assessment'
    upsk_path = os.path.join(cwd, '.bin', 'upsk.exe')
    
    # Read the report JSON
    with open('progress/technical-communication/module_01_report.json', 'r', encoding='utf-8') as f:
        report_json = f.read()
    
    # Try report via stdin (JSON piped to upsk report)
    result = subprocess.run(
        [upsk_path, 'report'],
        input=report_json,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    
    output = []
    output.append(f"=== upsk report (stdin) ===")
    output.append(f"Return code: {result.returncode}")
    output.append(f"STDOUT:\n{result.stdout}")
    output.append(f"STDERR:\n{result.stderr}")
    
    # Also try next command to advance
    result2 = subprocess.run(
        [upsk_path, 'next', '--summary', 'Completed Module 1 reflection on code review as communication', '--evidence', 'progress/technical-communication/reflection.md'],
        capture_output=True,
        text=True,
        cwd=cwd
    )
    
    output.append(f"\n=== upsk next ===")
    output.append(f"Return code: {result2.returncode}")
    output.append(f"STDOUT:\n{result2.stdout}")
    output.append(f"STDERR:\n{result2.stderr}")
    
    with open('fresh_upsk_output.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
        
except Exception as e:
    with open('fresh_upsk_output.txt', 'w', encoding='utf-8') as f:
        f.write(f"ERROR: {e}\n")
        f.write(traceback.format_exc())
