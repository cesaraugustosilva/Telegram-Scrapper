"""Criação do cliente Telethon e autenticação interativa."""

from getpass import getpass

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from config import Settings


def create_client(settings: Settings) -> TelegramClient:
    """Cria o cliente sem conectá-lo à rede."""
    return TelegramClient(
        settings.session_name,
        settings.api_id,
        settings.api_hash,
    )


async def authenticate(client: TelegramClient) -> None:
    """Autentica interativamente, incluindo senha de verificação em duas etapas."""
    await client.connect()
    if await client.is_user_authorized():
        return

    phone = input("Telefone com código do país (ex.: +5511999999999): ").strip()
    await client.send_code_request(phone)
    code = input("Código recebido no Telegram: ").strip()

    try:
        await client.sign_in(phone=phone, code=code)
    except SessionPasswordNeededError:
        password = getpass("Senha da verificação em duas etapas: ")
        await client.sign_in(password=password)
