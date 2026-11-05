import sqlite3
import os

# Procura o arquivo .db na raiz e na pasta app
caminhos_possiveis = [
    "sqlite.db",
    "database.db",
    "cardapio.db",
    "app/sqlite.db",
    "app/database.db",
]

arquivo_encontrado = None
for caminho in caminhos_possiveis:
    if os.path.exists(caminho):
        arquivo_encontrado = caminho
        break

if not arquivo_encontrado:
    print("❌ Nenhum arquivo .db encontrado.")
    exit()

print(f"✅ Banco encontrado: {arquivo_encontrado}\n")

conexao = sqlite3.connect(arquivo_encontrado)
cursor = conexao.cursor()

# 1. Listar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tabelas = [linha[0] for linha in cursor.fetchall()]
print("📋 Tabelas existentes:")
for t in tabelas:
    print(f"  - {t}")

# 2. Verificar versão do Alembic
print("\n🔢 Versão registrada no Alembic:")
try:
    cursor.execute("SELECT version_num FROM alembic_version;")
    versao = cursor.fetchone()
    print(f"  {versao[0] if versao else 'Tabela vazia'}")
except sqlite3.OperationalError:
    print("  Tabela 'alembic_version' não existe.")

# 3. Verificar colunas da tabela clientes
if "clientes" in tabelas:
    print("\n👥 Colunas da tabela 'clientes':")
    cursor.execute("PRAGMA table_info(clientes);")
    for coluna in cursor.fetchall():
        print(f"  - {coluna[1]} ({coluna[2]})")

# 4. Verificar clientes antes da atualização
if "clientes" in tabelas:
    print("\n📊 Clientes ANTES da atualização:")
    cursor.execute("SELECT id, nome, role FROM clientes;")
    for linha in cursor.fetchall():
        print(f"  ID: {linha[0]} | Nome: {linha[1]} | Role: {linha[2]}")
        
    # ==========================================
    # 5. PROMOVER O CLIENTE ID=1 PARA LOGISTA
    # ==========================================
    print("\n⚙️ Promovendo cliente ID=1 para LOGISTA...")
    cursor.execute("UPDATE clientes SET role = 'LOGISTA' WHERE id = 1")
    conexao.commit()
    
    # 6. Verificar clientes após a atualização
    print("\n📊 Clientes DEPOIS da atualização:")
    cursor.execute("SELECT id, nome, role FROM clientes;")
    for linha in cursor.fetchall():
        print(f"  ID: {linha[0]} | Nome: {linha[1]} | Role: {linha[2]}")

conexao.close()