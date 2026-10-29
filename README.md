# Telegram Transfer

Projeto Python local para consultar participantes que a API do Telegram torna
visíveis à conta autenticada e gerar um link de convite voluntário para um grupo
de destino administrado por você.

O projeto **não** adiciona membros automaticamente, não contorna restrições de
privacidade e não envia mensagens em massa.

## Requisitos

- Windows
- Python 3.14.7 (versão detectada na preparação deste projeto)
- Credenciais de aplicativo obtidas em <https://my.telegram.org/apps>

## Instalação no PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite `.env` e substitua `API_ID` e `API_HASH` pelas suas credenciais. Nunca
publique o `.env` nem os arquivos `.session`: a sessão permite acesso à conta.

## Uso

Na primeira execução, informe o telefone, o código recebido no Telegram e, se
habilitada, a senha de verificação em duas etapas.

Listar até 100 participantes que a API permite visualizar:

```powershell
python main.py members --group "@grupo_origem" --limit 100
```

Gerar/obter um link de convite para o grupo de destino:

```powershell
python main.py invite --group "@grupo_destino"
```

Também é possível definir `SOURCE_GROUP` e `DESTINATION_GROUP` no `.env` e omitir
`--group`. Identificadores podem ser usernames, IDs ou links que o Telethon consiga
resolver para a conta autenticada.

## Limites e segurança

- O Telegram decide quais participantes ficam visíveis; grupos podem ocultar a
  lista ou exigir privilégios administrativos.
- A função de convite depende da permissão administrativa de convidar usuários.
- Use o link apenas para adesão voluntária e respeite os Termos do Telegram, a
  privacidade dos usuários e a legislação aplicável.
- Evite limites elevados e chamadas repetitivas; a API pode aplicar `FloodWait`.
- Nenhuma informação é exportada automaticamente.
