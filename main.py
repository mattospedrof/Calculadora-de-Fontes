import customtkinter as ctk
import tkinter as tk
from tkinter import font as tkFont, colorchooser

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

HISTORICO_MAX  = 50
HISTORICO_SHOW = 2   # linhas visíveis no painel (além do cabeçalho)

SWATCHES = [
    "#1a1a2e", "#16213e", "#0f3460", "#0d1b2a",
    "#ffffff", "#f5f5f5", "#e0e0e0", "#aaaaaa",
    "#2b2b2b", "#1e1e1e", "#111111", "#000000",
    "#1e3a5f", "#3a1e1e", "#1e3a1e", "#3a3a1e",
    "#ff6b6b", "#ffd166", "#06d6a0", "#8338ec",
]

ALIGN_OPTIONS = {
    "◀  Esquerda": ("w",      "left"),
    "↔  Centro":   ("center", "center"),
    "▶  Direita":  ("e",      "right"),
}


# ─── FontPicker ────────────────────────────────────────────────────────────
class FontPicker(ctk.CTkFrame):
    def __init__(self, master, callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.callback      = callback
        self._selected     = ctk.StringVar(value="Georgia")
        self._todas_fontes = sorted(set(tkFont.families()))

        self._search_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, placeholder_text="Buscar fonte…",
                                  textvariable=self._search_var,
                                  font=("Segoe UI", 13))
        self.entry.pack(fill="x", padx=4, pady=(4, 2))
        self.entry.bind("<KeyRelease>", self._filtrar)

        self.lista = ctk.CTkScrollableFrame(self, height=120)
        self.lista.pack(fill="x", padx=4, pady=(0, 4))

        self._botoes = {}
        self._popular(self._todas_fontes)
        self._selecionar("Georgia", fire_callback=False)

    def _popular(self, fontes):
        for w in self.lista.winfo_children():
            w.destroy()
        self._botoes.clear()
        for f in fontes:
            btn = ctk.CTkButton(
                self.lista, text=f, height=26, anchor="w",
                fg_color="transparent", hover_color="#2a2d3e",
                font=("Courier New", 13),
                command=lambda name=f: self._selecionar(name),
            )
            btn.pack(fill="x", pady=1)
            self._botoes[f] = btn

    def _filtrar(self, *_):
        q = self._search_var.get().lower()
        self._popular([f for f in self._todas_fontes if q in f.lower()])

    def _selecionar(self, nome, fire_callback=True):
        for btn in self._botoes.values():
            btn.configure(fg_color="transparent")
        if nome in self._botoes:
            self._botoes[nome].configure(fg_color="#1f538d")
        self._selected.set(nome)
        self._search_var.set(nome)
        if fire_callback and self.callback:
            self.callback()

    def get(self):
        return self._selected.get()


# ─── ColorPicker ───────────────────────────────────────────────────────────
class ColorPicker(ctk.CTkFrame):
    def __init__(self, master, callback=None, initial="#1a1a2e", **kwargs):
        super().__init__(master, **kwargs)
        self.callback = callback
        self._cor     = initial

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=4, pady=(4, 2))

        grade = ctk.CTkFrame(top, fg_color="transparent")
        grade.pack(side="left")
        for i, cor in enumerate(SWATCHES):
            btn = tk.Button(grade, bg=cor, width=2, height=1, relief="flat",
                            cursor="hand2", bd=0, highlightthickness=2,
                            highlightbackground=cor, highlightcolor=cor,
                            activebackground=cor,
                            command=lambda c=cor: self._escolher(c))
            btn.grid(row=i // 5, column=i % 5, padx=2, pady=2)
            btn.bind("<Enter>", lambda e, b=btn, c=cor: b.config(highlightbackground="#ffffff"))
            btn.bind("<Leave>", lambda e, b=btn, c=cor: b.config(highlightbackground=c))

        ctk.CTkButton(top, text="＋ Mais\ncores", width=80, height=52,
                      command=self._mais_cores).pack(side="left", padx=(10, 0), anchor="n")

        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill="x", padx=4, pady=(2, 4))
        self.quadrado  = tk.Label(bottom, bg=self._cor, width=4, height=1, relief="solid")
        self.quadrado.pack(side="left", padx=(0, 8))
        self.label_hex = ctk.CTkLabel(bottom, text=self._cor, font=("Courier New", 13))
        self.label_hex.pack(side="left")

    def _escolher(self, cor):
        self._cor = cor
        self.quadrado.configure(bg=cor)
        self.label_hex.configure(text=cor)
        if self.callback:
            self.callback()

    def _mais_cores(self):
        cor = colorchooser.askcolor(color=self._cor, title="Escolher cor")[1]
        if cor:
            self._escolher(cor.upper())

    def get(self):
        return self._cor


class TextCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MTech - Calculadora de Fontes")
        self.geometry("1100x860+200")
        self.minsize(900, 700)
        self.resizable(True, True)

        self.historico  = []
        self.ultimo_x   = None
        self._alinhamento = ("center", "center")

        self._build_ui()
        self._bind_realtime()


    def _build_ui(self):
        LF = ("Segoe UI", 13, "bold")
        EF = ("Segoe UI", 13)

        self.grid_columnconfigure(0, weight=0, minsize=580)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        left_outer = ctk.CTkScrollableFrame(self, fg_color="transparent", width=460)
        left_outer.grid(row=0, column=0, sticky="nsew", padx=(14, 6), pady=14)
        left = left_outer

        ctk.CTkLabel(left, text="Texto: (Pule uma linha com a tecla Enter)", font=LF).pack(anchor="w")
        self.entrada_texto = ctk.CTkTextbox(left, height=160, font=EF)
        self.entrada_texto.pack(pady=(2, 10), fill="x")

        ctk.CTkLabel(left, text="Fonte:", font=LF).pack(anchor="w")
        self.font_picker = FontPicker(left, callback=self._on_change)
        self.font_picker.pack(pady=(2, 10), fill="x")

        row_ts = ctk.CTkFrame(left, fg_color="transparent")
        row_ts.pack(fill="x", pady=(0, 10))
        col_tam = ctk.CTkFrame(row_ts, fg_color="transparent")
        col_tam.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkLabel(col_tam, text="Tamanho (px):", font=LF).pack(anchor="w")
        self.entrada_tamanho = ctk.CTkEntry(col_tam, placeholder_text="ex: 18", font=EF)
        self.entrada_tamanho.pack(fill="x")
        col_est = ctk.CTkFrame(row_ts, fg_color="transparent")
        col_est.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(col_est, text="Estilo:", font=LF).pack(anchor="w")
        self.combo_estilo = ctk.CTkComboBox(
            col_est, values=["normal", "bold", "italic", "bold italic"],
            font=EF, command=self._on_change)
        self.combo_estilo.set("normal")
        self.combo_estilo.pack(fill="x")

        ctk.CTkLabel(left, text="Largura do frame (px):", font=LF).pack(anchor="w")
        self.entrada_largura = ctk.CTkEntry(left, placeholder_text="ex: 600", font=EF)
        self.entrada_largura.pack(pady=(2, 10), fill="x")

        ctk.CTkLabel(left, text="Alinhamento do texto:", font=LF).pack(anchor="w")
        align_frame = ctk.CTkFrame(left, fg_color="transparent")
        align_frame.pack(fill="x", pady=(2, 10))
        self._align_buttons = {}
        for label, (anchor, justify) in ALIGN_OPTIONS.items():
            btn = ctk.CTkButton(
                align_frame, text=label, font=EF, height=32,
                fg_color="#1f538d", hover_color="#144070",
                command=lambda lbl=label: self._set_align(lbl),
            )
            btn.pack(side="left", expand=True, fill="x", padx=2)
            self._align_buttons[label] = btn
        self._set_align("↔  Centro", fire=False)

        ctk.CTkLabel(left, text="Cor de fundo do preview:", font=LF).pack(anchor="w")
        self.color_picker = ColorPicker(left, callback=self._on_change, initial="#1a1a2e")
        self.color_picker.pack(pady=(2, 10), fill="x")

        btn_row = ctk.CTkFrame(left, fg_color="transparent")
        btn_row.pack(anchor="w", pady=8)
        ctk.CTkButton(btn_row, text="Copiar X", font=EF,
                      fg_color="#2d6a4f", hover_color="#1b4332",
                      width=140, height=30,
                      command=self.copiar_x).pack(side="left")

        self.resultado = ctk.CTkLabel(
            left, text="", justify="left", anchor="w",
            wraplength=430, font=("Courier New", 13))
        self.resultado.pack(pady=6, fill="x")

        right = ctk.CTkFrame(self, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=(0, 14), pady=14)
        right.grid_rowconfigure(1, weight=3)
        right.grid_rowconfigure(3, weight=1)
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(right, text="Pré-visualização:", font=LF).grid(
            row=0, column=0, sticky="w", pady=(0, 4))

        self.frame_preview = ctk.CTkFrame(right, fg_color="#1a1a2e")
        self.frame_preview.grid(row=1, column=0, sticky="nsew", pady=(0, 14))
        self.frame_preview.grid_propagate(False)
        self.label_preview = ctk.CTkLabel(
            self.frame_preview, text="", anchor="center", justify="center",
            wraplength=0)
        self.label_preview.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(right, text="Histórico de cálculos:", font=LF).grid(
            row=2, column=0, sticky="w", pady=(0, 4))

        self.tabela_hist = ctk.CTkTextbox(
            right, height=96, state="disabled", font=("Courier New", 12))
        self.tabela_hist.grid(row=3, column=0, sticky="nsew")

        ctk.CTkButton(
            right, text="Limpar histórico", font=EF,
            fg_color="#6b2737", hover_color="#4a1528", height=28,
            width=160,
            command=self._limpar_historico,
        ).grid(row=4, column=0, sticky="w", pady=(6, 0))


    def _set_align(self, label, fire=True):
        for lbl, btn in self._align_buttons.items():
            btn.configure(fg_color="#1f538d" if lbl == label else "#2b2d3a",
                          hover_color="#144070" if lbl == label else "#3a3d52")
        self._alinhamento = ALIGN_OPTIONS[label]
        if fire:
            self._on_change()


    def _bind_realtime(self):
        self.entrada_texto.bind("<KeyRelease>",   self._on_change)
        self.entrada_tamanho.bind("<KeyRelease>",  self._on_change)
        self.entrada_largura.bind("<KeyRelease>",  self._on_change)


    def _on_change(self, *_):
        self.calcular(silencioso=True)


    def calcular(self, silencioso=False):
        texto_raw = self.entrada_texto.get("1.0", "end").rstrip("\n")
        texto     = texto_raw.replace("\\n", "\n")

        fonte_nome        = self.font_picker.get()
        estilo            = self.combo_estilo.get()
        cor_fundo         = self.color_picker.get() or "#1a1a2e"
        anchor_val, just_val = self._alinhamento

        try:
            tamanho       = int(self.entrada_tamanho.get())
            largura_frame = int(self.entrada_largura.get())
        except ValueError:
            if not silencioso:
                self._set_resultado("⚠  Preencha tamanho e largura com números inteiros.")
            return

        if tamanho <= 0 or largura_frame <= 0:
            if not silencioso:
                self._set_resultado("⚠  Tamanho e largura precisam ser > 0.")
            return

        weight = "bold"   if "bold"   in estilo else "normal"
        slant  = "italic" if "italic" in estilo else "roman"

        fnt               = tkFont.Font(family=fonte_nome, size=tamanho,
                                        weight=weight, slant=slant)
        linhas            = texto.split("\n") if texto else [""]
        larguras_linhas   = [fnt.measure(ln) for ln in linhas]
        largura_max_texto = max(larguras_linhas)
        linespace         = fnt.metrics("linespace")
        altura_total      = linespace * len(linhas)

        self.frame_preview.configure(fg_color=cor_fundo)
        self.label_preview.configure(
            text=texto,
            font=(fonte_nome, tamanho, estilo),
            text_color="#ffffff",
            anchor=anchor_val,
            justify=just_val,
        )
        self.label_preview.update_idletasks()

        larg_widget = self.label_preview.winfo_reqwidth()
        alt_widget  = self.label_preview.winfo_reqheight()

        if anchor_val == "w":
            self.label_preview.place(relx=0.02, rely=0.5, anchor="w")
        elif anchor_val == "e":
            self.label_preview.place(relx=0.98, rely=0.5, anchor="e")
        else:
            self.label_preview.place(relx=0.5, rely=0.5, anchor="center")

        pos_x = max(0, int((largura_frame - larg_widget) / 2))
        self.ultimo_x = pos_x

        linhas_info = "\n".join(
            f"  Linha {i+1}: {w}px  »  \"{ln}\""
            for i, (ln, w) in enumerate(zip(linhas, larguras_linhas))
        )
        res = (
            f"Fonte  : {fonte_nome} — {estilo} — {tamanho}pt\n"
            f"Alinhamento: {next(k for k,v in ALIGN_OPTIONS.items() if v==(anchor_val,just_val))}\n"
            f"Linhas : {len(linhas)}\n"
            f"{linhas_info}\n\n"
            f"Larg. máx. texto (tkFont): {largura_max_texto}px\n"
            f"Altura total (linespace):  {altura_total}px\n\n"
            f"Widget  w={larg_widget}px  h={alt_widget}px\n"
            f"Frame   w={largura_frame}px\n"
            f"X centralizado  : {pos_x}px\n"
            f"─────────────────────────────\n"
            f"Dica: place(relx=0.5, anchor='center')"
        )
        self._set_resultado(res)
        self._resultado_base = res

        self._add_historico({
            "texto":    texto.replace("\n", "↵"),
            "fonte":    fonte_nome,
            "tamanho":  tamanho,
            "estilo":   estilo,
            "align":    anchor_val,
            "frame_w":  largura_frame,
            "x":        pos_x,
            "larg_txt": largura_max_texto,
        })

    def _set_resultado(self, texto):
        self.resultado.configure(text=texto)


    def _add_historico(self, entrada):
        if self.historico and self.historico[-1] == entrada:
            return
        self.historico.append(entrada)
        if len(self.historico) > HISTORICO_MAX:
            self.historico.pop(0)
        self._renderizar_historico()


    def _renderizar_historico(self):
        self.tabela_hist.configure(state="normal")
        self.tabela_hist.delete("1.0", "end")
        cab = f"{'#':<3} {'Texto':<14} {'Fonte':<13} {'Tam':>3} {'Estilo':<11} {'Alin':<7} {'Frame':>5} {'X':>5} {'Larg':>5}\n"
        sep = "─" * 76 + "\n"
        self.tabela_hist.insert("end", cab)
        self.tabela_hist.insert("end", sep)
        recentes = list(reversed(self.historico))[:HISTORICO_SHOW]
        for i, h in enumerate(recentes, 1):
            txt_c  = (h["texto"][:12] + "…") if len(h["texto"]) > 13 else h["texto"]
            fnt_c  = (h["fonte"][:11] + "…") if len(h["fonte"]) > 12 else h["fonte"]
            alin_c = h.get("align", "c")[:6]
            linha  = (
                f"{i:<3} {txt_c:<14} {fnt_c:<13} "
                f"{h['tamanho']:>3} {h['estilo']:<11} {alin_c:<7} "
                f"{h['frame_w']:>5} {h['x']:>5} {h['larg_txt']:>5}\n"
            )
            self.tabela_hist.insert("end", linha)
        self.tabela_hist.configure(state="disabled")
        self.tabela_hist.see("1.0")


    def _limpar_historico(self):
        self.historico.clear()
        self.tabela_hist.configure(state="normal")
        self.tabela_hist.delete("1.0", "end")
        self.tabela_hist.configure(state="disabled")


    def copiar_x(self):
        if self.ultimo_x is None:
            return
        self.clipboard_clear()
        self.clipboard_append(str(self.ultimo_x))
        self._resultado_base = self.resultado.cget("text")
        self._set_resultado(self._resultado_base + f"\n\n✅ X={self.ultimo_x} copiado!")
        
        if hasattr(self, "_copy_timer") and self._copy_timer:
            self.after_cancel(self._copy_timer)
        self._copy_timer = self.after(5000, self._limpar_msg_copia)


    def _limpar_msg_copia(self):
        self._set_resultado(getattr(self, "_resultado_base", ""))
        self._copy_timer = None


if __name__ == "__main__":
    app = TextCalculator()
    app.mainloop()