import time

from openai import OpenAI

from arch_nemesis.config import get_settings
from arch_nemesis.llm.models import LLMCallResult


class LLMClient:
    def complete(self, prompt: str, prompt_hash: str, agent_name: str) -> LLMCallResult:
        settings = get_settings()
        start = time.perf_counter()
        if settings.dry_run_mode:
            text = f"DRY_RUN {agent_name}: {prompt[:200]}"
            return LLMCallResult(
                text=text,
                provider="dry-run",
                model="deterministic-harness",
                prompt_hash=prompt_hash,
                latency_ms=int((time.perf_counter() - start) * 1000),
            )
        if settings.llm_provider != "openai":
            raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
        client = OpenAI(api_key=settings.openai_api_key, timeout=settings.llm_timeout_seconds)
        response = client.chat.completions.create(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.choices[0].message.content or ""
        return LLMCallResult(
            text=text,
            provider=settings.llm_provider,
            model=settings.llm_model,
            prompt_hash=prompt_hash,
            latency_ms=int((time.perf_counter() - start) * 1000),
        )
