# ai_llm.py
from langchain_core.language_models import BaseLLM
from langchain_core.outputs import LLMResult
from pydantic import Field
import requests

class LMStudioLLM(BaseLLM):
    api_url: str = Field(default="http://localhost:1234/v1/completions")

    @property
    def _llm_type(self) -> str:
        return "lm_studio"

    def _call(self, prompt: str, stop=None, **kwargs) -> str:
        headers = {"Content-Type": "application/json"}
        data = {
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop": ["### Kamu:"],
            **kwargs,
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['text'].strip()
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

    def _generate(self, prompts: list[str], stop=None, **kwargs) -> LLMResult:
        responses = [self._call(prompt, stop=stop, **kwargs) for prompt in prompts]
        return LLMResult(generations=[[{"text": response}] for response in responses])
