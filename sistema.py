import mysql.connector
from datetime import datetime

def sql(query):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="av04"
    )
    cursor = mydb.cursor()
    cursor.execute(query)
    try:
        result = cursor.fetchall()
    except:
        result = 0
    mydb.commit()
    mydb.close()
    return result

def transpor(lista):
    return [[lista[i][j] for i in range(len(lista))] for j in range(len(lista[0]))]

def listaProdutos(resultado):
    print(" ID  | Nome                             | Preco          | Quantidade")
    for i, j, k, l in resultado:
        print(" {:3} | {:32} | R$ {:10} | {}".format(i, j, k, l))

def verCarrinho(produtos):
    print(" ID  | Nome                             | Quantidade")
    for p in produtos:
        dados = pegaProduto(p)
        print(" {:3} | {:32} | {}".format(dados[0], dados[1], produtos[p]))

def pegaProduto(id):
    consulta = "select * from produto where id = {}".format(id)
    resultado = sql(consulta)
    if len(resultado) == 1:
        return resultado[0]
    return []

def menuVenda():
    print("Digite a opcao desejada:")
    print(" 1 - Listar produtos")
    print(" 2 - Acrescentar produtos")
    print(" 3 - Olhar carrinho")
    print(" 4 - Remover produtos")
    print(" 5 - Fechar compra")
    return input()

def insereCompra(cliente, loja, produto, quantidade, preco, now):
    consulta = "insert into compra values(NULL, {}, {}, {}, {}, {}, '{}')".format(cliente, produto, loja, quantidade, preco, now)
    sql(consulta)
    consulta = "update estoque set quantidade = quantidade - {} where produto = {} and loja = {}".format(quantidade, produto, loja)
    sql(consulta)

def venda():
    loja = input("Digite o CNPJ da loja: ")
    cliente = input("Digite o CPF do cliente: ")
    consulta = "select s.id, s.nome, t.preco, t.quantidade from (select * from estoque where loja = {} and quantidade > 0) t inner join produto s on t.produto = s.id order by s.nome".format(loja)
    resultado = sql(consulta)
    resultadoT = transpor(resultado)
    produtos = {}
    ans = menuVenda()
    while ans != '5':
        if ans == '1':
            print()
            print(" --- Listagem de produtos disponiveis na loja")
            listaProdutos(resultado)
            input("Pressione ENTER para voltar para o menu")
        if ans == '2':
            print()
            print(" --- Acrescentar produto")
            p = input("Digite o codigo do produto: ")
            q = input("Digite a quantidade: ")
            if int(p) not in resultadoT[0]:
                print("Produto nao disponivel")
            elif p in produtos.keys():
                if resultadoT[-1][resultadoT[0].index(int(p))] < float(q) + produtos[p] or float(q) < 0:
                    print("Quantidade indisponivel")
                else:
                    produtos[p] += float(q)
            else:
                if resultadoT[-1][resultadoT[0].index(int(p))] < float(q):
                    print("Quantidade indisponivel")
                else:
                    produtos[p] = float(q)
        if ans == '3':
            print()
            print(" --- Carrinho")
            verCarrinho(produtos)
            input("Pressione ENTER para voltar para o menu")
        if ans == '4':
            print()
            print(" --- Remover produto do carrinho")
            p = input("Digite o codigo do produto: ")
            q = input("Digite a quantidade que deseja remover (em branco para remover tudo): ")
            if p not in produtos.keys():
                print("Produto nao consta no carrinho")
                input("Pressione ENTER para voltar para o menu")
            else:
                if q == '':
                    produtos.pop(p)
                else:
                    produtos[p] -= float(q)
        ans = menuVenda()
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for p in produtos:
        insereCompra(cliente, loja, p, produtos[p], resultadoT[2][(resultadoT[0]).index(int(p))], now)
    main()

def procuraProduto(p, x, y):
    consulta = "select s.nome, s.telefone1, s.endereco, sqrt(power(s.x - {}, 2) + power(s.y - {}, 2)) distancia, t.quantidade, t.preco from estoque t inner join loja s on t.loja = s.cnpj where t.quantidade > 0 and produto = {} order by sqrt(power(s.x - {}, 2) + power(s.y - {}, 2)), t.quantidade DESC".format(x, y, p, x, y)
    return sql(consulta)

