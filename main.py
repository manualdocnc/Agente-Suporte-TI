
from google_docs import ler_documento
from gpt_service import gerar_resposta
from google_sheets import registrar_chamado


def identificar_categoria(pergunta):
    """
    Identifica a categoria do problema informado.
    """

    texto = pergunta.lower()

    categorias = {
        "Wi-Fi / Internet": ["wifi", "wi-fi", "internet", "rede"],
        "Impressoras": ["impressora", "imprimir", "impressão"],
        "Acesso a sistemas": ["senha", "login", "acesso", "sistema"],
        "Computadores": ["computador", "notebook", "pc", "monitor"]
    }

    for categoria, palavras in categorias.items():
        if any(palavra in texto for palavra in palavras):
            return categoria

    return "Suporte geral"


def processar_atendimento(nome, pergunta):
    """
    Coordena o atendimento entre Google Docs,
    GPT-OSS-20B e Google Sheets.
    """

    # 1. Consulta a documentação interna
    contexto = ler_documento()

    # 2. Verifica se a documentação foi encontrada
    if not contexto:
        registrado = registrar_chamado(
            nome,
            pergunta,
            "Falha na documentação",
            "Alta"
        )

        return {
            "status": "ABRIR_CHAMADO",
            "resposta": (
                "Não foi possível acessar a documentação interna. "
                "Seu problema será encaminhado ao suporte técnico."
            ),
            "registrado": registrado
        }

    # 3. Consulta a inteligência artificial
    resposta = gerar_resposta(
        pergunta,
        contexto
    )

    # 4. Identifica falha de comunicação com a IA
    if resposta.startswith(
        "Não foi possível consultar a inteligência artificial"
    ):
        registrado = registrar_chamado(
            nome,
            pergunta,
            "Falha na inteligência artificial",
            "Alta"
        )

        return {
            "status": "ABRIR_CHAMADO",
            "resposta": resposta,
            "registrado": registrado
        }

    # 5. Identifica o resultado da análise da IA
    resposta_upper = resposta.upper()

    if "STATUS: RESOLVIDO" in resposta_upper:
        return {
            "status": "RESOLVIDO",
            "resposta": resposta,
            "registrado": False
        }

    # 6. Registra problemas não resolvidos
    categoria = identificar_categoria(pergunta)

    registrado = registrar_chamado(
        nome,
        pergunta,
        categoria,
        "Média"
    )

    return {
        "status": "ABRIR_CHAMADO",
        "resposta": resposta,
        "registrado": registrado
    }
