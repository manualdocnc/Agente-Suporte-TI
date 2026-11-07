
import streamlit as st

from main import processar_atendimento
from google_sheets import registrar_chamado
from config import APP_NAME, APP_VERSION

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ Agente Inteligente de Suporte de TI")
st.caption(f"Versão {APP_VERSION}")

st.write(
    "Olá! Informe seu nome e descreva seu problema. "
    "Nosso agente tentará encontrar uma solução na documentação interna."
)

st.divider()

# Atendimento com inteligência artificial
st.header("🤖 Atendimento com IA")

nome = st.text_input("Nome do colaborador", key="nome_ia")

pergunta = st.text_area(
    "Descreva sua dúvida ou problema",
    placeholder="Exemplo: Não consigo conectar à rede Wi-Fi...",
    height=130,
    key="pergunta_ia"
)

if st.button("Consultar agente", type="primary"):
    if not nome.strip() or not pergunta.strip():
        st.warning("Preencha seu nome e descreva o problema.")
    else:
        with st.spinner("Analisando sua solicitação..."):
            resultado = processar_atendimento(
                nome.strip(),
                pergunta.strip()
            )

        st.subheader("Resultado do atendimento")
        st.write(resultado["resposta"])

        if resultado["status"] == "RESOLVIDO":
            st.success("Problema solucionado pela inteligência artificial.")
        else:
            if resultado["registrado"]:
                st.warning(
                    "Seu chamado foi registrado na planilha de suporte técnico."
                )
            else:
                st.error(
                    "Não foi possível registrar o chamado automaticamente. "
                    "Entre em contato com o suporte técnico."
                )

st.divider()

# Abertura manual de chamados
st.header("🎫 Abrir chamado manualmente")

st.write(
    "Se preferir, preencha os dados abaixo para encaminhar "
    "diretamente uma solicitação ao suporte técnico."
)

with st.form("formulario_chamado"):
    nome_chamado = st.text_input("Nome do colaborador")

    setor = st.text_input(
        "Setor / Departamento",
        placeholder="Exemplo: Financeiro"
    )

    problema = st.text_area(
        "Problema ou defeito",
        placeholder="Descreva detalhadamente o que aconteceu..."
    )

    area = st.selectbox(
        "Área responsável pelo atendimento",
        [
            "Hardware",
            "Software",
            "Redes / Internet",
            "Sistemas / Acessos",
            "Impressoras",
            "Suporte geral"
        ]
    )

    prioridade = st.selectbox(
        "Prioridade",
        ["Baixa", "Média", "Alta", "Urgente"]
    )

    enviar_chamado = st.form_submit_button(
        "📨 Abrir chamado",
        type="primary"
    )

    if enviar_chamado:
        if (
            not nome_chamado.strip()
            or not setor.strip()
            or not problema.strip()
        ):
            st.warning(
                "Preencha nome, setor e descrição do problema."
            )
        else:
            with st.spinner("Registrando chamado..."):
                sucesso = registrar_chamado(
                    nome=nome_chamado.strip(),
                    pergunta=problema.strip(),
                    categoria=area,
                    prioridade=prioridade,
                    setor=setor.strip(),
                    area_responsavel=area
                )

            if sucesso:
                st.success(
                    "Chamado aberto com sucesso! "
                    "As informações foram registradas na planilha."
                )
            else:
                st.error(
                    "Não foi possível registrar o chamado. "
                    "Entre em contato com o suporte técnico."
                )

st.divider()
st.caption(
    "Sistema acadêmico de integração entre GPT-OSS e Google Workspace."
)