def buscaProduto():
    nome = input("Digite o nome do produto desejado: ")
    consulta = "select * from produto where nome = '{}'".format(nome)
    resultado = sql(consulta)
    if len(resultado) == 0:
        print("Produto nao existe")
        return
    p = resultado[0][0] #id
    consulta = "select s.nome, s.telefone1, s.endereco, t.quantidade, t.preco from estoque t inner join loja s on t.loja = s.cnpj where t.quantidade > 0 and produto = {} order by t.quantidade DESC".format(p)
    resultado = sql(consulta)
    print(" Loja                           | Telefone    | Endereco                       | Quantidade | Preco")
    for i in resultado:
        print(" {:30} | {:11} | {:30} | {} | {}".format(*i))

def buscaProximidade(x, y):
    nome = input("Digite o nome do produto desejado: ")
    consulta = "select * from produto where nome = '{}'".format(nome)
    resultado = sql(consulta)
    if len(resultado) == 0:
        print("Produto nao existe")
        return
    p = resultado[0][0] #id
    resultado = procuraProduto(p, float(x), float(y))
    print(" Loja                           | Telefone    | Endereco                       | Distancia | Quantidade | Preco")
    for i in resultado:
        print(" {:30} | {:11} | {:30} | {:.2f} | {} km | {}".format(*i))

def verCliente():
    cpf = input("\nDigite o CPF do cliente :")
    consulta = "select * from {} where cpf = '{}'".format('cliente', cpf)

    resultado = sql(consulta)
    if len(resultado) == 0:
        print("Cliente nao encontrado")
    else:
        campos = ["CPF", "Nome", "Data_nasc", "Sexo", "Telefone", "Celular", "Email"]
        for i, j in zip(campos, resultado[0]):
            print("{}: {}".format(i, j))
    input("Pressione ENTER para continuar")

def menuCliente(x, y):
    print("O que vc deseja?")
    print(" 1 - Buscar produto")
    print(" 2 - Buscar por proximidade")
    print(" 3 - Ver dados")
    print(" 4 - Voltar")
    ans = input()
    if ans == '1':
        buscaProduto()
        menuCliente(x, y)
    if ans == '2':
        buscaProximidade(x, y)
        menuCliente(x, y)
    if ans == '3':
        verCliente()
        menuCliente(x, y)
    if ans == '4':
        return main()

def menuCadastro():
    print("Digite a opcao desejada:")
    print(" 1 - Cadastrar loja")
    print(" 2 - Cadastrar cliente")
    print(" 3 - Cadastrar produto")
    print(" 4 - Cadastrar estoque")
    print(" 5 - Voltar")
    return input()

def cadastro():
    ans = menuCadastro()
    while ans != '5':
        if ans == '1':
            nome = input("Digite o nome da loja: ")
            endereco = input("Digite o endereco da loja: ")
            telefone1 = input("Digite o telefone1 da loja: ")
            telefone2 = input("Digite o telefone2 da loja: ")
            telefone3 = input("Digite o telefone3 da loja: ")    
            x = input("Digite a coordenada x da loja: ")
            y = input("Digite a coordenada y da loja: ")
            email = input("Digite o email da loja: ")
            consulta = "INSERT INTO loja (cnpj, nome, endereco, telefone1, telefone2, telefone3, email, x, y) VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'); ".format(nome, endereco, telefone1, telefone2, telefone3, email, x, y)
            resultado = sql(consulta)

        if ans == '2':
            nome = input("Digite o nome do cliente: ")
            data_nasc = input("Digite a data de nascimento do cliente no formato AAAA-MM-DD: ")
            sexo = input("Digite o sexo do cliente: ")    
            telefone = input("Digite o telefone do cliente: ")
            celular = input("Digite o celular do cliente: ")                
            email = input("Digite o email do cliente: ")
            
            consulta = "INSERT INTO cliente (cpf, nome, data_nasc, sexo, telefone, celular, email) VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}'); ".format(nome, data_nasc, sexo, telefone, celular, email)
            resultado = sql(consulta)

        if ans == '3':
            nome = input("Digite o nome do produto: ")
            categoria = input("Digite a categoria do produto: ")
            descricao = input("Digite a descricao do produto: ")    
            
            consulta = "INSERT INTO produto (ID, nome, categoria, descricao) VALUES (NULL, '{}', '{}', '{}'); ".format(nome, categoria, descricao)
            resultado = sql(consulta)

        if ans == '4':
            cnpj = input("Digite o cnpj da loja: ")
            id_produto = input("Digite o id do produto: ")
            quantidade = input("Digite a quantidade do produto: ")
            preco = input("Digite o preco do produto: ")
            
            consulta = "INSERT INTO estoque (loja, produto, quantidade, preco) VALUES ('{}', '{}', '{}', '{}'); ".format(cnpj, id_produto, quantidade, preco)
            resultado = sql(consulta)

        ans = menuCadastro()
    return main()

