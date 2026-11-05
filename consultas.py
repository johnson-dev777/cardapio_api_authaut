import sqlite3

def consultar(query, titulo):
    conn = sqlite3.connect('cardapio.db')
    cursor = conn.cursor()
    cursor.execute(query)
    print(f"\n📊 {titulo}")
    for linha in cursor.fetchall():
        print(f"   {linha}")
    conn.close()

# 1. Itens criados por logista
consultar("""
    SELECT cl.nome, COUNT(ic.id) AS total
    FROM clientes cl
    LEFT JOIN itens_cardapio ic ON ic.criador_id = cl.id
    WHERE cl.role = 'LOGISTA'
    GROUP BY cl.id
""", "Itens criados por logista")

# 2. Pedidos por cliente
consultar("""
    SELECT cl.nome, COUNT(p.id) AS total
    FROM clientes cl
    LEFT JOIN pedidos p ON p.cliente_id = cl.id
    GROUP BY cl.id
""", "Pedidos por cliente")

# 3. Itens mais pedidos
consultar("""
    SELECT ic.nome, SUM(ip.quantidade) AS total
    FROM itens_cardapio ic
    JOIN itens_pedido ip ON ip.item_cardapio_id = ic.id
    GROUP BY ic.id
    ORDER BY total DESC
""", "Itens mais pedidos")

# 4. Todos os pedidos com cliente
consultar("""
    SELECT p.id, cl.nome, p.status, p.valor_total
    FROM pedidos p
    JOIN clientes cl ON cl.id = p.cliente_id
""", "Pedidos com cliente")