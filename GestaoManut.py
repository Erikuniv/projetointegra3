import pyodbc


# Informações de conexão
server = 'ERIK_DALIECI\SQLEXPRESS'  # Ou o nome/endereço do seu servidor
database = 'ProjetoIntegrador3'  # Substitua pelo nome do seu banco de dados
username = r'ERIK_DALIECI\erikd'  # Usar string raw ou escapar a barra invertida
password = ' '  # Substitua pela sua senha
driver = '{ODBC Driver 17 for SQL Server}'  # Verifique a versão instalada

# String de conexão (Autenticação do SQL Server - se você estiver usando um usuário SQL Server)
# connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# String de conexão (Autenticação do Windows - se você estiver usando sua conta do Windows)
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'


try:
    # Estabelece a conexão
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()

    # Executa uma consulta (exemplo)
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    print(f"Versão do SQL Server: {row[0]}")

    # Fecha a conexão
    cursor.close()
    cnxn.close()
    print("Conexão bem-sucedida!")

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Erro ao conectar: {ex}")
    print(f"SQLSTATE: {sqlstate}")
