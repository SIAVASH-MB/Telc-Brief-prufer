import prompts
import sys

def test_prompts():
    print("Testing B1 Prompt...")
    b1 = prompts.get_rubric("B1")
    if "Criterion I: Task Management" in b1:
        print("Success: B1 Rubric contains correct headers.")
    else:
        print("Failure: B1 Rubric missing headers.")
        sys.exit(1)

    print("Testing B2 Prompt...")
    b2 = prompts.get_rubric("B2")
    if "Criterion I: Task Management" in b2:
        print("Success: B2 Rubric contains correct headers.")
    else:
        print("Failure: B2 Rubric missing headers.")
        sys.exit(1)

    print("Testing System Prompt (No Topic)...")
    sys_prompt = prompts.get_system_prompt("B1")
    if "certified telc examiner" in sys_prompt:
        print("Success: System prompt correct.")
    else:
        print("Failure: System prompt incorrect.")
        sys.exit(1)

    print("Testing System Prompt (With Topic)...")
    fake_topic = {
        "subject": "Test Subject",
        "description": "Test Description",
        "points": ["P1", "P2", "P3", "P4"]
    }
    sys_prompt_topic = prompts.get_system_prompt("B1", fake_topic)
    if "Test Subject" in sys_prompt_topic and "Test Description" in sys_prompt_topic:
        print("Success: Topic correctly injected into system prompt.")
    else:
        print("Failure: Topic missing from system prompt.")
        sys.exit(1)

if __name__ == "__main__":
    test_prompts()
