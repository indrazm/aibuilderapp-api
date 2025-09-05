from agents import OpenAIChatCompletionsModel, RunConfig
from openai import AsyncOpenAI, OpenAI

from app.core.settings import settings

openai_client = OpenAI(
    api_key=settings.llm_settings.OPENAI_API_KEY,
    base_url=settings.llm_settings.OPENAI_BASE_URL,
)

asyncopenai_client = AsyncOpenAI(
    api_key=settings.llm_settings.OPENAI_API_KEY,
    base_url=settings.llm_settings.OPENAI_BASE_URL,
)

model = OpenAIChatCompletionsModel(openai_client=asyncopenai_client, model="openrouter/google/gemini-2.5-pro")

runner_config = RunConfig(model=model, tracing_disabled=True, model_provider=asyncopenai_client)
