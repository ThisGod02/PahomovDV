from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from mock_provider import MockGigaChatProvider


load_dotenv()


class GigaChatAssistant:
    def __init__(self) -> None:
        self.credentials = os.getenv("GIGACHAT_CREDENTIALS")
        self.scope = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
        self.model = os.getenv("GIGACHAT_MODEL", "GigaChat-2")
        self.verify_ssl = os.getenv("GIGACHAT_VERIFY_SSL_CERTS", "False").lower() == "true"
        self.mode = os.getenv("GIGACHAT_MODE", "mock").lower()
        self.provider = self._build_provider()

    def _build_provider(self) -> Any:
        if self.mode == "real" and self.credentials:
            try:
                from gigachat import GigaChat
            except Exception:
                return MockGigaChatProvider()
            return GigaChat(
                credentials=self.credentials,
                scope=self.scope,
                model=self.model,
                verify_ssl_certs=self.verify_ssl,
            )
        return MockGigaChatProvider()

    def _chat(self, prompt: str) -> str:
        if isinstance(self.provider, MockGigaChatProvider):
            return prompt
        response = self.provider.chat(prompt)
        return response.choices[0].message.content

    def generate_code(self, description: str, language: str = "python") -> str:
        if isinstance(self.provider, MockGigaChatProvider):
            return self.provider.generate_code(description, language)
        prompt = (
            f"You are a senior {language} developer. Write code for this task:\n"
            f"{description}\n"
            "Return only code."
        )
        return self._chat(prompt)

    def refactor_code(self, code: str, requirements: str) -> str:
        if isinstance(self.provider, MockGigaChatProvider):
            return self.provider.refactor_code(code, requirements)
        prompt = (
            "Refactor this Python code. Preserve behavior and improve readability.\n"
            f"Requirements: {requirements}\nCode:\n{code}\n"
            "Return only code."
        )
        return self._chat(prompt)

    def generate_tests(self, code: str, framework: str = "pytest") -> str:
        if isinstance(self.provider, MockGigaChatProvider):
            return self.provider.generate_tests(code, framework)
        prompt = (
            f"Write {framework} tests for this code. Cover positive, negative, and edge cases.\n{code}"
        )
        return self._chat(prompt)

    def generate_documentation(self, code: str, doc_type: str = "readme") -> str:
        if isinstance(self.provider, MockGigaChatProvider):
            return self.provider.generate_documentation(code, doc_type)
        prompt = f"Generate {doc_type} documentation for this code:\n{code}"
        return self._chat(prompt)

    @staticmethod
    def save_output(path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
