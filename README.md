System Monitoring (Python) 🖥️

Um sistema de monitoramento de hardware desenvolvido em Python para visualização em tempo real do desempenho do computador. Este projeto foi criado com foco em performance, usabilidade corporativa e arquitetura de software limpa, compondo meu portfólio profissional.

🚀 Funcionalidades Principais
Monitoramento Integrado: Coleta de dados precisos sobre o uso de CPU, Memória RAM (em % e GB) e processamento da Placa de Vídeo (GPU).

Tráfego de Rede Dinâmico: Acompanhamento de Download e Upload em tempo real, com formatação inteligente de unidades (B/s, KB/s ou MB/s).

Visualização Gráfica: Integração nativa com gráficos dinâmicos para análise de comportamento do processador ao longo do tempo.

Exportação de Dados: Geração automatizada de relatórios em .csv com o histórico de performance, permitindo análises posteriores em ferramentas de BI.

Arquitetura Escalável: Interface construída utilizando conceitos sólidos de Orientação a Objetos (OOP) e componentização visual.

🛠️ Tecnologias e Bibliotecas
Este projeto utiliza bibliotecas robustas do ecossistema Python para a coleta de dados e construção da interface desktop:

psutil: Biblioteca de referência para recuperação de métricas profundas do sistema operacional e hardware.

GPUtil: Utilizada para a extração direta da carga de trabalho e identificação de placas de vídeo NVIDIA.

matplotlib: Motor de renderização responsável pelo gráfico de linha contínuo embutido na aplicação.

customtkinter: Framework para a criação de uma interface gráfica (GUI) moderna, com visual sofisticado e suporte nativo a modo escuro.

Bibliotecas Nativas (csv, datetime, collections): Para manipulação eficiente de histórico em memória e exportação tabular.

💡 Por que este projeto?
Este sistema demonstra habilidades essenciais exigidas pelo mercado de desenvolvimento de software, como:

Lógica de Automação e SO: Compreensão de como o Python interage diretamente com os recursos físicos da máquina.

Ciclo de Vida do Dado: Experiência de ponta a ponta: extração de dados brutos, formatação visual para o usuário final e armazenamento persistente (CSV).

Engenharia de Interface: Capacidade de integrar renderização gráfica científica (Matplotlib) dentro de aplicações Desktop comerciais.

⚙️ Como rodar o projeto no modo Desenvolvedor
Clone este repositório:
git clone https://github.com/MatheusPinha/System-Monitoring-Python.git

Instale as dependências listadas:
pip install psutil gputil matplotlib customtkinter

Execute o arquivo principal:
python main.py

📦 Como compilar o projeto (Gerar o .exe final)
Para transformar este projeto em um executável autônomo do Windows (sem necessidade de instalar o Python na máquina alvo), utilize o PyInstaller:
pip install pyinstaller
pyinstaller --noconsole --onefile --collect-all customtkinter main.py

O arquivo final estará disponível dentro da pasta dist/.

Projeto desenvolvido por Matheus Pinha.
