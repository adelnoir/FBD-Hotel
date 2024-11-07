import sqlite3
import datetime

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
    numero_identificacao TEXT NOT NULL
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

def inserir_cliente(nome, email, telefone, numero_identificacao):
    """Função para inserir novos clientes"""
    cursor.execute('INSERT INTO clientes(nome, email, telefone, numero_identificacao) VALUES (?, ?, ?, ?)',
                   (nome, email, telefone, numero_identificacao))
    conn.commit()
    # print(f'Cliente {nome} inserido com sucesso!')

def inserir_quarto(tipo, preco_noite, status):
    """Função para inserir novos quartos"""
    cursor.execute('INSERT INTO quartos(tipo, preco_noite, status) VALUES (?, ?, ?)',
                   (tipo, preco_noite, status))
    conn.commit()
    # print(f'Quarto {tipo} inserido com sucesso!')

def inserir_reserva(data_check_in, data_check_out, status):
    """Função para inserir novas reservas"""
    # Seleciona o último cliente inserido
    cursor.execute('SELECT id FROM clientes ORDER BY id DESC')
    cliente_id = cursor.fetchone()[0]

    # Seleciona o último quarto inserido
    cursor.execute('SELECT id FROM quartos ORDER BY id DESC')
    quarto_id = cursor.fetchone()[0]

    # Converte data_check_in e data_check_out para string no formato ISO 8601
    data_check_in_str = data_check_in.strftime('%Y-%m-%d')
    data_check_out_str = data_check_out.strftime('%Y-%m-%d')

    # Insere a nova reserva com o cliente e quarto selecionados
    cursor.execute('INSERT INTO reservas(cliente_id, quarto_id, data_check_in, data_check_out, status) VALUES (?, ?, ?, ?, ?)',
                   (cliente_id, quarto_id, data_check_in_str,data_check_out_str, status))
    conn.commit()
    # print(f'Reserva de cliente ID: {cliente_id} no quarto {quarto_id} inserida com sucesso!')

def inserir_pagamento(valor, data_pagamento, metodo):
    """Função para inserir novos pagamentos"""
    # Seleciona a última reserva inserida usando ORDENAR por id DESCENDENTE
    cursor.execute('SELECT id FROM reservas ORDER BY id DESC')
    reserva_id = cursor.fetchone()[0]

    # cursor.execute('SELECT preco_noite FROM quartos ORDER BY id DESC')
    # preco_noite = cursor.fetchall()[0]
    #
    # cursor.execute('SELECT status FROM quartos ORDER BY id DESC')
    # status_pagamento = cursor.fetchall()[0]

    data_pagamento_str = data_pagamento.strftime('%Y-%m-%d')

    cursor.execute('INSERT INTO pagamentos(reserva_id, valor, data_pagamento, metodo) VALUES (?, ?, ?, ?)',
        (reserva_id, valor, data_pagamento_str, metodo))

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

def inserir_dados():
    print("\nInserir dados do cliente\n-------------------")

    nome = input("Insira o nome do cliente: ")
    email = input("Insira o email: ")
    telefone = input("Insira o telefone: ")
    numero_identificacao = input("Insira o NIF: ")

    print("\nInserir dados do quarto\n-------------------")

    tipos = ["Individual", "Duplo", "Suite"]
    print("Os tipos de quarto são", tipos)

    while True:
        tipo = int(input(
            "Qual é o tipo de quarto desejado pelo cliente?\n[0] - Individual\n[1] - Duplo\n[2] - Suite\n"))
        if tipo in [0, 1, 2]:
            tipo = tipos[tipo]
            break
        else:
            print("\nTipo de quarto inserido inválido! Por favor, insira um tipo de quarto válido.")

    preco_noite = input("Preço por noite: ")

    statuses = ["Disponivel", "Ocupado", "Em Manutenção"]
    print("\nOs status de quarto são: ", statuses)

    while True:
        status_quarto = int(
            input("Insira o status do quarto:\n[0] - Disponivel\n[1] - Ocupado\n[2] - Em Manutenção\n"))
        if status_quarto in [0, 1, 2]:
            status_quarto = statuses[status_quarto]
            break
        else:
            print("\nMetodo inserido inválido! Por favor, insira um metodo válido.\n")



    print("\nInserir dados da reserva\n-------------------")
    format = "%d/%m/%Y"

    while True:
        try:
            data_check_in = input("Insira a data do check-in (dd/mm/yyyy): ")
            data_check_in_as_dt = datetime.datetime.strptime(data_check_in, format)
            data_check_out = input("Insira a data do check-out (dd/mm/yyyy): ")
            data_check_out_as_dt = datetime.datetime.strptime(data_check_out, format)
            break
        except ValueError:
            print("Formato de data inválido! Por favor, insira no formato dd/mm/yyyy.")

    # statuses = ["Confirmada", "Pendente", "Cancelada"]
    #
    # while True:
    #     status = int(input("\nInsira o status da reserva\n[0] - Confirmada\n[1] - Pendente\n[2] - Cancelada\n"))
    #     if status in [0, 1, 2]:
    #         status = statuses[status]
    #         break
    #     else:
    #         print("\nMetodo inserido inválido! Por favor, insira um metodo válido.\n")



    print("\nInserir dados do pagamento\n-------------------")

    while True:
        try:
            valor = float(input("Insira o valor do pagamento: "))
            break
        except ValueError:
            print("Valor inserido inválido! Por favor, insira um valor válido.")

    while True:
        try:
            data_pagamento = input("Insira a data do pagamento (dd/mm/yyyy): ")
            data_pagamento_as_dt = datetime.datetime.strptime(data_pagamento, format)
            break
        except ValueError:
            print("Formato de data inválido! Por favor, insira no formato dd/mm/yyyy.")

    metodos = ["Numerário", "Cartão de Crédito", "Transferência Bancária"]
    print("\nOs métodos de pagamento são", metodos)

    while True:
        metodo = int(input("Qual metodo de pagamento deseja usar?\n[0] - Numerário\n[1] - Cartão de Crédito\n[2] - Transferência bancária\n"))
        if metodo in [0,1,2]:
            metodo = metodos[metodo]
            break
        else:
            print("\nMetodo inserido inválido! Por favor, insira um metodo válido.\n")

    noite = (data_check_out_as_dt - data_check_in_as_dt).days
    print(f"O cliente vai ficar {noite} noites no hotel.")

    if tipo == 0:
        preco_noite = 87
        preco = preco_noite * noite
    elif tipo == 1:
        preco_noite = 120
        preco = preco_noite * noite
    elif tipo == 2:
        preco_noite = 175
        preco = preco_noite * noite

    if preco < valor:
        status = "Pendente"
    else:
        status = "Confirmada"

    inserir_cliente(nome, email, telefone, numero_identificacao)
    inserir_quarto(tipo, preco_noite, status_quarto)
    inserir_reserva(data_check_in_as_dt, data_check_out_as_dt, status)
    inserir_pagamento(valor, data_pagamento_as_dt, metodo)
    conn.commit()

