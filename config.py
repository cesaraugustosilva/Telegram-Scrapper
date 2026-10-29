"""Carregamento e validação da configuração local."""

from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class Settings:
    api_id: int
    api_hash: str
    session_name: str
    source_group: str | None
    destination_group: str | None


def _optional(name: str) -> str | None:
    value = os.getenv(name, "").strip()
    return value or None


def load_settings() -> Settings:
    """Lê o .env e falha cedo quando as credenciais são inválidas."""
    load_dotenv()

    raw_api_id = os.getenv("API_ID", "").strip()
    api_hash = os.getenv("API_HASH", "").strip()

    if not raw_api_id or not api_hash:
        raise RuntimeError(
            "Defina API_ID e API_HASH no arquivo .env (use .env.example como base)."
        )

    try:
        api_id = int(raw_api_id)
    except ValueError as exc:
        raise RuntimeError("API_ID deve ser um número inteiro.") from exc

    return Settings(
        api_id=api_id,
        api_hash=api_hash,
        session_name=os.getenv("SESSION_NAME", "telegram_transfer").strip()
        or "telegram_transfer",
        source_group=_optional("SOURCE_GROUP"),
        destination_group=_optional("DESTINATION_GROUP"),
    )
