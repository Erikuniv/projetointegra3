import tkinter as tk
from tkinter import messagebox
import pyodbc

def conectar_banco():
    """Função para conectar ao banco de dados."""
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=ERIK_DALIECI\\SQLEXPRESS;'  # Ou o nome/endereço do seu servidor
            'DATABASE=ProjetoIntegrador3;'  # Substitua pelo nome do seu banco de dados
            'UID=ERIK_DALIECI\\erikd;'  # Usar string raw ou escapar a barra invertida
            'PWD=;'  # Substitua pela sua senha
        )
        return conn
    except pyodbc.Error as ex:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {ex}")
        return None

def criar_janela():
    """Cria a janela principal do aplicativo."""
    janela = tk.Tk()
    janela.title("Preencher Dados da Tabela")

    # Campos de entrada
    tk.Label(janela, text="Número da Ordem:").grid(row=0, column=0)
    numero_ordem_entry = tk.Entry(janela)
    numero_ordem_entry.grid(row=0, column=1)

    tk.Label(janela, text="Tipo de Falha:").grid(row=1, column=0)
    tipo_falha_entry = tk.Entry(janela)
    tipo_falha_entry.grid(row=1, column=1)

    tk.Label(janela, text="Cliente:").grid(row=2, column=0)
    cliente_entry = tk.Entry(janela)
    cliente_entry.grid(row=2, column=1)

    tk.Label(janela, text="Endereço:").grid(row=3, column=0)
    endereco_entry = tk.Entry(janela)
    endereco_entry.grid(row=3, column=1)

    tk.Label(janela, text="Cidade:").grid(row=4, column=0)
    cidade_entry = tk.Entry(janela)
    cidade_entry.grid(row=4, column=1)

    tk.Label(janela, text="Descrição do Trabalho:").grid(row=5, column=0)
    descricao_trabalho_entry = tk.Entry(janela)
    descricao_trabalho_entry.grid(row=5, column=1)

    # Função para inserir dados
    def inserir_dados():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO SUA_TABELA (numero_ordem, tipo_falha, cliente, endereco, cidade, descricao_trabalho)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    numero_ordem_entry.get(),
                    tipo_falha_entry.get(),
                    cliente_entry.get(),
                    endereco_entry.get(),
                    cidade_entry.get(),
                    descricao_trabalho_entry.get()
                ))
                conn.commit()
                messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
            except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                messagebox.showerror("Erro", f"Erro ao inserir dados: {sqlstate}")
            finally:
                conn.close()

    # Botão para inserir dados
    tk.Button(janela, text="Inserir Dados", command=inserir_dados).grid(row=6, column=0, columnspan=2)

    janela.mainloop()

# Executa a função para criar a janela
criar_janela()
import tkinter as tk
from tkinter import messagebox
import pyodbc

def conectar_banco():
    """Função para conectar ao banco de dados."""
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=ERIK_DALIECI\\SQLEXPRESS;'  # Ou o nome/endereço do seu servidor
            'DATABASE=ProjetoIntegrador3;'  # Substitua pelo nome do seu banco de dados
            'UID=ERIK_DALIECI\\erikd;'  # Usar string raw ou escapar a barra invertida
            'PWD=;'  # Substitua pela sua senha
        )
        return conn
    except pyodbc.Error as ex:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {ex}")
        return None

def criar_janela():
    """Cria a janela principal do aplicativo."""
    janela = tk.Tk()
    janela.title("Preencher Dados da Tabela")

    # Campos de entrada
    tk.Label(janela, text="Número da Ordem:").grid(row=0, column=0)
    numero_ordem_entry = tk.Entry(janela)
    numero_ordem_entry.grid(row=0, column=1)

    tk.Label(janela, text="Tipo de Falha:").grid(row=1, column=0)
    tipo_falha_entry = tk.Entry(janela)
    tipo_falha_entry.grid(row=1, column=1)

    tk.Label(janela, text="Cliente:").grid(row=2, column=0)
    cliente_entry = tk.Entry(janela)
    cliente_entry.grid(row=2, column=1)

    tk.Label(janela, text="Endereço:").grid(row=3, column=0)
    endereco_entry = tk.Entry(janela)
    endereco_entry.grid(row=3, column=1)

    tk.Label(janela, text="Cidade:").grid(row=4, column=0)
    cidade_entry = tk.Entry(janela)
    cidade_entry.grid(row=4, column=1)

    tk.Label(janela, text="Descrição do Trabalho:").grid(row=5, column=0)
    descricao_trabalho_entry = tk.Entry(janela)
    descricao_trabalho_entry.grid(row=5, column=1)

    # Função para inserir dados
    def inserir_dados():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO SUA_TABELA (numero_ordem, tipo_falha, cliente, endereco, cidade, descricao_trabalho)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    numero_ordem_entry.get(),
                    tipo_falha_entry.get(),
                    cliente_entry.get(),
                    endereco_entry.get(),
                    cidade_entry.get(),
                    descricao_trabalho_entry.get()
                ))
                conn.commit()
                messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
            except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                messagebox.showerror("Erro", f"Erro ao inserir dados: {sqlstate}")
            finally:
                conn.close()

    # Botão para inserir dados
    tk.Button(janela, text="Inserir Dados", command=inserir_dados).grid(row=6, column=0, columnspan=2)

    janela.mainloop()

# Executa a função para criar a janela
criar_janela()
