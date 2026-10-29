"""CLI inicial do Telegram Transfer."""

import argparse
import asyncio

from config import Settings, load_settings
from invites import generate_destination_invite_link
from members import get_accessible_participants
from telegram_client import authenticate, create_client


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Telegram Transfer",
        description="Consulta participantes acessíveis e gera convite voluntário.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("auth", help="Autenticar e validar a sessão")

    list_parser = subparsers.add_parser("members", help="Listar membros acessíveis")
    list_parser.add_argument("--group", help="@username, ID ou link do grupo")
    list_parser.add_argument("--limit", type=int, default=100)

    invite_parser = subparsers.add_parser("invite", help="Gerar link de convite")
    invite_parser.add_argument("--group", help="@username, ID ou link do destino")
    return parser


def require_group(value: str | None, setting_name: str) -> str | int:
    if value:
        value = value.strip()
        if value.lstrip("-").isdigit():
            return int(value)
        return value
    raise RuntimeError(
        f"Informe --group ou defina {setting_name} no arquivo .env."
    )


async def run(args: argparse.Namespace, settings: Settings) -> None:
    client = create_client(settings)
    try:
        await authenticate(client)

        if args.command == "auth":
            print("Autenticação validada com sucesso.")
        elif args.command == "members":
            group = require_group(args.group or settings.source_group, "SOURCE_GROUP")
            members = await get_accessible_participants(
                client, group, limit=args.limit
            )
            for member in members:
                username = f"@{member.username}" if member.username else "sem username"
                bot = " [bot]" if member.is_bot else ""
                print(f"{member.id}: {member.display_name} ({username}){bot}")
            print(f"Total retornado: {len(members)}")
        else:
            group = require_group(
                args.group or settings.destination_group, "DESTINATION_GROUP"
            )
            link = await generate_destination_invite_link(client, group)
            print(f"Link de convite: {link}")
    finally:
        await client.disconnect()


def main() -> None:
    args = build_parser().parse_args()
    settings = load_settings()
    asyncio.run(run(args, settings))


if __name__ == "__main__":
    main()
