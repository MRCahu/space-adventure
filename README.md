# Space Adventure

![image](https://github.com/user-attachments/assets/caa62247-251c-428b-b290-9c5b19d3196e)


Jogo 2D em Python/Turtle onde você pilota uma nave espacial para coletar estrelas e desviar de asteroides. Projetado para ser leve, modular e configurável, o *Space Adventure* serve tanto como projeto educativo para quem está começando em Python quanto como demonstração de boas práticas de engenharia de software.

---

## 🎯 Visão Geral

- **Objetivo**: Colete todas as estrelas amarelas antes que acabem suas vidas, evitando colisões com asteroides.
- **Público-alvo**: Estudantes de programação, entusiastas de jogos em Python e desenvolvedores que desejam um exemplo prático de CLI, logging e arquitetura orientada a objetos.
- **Diferenciais**:  
  - Configuração via linha de comando (`argparse`);  
  - Logging para depuração (`logging`);  
  - Código PEP 8, totalmente tipado e modular;  
  - Fácil extensão para novos níveis e elementos de jogo.

---

## 🚀 Funcionalidades Principais

- **Controle da nave** com teclas `<Up>`, `<Left>`, `<Right>`.
- **Configuração dinâmica** de resolução, número de estrelas, asteroides, vidas e velocidade.
- **HUD** (Heads-Up Display) exibindo nível, pontuação e vidas restantes.
- **Sistema de níveis** com incremento de velocidade e quantidade de asteroides a cada vitória.
- **Mensagens de vitória/derrota** e opção de reinício imediato (`R`).
- **Estrutura de projeto** pronta para testes, CI/CD e contribuição colaborativa.

---

## 🛠 Pré-requisitos

- **Python 3.7+**  
- **Tkinter** (incluído na maioria das distribuições Python)  
- Terminal (CMD, PowerShell, Bash, etc.)

---

## 📦 Instalação

1. **Clone este repositório**  
   ```bash
   git clone https://github.com/SEU_USUARIO/space-adventure.git
   cd space-adventure

python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt

python space_adventure_improved.py

| Flag          | Descrição                                    | Padrão |
| ------------- | -------------------------------------------- | ------ |
| `--width`     | Largura da janela (px)                       | 800    |
| `--height`    | Altura da janela (px)                        | 600    |
| `--stars`     | Número de estrelas para coletar              | 10     |
| `--asteroids` | Número inicial de asteroides                 | 5      |
| `--lives`     | Número de vidas                              | 3      |
| `--speed`     | Velocidade da nave                           | 20.0   |
| `--debug`     | Habilita mensagens de logging em nível DEBUG | false  |

python space_adventure_improved.py --width 1024 --height 768 --stars 15 --asteroids 8 --debug

space-adventure/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── docs/
│   └── screenshot.png
└── space_adventure_improved.py

git checkout -b feature/nova-funcionalidade

