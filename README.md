![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-darkblue)

# 🔤 Calculadora de Fontes

Uma ferramenta desktop para calcular e visualizar métricas de tamanhos de fontes em tempo real — ideal para devs que usam `tkinter` / `CustomTkinter` e precisam posicionar textos com precisão via `place()`.

---

## ✨ Funcionalidades

- **Preview em tempo real** — A visualização atualiza automaticamente após preencher todos os campos.
- **Todas as fontes do sistema** — Seletor com busca instantânea e scroll, listando todas as fontes.
- **Estilos completos** — Suporte a `normal`, `bold`, `italic` e `bold italic`.
- **Alinhamento** — Visualize o texto alinhado à esquerda, centralizado ou à direita diretamente no preview.
- **Seletor de cor de fundo** — Selecione sua cor de fundo conforme cores prévias ou escolha a cor que quiser se preferir.
- **Métricas detalhadas** — largura por linha, altura total (linespace), dimensões reais do widget e coordenada X calculada para centralização
- **Copiar coordenada X** — copia a coordenada X para a área de transferência;
- **Histórico compacto** — exibe os 2 últimos cálculos em tabela, armazenando até 50 internamente
- **Interface redimensionável** — layout responsivo para diversos tamanhos de tela (recomendável usar em tela cheia).

---

## 📸 Screenshot

> _Adicione aqui um screenshot da aplicação rodando._

---

## 🛠️ Requisitos

| Dependência | Versão mínima |
|---|---|
| Python | 3.10+ |
| customtkinter | 5.x |

Instale a dependência com:

```bash
pip install customtkinter
```

> `tkinter` já vem incluído na instalação padrão do Python para Windows e macOS. No Linux (Debian/Ubuntu):
> ```bash
> sudo apt install python3-tk
> ```

---

## 🚀 Como usar

```bash
git clone https://github.com/mattospedrof/calculadora-de-fontes.git
cd calculadora-de-fontes
pip install customtkinter
python main.py
```

---

## 🧭 Guia rápido

1. **Digite o texto** no campo superior
2. **Busque e selecione a fonte** na lista com scroll
3. **Defina tamanho e estilo**
4. **Informe a largura real do frame** onde o texto será exibido no seu projeto
5. **Escolha o alinhamento** desejado (esquerda / centro / direita)
6. Os resultados aparecem automaticamente — **largura, altura, coordenada X**
7. Clique em **Copiar X** para copiar a coordenada para o clipboard

---

## 📐 O que a ferramenta calcula?

Dado um texto, fonte, tamanho e largura de frame, a calculadora retorna:

```
Fonte   : Georgia — bold — 22pt
Linhas  : 2
  Linha 1: 70px  »  "Hello"
  Linha 2: 111px »  "World!!!"

Larg. máx. texto (tkFont): 111px
Altura total (linespace):  68px

Widget  w=104px  h=64px
Frame   w=300px
X centralizado  : 98px
─────────────────────────────
Dica: place(relx=0.5, anchor='center')
```

Isso permite usar no seu código tkinter:

```python
label.place(x=98, y=sua_posicao_y)
# ou simplesmente:
label.place(relx=0.5, anchor="center")
```

---

## 📁 Estrutura do projeto

```
calculadora-de-fontes/
└── main.py
└── README.md
└── LICENSE
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

1. Fork o repositório
2. Crie sua branch: `git checkout -b minha-feature`
3. Commit suas mudanças: `git commit -m 'feat: minha feature'`
4. Push: `git push origin minha-feature`
5. Abra um Pull Request

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.