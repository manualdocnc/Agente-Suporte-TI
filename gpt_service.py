
from openai import OpenAI, OpenAIError

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_BASE_URL
)


# Inicializa a conexão com a Groq
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url=GROQ_BASE_URL
)


def gerar_resposta(pergunta, contexto_documentos=""):
    """
    Envia a pergunta do colaborador ao GPT-OSS-20B,
    utilizando a documentação interna como referência.
    """

    prompt_sistema = """
    Você é um agente inteligente de suporte técnico de TI
    de uma empresa.

    Sua função é ajudar colaboradores com dúvidas sobre:

    - Configuração de Wi-Fi
    - Impressoras
    - Acesso a sistemas
    - Procedimentos operacionais
    - Problemas básicos de informática

    REGRAS IMPORTANTES:

    1. Utilize prioritariamente a documentação fornecida.
    2. Não invente informações ou procedimentos.
    3. Forneça instruções claras e organizadas.
    4. Se a documentação não apresentar uma solução,
       informe que será necessário abrir um chamado.
    5. Se o problema exigir suporte avançado,
       recomende atendimento humano.
    6. Nunca solicite senhas ou dados confidenciais.

    FORMATO OBRIGATÓRIO DA RESPOSTA:

    STATUS: RESOLVIDO ou ABRIR_CHAMADO

    RESPOSTA:
    Explique a solução ou o motivo do encaminhamento.
    """

    prompt_usuario = f"""
    DOCUMENTAÇÃO INTERNA DA EMPRESA:

    {contexto_documentos}

    PERGUNTA DO COLABORADOR:

    {pergunta}

    Analise a pergunta e siga as regras estabelecidas.
    """

    try:
        resposta = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": prompt_sistema
                },
                {
                    "role": "user",
                    "content": prompt_usuario
                }
            ],
            reasoning_effort="medium",
            max_completion_tokens=1500
        )

        conteudo = resposta.choices[0].message.content

        if not conteudo:
            return "Não foi possível gerar uma resposta."

        return conteudo.strip()

    except OpenAIError as erro:
        print(f"Erro na comunicação com a Groq: {erro}")
        return (
            "Não foi possível consultar a inteligência artificial. "
            "Tente novamente ou procure o suporte técnico."
        )
