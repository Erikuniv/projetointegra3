import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime
import pymysql

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
    janela.title("Gestão de Manutenção")
    janela.state('zoomed')  # Maximiza a janela

    # Título
    titulo = tk.Label(janela, text="GESTÃO DE MANUTENÇÃO", font=("Helvetica", 16))
    titulo.pack(pady=10, anchor='w')

    # Frame para os campos de entrada
    frame_campos = tk.Frame(janela)
    frame_campos.pack(pady=10)

    # Campos de entrada organizados em 2 linhas e 4 colunas
    campos = [
        ("Tipo:", ttk.Combobox(frame_campos, values=["Preventiva", "Corretiva"])),
        ("Equipamento:", tk.Entry(frame_campos)),
        ("Data Previsão:", tk.Entry(frame_campos)),
        ("Data Conclusão:", tk.Entry(frame_campos)),
        ("Responsável:", tk.Entry(frame_campos)),
        ("Status:", ttk.Combobox(frame_campos, values=["Em andamento", "Atrasada", "Concluída"])),
        ("Descrição:", tk.Entry(frame_campos)),
        ("Custo:", tk.Entry(frame_campos))
    ]

    for i, (label_text, widget) in enumerate(campos):
        tk.Label(frame_campos, text=label_text).grid(row=i//4, column=(i%4)*2, padx=5, pady=5, sticky='e')
        widget.grid(row=i//4, column=(i%4)*2+1, padx=5, pady=5, sticky='w')

    tipo_combobox, equipamento_entry, data_previsao_entry, data_conclusao_entry, responsavel_entry, status_combobox, descricao_entry, custo_entry = [widget for _, widget in campos]

    # Função para gerar número de ordem
    def gerar_numero_ordem():
        numero_aleatorio = str(random.randint(100000, 999999))
        return numero_aleatorio

    # Função para verificar se todos os campos estão preenchidos
    def campos_preenchidos():
        return all([
            tipo_combobox.get(),
            equipamento_entry.get(),
            data_previsao_entry.get(),
            data_conclusao_entry.get(),
            responsavel_entry.get(),
            status_combobox.get(),
            descricao_entry.get(),
            custo_entry.get()
        ])

    # Função para converter data
    def converter_data(data_str):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(data_str, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        messagebox.showerror("Erro", f"Formato de data inválido: {data_str}")
        return None

    # Função para limpar os campos de entrada
    def limpar_campos():
        tipo_combobox.set('')
        equipamento_entry.delete(0, tk.END)
        data_previsao_entry.delete(0, tk.END)
        data_conclusao_entry.delete(0, tk.END)
        responsavel_entry.delete(0, tk.END)
        status_combobox.set('')
        descricao_entry.delete(0, tk.END)
        custo_entry.delete(0, tk.END)

    # Função para inserir dados
    def inserir_dados():
        if not campos_preenchidos():
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos")
            return

        numero_ordem = gerar_numero_ordem()

        data_previsao = converter_data(data_previsao_entry.get())
        data_conclusao = converter_data(data_conclusao_entry.get())

        if not data_previsao or not data_conclusao:
            return

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
                    data_previsao,
                    data_conclusao,
                    responsavel_entry.get(),
                    status_combobox.get(),
                    equipamento_entry.get(),
                    custo_entry.get()
                ))
                conn.commit()
                messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
                limpar_campos()  # Limpa os campos de entrada
                exibir_dados()  # Atualiza a exibição dos dados
            except Error as ex:
                messagebox.showerror("Erro", f"Erro ao inserir dados: {ex}")
            finally:
                conn.close()

    # Função para abrir a janela de edição
    def abrir_janela_edicao(item_id, dados):
        janela_edicao = tk.Toplevel(janela)
        janela_edicao.title("Editar Dados")
        janela_edicao.geometry("600x400")

        frame_edicao = tk.Frame(janela_edicao)
        frame_edicao.pack(pady=10)

        campos_edicao = [
            ("Tipo:", ttk.Combobox(frame_edicao, values=["Preventiva", "Corretiva"])),
            ("Equipamento:", tk.Entry(frame_edicao)),
            ("Data Previsão:", tk.Entry(frame_edicao)),
            ("Data Conclusão:", tk.Entry(frame_edicao)),
            ("Responsável:", tk.Entry(frame_edicao)),
            ("Status:", ttk.Combobox(frame_edicao, values=["Em andamento", "Atrasada", "Concluída"])),
            ("Descrição:", tk.Entry(frame_edicao)),
            ("Custo:", tk.Entry(frame_edicao))
        ]

        for i, (label_text, widget) in enumerate(campos_edicao):
            tk.Label(frame_edicao, text=label_text).grid(row=i//4, column=(i%4)*2, padx=5, pady=5, sticky='e')
            widget.grid(row=i//4, column=(i%4)*2+1, padx=5, pady=5, sticky='w')

        tipo_combobox_edicao, equipamento_entry_edicao, data_previsao_entry_edicao, data_conclusao_entry_edicao, responsavel_entry_edicao, status_combobox_edicao, descricao_entry_edicao, custo_entry_edicao = [widget for _, widget in campos_edicao]

        # Preencher os campos com os dados da linha selecionada
        tipo_combobox_edicao.set(dados[2])
        equipamento_entry_edicao.insert(0, dados[8])
        data_previsao_entry_edicao.insert(0, dados[4])
        data_conclusao_entry_edicao.insert(0, dados[5])
        responsavel_entry_edicao.insert(0, dados[6])
        status_combobox_edicao.set(dados[7])
        descricao_entry_edicao.insert(0, dados[3])
        custo_entry_edicao.insert(0, dados[9])

        def salvar_edicao():
            if not all([
                tipo_combobox_edicao.get(),
                equipamento_entry_edicao.get(),
                data_previsao_entry_edicao.get(),
                data_conclusao_entry_edicao.get(),
                responsavel_entry_edicao.get(),
                status_combobox_edicao.get(),
                descricao_entry_edicao.get(),
                custo_entry_edicao.get()
            ]):
                messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos")
                return

            data_previsao = converter_data(data_previsao_entry_edicao.get())
            data_conclusao = converter_data(data_conclusao_entry_edicao.get())

            if not data_previsao or not data_conclusao:
                return

            conn = conectar_banco()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE om_manutencao
                        SET tipo=%s, descricao=%s, data_previsao=%s, data_conclusao=%s, responsavel=%s, status=%s, equipamento=%s, custo=%s
                        WHERE id=%s
                    """, (
                        tipo_combobox_edicao.get(),
                        descricao_entry_edicao.get(),
                        data_previsao,
                        data_conclusao,
                        responsavel_entry_edicao.get(),
                        status_combobox_edicao.get(),
                        equipamento_entry_edicao.get(),
                        custo_entry_edicao.get(),
                        item_id
                    ))
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                    exibir_dados()  # Atualiza a exibição dos dados
                    janela_edicao.destroy()
                except Error as ex:
                    messagebox.showerror("Erro", f"Erro ao atualizar dados: {ex}")
                finally:
                    conn.close()

        tk.Button(janela_edicao, text="Salvar", command=salvar_edicao).pack(pady=10)

    # Função para editar dados
    def editar_dados():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um item para editar")
            return

        item = tree.item(selected_item)
        item_id = tree.set(selected_item, "id")  # Recupera o id real do banco de dados
        dados = item['values']

        abrir_janela_edicao(item_id, dados)

    # Função para concluir ordem
    def concluir_ordem():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um item para concluir")
            return

        item = tree.item(selected_item)
        item_id = tree.set(selected_item, "id")  # Recupera o id real do banco de dados

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
                messagebox.showerror("Erro ao concluir ordem", f"Erro ao concluir ordem: {ex}")
            finally:
                conn.close()

    # Função para excluir ordem
    def excluir_ordem():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um item para excluir")
            return

        item = tree.item(selected_item)
        item_id = tree.set(selected_item, "id")  # Recupera o id real do banco de dados

        def confirmar_exclusao():
            conn = conectar_banco()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM om_manutencao WHERE id=%s", (item_id,))
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Ordem excluída com sucesso!")
                    exibir_dados()  # Atualiza a exibição dos dados
                except Error as ex:
                    messagebox.showerror("Erro ao excluir ordem", f"Erro ao excluir ordem: {ex}")
                finally:
                    conn.close()
                confirmacao.destroy()

        # Janela de confirmação
        confirmacao = tk.Toplevel(janela)
        confirmacao.title("Confirmar Exclusão")
        confirmacao.geometry("300x150")
        tk.Label(confirmacao, text="Tem certeza que deseja excluir esta ordem?").pack(pady=20)
        tk.Button(confirmacao, text="Sim", command=confirmar_exclusao).pack(side=tk.LEFT, padx=20)
        tk.Button(confirmacao, text="Não", command=confirmacao.destroy).pack(side=tk.RIGHT, padx=20)

    # Função para atualizar as informações exibidas
    def atualizar_informacoes():
        exibir_dados()

    # Frame para os botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    # Botões para inserir, editar, concluir, excluir e atualizar informações
    tk.Button(frame_botoes, text="Inserir Dados", command=inserir_dados).grid(row=0, column=0, padx=10)
    tk.Button(frame_botoes, text="Editar Dados", command=editar_dados).grid(row=0, column=1, padx=10)
    tk.Button(frame_botoes, text="Concluir Ordem", command=concluir_ordem).grid(row=0, column=2, padx=10)
    tk.Button(frame_botoes, text="Excluir Ordem", command=excluir_ordem).grid(row=0, column=3, padx=10)
    tk.Button(frame_botoes, text="Atualizar Informações", command=atualizar_informacoes).grid(row=0, column=4, padx=10)

    # Frame para exibir os dados
    frame_dados = tk.Frame(janela)
    frame_dados.pack(pady=10, expand=True, fill='both')

    # Treeview para exibir os dados
    colunas = ("id", "numero_ordem", "tipo", "descricao", "data_previsao", "data_conclusao", "responsavel", "status", "equipamento", "custo")
    tree = ttk.Treeview(frame_dados, columns=colunas, show="headings")
    tree.pack(expand=True, fill='both')

    # Ocultar a coluna 'id'
    tree.column("id", width=0, stretch=tk.NO)
    tree.heading("id", text="")

    for col in colunas[1:]:  # Exclui a coluna 'id' da exibição
        tree.heading(col, text=col.replace("_", " ").capitalize())
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
                    tree.insert("", "end", values=row)  # Inclui o 'id' como tag
                print("Dados exibidos com sucesso")
            except Error as ex:
                messagebox.showerror("Erro ao buscar dados", f"Erro ao buscar dados: {ex}")
            finally:
                conn.close()

    # Exibe os dados ao iniciar a aplicação
    exibir_dados()

    janela.mainloop()

# Executa a função para criar a janela
criar_janela()
