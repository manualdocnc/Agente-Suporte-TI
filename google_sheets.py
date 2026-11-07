
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
from zoneinfo import ZoneInfo

from config import (
    GOOGLE_SHEET_ID,
    GOOGLE_CREDENTIALS_FILE
)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]


def conectar_google_sheets():
    credenciais = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_FILE,
        scopes=SCOPES
    )

    servico = build("sheets", "v4", credentials=credenciais)
    return servico


def registrar_chamado(
    nome,
    pergunta,
    categoria="Suporte geral",
    prioridade="Média",
    setor="Não informado",
    area_responsavel=None
):
    try:
        servico = conectar_google_sheets()

        data_hora = datetime.now(
            ZoneInfo("America/Sao_Paulo")
        ).strftime("%d/%m/%Y %H:%M:%S")

        dados = [[
            data_hora,
            nome,
            setor,
            pergunta,
            area_responsavel or categoria,
            prioridade,
            "Pendente"
        ]]

        corpo = {"values": dados}

        servico.spreadsheets().values().append(
            spreadsheetId=GOOGLE_SHEET_ID,
            range="Chamados!A:G",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=corpo
        ).execute()

        print("Chamado registrado com sucesso!")
        return True

    except Exception as erro:
        print(f"Erro ao registrar chamado: {erro}")
        return False