def menuAtt():
    print("Digite a opcao desejada:")
    print(" 1 - Atualizar loja")
    print(" 2 - Atualizar cliente")
    print(" 3 - Atualizar produto")
    print(" 4 - Atualizar estoque")
    print(" 5 - Voltar")
    return input()

def att():
    ans = menuAtt()
    while ans != '5':
        if ans == '1':
            while True:
                cnpj = input("\nDigite o CNPJ da loja: ")
                consulta = "select * from {} where cnpj = '{}'".format('loja', cnpj)
                
                resultado = sql(consulta)
                if len(resultado) == 0:
                    print("Loja nao encontrada")
                    break
                    
                campos = ["CNPJ", "Nome", "Endereco", "Telefone1", "Telefone2", "Telefone3", "Email", "x", "y"]
                for i, j in zip(campos, resultado[0]):
                    print("{}: {}".format(i, j))
                input("Pressione ENTER para continuar")

                while True:
                    print("\nEscolha o campo que deseja alterar:")
                    for i, j in enumerate(campos[1:]):
                        print(" {} - {}".format(i + 1, j))
                    ans1 = input()
                    ans2 = input("\nColoque o valor desejado")

                    consulta = "UPDATE loja SET {} = '{}' WHERE cnpj = {}".format(campos[int(ans1)], ans2, cnpj)
                    sql(consulta)
                    
                    print("\nDeseja alterar outro campo?")
                    print(" 1 - Sim")
                    print(" 2 - Nao")
                    ans = input()

                    if int(ans) == 2:
                        break

                print("\nDeseja atualizar outra loja?")
                print(" 1 - Sim")
                print(" 2 - Nao")
                ans = input()

                if int(ans) == 2:
                    break
        elif ans == '2':
            while True:
                cpf = input("\nDigite o CPF do cliente :")
                consulta = "select * from {} where cpf = '{}'".format('cliente', cpf)
                
                resultado = sql(consulta)
                if len(resultado) == 0:
                    print("Cliente nao encontrado")
                    break
                campos = ["CPF", "Nome", "Data_nasc", "Sexo", "Telefone", "Celular", "Email"]
                for i, j in zip(campos, resultado[0]):
                    print("{}: {}".format(i, j))
                input("Pressione ENTER para continuar")

                while True:
                    print("\nEscolha o campo que deseja alterar:")
                    for i, j in enumerate(campos[1:]):
                        print(" {} - {}".format(i + 1, j))
                    ans1 = input()
                    ans2 = input("\nColoque o valor desejado")

                    consulta = "UPDATE cliente SET {} = '{}' WHERE cpf = {}".format(campos[int(ans1)], ans2, cpf)
                    sql(consulta)
                    
                    print("\nDeseja alterar outro campo?")
                    print(" 1 - Sim")
                    print(" 2 - Nao")
                    ans = input()

                    if int(ans) == 2:
                        break

                print("\nDeseja atualizar outro cliente?")
                print(" 1 - Sim")
                print(" 2 - Nao")
                ans = input()

                if int(ans) == 2:
                    break
        elif ans == '3':
            while True:
                id = input("\nDigite o ID do produto:")
                consulta = "select * from {} where ID = '{}'".format('produto', id)
                
                resultado = sql(consulta)
                if len(resultado) == 0:
                    print("Produto nao encontrado")
                    break
                campos = ["ID", "Nome", "Categoria", "Descricao"]
                
                for i, j in zip(campos, resultado[0]):
                    print("{}: {}".format(i, j))
                input("Pressione ENTER para continuar")

                while True:
                    print("\nEscolha o campo que deseja alterar:")
                    for i, j in enumerate(campos[1:]):
                        print(" {} - {}".format(i + 1, j))
                    ans1 = input()
                    ans2 = input("\nColoque o valor desejado")

                    consulta = "UPDATE produto SET {} = '{}' WHERE id = {}".format(campos[int(ans1)], ans2, id)
                    sql(consulta)
                    
                    print("\nDeseja alterar outro campo?")
                    print(" 1 - Sim")
                    print(" 2 - Nao")
                    ans = input()

                    if int(ans) == 2:
                        break

                print("\nDeseja atualizar outro produto?")
                print(" 1 - Sim")
                print(" 2 - Nao")
                ans = input()

                if int(ans) == 2:
                    break
        elif ans == '4':
            while True:
                cnpj = input("\nDigite o CNPJ da loja: ")
                id = input("\nDigite o ID do produto: ")
                consulta = "select * from {} where loja = '{}' and produto = '{}'".format('estoque', cnpj, id)
                
                resultado = sql(consulta)
                if len(resultado) == 0:
                    print("Produto nao encontrado")
                    break
                campos = ["Loja", "Produto", "Quantidade", "Preco"]
                
                for i, j in zip(campos, resultado[0]):
                    print("{}: {}".format(i, j))
                input("Pressione ENTER para continuar")

                while True:
                    print("\nEscolha o campo que deseja alterar:")
                    for i, j in enumerate(campos[2:]):
                        print(" {} - {}".format(i + 1, j))
                    ans1 = input()
                    ans2 = input("\nColoque o valor desejado")

                    consulta = "UPDATE estoque SET {} = '{}' WHERE loja = '{}' and produto = '{}'".format(campos[int(ans1)+1], ans2, cnpj, id)
                    sql(consulta)
                    
                    print("\nDeseja alterar outro campo?")
                    print(" 1 - Sim")
                    print(" 2 - Nao")
                    ans = input()

                    if int(ans) == 2:
                        break

                print("\nDeseja atualizar outro estoque?")
                print(" 1 - Sim")
                print(" 2 - Nao")
                ans = input()

                if int(ans) == 2:
                    break
        elif int(ans) == 5:
            break
        ans = menuAtt()
    main()

