import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import csv

class Chamado:
    def __init__(self, numero, tipo):
        self.numero = numero
        self.tipo = tipo
        self.tempo_abertura = datetime.now()
        self.tempo_limite = self.tempo_abertura + timedelta(hours=2) if tipo == "Urgente" else self.tempo_abertura + timedelta(hours=4)
        self.tempo_decorrido = timedelta()
        self.pausado = False
        self.finalizado = False
        self.tecnico = None

    def adicionar_tecnico(self, tecnico):
        self.tecnico = tecnico

    def iniciar(self):
        self.tempo_decorrido = datetime.now() - self.tempo_abertura
        self.pausado = False

    def pausar_retomar(self):
        if self.pausado:
            self.tempo_abertura = datetime.now() - self.tempo_decorrido
        else:
            self.tempo_decorrido = datetime.now() - self.tempo_abertura
        self.pausado = not self.pausado

    def finalizar(self):
        if not self.finalizado:
            self.tempo_decorrido = datetime.now() - self.tempo_abertura
            self.finalizado = True
            return True
        return False

    def reiniciar(self):
        self.tempo_abertura = datetime.now()
        self.tempo_decorrido = timedelta()
        self.finalizado = False

    def remover_tecnico(self):
        self.tecnico = None


class AplicacaoChamados:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Chamados")
        self.chamados = []

        self.label_numero = ttk.Label(self.root, text="Número do Chamado:")
        self.label_numero.pack()
        self.entry_numero = ttk.Entry(self.root)
        self.entry_numero.pack()

        self.label_tipo = ttk.Label(self.root, text="Tipo do Chamado:")
        self.label_tipo.pack()
        self.combo_tipo = ttk.Combobox(self.root, values=["Urgente", "Normal"])
        self.combo_tipo.pack()
                
        self.label_tecnico = ttk.Label(self.root, text="Técnico Designado:")
        self.label_tecnico.pack()
        self.combo_tecnico = ttk.Combobox(self.root, values=["Anderson", "Daniel", "Douglas", "Fábio", "Giovanni", "Jean", "Jonathan", "Leonardo", "Luis Eduardo", "Marcelo", "Marcos", "Vinicius"])
        self.combo_tecnico.pack()

        
        ##self.entry_tecnico = ttk.Entry(self.root)
        ##self.entry_tecnico.pack()

        self.botao_adicionar = ttk.Button(self.root, text="Adicionar Chamado", command=self.adicionar_chamado)
        self.botao_adicionar.pack()

        self.treeview = ttk.Treeview(self.root, columns=("Número", "Tipo", "Técnico", "Tempo Abertura", "Tempo Decorrido", "Tempo Restante", "Status"), show="headings")
        self.treeview.heading("Número", text="Número")
        self.treeview.heading("Tipo", text="Tipo")
        self.treeview.heading("Técnico", text="Técnico")
        self.treeview.heading("Tempo Abertura", text="Tempo de Abertura")
        self.treeview.heading("Tempo Decorrido", text="Tempo Decorrido")
        self.treeview.heading("Tempo Restante", text="Tempo Restante")
        self.treeview.heading("Status", text="Status")
        self.treeview.pack()

        self.botao_remover = ttk.Button(self.root, text="Remover Chamado", command=self.remover_chamado)
        self.botao_remover.pack()

        self.botao_iniciar = ttk.Button(self.root, text="Iniciar Atendimento", command=self.iniciar_atendimento)
        self.botao_iniciar.pack()

        self.botao_pausar_retomar = ttk.Button(self.root, text="Pausar/Retomar Atendimento", command=self.pausar_retomar_atendimento)
        self.botao_pausar_retomar.pack()

        self.botao_finalizar = ttk.Button(self.root, text="Finalizar Chamado", command=self.finalizar_chamado)
        self.botao_finalizar.pack()

        self.botao_reiniciar = ttk.Button(self.root, text="Reiniciar Chamado", command=self.reiniciar_chamado)
        self.botao_reiniciar.pack()

        self.botao_remover_tecnico = ttk.Button(self.root, text="Remover Técnico", command=self.remover_tecnico)
        self.botao_remover_tecnico.pack()

        self.botao_salvar_csv = ttk.Button(self.root, text="Salvar Chamados em CSV", command=self.salvar_csv)
        self.botao_salvar_csv.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)

    def adicionar_chamado(self):
        numero = self.entry_numero.get().strip()
        tipo = self.combo_tipo.get()
        tecnico = self.combo_tecnico.get().strip()

        if numero and tipo:
            chamado = Chamado(numero, tipo)
            if tecnico:
                chamado.adicionar_tecnico(tecnico)
            self.chamados.append(chamado)
            self.atualizar_tabela()
            messagebox.showinfo("Adicionar Chamado", f"Chamado {numero} adicionado com sucesso.")
            self.entry_numero.delete(0, tk.END)
            self.combo_tipo.set("")
            self.combo_tecnico.delete(0, tk.END)
        else:
            messagebox.showwarning("Adicionar Chamado", "Número e tipo do chamado são obrigatórios.")

    def remover_chamado(self):
        item_selecionado = self.treeview.focus()
        if item_selecionado:
            index = int(self.treeview.item(item_selecionado)["text"]) - 1
            chamado = self.chamados[index]
            self.chamados.remove(chamado)
            self.atualizar_tabela()
            messagebox.showinfo("Remover Chamado", f"Chamado {chamado.numero} removido com sucesso.")

    def atualizar_tabela(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        for i, chamado in enumerate(self.chamados):
            tecnico = chamado.tecnico if chamado.tecnico else "-"
            tempo_abertura = chamado.tempo_abertura.strftime("%Y-%m-%d %H:%M:%S")
            tempo_decorrido = str(chamado.tempo_decorrido).split(".")[0]
            tempo_restante = str(chamado.tempo_limite - datetime.now()).split(".")[0]
            status = "Finalizado" if chamado.finalizado else "Em Atendimento"
            self.treeview.insert("", tk.END, text=str(i + 1), values=(chamado.numero, chamado.tipo, tecnico,
                                                                      tempo_abertura, tempo_decorrido,
                                                                      tempo_restante, status))
    def atualizar_botoes(self):
        item_selecionado = self.treeview.focus()
        if item_selecionado:
            index = int(self.treeview.item(item_selecionado)["text"]) - 1
            chamado = self.chamados[index]
            if chamado.finalizado:
                self.botao_iniciar.config(state=tk.DISABLED)
                self.botao_pausar_retomar.config(state=tk.DISABLED)
                self.botao_finalizar.config(state=tk.DISABLED)
                self.botao_reiniciar.config(state=tk.NORMAL)
                self.botao_remover_tecnico.config(state=tk.DESABLE)
            else:
                self.botao_iniciar.config(state=tk.NORMAL)
                self.botao_pausar_retomar.config(state=tk.NORMAL if chamado.iniciado else tk.DISABLED)
                self.botao_finalizar.config(state=tk.NORMAL if chamado.iniciado else tk.DISABLED)
                self.botao_reiniciar.config(state=tk.DISABLED)
                self.botao_remover_tecnico.config(state=tk.DISABLED)
        else:
            self.botao_iniciar.config(state=tk.NORMAL)
            self.botao_pausar_retomar.config(state=tk.NORMAL)
            self.botao_finalizar.config(state=tk.NORMAL)
            self.botao_reiniciar.config(state=tk.NORMAL)
            self.botao_remover_tecnico.config(state=tk.DISABLED)

    
    def iniciar_atendimento(self):
        item_selecionado = self.treeview.focus()
        if item_selecionado:
            index = int(self.treeview.item(item_selecionado)["text"]) - 1
            chamado = self.chamados[index]
            chamado.iniciar()
            self.atualizar_tabela()
            self.atualizar_botoes()
            messagebox.showinfo("Iniciar Atendimento", f"Atendimento do chamado {chamado.numero} iniciado.")

    def pausar_retomar_atendimento(self):
        item_selecionado = self.treeview.focus()
        if item_selecionado:
            index = int(self.treeview.item(item_selecionado)["text"]) - 1
            chamado = self.chamados[index]
            chamado.pausar_retomar()
            self.atualizar_tabela()
            self.atualizar_botoes()
            if chamado.pausado:
                messagebox.showinfo("Pausar Atendimento", f"Atendimento do chamado {chamado.numero} pausado.")
            else:
                messagebox.showinfo("Retomar Atendimento", f"Atendimento do chamado {chamado.numero} retomado.")

    def finalizar_chamado(self):
        item_selecionado = self.treeview.focus()
        if item_selecionado:
            index = int(self.treeview.item(item_selecionado)["text"]) - 1
            chamado = self.chamados[index]
            if chamado.finalizar():
                self.atualizar_tabela()
                self.atualizar_botoes()
                messagebox.showinfo("Finalizar Chamado", f"Chamado {chamado.numero} finalizado.")
            else:
                messagebox.showwarning("Finalizar Chamado", f"O chamado {chamado.numero} já está finalizado.")

    def reiniciar_chamado(self):
        item_selecionado = self.treeview.focus()
        if item_selecionado:
            index = int(self.treeview.item(item_selecionado)["text"]) - 1
            chamado = self.chamados[index]
            chamado.reiniciar()
            self.atualizar_tabela()
            self.atualizar_botoes()
            messagebox.showinfo("Reiniciar Chamado", f"Chamado {chamado.numero} reiniciado.")

    def remover_tecnico(self):
        item_selecionado = self.treeview.focus()
        if item_selecionado:
            index = int(self.treeview.item(item_selecionado)["text"]) - 1
            chamado = self.chamados[index]
            chamado.remover_tecnico()
            self.atualizar_tabela()
            self.atualizar_botoes()
            messagebox.showinfo("Remover Técnico", f"Técnico removido do chamado {chamado.numero}.")

    def salvar_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Número", "Tipo", "Técnico", "Tempo de Abertura", "Tempo Decorrido", "Tempo Restante", "Status"])
                for chamado in self.chamados:
                    tecnico = chamado.tecnico if chamado.tecnico else "-"
                    tempo_abertura = chamado.tempo_abertura.strftime("%Y-%m-%d %H:%M:%S")
                    tempo_decorrido = str(chamado.tempo_decorrido).split(".")[0]
                    tempo_restante = str(chamado.tempo_limite - datetime.now()).split(".")[0]
                    status = "Finalizado" if chamado.finalizado else "Em Atendimento"
                    writer.writerow([chamado.numero, chamado.tipo, tecnico, tempo_abertura, tempo_decorrido,
                                     tempo_restante, status])
            messagebox.showinfo("Salvar Chamados em CSV", "Chamados salvos com sucesso.")

    def fechar_aplicacao(self):
        if messagebox.askokcancel("Fechar Aplicação", "Deseja realmente fechar a aplicação?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    aplicacao = AplicacaoChamados(root)
    root.mainloop()
