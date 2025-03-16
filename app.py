import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from PIL import Image, ImageTk
import os  # Adicionado para abrir o PDF automaticamente

# Dados da tabela
data = [
    ["Número Ordem", "Tipo", "Descrição", "Data Previsão", "Data Conclusão", "Responsável", "Status", "Equipamento"],
    ["955681", "Cometiva", "PNEU DA BRE FUROU", "15/03/2025", "15/03/2025", "BICICLETERO JORGE", "Em andamento", "PNEU"],
    ["450847", "Provenida", "enclos e pneu", "15/03/2025", "15/03/2025", "bicicletário mario", "Conclusão", "bike"]
]

# Criação do PDF
pdf = SimpleDocTemplate("manutencao.pdf", pagesize=A4)
styles = getSampleStyleSheet()
elements = []

# Título
title = Paragraph("BESTÃO DE MANUTENÇÃO", styles['Title'])
elements.append(title)

# Criação da tabela
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

elements.append(table)

# Geração do PDF
pdf.build(elements)

def conectar_banco():
    """Função para conectar ao banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='projetointegrador03',
            use_pure=True  # Força o uso do conector puro
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
    janela.configure(bg='#f0f0f0')  # Cor de fundo da janela

    # Título
    titulo = tk.Label(janela, text="GESTÃO DE MANUTENÇÃO", font=("Helvetica", 16), bg='#f0f0f0')
    titulo.pack(pady=10, anchor='w')

    # Frame para os campos de entrada
    frame_campos = tk.Frame(janela, bg='#f0f0f0')
    frame_campos.pack(pady=10)

    # Campos de entrada organizados em 2 linhas e 4 colunas
    campos = [
        ("Tipo de Manut.:", ttk.Combobox(frame_campos, values=["Preventiva", "Corretiva"])),
        ("Equipamento:", tk.Entry(frame_campos)),
        ("Data Previsão:", DateEntry(frame_campos, date_pattern='dd/MM/yyyy')),
        ("Data Conclusão:", DateEntry(frame_campos, date_pattern='dd/MM/yyyy')),
        ("Responsável:", tk.Entry(frame_campos)),
        ("Status:", ttk.Combobox(frame_campos, values=["Em andamento", "Atrasada", "Concluída"])),
        ("Descrição:", tk.Entry(frame_campos)),
        ("Custo:", tk.Entry(frame_campos))
    ]

    for i, (label_text, widget) in enumerate(campos):
        tk.Label(frame_campos, text=label_text, bg='#f0f0f0').grid(row=i//4, column=(i%4)*2, padx=5, pady=5, sticky='e')
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
        messagebox.showerror("Erro", f"Formato de data inválido: {data_str}. Use o formato DD/MM/AAAA ou AAAA-MM-DD.")
        return None

    # Função para formatar data para exibição
    def formatar_data(data):
        if isinstance(data, datetime):
            return data.strftime("%d/%m/%Y")
        elif isinstance(data, str):
            try:
                # Converte a string no formato "YYYY-MM-DD" para datetime e formata como "DD/MM/YYYY"
                return datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError:
                return data
        return data

    # Função para limpar os campos de entrada
    def limpar_campos():
        tipo_combobox.set('')
        equipamento_entry.delete(0, tk.END)
        data_previsao_entry.set_date(datetime.today())
        data_conclusao_entry.set_date(datetime.today())
        responsavel_entry.delete(0, tk.END)
        status_combobox.set('')
        descricao_entry.delete(0, tk.END)
        custo_entry.delete(0, tk.END)

    # Função para validar o campo de custo
    def validar_custo(custo):
        try:
            float(custo.replace(',', '.'))
            return True
        except ValueError:
            return False

    # Função para formatar custo para exibição
    def formatar_custo(custo):
        try:
            # Converte o valor decimal para string e substitui o ponto por vírgula
            if isinstance(custo, str):
                valor = float(custo.replace(',', '.'))
            else:
                valor = float(custo)  # Converte decimal.Decimal para float
            return f"R$ {valor:,.2f}".replace('.', ',')
        except ValueError:
            return custo

    # Função para inserir dados
    def inserir_dados():
        if not campos_preenchidos():
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos")
            return

        if not validar_custo(custo_entry.get()):
            messagebox.showwarning("Aviso", "O campo 'Custo' deve ser um número válido.")
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
                    INSERT INTO om_manutencao (numero_ordem, tipo, descricao, data_previsao, data_conclusao, responsavel, status, equipamento, custo, ativo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    numero_ordem,
                    tipo_combobox.get(),
                    descricao_entry.get(),
                    data_previsao,
                    data_conclusao,
                    responsavel_entry.get(),
                    status_combobox.get(),
                    equipamento_entry.get(),
                    custo_entry.get().replace(',', '.'),
                    True  # Define o registro como ativo
                ))
                conn.commit()
                messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
                limpar_campos()  # Limpa os campos de entrada
                exibir_dados()  # Atualiza a exibição dos dados
            except Error as ex:
                messagebox.showerror("Erro", f"Erro ao inserir dados: {ex}")
            finally:
                conn.close()

    # Função para exibir dados na Treeview
    def exibir_dados():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM om_manutencao WHERE ativo = TRUE")
                rows = cursor.fetchall()

                # Limpa a Treeview antes de inserir novos dados
                for row in tree.get_children():
                    tree.delete(row)

                # Insere os dados na Treeview
                for row in rows:
                    # Formata as datas para DIA/MES/ANO
                    data_previsao_formatada = formatar_data(row[4])
                    data_conclusao_formatada = formatar_data(row[5])

                    # Insere os dados sem o ID
                    tree.insert("", "end", values=(
                        row[1],  # Número Ordem
                        row[2],  # Tipo
                        row[3],  # Descrição
                        data_previsao_formatada,  # Data Previsão
                        data_conclusao_formatada,  # Data Conclusão
                        row[6],  # Responsável
                        row[7],  # Status
                        row[8],  # Equipamento
                        formatar_custo(row[9])  # Custo
                    ))
            except Error as ex:
                messagebox.showerror("Erro", f"Erro ao buscar dados: {ex}")
            finally:
                conn.close()

    # Função para abrir a janela de edição
    def abrir_janela_edicao(item_id, dados):
        janela_edicao = tk.Toplevel(janela)
        janela_edicao.title("Editar Dados")
        janela_edicao.geometry("600x400")
        janela_edicao.configure(bg='#f0f0f0')

        frame_edicao = tk.Frame(janela_edicao, bg='#f0f0f0')
        frame_edicao.pack(pady=10)

        campos_edicao = [
            ("Tipo:", ttk.Combobox(frame_edicao, values=["Preventiva", "Corretiva"])),
            ("Equipamento:", tk.Entry(frame_edicao)),
            ("Data Previsão:", DateEntry(frame_edicao, date_pattern='dd/MM/yyyy')),
            ("Data Conclusão:", DateEntry(frame_edicao, date_pattern='dd/MM/yyyy')),
            ("Responsável:", tk.Entry(frame_edicao)),
            ("Status:", ttk.Combobox(frame_edicao, values=["Em andamento", "Atrasada", "Concluída"])),
            ("Descrição:", tk.Entry(frame_edicao)),
            ("Custo:", tk.Entry(frame_edicao))
        ]

        for i, (label_text, widget) in enumerate(campos_edicao):
            tk.Label(frame_edicao, text=label_text, bg='#f0f0f0').grid(row=i//4, column=(i%4)*2, padx=5, pady=5, sticky='e')
            widget.grid(row=i//4, column=(i%4)*2+1, padx=5, pady=5, sticky='w')

        tipo_combobox_edicao, equipamento_entry_edicao, data_previsao_entry_edicao, data_conclusao_entry_edicao, responsavel_entry_edicao, status_combobox_edicao, descricao_entry_edicao, custo_entry_edicao = [widget for _, widget in campos_edicao]

        # Preencher os campos com os dados da linha selecionada
        tipo_combobox_edicao.set(dados[1])
        equipamento_entry_edicao.insert(0, dados[7])
        
        # Ajuste para lidar com diferentes formatos de data
        try:
            data_previsao = datetime.strptime(dados[3], "%d/%m/%Y")
        except ValueError:
            data_previsao = datetime.strptime(dados[3], "%Y-%m-%d")
        data_previsao_entry_edicao.set_date(data_previsao)
        
        try:
            data_conclusao = datetime.strptime(dados[4], "%d/%m/%Y")
        except ValueError:
            data_conclusao = datetime.strptime(dados[4], "%Y-%m-%d")
        data_conclusao_entry_edicao.set_date(data_conclusao)
        
        responsavel_entry_edicao.insert(0, dados[5])
        status_combobox_edicao.set(dados[6])
        descricao_entry_edicao.insert(0, dados[2])
        custo_entry_edicao.insert(0, dados[8])

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

            if not validar_custo(custo_entry_edicao.get()):
                messagebox.showwarning("Aviso", "O campo 'Custo' deve ser um número válido.")
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
                        custo_entry_edicao.get().replace(',', '.'),
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

        # Frame para os botões OK e Cancelar
        frame_botoes_edicao = tk.Frame(janela_edicao, bg='#f0f0f0')
        frame_botoes_edicao.pack(pady=10)

        tk.Button(frame_botoes_edicao, text="OK", command=salvar_edicao, bg='#4CAF50', fg='white').pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botoes_edicao, text="Cancelar", command=janela_edicao.destroy, bg='#f44336', fg='white').pack(side=tk.LEFT, padx=10)

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
                    cursor.execute("UPDATE om_manutencao SET ativo = FALSE WHERE id = %s", (item_id,))
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Ordem marcada como excluída com sucesso!")
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
        confirmacao.configure(bg='#f0f0f0')
        tk.Label(confirmacao, text="Tem certeza que deseja excluir esta ordem?", bg='#f0f0f0').pack(pady=20)
        tk.Button(confirmacao, text="Sim", command=confirmar_exclusao, bg='#f44336', fg='white').pack(side=tk.LEFT, padx=20)
        tk.Button(confirmacao, text="Não", command=confirmacao.destroy, bg='#4CAF50', fg='white').pack(side=tk.RIGHT, padx=20)

    # Função para atualizar as informações exibidas
    def atualizar_informacoes():
        exibir_dados()

    # Função para gerar o relatório em PDF
    def gerar_relatorio_pdf():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM om_manutencao WHERE ativo = TRUE")
                rows = cursor.fetchall()
                if not rows:
                    messagebox.showinfo("Informação", "Não há dados para gerar o relatório.")
                    return

                c = canvas.Canvas("relatorio_manutencao.pdf", pagesize=letter)
                width, height = letter
                c.drawString(30, height - 40, "Relatório de Manutenção")
                c.drawString(30, height - 60, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

                y = height - 80
                for row in rows:
                    y -= 20
                    c.drawString(30, y, f"ID: {row[0]}, Ordem: {row[1]}, Tipo: {row[2]}, Descrição: {row[3]}, Data Previsão: {formatar_data(row[4])}, Data Conclusão: {formatar_data(row[5])}, Responsável: {row[6]}, Status: {row[7]}, Equipamento: {row[8]}, Custo: {formatar_custo(row[9])}")

                c.save()
                messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")

                # Abre o PDF automaticamente
                os.startfile("relatorio_manutencao.pdf")  # Para Windows
                # Para outros sistemas operacionais, use:
                # os.system("open relatorio_manutencao.pdf")  # macOS
                # os.system("xdg-open relatorio_manutencao.pdf")  # Linux
            except Error as ex:
                messagebox.showerror("Erro", f"Erro ao gerar relatório: {ex}")
            finally:
                conn.close()

    # Frame para os botões
    frame_botoes = tk.Frame(janela, bg='#f0f0f0')
    frame_botoes.pack(pady=10)

    # Botões para inserir, editar, concluir, excluir e atualizar informações
    tk.Button(frame_botoes, text="Salvar", command=inserir_dados, bg='#4CAF50', fg='white').grid(row=0, column=0, padx=10)
    tk.Button(frame_botoes, text="Editar Ordem", command=editar_dados, bg='#2196F3', fg='white').grid(row=0, column=1, padx=10)
    tk.Button(frame_botoes, text="Concluir Ordem", command=concluir_ordem, bg='#FF9800', fg='white').grid(row=0, column=2, padx=10)
    tk.Button(frame_botoes, text="Excluir Ordem", command=excluir_ordem, bg='#f44336', fg='white').grid(row=0, column=3, padx=10)
    tk.Button(frame_botoes, text="Atualizar Informações", command=atualizar_informacoes, bg='#9E9E9E', fg='white').grid(row=0, column=4, padx=10)

    # Adicionando o botão de impressão com ícone
    tk.Button(frame_botoes, text="Gerar Relatório PDF", command=gerar_relatorio_pdf, bg='#607D8B', fg='white').grid(row=0, column=5, padx=10)

    # Criando a Treeview para exibir os dados
    colunas = ("Número Ordem", "Tipo", "Descrição", "Data Previsão", "Data Conclusão", "Responsável", "Status", "Equipamento", "Custo")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
    tree.pack(pady=10, padx=10, fill="both", expand=True)

    # Exibir os dados ao iniciar a aplicação
    exibir_dados()

    # Iniciar a aplicação
    janela.mainloop()

# Iniciar a aplicação
criar_janela()