import customtkinter as ctk
import psutil
import GPUtil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import csv
from datetime import datetime
import os

# =======================================================
# FUNÇÕES AUXILIARES
# =======================================================
def formatar_rede(bytes_segundo):
    """Converte bytes por segundo para a unidade mais adequada automaticamente"""
    if bytes_segundo < 1024:
        return f"{bytes_segundo:.0f} B/s"
    elif bytes_segundo < 1024 * 1024:
        kb_segundo = bytes_segundo / 1024
        return f"{kb_segundo:.2f} KB/s"
    else:
        mb_segundo = bytes_segundo / (1024 * 1024)
        return f"{mb_segundo:.2f} MB/s"

# Configuração do tema global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =======================================================
# COMPONENTE REUTILIZÁVEL ATUALIZADO
# =======================================================
class ComponenteMonitoramento(ctk.CTkFrame):
    def __init__(self, master, titulo, tem_barra=True, **kwargs):
        super().__init__(master, **kwargs)
        self.tem_barra = tem_barra
        
        self.label = ctk.CTkLabel(self, text=f"{titulo}: Calculando...", font=("Arial", 14))
        self.label.pack(pady=(5, 0))
        
        if self.tem_barra:
            self.barra = ctk.CTkProgressBar(self, width=350)
            self.barra.pack(pady=(5, 10))
            self.barra.set(0)

    def atualizar(self, percentual, texto_extra=""):
        if self.tem_barra:
            # Limita a barra entre 0 e 100% para evitar erros visuais
            valor_barra = min(max(percentual / 100, 0.0), 1.0)
            self.barra.set(valor_barra)
        self.label.configure(text=texto_extra)

# =======================================================
# JANELA PRINCIPAL
# =======================================================
class MonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PC System Monitor Pro")
        self.geometry("800x850") # Aumentado para caber todos os itens

        # Variáveis para Rede e Histórico (CSV)
        self.ultimo_net_io = psutil.net_io_counters()
        self.historico_dados = [] # Guarda todas as linhas para o CSV

        # Título
        self.label_titulo = ctk.CTkLabel(self, text="Painel de Desempenho", font=("Arial", 22, "bold"))
        self.label_titulo.pack(pady=10)

        # 1. Instanciando os Componentes
        self.comp_cpu = ComponenteMonitoramento(self, "CPU")
        self.comp_cpu.pack(fill="x", padx=20)

        self.comp_ram = ComponenteMonitoramento(self, "RAM")
        self.comp_ram.pack(fill="x", padx=20)

        self.comp_gpu = ComponenteMonitoramento(self, "GPU")
        self.comp_gpu.pack(fill="x", padx=20)

        # Componente de Rede (sem barra de progresso)
        self.comp_rede = ComponenteMonitoramento(self, "Rede", tem_barra=False)
        self.comp_rede.pack(fill="x", padx=20, pady=5)

        # Botão de Exportar CSV
        self.btn_exportar = ctk.CTkButton(self, text="📥 Exportar Relatório CSV", command=self.exportar_csv, fg_color="#28a745", hover_color="#218838")
        self.btn_exportar.pack(pady=10)

        # 2. Configuração do Gráfico (Matplotlib)
        self.historico_cpu = deque([0]*60, maxlen=60)
        
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(6, 2.5), dpi=100)
        self.fig.patch.set_facecolor('#242424')
        self.ax.set_facecolor('#242424')
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Uso da CPU (Tempo Real)")
        self.linha, = self.ax.plot(self.historico_cpu, color='cyan')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=10)

        # Inicia o loop de monitoramento
        self.atualizar_dados()

    def exportar_csv(self):
        # Gera um nome de arquivo com a data e hora atual
        nome_arquivo = f"relatorio_sistema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            # Escreve o cabeçalho
            writer.writerow(["Data/Hora", "CPU (%)", "RAM (%)", "RAM (GB)", "GPU (%)", "Download (MB/s)", "Upload (MB/s)"])
            # Escreve todos os dados salvos
            writer.writerows(self.historico_dados)
        
        # Feedback visual de sucesso no botão
        self.btn_exportar.configure(text=f"✅ Salvo: {nome_arquivo}", fg_color="#17a2b8")
        self.after(3000, lambda: self.btn_exportar.configure(text="📥 Exportar Relatório CSV", fg_color="#28a745"))

    def atualizar_dados(self):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- Coleta CPU, RAM e GPU ---
        uso_cpu = psutil.cpu_percent()
        memoria = psutil.virtual_memory()
        uso_ram_percent = memoria.percent
        ram_usada_gb = memoria.used / (1024 ** 3)
        
        gpus = GPUtil.getGPUs()
        uso_gpu = gpus[0].load * 100 if gpus else 0.0

        # --- Coleta Rede (Bytes Brutos) ---
        atual_net_io = psutil.net_io_counters()
        
        # Diferença em bytes desde o último tick
        bytes_recv_segundo = atual_net_io.bytes_recv - self.ultimo_net_io.bytes_recv
        bytes_sent_segundo = atual_net_io.bytes_sent - self.ultimo_net_io.bytes_sent
        
        self.ultimo_net_io = atual_net_io # Atualiza a referência para o próximo segundo

        # Textos dinâmicos para a Interface (B/s, KB/s, MB/s)
        texto_download = formatar_rede(bytes_recv_segundo)
        texto_upload = formatar_rede(bytes_sent_segundo)

        # Valores em Megabytes padronizados para o CSV
        download_mbs = bytes_recv_segundo / (1024 * 1024)
        upload_mbs = bytes_sent_segundo / (1024 * 1024)

        # --- Salva no Histórico para o CSV ---
        self.historico_dados.append([
            agora, uso_cpu, uso_ram_percent, round(ram_usada_gb, 2), 
            round(uso_gpu, 2), round(download_mbs, 2), round(upload_mbs, 2)
        ])

        # --- Atualiza Interface Visual ---
        self.comp_cpu.atualizar(uso_cpu, f"Uso da CPU: {uso_cpu:.1f}%")
        self.comp_ram.atualizar(uso_ram_percent, f"Uso da RAM: {ram_usada_gb:.1f}GB ({uso_ram_percent:.1f}%)")
        self.comp_gpu.atualizar(uso_gpu, f"GPU ({gpus[0].name if gpus else 'N/A'}): {uso_gpu:.1f}%")
        self.comp_rede.atualizar(0, f"Rede - Download: {texto_download} | Upload: {texto_upload}")

        # --- Atualiza Gráfico ---
        self.historico_cpu.append(uso_cpu)
        self.linha.set_ydata(self.historico_cpu)
        self.canvas.draw()

        # Chama esta mesma função novamente após 1000 milissegundos (1 segundo)
        self.after(1000, self.atualizar_dados)

if __name__ == "__main__":
    app = MonitorApp()
    app.mainloop()