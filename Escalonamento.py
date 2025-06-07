import tkinter as tk
from tkinter import ttk
from collections import deque
import time
import threading


class Processo:
    def __init__(self, nome, duracao, simbolo):
        self.nome = nome
        self.duracao = duracao
        self.progresso = 0
        self.finalizado = False
        self.simbolo = simbolo
        self.temp_final = None

    def atualizar(self, qtd):
        self.progresso += qtd
        if self.progresso >= self.duracao:
            self.progresso = self.duracao
            self.finalizado = True
            self.temp_final = time.time()

    def exibir_barra(self):
        barra = self.simbolo * self.progresso
        espaco = ' ' * (self.duracao - self.progresso)
        return f"{self.nome}: [{barra}{espaco}] {self.progresso}/{self.duracao}"


class Fila:
    def __init__(self):
        self.dados = deque()

    def add(self, p):
        self.dados.append(p)

    def remover(self):
        if self.dados:
            return self.dados.popleft()

    def vazia(self):
        return len(self.dados) == 0

    def __iter__(self):
        return iter(self.dados)


class app:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Escalonamento")
        self.algoritmo = tk.StringVar(value="FIFO")
        self.processos = []
        self.resultados = []
        self.root.configure(bg="#2E2E2E")  

        
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Custom.TFrame", background="#2E2E2E")
        style.configure("TLabel", background="#2E2E2E", foreground="#E0E0E0")
        style.configure("TRadiobutton", background="#2E2E2E", foreground="#E0E0E0")
        style.configure("TButton", background="#3A7CA5", foreground="#FFFFFF", padding=6)
        style.map("TButton", background=[('active', "#EBA709")],foreground=[('disabled', "#EBA709")])

        self.algoritmo = tk.StringVar(value="FIFO")
        self.criar_interface()
        self.criar_interface()

    def criar_interface(self):
        frame = ttk.Frame(self.root, padding=20,style = 'Custom.TFrame')
        frame.grid(row=0, column=0, sticky="w")
        

    
        ttk.Label(frame, text="Simulador de Escalonamento de Processos", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10))

    
        ttk.Label(frame, text="Escolha o tipo de escalonamento: ", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(frame, text="FIFO(Primeiro a chegar, primeiro a executar)", variable=self.algoritmo, value="FIFO").grid(row=2, column=0, columnspan=3, sticky="w", pady=(0, 5))
        ttk.Radiobutton(frame, text="Round Robin(Turnos de execuçao)", variable=self.algoritmo, value="RR").grid(row=3, column=0, columnspan=3, sticky="w")

    
        ttk.Label(frame, text="Tempo por processo (quantum):", font=("Helvetica", 10)).grid(row=4, column=0, sticky="w", pady=(10, 0))
        self.quantum_entry = ttk.Entry(frame, width=10)
        self.quantum_entry.grid(row=4, column=1, sticky="w")

    
        self.iniciar_btn = ttk.Button(frame, text="▶️ Começar Simulaçao", command=self.iniciar_simulacao)
        self.iniciar_btn.grid(row=5, column=0, columnspan=3, pady=(15, 0))

    
        self.output = tk.Text(self.root, height=20, width=70, font=("Courier New", 10))
        self.output.grid(row=1, column=0, padx=20, pady=(10, 20))

    def escrever(self, texto):
        self.output.insert(tk.END, texto + '\n')
        self.output.see(tk.END)

    def iniciar_simulacao(self):
        self.output.delete("1.0", tk.END)
        self.resultados.clear()

        
        p1 = Processo("Fabio", 10, "😎")
        p2 = Processo("Isaac", 8, "🧑🏻‍💻")
        p3 = Processo("Girotto", 6, "😄")

        self.fila = Fila()
        for p in [p1, p2, p3]:
            self.fila.add(p)

        
        t = threading.Thread(target=self.executar_escalonador)
        t.start()

    def executar_escalonador(self):
        if self.algoritmo.get() == "FIFO":
            self.escalonador_fifo()
        elif self.algoritmo.get() == "RR":
            try:
                q = int(self.quantum_entry.get())
                self.escalonador_round_robin(q)
            except ValueError:
                self.escrever("Quantum invalido.")

        self.escrever("\nTodos os processos foram executados.")
        if self.resultados:
            vencedor = sorted(self.resultados, key=lambda x: x[1])[0][0]#sorted pega do menor pro maior
            self.escrever(f'O vencedor foi {vencedor}')

    def escalonador_fifo(self):
        while not self.fila.vazia():
            proc = self.fila.remover()
            while not proc.finalizado:
                proc.atualizar(1)
                self.atualizar_tela(proc, "FIFO")
                time.sleep(1)
            self.resultados.append((proc.nome, proc.temp_final))
            self.escrever(f"{proc.nome} concluido.")
            time.sleep(1)

    def escalonador_round_robin(self, quantum):
        while not self.fila.vazia():
            atual = self.fila.remover()

            if atual.finalizado:
                continue

            atual.atualizar(min(quantum, atual.duracao - atual.progresso))
            self.atualizar_tela(atual, "Round Robin")
            time.sleep(1)

            if not atual.finalizado:
                self.fila.add(atual)
            else:
                self.resultados.append((atual.nome, atual.temp_final))
                self.escrever(f"{atual.nome} terminou")
                time.sleep(1)

    def atualizar_tela(self, atual, modo):
        self.output.delete("1.0", tk.END)
        self.escrever(f"Executando {atual.nome} ({modo})\n")
        self.escrever(atual.exibir_barra())
        for p in self.fila:
            self.escrever(p.exibir_barra())



if __name__ == "__main__":
    root = tk.Tk()
    app = app(root)
    root.mainloop()