def menuRelatorio():
    print("\nDigite a opcao desejada:")
    print(" 1 - Quantidade de lojas por categoria")
    print(" 2 - Quantidade de produtos em uma dada loja")
    print(" 3 - Top 10 dos produtos mais vendidos")
    print(" 4 - Top 10 das lojas que vendem mais (por quantidade de produtos ou por valor total vendido")
    print(" 5 - Produto mais vendido por dia da semana")
    print(" 6 - Voltar ")
    return input()

def relatorio():
    ans = menuRelatorio()
    while ans != '6':
        if ans == '1':
            consulta = "select categoria, count(*) as quantidade from loja group by categoria order by quantidade desc"
            resultado = sql(consulta)

            print(" Categoria       | Quantidade   ")
            for i in resultado:
                print(" {:15} | {}".format(*i))

            input("\nPressione ENTER para voltar para o menu")

        if ans == '2':
            cnpj = input("\nDigite o CNPJ da loja: ")
            
            consulta = "select s.nome, quantidade from estoque t inner join produto s on t.produto = s.id where t.loja = '{}' group by s.nome order by s.quantidade".format(cnpj)
            resultado = sql(consulta)

            print(" Nome                 | Quantidade   ")
            for i in resultado:
                print(" {:20} | {}".format(*i))

            input("\nPressione ENTER para voltar para o menu")

        if ans == '3':            
            consulta = "select s.produto, t.nome, s.quantidade from (select produto, sum(quantidade) as quantidade from compra group by produto order by quantidade desc limit 10) s inner join produto t on s.produto = t.id"
            resultado = sql(consulta)

            print(" ID  | Nome                           | Quantidade   ")
            for i in resultado:
                print(" {:3} | {:30} | {}".format(*i))

            input("\nPressione ENTER para voltar para o menu")

        if ans == '4':
            print("\nDigite a opcao desejada:")
            print(" 1 - Por quantidade de produtos")
            print(" 2 - Por somatório de valores de venda ")
            ans = input()

            if ans == '1':
                consulta = "select t.cnpj, t.nome, s.quantidade from (select loja, sum(quantidade) as quantidade from compra group by loja order by quantidade desc limit 10) s inner join loja t on s.loja = t.cnpj"
                resultado = sql(consulta)

                print(" CNPJ | Nome                           | Quantidade")
                for i in resultado:
                    print(" {:4} | {:30} | {}".format(*i))

            if ans == '2':
                consulta = "select t.cnpj, t.nome, s.quantidade from (select loja, sum(quantidade * preco) as quantidade from compra group by loja order by quantidade desc limit 10) s inner join loja t on s.loja = t.cnpj"
                resultado = sql(consulta)

                print(" CNPJ | Nome                           | Faturamento")
                for i in resultado:
                    print(" {:4} | {:30} | {}".format(*i))
            input("\nPressione ENTER para voltar para o menu")

        if ans == '5':
            consulta = "select t.dia_semana, t.produto, s.nome, t.quantidade from (select t.dia_semana, max(s.produto) produto, t.quantidade"
            consulta += " from (select t.dia_semana, max(t.quantidade) quantidade from (select dayofweek(hora) dia_semana,"
            consulta += " produto, sum(quantidade) quantidade from compra group by dayofweek(hora), produto) t"
            consulta += " group by t.dia_semana) t inner join (select dayofweek(hora) dia_semana, produto, sum(quantidade) quantidade"
            consulta += " from compra group by dayofweek(hora), produto) s on t.dia_semana = s.dia_semana and t.quantidade = s.quantidade"
            consulta += " group by t.dia_semana, t.quantidade) t inner join produto s on t.produto = s.id order by t.dia_semana"
            resultado = sql(consulta)
            
            dias = ["Domingo", "Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado"]

            print(" Dia Semana | ID  | Nome                           | Total   ")
            for i in resultado:
                print(" {:10} | {:3} | {:30} | {} ".format(dias[int(i[0]) - 1], i[1], i[2], i[3]))
            input("\nPressione ENTER para voltar para o menu")
        ans = menuRelatorio()
    main()

