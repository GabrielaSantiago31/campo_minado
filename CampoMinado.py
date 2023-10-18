import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class Tabuleiro:
    def __init__(self, tamanho, num_minas):
        self.tamanho = tamanho
        self.num_minas = num_minas
        self.tabuleiro = self.inicializar_tabuleiro()
        self.minas = self.colocar_minas()

    def inicializar_tabuleiro(self):
        return [['*' for _ in range(self.tamanho[1])] for _ in range(self.tamanho[0])]

    def colocar_minas(self):
        minas = set()
        while len(minas) < self.num_minas:
            x = random.randint(0, self.tamanho[0] - 1)
            y = random.randint(0, self.tamanho[1] - 1)
            minas.add((x, y))
        return minas

    def contar_minas_adjacentes(self, x, y):
        contador = 0
        for i in range(max(0, x - 1), min(self.tamanho[0], x + 2)):
            for j in range(max(0, y - 1), min(self.tamanho[1], y + 2)):
                if (i, j) in self.minas:
                    contador += 1
        return contador

    def revelar_ponto_seguro(self):
        x, y = random.randint(0, self.tamanho[0] - 1), random.randint(0, self.tamanho[1] - 1)
        while (x, y) in self.minas:
            x, y = random.randint(0, self.tamanho[0] - 1), random.randint(0, self.tamanho[1] - 1)

        minas_adjacentes = self.contar_minas_adjacentes(x, y)
        if minas_adjacentes == 0:
            self.tabuleiro[x][y] = str(self.contar_minas_adjacentes(x, y))
        else:
            self.tabuleiro[x][y] = str(minas_adjacentes)

        return x, y

