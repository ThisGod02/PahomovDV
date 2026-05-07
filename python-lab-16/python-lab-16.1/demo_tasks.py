from __future__ import annotations

from pathlib import Path

from gigachat_client import GigaChatAssistant


LEGACY_CODE = """
def total(items):
    s = 0
    for i in items:
        s += i['price'] * i['quantity']
    return s
"""


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "generated"
    assistant = GigaChatAssistant()

    generated_code = assistant.generate_code("Write a Python function that checks if a string is a palindrome.")
    refactored_code = assistant.refactor_code(
        LEGACY_CODE,
        "Add type hints, validation, and clearer variable names.",
    )
    generated_tests = assistant.generate_tests(generated_code)
    generated_docs = assistant.generate_documentation(generated_code)

    assistant.save_output(output_dir / "generated_code.py", generated_code)
    assistant.save_output(output_dir / "refactored_code.py", refactored_code)
    assistant.save_output(output_dir / "test_generated_code.py", generated_tests)
    assistant.save_output(output_dir / "README_generated.md", generated_docs)

    print("GigaChat demo completed")
    print(f"Mode: {assistant.mode}")
    print(f"Artifacts: {output_dir}")


if __name__ == "__main__":
    main()
