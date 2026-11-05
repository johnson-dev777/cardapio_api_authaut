import sqlite3

conn = sqlite3.connect('cardapio.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT cl.nome, COUNT(ic.id) AS total
    FROM clientes cl
    LEFT JOIN itens_cardapio ic ON ic.criador_id = cl.id
    WHERE cl.role = 'LOGISTA'
    GROUP BY cl.id
""")

print("📊 Itens criados por logista:")
for nome, total in cursor.fetchall():
    print(f"   {nome}: {total} item(ns)")

conn.close()