class Jogo:
    def __init__(self, tamanho, num_minas, root):
        self.root = root
        self.tamanho = tamanho
        self.num_minas = num_minas

        self.jogadas_restantes = self.tamanho[0] * self.tamanho[1] - self.num_minas
        self.minas_restantes = self.num_minas

        self.dicas_usadas = 0
        self.limite_dicas = self.tamanho[0]  # Agora, o limite de dicas é igual ao nível

        self.primeira_jogada = True
        self.criar_interface_jogo()
        self.atualizar_interface()

    def criar_botao(self, x, y):
        def callback():
            if self.primeira_jogada:
                while (x, y) in self.tabuleiro.minas:
                    self.tabuleiro = Tabuleiro(self.tamanho, self.num_minas)
            self.primeira_jogada = False

            if (x, y) in self.tabuleiro.minas:
                imagem = tk.PhotoImage(file="imagens/mina.png")
                imagem = imagem.subsample(2, 2)
                self.buttons[x][y].config(image=imagem, height=30, width=30, state=tk.DISABLED)
                self.atualizar_minas_restantes()
                messagebox.showinfo("Fim de Jogo", "Você perdeu! Acertou uma mina.")
                self.tabuleiro.tabuleiro[x][y] = 'X'
                self.mostrar_tabuleiro()
                self.root.quit()
            else:
                if self.tabuleiro.tabuleiro[x][y] == '*':
                    self.jogadas_restantes -= 1
                    minas_adjacentes = self.tabuleiro.contar_minas_adjacentes(x, y)
                    if minas_adjacentes >= 0:
                        self.tabuleiro.tabuleiro[x][y] = str(minas_adjacentes)
                    else:
                        self.tabuleiro.tabuleiro[x][y] = ' '
                    self.buttons[x][y].config(text=str(self.tabuleiro.tabuleiro[x][y]), state=tk.DISABLED)
                    if self.jogadas_restantes == 0:
                        self.mostrar_tabuleiro()
                        messagebox.showinfo("Fim de Jogo", "Você venceu! Parabéns.")
                        self.root.quit()

        button = tk.Button(self.tabuleiro_frame, text="", width=4, height=2, command=callback)
        button.grid(row=x, column=y, sticky='nsew')
        self.buttons[x].append(button)

    def criar_interface_jogo(self):
        self.tabuleiro = Tabuleiro(self.tamanho, self.num_minas)
        self.buttons = [[] for _ in range(self.tamanho[0])]

        self.tabuleiro_frame = tk.Frame(self.root)
        self.tabuleiro_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        for i in range(self.tamanho[0]):
            for j in range(self.tamanho[1]):
                self.criar_botao(i, j)

        for i in range(self.tamanho[0]):
            self.tabuleiro_frame.grid_rowconfigure(i, weight=1)

        for j in range(self.tamanho[1]):
            self.tabuleiro_frame.grid_columnconfigure(j, weight=1)

        self.botoes_frame = tk.Frame(self.root)
        self.botoes_frame.grid(row=1, column=0, padx=5, pady=5, sticky='n')

        self.botao_reset = tk.Button(self.botoes_frame, text="Reset", command=self.reiniciar_jogo)
        self.botao_reset.grid(row=0, column=0, padx=5, pady=5)

        self.botao_dica = tk.Button(self.botoes_frame, text="Dica ({}/{})".format(self.dicas_usadas, self.limite_dicas), command=self.usar_dica)
        self.botao_dica.grid(row=0, column=1, padx=5, pady=5)

        self.botao_sair = tk.Button(self.botoes_frame, text="Sair", command=self.sair_do_jogo)
        self.botao_sair.grid(row=0, column=2, padx=5, pady=5)

        self.minas_label = tk.Label(self.root, text=f'Minas Restantes: {self.minas_restantes}')
        self.minas_label.grid(row=2, column=0, padx=5, pady=5)

    def reiniciar_jogo(self):
        self.dicas_usadas = 0
        self.atualizar_minas_restantes()
        self.primeira_jogada = True
        self.criar_interface_jogo()

    def mostrar_tabuleiro(self):
        for x in range(self.tamanho[0]):
            for y in range(self.tamanho[1]):
                if self.tabuleiro.tabuleiro[x][y] == 'X':
                    self.buttons[x][y].config(text='X', state=tk.DISABLED)

    def atualizar_minas_restantes(self):
        self.minas_restantes -= 1
        if self.minas_restantes >= 0:
            self.minas_label.config(text=f'Minas Restantes: {self.minas_restantes}')

    def usar_dica(self):
        if self.dicas_usadas < self.limite_dicas:
            x, y = self.tabuleiro.revelar_ponto_seguro()
            if x is not None and y is not None:
                self.buttons[x][y].config(text=str(self.tabuleiro.tabuleiro[x][y]), state=tk.DISABLED)
                self.jogadas_restantes -= 1
                self.dicas_usadas += 1
                self.botao_dica.config(text="Dica ({}/{})".format(self.dicas_usadas, self.limite_dicas))
                if self.jogadas_restantes == 0:
                    self.mostrar_tabuleiro()
                    messagebox.showinfo("Fim de Jogo", "Você venceu! Parabéns.")
                    self.sair_do_jogo()
                    self.atualizar_minas_restantes()
            else:
                messagebox.showinfo("Sem pontos seguros", "Não há mais pontos seguros para revelar.")
        else:
            messagebox.showinfo("Limite de Dicas", "Você já usou todas as dicas disponíveis.")
            self.botao_dica.config(state=tk.DISABLED)

    def sair_do_jogo(self):
        self.root.quit()

    def atualizar_interface(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.botoes_frame.grid(row=1, column=0, padx=5, pady=5)

def main():
    root = tk.Tk()
    root.title("Campo Minado")
    escolha = 'S'

    while escolha == 'S':
        nivel = simpledialog.askinteger("Dificuldade", "Digite a dificuldade (número de linhas/colunas):", initialvalue=5)
        num_minas = nivel
        if nivel is not None and num_minas is not None:
            tamanho = (nivel, nivel)
            if num_minas <= nivel * nivel:
                jogo = Jogo(tamanho, num_minas, root)
                root.mainloop()
                escolha = simpledialog.askstring("Jogar Novamente", "Deseja jogar novamente? (S para sim, N para não):").strip().upper()
            else:
                messagebox.showerror("Erro", "O número de minas deve ser menor ou igual ao número de células.")
        else:
            escolha = 'N'

if __name__ == "__main__":
    main()
