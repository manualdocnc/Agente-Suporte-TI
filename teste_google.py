
from google_docs import ler_documento

print("Testando conexão com Google Docs...")

conteudo = ler_documento()

if conteudo:
    print("CONEXÃO REALIZADA COM SUCESSO!")
    print("Conteúdo encontrado:")
    print(conteudo[:500])
else:
    print("Não foi possível ler o documento.")
