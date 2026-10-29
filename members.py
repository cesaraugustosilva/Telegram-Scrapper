"""Consulta limitada aos participantes que a API disponibiliza."""

from dataclasses import dataclass

from telethon import TelegramClient
from telethon.errors import ChatAdminRequiredError, ChannelPrivateError


@dataclass(frozen=True, slots=True)
class VisibleMember:
    id: int
    display_name: str
    username: str | None
    is_bot: bool


async def get_accessible_participants(
    client: TelegramClient,
    group: str | int,
    *,
    limit: int | None = None,
) -> list[VisibleMember]:
    """Retorna somente usuários que o Telegram permite à conta consultar.

    A função não tenta contornar listas ocultas, permissões administrativas,
    limites de API ou privacidade. Dados sensíveis, como telefone e access_hash,
    não são incluídos no resultado.
    """
    try:
        users = await client.get_participants(group, limit=limit)
    except ChatAdminRequiredError as exc:
        raise PermissionError(
            "O Telegram exige permissão administrativa para consultar essa lista."
        ) from exc
    except ChannelPrivateError as exc:
        raise PermissionError(
            "O grupo é privado ou não está acessível à conta autenticada."
        ) from exc

    return [
        VisibleMember(
            id=user.id,
            display_name=" ".join(
                part for part in (user.first_name, user.last_name) if part
            )
            or "Sem nome",
            username=user.username,
            is_bot=bool(user.bot),
        )
        for user in users
    ]
