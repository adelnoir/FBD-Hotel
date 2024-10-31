import sqlite3

# Iniciar conexão com a base de dados 'hotel.db'
conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

# Criação das tabelas: Cliente, Quartos, Reservas e Pagamentos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL,
    documento_identificacao TEXT NOT NULL
    )
    ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS quartos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    preco_noite TEXT NOT NULL,
    status TEXT NOT NULL
        )
    ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    quarto_id INTEGER NOT NULL,
    data_check_in DATE NOT NULL,
    data_check_out DATE NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (quarto_id) REFERENCES quartos(id)
        )
    ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pagamentos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reserva_id INTEGER NOT NULL,
    valor REAL NOT NULL,
    data_pagamento DATE NOT NULL,
    metodo TEXT NOT NULL,
    FOREIGN KEY (reserva_id) REFERENCES reservas(id)
        )
    ''')

conn.commit()

# Função para inserir novos clientes
def inserir_cliente(nome, email, telefone, documento_identificacao):
    cursor.execute('INSERT INTO clientes(nome, email, telefone, documento_identificacao) VALUES (?, ?, ?, ?)',
                   (nome, email, telefone, documento_identificacao))
    conn.commit()
    # print(f'Cliente {nome} inserido com sucesso!')

# Função para inserir novos quartos
def inserir_quarto(tipo, preco_noite, status):
    cursor.execute('INSERT INTO quartos(tipo, preco_noite, status) VALUES (?, ?, ?)', (tipo, preco_noite, status))
    conn.commit()
    # print(f'Quarto {tipo} inserido com sucesso!')

# Função para inserir novas reservas
def inserir_reserva(data_check_in, data_check_out, status):
    # Seleciona o último cliente inserido
    cursor.execute('SELECT id FROM clientes ORDER BY id DESC')
    cliente_id = cursor.fetchone()[0]

    # Seleciona o último quarto inserido
    cursor.execute('SELECT id FROM quartos ORDER BY id DESC')
    quarto_id = cursor.fetchone()[0]

    # Insere a nova reserva com o cliente e quarto selecionados
    cursor.execute('INSERT INTO reservas(cliente_id, quarto_id, data_check_in, data_check_out, status) VALUES (?, ?, ?, ?, ?)',
                   (cliente_id, quarto_id, data_check_in, data_check_out, status))
    conn.commit()
    # print(f'Reserva de cliente ID: {cliente_id} no quarto {quarto_id} inserida com sucesso!')

# Função para inserir novas reservas
def inserir_pagamento(valor, data_pagamento, metodo):
    # Seleciona a última reserva inserida
    cursor.execute('SELECT id FROM reservas ORDER BY id DESC')
    reserva_id = cursor.fetchone()[0]

    cursor.execute('SELECT preco_noite FROM quartos ORDER BY id DESC')
    preco_noite = cursor.fetchall()[0]

    cursor.execute('SELECT status FROM quartos ORDER BY id DESC')
    status_pagamento = cursor.fetchall()[0]


    cursor.execute('INSERT INTO pagamentos(reserva_id, valor, data_pagamento, metodo) VALUES (?, ?, ?, ?)',
        (reserva_id, valor, data_pagamento, metodo))

    # Supostamente era para fazer a condição se o valor do pagamento fosse menor que o preco_noite
    # então o 'status' da reserva ficaria pendente, mas percebi que se fizer isso vou ter de ter em conta
    # os dias da estadia e fazer outra variável para saber o valor total a pagar e nao tenho paciência.

    # if valor < preco_noite:
    #     cursor.execute('''
    #                     UPDATE reservas
    #                     SET status = 'Pendente'
    #                     ''')
    # else:
    #     cursor.execute('''
    #                     UPDATE reservas
    #                     SET status = 'Confirmada'
    #                     ''')

    conn.commit()
    # print(f'Reserva de cliente ID: {cliente_id} no quarto {quarto_id} inserida com sucesso!')

# Exemplo de uso das funções
# Cliente 1
inserir_cliente('Leonardo', 'leonardopeixoto2005@gmail.com', '931984057', '268793213')
inserir_quarto('Individual', '30', 'Disponível')
inserir_reserva('2024-11-01', '2024-11-05', 'Confirmada')
inserir_pagamento('120','2024-10-31','Cartão de crédito')

# Cliente 2
inserir_cliente('Miguel', 'miguelitofixolas20@gmail.com', '943586723', '262351233')
inserir_quarto('Duplo', '55', 'Em Manutenção')
inserir_reserva('2024-12-04', '2024-12-12', 'Pendente')
inserir_pagamento('385','2024-11-25','Transferência Bancária')

# Cliente 3
inserir_cliente('Joana', 'joanalourencorego@gmail.com', '969711796', '213132255')
inserir_quarto('Suite', '40', 'Disponível')
inserir_reserva('2024-11-21', '2024-11-25', 'Confirmada')
inserir_pagamento('120','2024-11-12','Cartão de crédito')

# Listar todas as reservas ativas (reservas confirmadas) e respetivos clientes e quartos
cursor.execute('''
    SELECT reservas.id, clientes.nome, quartos.tipo, reservas.data_check_in, reservas.data_check_out
    FROM reservas
    JOIN clientes ON reservas.cliente_id = clientes.id
    JOIN quartos ON reservas.quarto_id = quartos.id
    WHERE reservas.status = 'Confirmada'
''')

print("Listagem de todas as reservas ativas (reservas confirmadas) e respetivos clientes e quartos:\n--------------------------")
resultado = cursor.fetchall()
for reserva in resultado:
    print(f'Reserva ID: {reserva[0]}, Cliente: {reserva[1]}, Quarto: {reserva[2]}, Check-in: {reserva[3]}, Check-out: {reserva[4]}')

# Listar todos os quartos disponíveis.
print("\nListagem de todos os quartos disponíveis:\n--------------------------")
cursor.execute('''
    SELECT * FROM quartos
    WHERE status = 'Disponível'
    ''')

resultado = cursor.fetchall()
for quarto in resultado:
    print(quarto)

# Consultar todas as reservas de um cliente específico

def consultar_reserva(reserva_id):

    cursor.execute('SELECT * FROM reservas WHERE id = (?)', (reserva_id,))
    reserva_cliente = cursor.fetchall()
    conn.commit()
    print(f'\nAs reservas do cliente {reserva_id} são:', reserva_cliente)

consultar_reserva(2)

# Listar todos os pagamentos pendentes
print("\nListagem de todos os pagamentos pendentes\n--------------------------")
cursor.execute('''SELECT * FROM reservas
                WHERE status = 'Pendente'
                ''')

pagamentos = cursor.fetchall()
for pagamento in pagamentos:
    print(pagamento)

conn.close()
