from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def generate_summary(self, text: str) -> str:
        pass


class MockLLMClient(LLMClient):
    def generate_summary(self, text: str) -> str:
        return f"This is a mock summary of the following activities:\n\n{text}"


def get_llm_client() -> LLMClient:
    # In a real application, this would read from config and return a real client.
    return MockLLMClient()
