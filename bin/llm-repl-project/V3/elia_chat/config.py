import os
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, SecretStr


class EliaChatModel(BaseModel):
    name: str
    """The name of the model e.g. `gpt-3.5-turbo`.
    This must match the name of the model specified by the provider.
    """
    id: str | None = None
    """If you have multiple versions of the same model (e.g. a personal
    OpenAI gpt-3.5 and a work OpenAI gpt-3.5 with different API keys/org keys),
    you need to be able to refer to them. For example, when setting the `default_model`
    key in the config, if you write `gpt-3.5`, there's no way to know whether you
    mean your work or your personal `gpt-3.5`. That's where `id` comes in."""
    display_name: str | None = None
    """The display name of the model in the UI."""
    provider: str | None = None
    """The provider of the model, e.g. openai, anthropic, etc"""
    api_key: SecretStr | None = None
    """If set, this will be used in place of the environment variable that
    would otherwise be used for this model (instead of OPENAI_API_KEY,
    ANTHROPIC_API_KEY, etc.)."""
    api_base: AnyHttpUrl | None = None
    """If set, this will be used as the base URL for making API calls.
    This can be useful if you're hosting models on a LocalAI server, for
    example."""
    organization: str | None = None
    """Some providers, such as OpenAI, allow you to specify an organization.
    In the case of """
    description: str | None = Field(default=None)
    """A description of the model which may appear inside the Elia UI."""
    product: str | None = Field(default=None)
    """For example `ChatGPT`, `Claude`, `Gemini`, etc."""
    temperature: float = Field(default=1.0)
    """The temperature to use. Low temperature means the same prompt is likely
    to produce similar results. High temperature means a flatter distribution
    when predicting the next token, and so the next token will be more random.
    Setting a very high temperature will likely produce junk output."""
    max_retries: int = Field(default=0)
    """The number of times to retry a request after it fails before giving up."""

    @property
    def lookup_key(self) -> str:
        return self.id or self.name


def get_builtin_ollama_models() -> list[EliaChatModel]:
    return [
        EliaChatModel(
            id="tinyllama",
            name="tinyllama:latest",
            display_name="TinyLlama",
            provider="Ollama",
            product="TinyLlama",
            description="Lightweight 1.1B parameter model for development and testing.",
            api_base="http://localhost:11434",
            temperature=0.7,
        ),
        EliaChatModel(
            id="phi3-mini",
            name="phi3:mini",
            display_name="Phi-3 Mini",
            provider="Ollama",
            product="Microsoft Phi-3",
            description="Compact 3.8B parameter model with strong performance.",
            api_base="http://localhost:11434",
            temperature=0.7,
        ),
        EliaChatModel(
            id="phi3.5-mini",
            name="phi3.5:3.8b-mini-instruct-q4_K_M",
            display_name="Phi-3.5 Mini",
            provider="Ollama",
            product="Microsoft Phi-3.5",
            description="Enhanced 3.8B parameter model with improved instruction following.",
            api_base="http://localhost:11434",
            temperature=0.7,
        ),
        EliaChatModel(
            id="mistral-7b",
            name="mistral:7b-instruct-q4_K_M",
            display_name="Mistral 7B Instruct",
            provider="Ollama",
            product="Mistral AI",
            description="High-quality 7B parameter instruction-tuned model.",
            api_base="http://localhost:11434",
            temperature=0.7,
        ),
        EliaChatModel(
            id="llama3.1-8b",
            name="llama3.1:8b-instruct-q4_K_M",
            display_name="Llama 3.1 8B",
            provider="Ollama",
            product="Meta Llama 3.1",
            description="Advanced 8B parameter model with strong reasoning capabilities.",
            api_base="http://localhost:11434",
            temperature=0.7,
        ),
        EliaChatModel(
            id="codellama-7b",
            name="codellama:7b-instruct-q4_K_M",
            display_name="CodeLlama 7B",
            provider="Ollama",
            product="Meta CodeLlama",
            description="Specialized 7B parameter model for code generation and assistance.",
            api_base="http://localhost:11434",
            temperature=0.7,
        ),
        EliaChatModel(
            id="qwen2.5-7b",
            name="qwen2.5:7b",
            display_name="Qwen 2.5 7B",
            provider="Ollama",
            product="Alibaba Qwen",
            description="Multilingual 7B parameter model with strong performance.",
            api_base="http://localhost:11434",
            temperature=0.7,
        ),
    ]


def get_builtin_anthropic_models() -> list[EliaChatModel]:
    return []


def get_builtin_google_models() -> list[EliaChatModel]:
    return []


def get_builtin_models() -> list[EliaChatModel]:
    return get_builtin_ollama_models()


class LaunchConfig(BaseModel):
    """The config of the application at launch.

    Values may be sourced via command line options, env vars, config files.
    """

    model_config = ConfigDict(frozen=True)

    default_model: str = Field(default="tinyllama")
    """The ID or name of the default model."""
    system_prompt: str = Field(
        default=os.getenv(
            "ELIA_SYSTEM_PROMPT", "You are a helpful assistant named Elia."
        )
    )
    message_code_theme: str = Field(default="monokai")
    """The default Pygments syntax highlighting theme to be used in chatboxes."""
    models: list[EliaChatModel] = Field(default_factory=list)
    builtin_models: list[EliaChatModel] = Field(
        default_factory=get_builtin_models, init=False
    )
    theme: str = Field(default="nebula")

    @property
    def all_models(self) -> list[EliaChatModel]:
        return self.models + self.builtin_models

    @property
    def default_model_object(self) -> EliaChatModel:
        from elia_chat.models import get_model

        return get_model(self.default_model, self)

    @classmethod
    def get_current(cls) -> "LaunchConfig":
        return cls()
