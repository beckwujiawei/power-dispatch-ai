from app.config import config


SUPPORTED_PROVIDERS = {"mock", "deepseek", "guangming"}


def get_model_status() -> dict:
    """Return safe model configuration information without exposing secrets."""
    provider = config.model_provider
    return {
        "provider": provider,
        "model": config.model_name,
        "configured": provider in SUPPORTED_PROVIDERS and (
            provider == "mock" or bool(config.model_base_url)
        ),
        "mode": "demo" if provider == "mock" else "external",
    }
