
from googleapiclient.discovery import build
from google.oauth2 import service_account

from config import GOOGLE_DOC_ID, GOOGLE_CREDENTIALS_FILE


# Permissão de leitura dos documentos
SCOPES = [
    "https://www.googleapis.com/auth/documents.readonly"
]


def conectar_google_docs():
    """
    Realiza a autenticação e conexão com Google Docs.
    """

    credenciais = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_FILE,
        scopes=SCOPES
    )

    servico = build(
        "docs",
        "v1",
        credentials=credenciais
    )

    return servico


def extrair_conteudo(elementos):
    """
    Extrai textos de parágrafos e tabelas do documento.
    """

    textos = []

    for elemento in elementos:

        if "paragraph" in elemento:
            for parte in elemento["paragraph"].get("elements", []):
                texto = parte.get("textRun", {}).get("content", "")
                textos.append(texto)

        elif "table" in elemento:
            for linha in elemento["table"].get("tableRows", []):
                for celula in linha.get("tableCells", []):
                    textos.extend(
                        extrair_conteudo(
                            celula.get("content", [])
                        )
                    )

    return textos


def ler_documento():
    """
    Busca o documento no Google Docs e retorna seu conteúdo.
    """

    try:
        servico = conectar_google_docs()

        documento = servico.documents().get(
            documentId=GOOGLE_DOC_ID
        ).execute()

        conteudo = documento.get("body", {}).get("content", [])

        textos = extrair_conteudo(conteudo)

        resultado = "".join(textos).strip()

        if not resultado:
            return "O documento não possui conteúdo textual."

        return resultado

    except Exception as erro:
        print(f"Erro ao acessar Google Docs: {erro}")
        return ""
