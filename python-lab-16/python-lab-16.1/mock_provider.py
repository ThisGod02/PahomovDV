from __future__ import annotations


class MockGigaChatProvider:
    def generate_code(self, description: str, language: str) -> str:
        if "palindrome" in description.lower():
            return """def is_palindrome(value: str) -> bool:\n    \"\"\"Return True if the string reads the same both ways.\"\"\"\n    normalized = ''.join(char.lower() for char in value if char.isalnum())\n    return normalized == normalized[::-1]\n"""
        return f"# Mock code for {language}\n# Task: {description}\n"

    def refactor_code(self, code: str, requirements: str) -> str:
        return (
            'def calculate_total(items: list[dict]) -> float:\n'
            '    """Calculate total order amount with basic validation."""\n'
            "    total = 0.0\n"
            "    for item in items:\n"
            "        quantity = int(item.get('quantity', 0))\n"
            "        price = float(item.get('price', 0))\n"
            "        if quantity < 0 or price < 0:\n"
            "            raise ValueError('Negative values are not allowed')\n"
            "        total += quantity * price\n"
            "    return total\n"
        )

    def generate_tests(self, code: str, framework: str) -> str:
        return (
            "from generated_code import is_palindrome\n\n"
            "def test_palindrome_positive() -> None:\n"
            "    assert is_palindrome('Level') is True\n\n"
            "def test_palindrome_negative() -> None:\n"
            "    assert is_palindrome('Python') is False\n"
        )

    def generate_documentation(self, code: str, doc_type: str) -> str:
        return (
            "# Generated README\n\n"
            "This demo shows how an LLM assistant can generate code, tests, and documentation.\n"
        )
