
from google_sheets import registrar_chamado

print("Testando conexão com Google Sheets...")

resultado = registrar_chamado(
    nome="Colaborador Teste",
    pergunta="Teste de registro automático de chamado.",
    categoria="Teste do sistema",
    prioridade="Baixa"
)

if resultado:
    print("CONEXÃO REALIZADA COM SUCESSO!")
    print("Chamado registrado na planilha.")
else:
    print("ERRO: Não foi possível registrar o chamado.")