def menuVer():
    print("\nO que vc deseja?")
    print(" 1 - Lista de lojas")
    print(" 2 - Lista de clientes")
    print(" 3 - Lista de produtos")
    print(" 4 - Detalhes de uma loja")
    print(" 5 - Detalhes de um cliente")
    print(" 6 - Detalhes de um produto")
    print(" 7 - Voltar")
    ans = input()
    acoes = [
        "listagem('loja')",
        "listagem('cliente')",
        "listagem('produto')",
        "detalhe('loja')",
        "detalhe('cliente')",
        "detalhe('produto')",
        "main()"
    ]
    eval(acoes[int(ans)-1])

def listagem(tipo):
    campos = {
        'cliente': ["CPF", "Nome"],
        'loja': ["CNPJ", "Nome", "x", "y"],
        'produto': ["ID", "Nome", "Categoria"]
    }
    tamanhos = {
        'cliente': [4, 30],
        'loja': [4, 30, 4, 4],
        'produto': [4, 30, 20]
    }
    consulta = "select "
    for i in campos[tipo]:
        consulta += "{}, ".format(i)
    consulta = consulta[:-2]
    consulta += " from {}".format(tipo)
    resultado = sql(consulta)
    linhas = ""
    for i in tamanhos[tipo]:
        linhas += " {:" + str(i)+ "} |"
    linhas = linhas[:-1]
    print(linhas.format(*(campos[tipo])))
    for i in resultado:
        print(linhas.format(*i))
    input("Pressione ENTER para continuar")
    menuVer()

def detalhe(tipo):
    chaves = {'cliente': 'CPF', 'loja': 'CNPJ', 'produto': 'ID'}
    campos = {
        'cliente': ["CPF", "Nome", "Data_nasc", "Sexo", "Telefone", "Celular", "Email"],
        'loja': ["CNPJ", "Nome", "Endereco", "Telefone1", "Telefone2", "Telefone3", "Email", "x", "y"],
        'produto': ["ID", "Nome", "Categoria", "Descricao"]
    }
    k = input("\nDigite o {} do {}:".format(chaves[tipo], tipo))
    consulta = "select * from {} where {} = '{}'".format(tipo, chaves[tipo], k)

    resultado = sql(consulta)
    if len(resultado) == 0:
        print("{} nao encontrado".format(tipo.capitalize()))
    else:
        for i, j in zip(campos[tipo], resultado[0]):
            print("{}: {}".format(i, j))
    input("Pressione ENTER para continuar")
    menuVer()

def main():
    print("O que vc deseja?")
    print(" 1 - Cadastro")
    print(" 2 - Alterar dados")
    print(" 3 - Ver dados")
    print(" 4 - Relatorio")
    print(" 5 - Area do cliente")
    print(" 6 - Realizar venda")
    print(" 7 - Sair")
    ans = input()
    if ans == '1':
        cadastro()
    if ans == '2':
        att()
    if ans == '3':
        menuVer()
    if ans == '4':
        relatorio()
    if ans == '5':
        x = input("Digite sua cordenada x: ")
        y = input("Digite sua cordenada y: ")
        print()
        menuCliente(x, y)
    if ans == '6':
        venda()
    if ans == '7':
        return

main()