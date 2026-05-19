import json
import sys

try:
    data = json.load(sys.stdin)
    session = data.get("session", {})
    skill = session.get("skill", {})
    module = session.get("module", {})
    step = session.get("step", {})
    print(f"Skill: {skill.get('slug')}")
    print(f"Module: {module.get('id')} ({module.get('label')})")
    print(f"Step: {step.get('id')} ({step.get('label')})")
    
    # Also print prompt suggestions
    prompts = data.get("prompt_suggestions", [])
    if prompts:
        print("\nSuggestions:")
        for p in prompts:
            print(f"- {p}")
except Exception as e:
    print(f"Error parsing JSON: {e}")
