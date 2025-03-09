import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
import random
import datetime

def conectar_banco():
    """Função para conectar ao banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(
            host='localhost',  # Endereço do servidor
            user='root',       # Usuário do banco de dados
            password='',       # Senha do banco de dados (deixe vazio se não houver senha)
            database='projetointegrador03'  # Nome do banco de dados
        )
        if conn.is_connected():
            print("Conexão bem-sucedida")
            return conn
    except Error as ex:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {ex}")
        return None

def criar_janela():
    """Cria a janela principal do aplicativo."""
    janela = tk.Tk()
    janela.title("Preencher Dados da Tabela")
    janela.geometry("800x600")  # Define o tamanho da janela

    # Frame para os campos de entrada
    frame_campos = tk.Frame(janela)
    frame_campos.pack(pady=10)

    # Campos de entrada
    tk.Label(frame_campos, text="Tipo:").grid(row=0, column=0, padx=5, pady=5)
    tipo_combobox = ttk.Combobox(frame_campos, values=["Preventiva", "Corretiva"])
    tipo_combobox.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_campos, text="Descrição:").grid(row=1, column=0, padx=5, pady=5)
    descricao_entry = tk.Entry(frame_campos)
    descricao_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_campos, text="Data Previsão:").grid(row=2, column=0, padx=5, pady=5)
    data_previsao_entry = tk.Entry(frame_campos)
    data_previsao_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_campos, text="Data Conclusão:").grid(row=3, column=0, padx=5, pady=5)
    data_conclusao_entry = tk.Entry(frame_campos)
    data_conclusao_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(frame_campos, text="Responsável:").grid(row=4, column=0, padx=5, pady=5)
    responsavel_entry = tk.Entry(frame_campos)
    responsavel_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(frame_campos, text="Status:").grid(row=5, column=0, padx=5, pady=5)
    status_combobox = ttk.Combobox(frame_campos, values=["Em andamento", "Atrasada", "Concluída"])
    status_combobox.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(frame_campos, text="Equipamento:").grid(row=6, column=0, padx=5, pady=5)
    equipamento_entry = tk.Entry(frame_campos)
    equipamento_entry.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(frame_campos, text="Custo:").grid(row=7, column=0, padx=5, pady=5)
    custo_entry = tk.Entry(frame_campos)
    custo_entry.grid(row=7, column=1, padx=5, pady=5)

    # Função para gerar número de ordem
    def gerar_numero_ordem():
        numero_aleatorio = str(random.randint(100000, 999999))
        return numero_aleatorio

    # Função para verificar se todos os campos estão preenchidos
    def campos_preenchidos():
        return all([
            tipo_combobox.get(),
            descricao_entry.get(),
            data_previsao_entry.get(),
            data_conclusao_entry.get(),
            responsavel_entry.get(),
            status_combobox.get(),
            equipamento_entry.get(),
            custo_entry.get()
        ])

    # Função para inserir dados
    def inserir_dados():
        if not campos_preenchidos():
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos")
            return

        numero_ordem = gerar_numero_ordem()

        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO om_manutencao (numero_ordem, tipo, descricao, data_previsao, data_conclusao, responsavel, status, equipamento, custo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    numero_ordem,
                    tipo_combobox.get(),
                    descricao_entry.get(),
                    data_previsao_entry.get(),
                    data_conclusao_entry.get(),
                    responsavel_entry.get(),
                    status_combobox.get(),
                    equipamento_entry.get(),
                    custo_entry.get()
                ))
                conn.commit()
                messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
                exibir_dados()  # Atualiza a exibição dos dados
            except Error as ex:
                messagebox.showerror("Erro", f"Erro ao inserir dados: {ex}")
            finally:
                conn.close()

    # Função para editar dados
    def editar_dados():
        if not campos_preenchidos():
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos")
            return

        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um item para editar")
            return

        item = tree.item(selected_item)
        item_id = item['values'][0]

        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE om_manutencao
                    SET tipo=%s, descricao=%s, data_previsao=%s, data_conclusao=%s, responsavel=%s, status=%s, equipamento=%s, custo=%s
                    WHERE id=%s
                """, (
                    tipo_combobox.get(),
                    descricao_entry.get(),
                    data_previsao_entry.get(),
                    data_conclusao_entry.get(),
                    responsavel_entry.get(),
                    status_combobox.get(),
                    equipamento_entry.get(),
                    custo_entry.get(),
                    item_id
                ))
                conn.commit()
                messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                exibir_dados()  # Atualiza a exibição dos dados
            except Error as ex:
                messagebox.showerror("Erro", f"Erro ao atualizar dados: {ex}")
            finally:
                conn.close()

    # Função para concluir ordem
    def concluir_ordem():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um item para concluir")
            return

        item = tree.item(selected_item)
        item_id = item['values'][0]

        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE om_manutencao
                    SET status='Concluída'
                    WHERE id=%s
                """, (item_id,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Ordem concluída com sucesso!")
                exibir_dados()  # Atualiza a exibição dos dados
            except Error as ex:
                messagebox.showerror("Erro", f"Erro ao concluir ordem: {ex}")
            finally:
                conn.close()

    # Função para limpar os campos de entrada
    def limpar_campos():
        tipo_combobox.set('')
        descricao_entry.delete(0, tk.END)
        data_previsao_entry.delete(0, tk.END)
        data_conclusao_entry.delete(0, tk.END)
        responsavel_entry.delete(0, tk.END)
        status_combobox.set('')
        equipamento_entry.delete(0, tk.END)
        custo_entry.delete(0, tk.END)

    # Função para atualizar as informações exibidas
    def atualizar_informacoes():
        exibir_dados()

    # Botões para inserir, editar, concluir, limpar campos e atualizar informações
    tk.Button(frame_campos, text="Inserir Dados", command=inserir_dados).grid(row=8, column=0, columnspan=2, pady=10)
    tk.Button(frame_campos, text="Editar Dados", command=editar_dados).grid(row=9, column=0, columnspan=2, pady=10)
    tk.Button(frame_campos, text="Concluir Ordem", command=concluir_ordem).grid(row=10, column=0, columnspan=2, pady=10)
    tk.Button(frame_campos, text="Limpar Campos", command=limpar_campos).grid(row=11, column=0, columnspan=2, pady=10)
    tk.Button(frame_campos, text="Atualizar Informações", command=atualizar_informacoes).grid(row=12, column=0, columnspan=2, pady=10)

    # Frame para exibir os dados
    frame_dados = tk.Frame(janela)
    frame_dados.pack(pady=10, expand=True, fill='both')

    # Treeview para exibir os dados
    colunas = ("id", "numero_ordem", "tipo", "descricao", "data_previsao", "data_conclusao", "responsavel", "status", "equipamento", "custo")
    tree = ttk.Treeview(frame_dados, columns=colunas, show="headings")
    tree.pack(expand=True, fill='both')

    for col in colunas:
        tree.heading(col, text=col.replace("_", " "))
        tree.column(col, width=100)

    # Função para exibir os dados
    def exibir_dados():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, numero_ordem, tipo, descricao, data_previsao, data_conclusao, responsavel, status, equipamento, custo FROM om_manutencao")
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    tree.insert("", "end", values=row)
                print("Dados exibidos com sucesso")
            except Error as ex:
                messagebox.showerror("Erro", f"Erro ao buscar dados: {ex}")
            finally:
                conn.close()

    # Exibe os dados ao iniciar a aplicação
    exibir_dados()

    janela.mainloop()

# Executa a função para criar a janela
criar_janela()
