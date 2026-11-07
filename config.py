
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configurações da Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "openai/gpt-oss-20b"

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Configurações do sistema
APP_NAME = "Agente Inteligente de Suporte de TI"

APP_VERSION = "1.0.0"

# Validação da chave
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY não encontrada no arquivo .env"
    )

# Configurações do Google Docs
GOOGLE_DOC_ID = os.getenv("GOOGLE_DOC_ID")

GOOGLE_CREDENTIALS_FILE = os.getenv(
    "GOOGLE_CREDENTIALS_FILE",
    "credentials/credentials.json"
)

# Configurações do Google Sheets
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")