def listar_dados():
    print("\nLista de Clientes:\n--------------")
    cursor.execute('SELECT * FROM clientes')
    resultado = cursor.fetchall()
    for cliente in resultado:
        print(cliente)

    print("\nLista de Quartos:\n--------------")
    cursor.execute('SELECT * FROM quartos')
    resultado = cursor.fetchall()
    for quarto in resultado:
        print(quarto)

    print("\nLista de Reservas:\n--------------")
    cursor.execute('SELECT * FROM reservas')
    resultado = cursor.fetchall()
    for reserva in resultado:
        print(reserva)

    print("\nLista de Pagamentos:\n--------------")
    cursor.execute('SELECT * FROM pagamentos')
    resultado = cursor.fetchall()
    for pagamento in resultado:
        print(pagamento)

def apagar_dados():
    # print("\nApagar dados do cliente\n-------------------")
    # cliente_id = int(input("Insira o ID do cliente a ser apagado: "))
    # cursor.execute('DELETE FROM clientes WHERE id = (?)', (cliente_id,))
    # conn.commit()
    # print(f"Cliente com ID {cliente_id} apagado com sucesso!")

    cursor.execute('DROP TABLE clientes')
    cursor.execute('DROP TABLE quartos')
    cursor.execute('DROP TABLE reservas')
    cursor.execute('DROP TABLE pagamentos')
    conn.commit()

def main():
    while True:
        inp = int(input("O que quer fazer na base de dados? (1 - Inserir dados) (2 - Apagar dados) (0 - Sair e listar dados): "))

        if inp == 1:
            # Execução da função inserir dados
            inserir_dados()

        elif inp == 2:
            apagar_dados()
        elif inp == 0:
            listar_dados()
            break  # Encerra o laço para sair do programa
        else:
            print("Opção inválida. Tente novamente.")

# Chama o menu principal
main()

conn.close()

# Listar todas as reservas ativas (reservas confirmadas) e respetivos clientes e quartos
# cursor.execute('''
#     SELECT reservas.id, clientes.nome, quartos.tipo, reservas.data_check_in, reservas.data_check_out
#     FROM reservas
#     JOIN clientes ON reservas.cliente_id = clientes.id
#     JOIN quartos ON reservas.quarto_id = quartos.id
#     WHERE reservas.status = 'Confirmada'
# ''')
#
# print("\nListagem de todas as reservas ativas (reservas confirmadas) e respetivos clientes e quartos:\n--------------------------")
# resultado = cursor.fetchall()
# for reserva in resultado:
#     print(f'Reserva ID: {reserva[0]}, Cliente: {reserva[1]}, Quarto: {reserva[2]}, Check-in: {reserva[3]}, Check-out: {reserva[4]}')

# Listar todos os quartos disponíveis.
# print("\nListagem de todos os quartos disponíveis:\n--------------------------")
# cursor.execute('''
#     SELECT * FROM quartos
#     WHERE status = 'Disponível'
#     ''')
#
# resultado = cursor.fetchall()
# for quarto in resultado:
#     print(quarto)
#

# Consultar todas as reservas de um cliente específico

# def consultar_reserva(reserva_id):
#
#     cursor.execute('SELECT * FROM reservas WHERE id = (?)', (reserva_id,))
#     reserva_cliente = cursor.fetchall()
#     conn.commit()
#     print(f'\nAs reservas do cliente {reserva_id} são:', reserva_cliente)
#
# consultar_reserva(2)
#
# # Listar todos os pagamentos pendentes
# print("\nListagem de todos os pagamentos pendentes\n--------------------------")
# cursor.execute('''SELECT * FROM reservas
#                 WHERE status = 'Pendente'
#                 ''')
#
# pagamentos = cursor.fetchall()
# for pagamento in pagamentos:
#     print(pagamento)
