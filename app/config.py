from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for the demo and future internal deployment."""

    model_provider: str = os.getenv("MODEL_PROVIDER", "mock").strip().lower()
    model_name: str = os.getenv("MODEL_NAME", "mock-dispatch-model")
    model_base_url: str = os.getenv("MODEL_BASE_URL", "").strip()
    model_timeout: float = float(os.getenv("MODEL_TIMEOUT", "30"))


config = AppConfig()
