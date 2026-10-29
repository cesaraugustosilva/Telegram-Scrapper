"""Geração de convite voluntário para o grupo de destino."""

from telethon import TelegramClient, functions
from telethon.errors import ChatAdminRequiredError


async def generate_destination_invite_link(
    client: TelegramClient,
    destination_group: str | int,
) -> str:
    """Exporta um link de convite se a conta tiver autorização administrativa.

    O próprio Telegram valida a permissão da conta. A função apenas cria/obtém o
    link; ela não adiciona usuários nem envia mensagens.
    """
    try:
        result = await client(
            functions.messages.ExportChatInviteRequest(peer=destination_group)
        )
    except ChatAdminRequiredError as exc:
        raise PermissionError(
            "A conta precisa ser administradora e poder convidar usuários no destino."
        ) from exc

    link = getattr(result, "link", None)
    if not link:
        raise RuntimeError("O Telegram não retornou um link de convite.")
    return link
