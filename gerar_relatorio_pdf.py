# -*- coding: utf-8 -*-
"""
Gerador do Relatório em PDF – Trabalho 2 de Eletromagnetismo (FEELT31405)
Gera os diagramas auxiliares (esquema do núcleo e fluxograma) e compila o
arquivo T2_EM_ARTHUR_LUIS.pdf usando ReportLab.

Dependências:
  - matplotlib
  - reportlab
"""

import os
import tempfile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether
)

PASTA_TRABALHO = os.path.dirname(os.path.abspath(__file__))
PDF_SAIDA = os.path.join(PASTA_TRABALHO, "T2_EM_ARTHUR_LUIS.pdf")

# Registra Times New Roman do Windows para suporte completo a Unicode (μ, Φ, ℓ, ≥, ≤, ×)
pdfmetrics.registerFont(TTFont("TNR", r"C:\Windows\Fonts\times.ttf"))
pdfmetrics.registerFont(TTFont("TNR-Bold", r"C:\Windows\Fonts\timesbd.ttf"))
pdfmetrics.registerFont(TTFont("TNR-Italic", r"C:\Windows\Fonts\timesi.ttf"))
pdfmetrics.registerFont(TTFont("TNR-BoldItalic", r"C:\Windows\Fonts\timesbi.ttf"))
pdfmetrics.registerFontFamily(
    "TNR", normal="TNR", bold="TNR-Bold", italic="TNR-Italic", boldItalic="TNR-BoldItalic"
)


def gerar_esquema_nucleo(pasta_tmp: str) -> str:
    """Gera o diagrama do circuito magnético com cotas (Figura 1)."""
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    outer = patches.Rectangle((1.2, 0.8), 4.6, 3.4, linewidth=1.8,
                              edgecolor="#1f4e79", facecolor="#dce6f1")
    inner = patches.Rectangle((2.1, 1.6), 2.8, 1.8, linewidth=1.5,
                              edgecolor="#1f4e79", facecolor="white")
    ax.add_patch(outer)
    ax.add_patch(inner)

    gap = patches.Rectangle((4.88, 2.25), 0.94, 0.50, linewidth=1.2,
                            edgecolor="white", facecolor="white", zorder=3)
    ax.add_patch(gap)
    ax.plot([4.9, 5.8], [2.25, 2.25], color="#1f4e79", lw=1.6, zorder=4)
    ax.plot([4.9, 5.8], [2.75, 2.75], color="#1f4e79", lw=1.6, zorder=4)

    for y_coil in [1.65, 2.05, 2.45, 2.85, 3.25]:
        coil = patches.FancyBboxPatch((0.95, y_coil), 1.4, 0.22,
                                      boxstyle="round,pad=0.03",
                                      facecolor="#f4b183", edgecolor="#833c0c",
                                      linewidth=1.2, zorder=5)
        ax.add_patch(coil)

    ax.annotate("I = 0,40 A\n(N espiras)", xy=(1.0, 3.35), xytext=(0.1, 4.15),
                fontsize=9, fontweight="bold", color="#833c0c",
                arrowprops=dict(arrowstyle="->", color="#833c0c", lw=1.4))

    ax.plot([1.65, 5.35, 5.35, 1.65, 1.65], [1.2, 1.2, 3.8, 3.8, 1.2],
            color="#c00000", ls="--", lw=1.3, zorder=6)

    ax.annotate("", xy=(3.9, 3.8), xytext=(3.1, 3.8),
                arrowprops=dict(arrowstyle="->", color="#c00000", lw=2.0), zorder=7)
    ax.text(3.5, 3.95, "Fluxo Φ", color="#c00000", fontsize=9.5,
            fontweight="bold", ha="center")

    ax.annotate("", xy=(6.05, 2.25), xytext=(6.05, 2.75),
                arrowprops=dict(arrowstyle="<->", color="#000000", lw=1.2))
    ax.text(6.2, 2.5, "Entreferro g\n(g_nom = 0,10 mm;\nΔg = +0,15 mm)",
            fontsize=8.5, va="center")

    ax.text(3.5, 0.42, "Percurso médio no núcleo: ℓ_fe = 0,24 m",
            fontsize=9, ha="center", fontweight="bold", color="#1f4e79")

    sec = patches.Rectangle((8.0, 1.8), 1.4, 1.4, linewidth=1.6,
                            edgecolor="#1f4e79", facecolor="#dce6f1")
    ax.add_patch(sec)
    ax.text(8.7, 3.45, "Seção Transversal", fontsize=9.5, fontweight="bold",
            ha="center", color="#1f4e79")
    ax.text(8.7, 2.5, "A = 3,00 cm²\n= 3,00×10⁻⁴ m²", fontsize=8.5,
            ha="center", va="center")
    ax.text(8.7, 1.4, "B = Φ / A\n(seção uniforme)", fontsize=8.5,
            ha="center", va="top", color="#333333")

    plt.tight_layout()
    out = os.path.join(pasta_tmp, "fig_nucleo.png")
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out


def gerar_fluxograma(pasta_tmp: str) -> str:
    """Gera o fluxograma do algoritmo implementado (Figura 2)."""
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    caixas = [
        (5.0, 9.2, 5.6, 0.9, "Início: Definir constantes (μ0, ℓ_fe, A, I, R1, R2) e materiais", "#dce6f1"),
        (5.0, 7.8, 5.6, 0.9, "Passo 3: Funções do modelo (R_fe, R_g, B, Φ, L, W) e validação\n(caso g=0, Lei de Ampère e W = W_fe + W_g)", "#e2efda"),
        (5.0, 6.3, 5.6, 0.9, "Passo 4: Analisar configuração inicial (Ferrite, N=200)\nem g=0,10 mm e g=0,25 mm → Gerar gráfico G1", "#fff2cc"),
        (5.0, 4.8, 5.6, 0.9, "Passo 5: Estimar folga equivalente g_eq para L=42,0 mH\ne comparar energias nominal vs. estimada", "#fce4d6"),
        (5.0, 3.3, 5.6, 0.9, "Passo 6: Varredura (Material × N × g_nom) em laços simples;\nfiltrar R1, R2 e validade linear simultaneamente → Gerar G2", "#e2efda"),
        (5.0, 1.8, 5.6, 0.9, "Selecionar menor N válido (Aço-silício, N=220, g_nom=0,05 mm)\nComparar Inicial vs. Final → Gerar G3", "#dce6f1"),
        (5.0, 0.5, 3.0, 0.7, "Fim: Imprimir saídas 'Passo N (item)'", "#d9d9d9"),
    ]

    for x, y, w, h, texto, cor in caixas:
        rect = patches.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                      boxstyle="round,pad=0.08",
                                      facecolor=cor, edgecolor="#333333", lw=1.2)
        ax.add_patch(rect)
        ax.text(x, y, texto, ha="center", va="center", fontsize=8.5)

    for i in range(len(caixas) - 1):
        y_top = caixas[i][1] - caixas[i][3] / 2 - 0.06
        y_bot = caixas[i + 1][1] + caixas[i + 1][3] / 2 + 0.06
        ax.annotate("", xy=(5.0, y_bot), xytext=(5.0, y_top),
                    arrowprops=dict(arrowstyle="->", lw=1.3, color="#333333"))

    plt.tight_layout()
    out = os.path.join(pasta_tmp, "fig_fluxograma.png")
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out


def desenhar_cabecalho_rodape(canvas, doc):
    """Numera páginas a partir da página 2 (conteúdo), omitindo da capa."""
    page_num = canvas.getPageNumber()
    if page_num == 1:
        return
    canvas.saveState()
    canvas.setFont("TNR", 10)
    canvas.setFillColor(colors.HexColor("#444444"))
    canvas.drawRightString(A4[0] - 2.5 * cm, 1.5 * cm, f"Página {page_num - 1}")
    canvas.drawString(2.5 * cm, A4[1] - 1.7 * cm,
                      "FEELT31405 – Eletromagnetismo | Trabalho 2 (2026-2)")
    canvas.restoreState()


def criar_estilos():
    base = getSampleStyleSheet()
    return {
        "CapaInst": ParagraphStyle(
            "CapaInst", parent=base["Normal"], fontName="TNR-Bold", fontSize=13,
            leading=18, alignment=TA_CENTER
        ),
        "CapaTitulo": ParagraphStyle(
            "CapaTitulo", parent=base["Normal"], fontName="TNR-Bold", fontSize=16,
            leading=22, alignment=TA_CENTER, spaceBefore=24, spaceAfter=18
        ),
        "CapaInfo": ParagraphStyle(
            "CapaInfo", parent=base["Normal"], fontName="TNR", fontSize=12,
            leading=18, alignment=TA_CENTER
        ),
        "H1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontName="TNR-Bold", fontSize=13,
            leading=18, spaceBefore=14, spaceAfter=6, alignment=TA_LEFT
        ),
        "H2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="TNR-Bold", fontSize=12,
            leading=17, spaceBefore=10, spaceAfter=4, alignment=TA_LEFT
        ),
        "Corpo": ParagraphStyle(
            "Corpo", parent=base["Normal"], fontName="TNR", fontSize=12,
            leading=18, alignment=TA_JUSTIFY, spaceAfter=6
        ),
        "Equacao": ParagraphStyle(
            "Equacao", parent=base["Normal"], fontName="TNR-Italic", fontSize=11.5,
            leading=16, alignment=TA_CENTER, spaceBefore=4, spaceAfter=6
        ),
        "Legenda": ParagraphStyle(
            "Legenda", parent=base["Normal"], fontName="TNR-Italic", fontSize=10,
            leading=12, alignment=TA_CENTER, spaceBefore=3, spaceAfter=8
        ),
        "TabelaCel": ParagraphStyle(
            "TabelaCel", parent=base["Normal"], fontName="TNR", fontSize=9.5,
            leading=12, alignment=TA_LEFT
        ),
        "TabelaCab": ParagraphStyle(
            "TabelaCab", parent=base["Normal"], fontName="TNR-Bold", fontSize=9.5,
            leading=12, alignment=TA_CENTER, textColor=colors.white
        ),
        "Ref": ParagraphStyle(
            "Ref", parent=base["Normal"], fontName="TNR", fontSize=11,
            leading=15, alignment=TA_LEFT, spaceAfter=5
        ),
    }


def fazer_tabela(dados, larguras, estilos):
    linhas = []
    for idx, row in enumerate(dados):
        st = estilos["TabelaCab"] if idx == 0 else estilos["TabelaCel"]
        linhas.append([Paragraph(str(c), st) for c in row])
    t = Table(linhas, colWidths=larguras, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f6fa")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def construir_pdf():
    st = criar_estilos()
    doc = SimpleDocTemplate(
        PDF_SAIDA, pagesize=A4,
        leftMargin=2.5 * cm, rightMargin=2.5 * cm,
        topMargin=2.5 * cm, bottomMargin=2.5 * cm,
        title="Trabalho 2 - Análise do Núcleo Magnético de um Transformador de Isolamento",
        author="Arthur Montes Cuoco; Luis Gustavo Oliveira Sena"
    )
    W_UTIL = A4[0] - 5.0 * cm

    with tempfile.TemporaryDirectory() as pasta_tmp:
        img_nuc = gerar_esquema_nucleo(pasta_tmp)
        img_flux = gerar_fluxograma(pasta_tmp)
        story = []

        # CAPA
        story.append(Paragraph("UNIVERSIDADE FEDERAL DE UBERLÂNDIA", st["CapaInst"]))
        story.append(Paragraph("FACULDADE DE ENGENHARIA ELÉTRICA (FEELT)", st["CapaInst"]))
        story.append(Spacer(1, 1.2 * cm))
        story.append(Paragraph("Disciplina: Eletromagnetismo (FEELT31405)", st["CapaInfo"]))
        story.append(Paragraph("Professor: Luiz Arthur Tarralo Passatuto", st["CapaInfo"]))
        story.append(Paragraph("Turma: FEELT31411 &nbsp;|&nbsp; Semestre: 2026-2", st["CapaInfo"]))
        story.append(Spacer(1, 2.5 * cm))
        story.append(Paragraph(
            "Trabalho 2<br/>Análise do Núcleo Magnético de um Transformador de Isolamento",
            st["CapaTitulo"]
        ))
        story.append(Spacer(1, 2.5 * cm))
        story.append(Paragraph("<b>Integrantes:</b>", st["CapaInfo"]))
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph(
            "Arthur Montes Cuoco – Matrícula: 12411EEL028<br/>"
            "Luis Gustavo Oliveira Sena – Matrícula: 12211FIS210",
            st["CapaInfo"]
        ))
        story.append(Spacer(1, 4.0 * cm))
        story.append(Paragraph("Uberlândia – MG<br/>08/12/2026", st["CapaInfo"]))
        story.append(PageBreak())

        # 1 INTRODUÇÃO
        story.append(Paragraph("1 Introdução", st["H1"]))
        story.append(Paragraph(
            "Transformadores de isolamento são amplamente empregados em fontes de alimentação "
            "de equipamentos industriais, eletrônicos e de comunicação para prover isolação "
            "galvânica e acoplamento magnético entre circuitos (FITZGERALD; KINGSLEY; UMANS, 2014). "
            "O núcleo ferromagnético concentra o fluxo magnético que enlaza os enrolamentos; contudo, "
            "suas propriedades magnéticas e a presença de pequenas folgas mecânicas (entreferros) "
            "entre as peças afetam diretamente a magnetização, a indutância e o armazenamento de energia. "
            "Antes de avaliar o dispositivo em regime de corrente alternada (CA), o comportamento "
            "magnético do núcleo pode ser caracterizado por meio de um ensaio magnetostático em "
            "corrente contínua (CC).",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "Este trabalho tem como objetivos: (i) deduzir o modelo analítico de circuito magnético "
            "em série com entreferro; (ii) formular previsões físicas antes da simulação; "
            "(iii) implementar e validar um programa em Python que automatize os cálculos e gere "
            "os gráficos obrigatórios; (iv) analisar a configuração inicial de ferrite e investigar "
            "uma anomalia experimental de indutância; e (v) selecionar uma combinação de material, "
            "número de espiras e folga nominal que satisfaça simultaneamente os requisitos de "
            "indutância mínima (R1) e limite de densidade de fluxo (R2) nas condições nominal e "
            "com tolerância de montagem.",
            st["Corpo"]
        ))

        story.append(KeepTogether([
            Image(img_nuc, width=W_UTIL * 0.96, height=W_UTIL * 0.47),
            Paragraph(
                "Figura 1 – Esquema do núcleo magnético de uma só malha com bobina de ensaio, "
                "entreferro g, percurso médio ℓ<sub>fe</sub> = 0,24 m e seção transversal A = 3,00 cm² "
                "(fora de escala).",
                st["Legenda"]
            )
        ]))

        story.append(Paragraph(
            "A Tabela 1 resume os parâmetros geométricos, materiais hipotéticos de referência e "
            "requisitos de projeto adotados (PASSATUTO, 2026). Assumem-se como <b>hipóteses de "
            "trabalho</b>: regime magnetostático; materiais lineares, homogêneos e isotrópicos "
            "enquanto o limite de B não for ultrapassado; permeabilidade do ar igual a μ<sub>0</sub>; "
            "seção transversal constante (A = 3,00×10<sup>−4</sup> m²); campo uniforme no núcleo e no "
            "entreferro; e ausência de dispersão, espraiamento, histerese ou correntes parasitas. "
            "Resultados que excedam o limite de B de cada material constituem extrapolações inválidas "
            "do modelo linear.",
            st["Corpo"]
        ))

        tab1 = [
            ["Grandeza", "Valor / Especificação"],
            ["Comprimento médio do núcleo (ℓ<sub>fe</sub>)", "0,24 m"],
            ["Área transversal (A)", "3,00 cm² = 3,00×10<sup>−4</sup> m²"],
            ["Bobina e corrente de ensaio", "N<sub>inicial</sub> = 200 espiras; I = 0,40 A (contínua)"],
            ["Entreferro e tolerância", "g<sub>inicial</sub> = 0,10 mm; acréscimo Δg = +0,15 mm"],
            ["Materiais (μ<sub>r</sub>; limite de B)", "Ferrite: 2200; 0,35 T | Aço-silício: 1500; 1,40 T | Pó de ferro: 125; 0,90 T"],
            ["Permeabilidade do vácuo (μ<sub>0</sub>)", "4π×10<sup>−7</sup> H/m"],
            ["Requisitos de projeto", "R1: L ≥ 50,0 mH | R2: B ≤ 80% do limite do material"],
        ]
        story.append(KeepTogether([
            Paragraph("Tabela 1 – Dados geométricos, materiais e requisitos do problema.", st["Legenda"]),
            fazer_tabela(tab1, [W_UTIL * 0.40, W_UTIL * 0.60], st),
            Spacer(1, 0.3 * cm)
        ]))

        # 2 DESENVOLVIMENTO
        story.append(Paragraph("2 Desenvolvimento", st["H1"]))
        story.append(Paragraph(
            "O Quadro-Resumo a seguir (Tabela 2) sintetiza os principais resultados obtidos em "
            "cada etapa do roteiro e indica as figuras e tabelas correspondentes.",
            st["Corpo"]
        ))

        tab2 = [
            ["Passo", "Resultado Principal", "Figura / Tabela"],
            ["Passo 1 – Modelagem física", "Dedução de R<sub>fe</sub>, R<sub>g</sub>, Φ, B, L, W<sub>fe</sub> e W<sub>g</sub>.", "Eq. (1)–(5), Fig. 1"],
            ["Passo 2 – Previsões", "Tendências de Φ, B e L com g, N e μ<sub>r</sub> antes da simulação.", "Seção 2.2"],
            ["Passo 3 – Implementação e validação", "Resíduos nulos (~0 para g=0 e Ampère; 1,73×10<sup>−18</sup> J em W).", "Fig. 2, Tabela 3"],
            ["Passo 4 – Configuração inicial", "Nominal: L = 72,1200 mH, B = 0,4808 T (> 0,35 T, inválido). Com Δg: L = 41,9939 mH.", "Fig. 3 (G1), Tabela 4"],
            ["Passo 5 – Anomalia na montagem", "Para L = 42,0 mH, g<sub>eq</sub> = 0,2499 mm e B = 0,2800 T (69,62% de W no entreferro).", "Tabela 5"],
            ["Passo 6 – Decisão de projeto", "Aço-silício, N = 220 (+20 espiras), g<sub>nom</sub> = 0,05 mm; L<sub>tol</sub> = 50,6844 mH.", "Fig. 4 (G2), Fig. 5 (G3), Tab. 6"],
        ]
        story.append(KeepTogether([
            Paragraph("Tabela 2 – Quadro-resumo dos resultados do desenvolvimento.", st["Legenda"]),
            fazer_tabela(tab2, [W_UTIL * 0.27, W_UTIL * 0.51, W_UTIL * 0.22], st),
            Spacer(1, 0.3 * cm)
        ]))

        # 2.1 Passo 1
        story.append(Paragraph("2.1 Passo 1 – Modelagem física (à mão, antes de programar)", st["H2"]))
        story.append(Paragraph(
            "<b>(a)</b> O circuito magnético é ilustrado na Figura 1, identificando a bobina de N "
            "espiras com corrente contínua I, o sentido do fluxo Φ pela regra da mão direita, o "
            "percurso médio ℓ<sub>fe</sub> no núcleo e o entreferro de comprimento g. Pode-se adotar "
            "o mesmo fluxo Φ nas duas regiões devido à lei de Gauss para o magnetismo "
            "(∫<sub>S</sub> <b>B</b>·d<b>S</b> = 0) combinada às hipóteses de ausência de fluxo de dispersão e de "
            "espraiamento na junta, além da seção transversal constante A (SADIKU, 2012).",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "<b>(b)</b> Aplicando a Lei Circuital de Ampère ao longo do percurso médio fechado "
            "(ℓ<sub>fe</sub> + g) e utilizando a relação constitutiva linear B = μH:",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "H<sub>fe</sub> · ℓ<sub>fe</sub> + H<sub>g</sub> · g = N·I &nbsp;&nbsp;→&nbsp;&nbsp; "
            "H<sub>fe</sub> = B / (μ<sub>0</sub> μ<sub>r</sub>) &nbsp;&nbsp;e&nbsp;&nbsp; "
            "H<sub>g</sub> = B / μ<sub>0</sub> &nbsp;&nbsp;&nbsp;&nbsp;(1)",
            st["Equacao"]
        ))
        story.append(Paragraph(
            "Como B = Φ / A, obtêm-se as relutâncias parciais do núcleo (R<sub>fe</sub>) e do "
            "entreferro (R<sub>g</sub>) em série, bem como o fluxo magnético Φ:",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "R<sub>fe</sub> = ℓ<sub>fe</sub> / (μ<sub>0</sub> μ<sub>r</sub> A) &nbsp;&nbsp;[H<sup>−1</sup>], &nbsp;&nbsp;&nbsp; "
            "R<sub>g</sub> = g / (μ<sub>0</sub> A) &nbsp;&nbsp;[H<sup>−1</sup>], &nbsp;&nbsp;&nbsp; "
            "R = R<sub>fe</sub> + R<sub>g</sub> &nbsp;&nbsp;&nbsp;&nbsp;(2)",
            st["Equacao"]
        ))
        story.append(Paragraph(
            "Φ = (N · I) / (R<sub>fe</sub> + R<sub>g</sub>) = (N · I · μ<sub>0</sub> · A) / "
            "(ℓ<sub>fe</sub>/μ<sub>r</sub> + g) &nbsp;&nbsp;[Wb] &nbsp;&nbsp;&nbsp;&nbsp;(3)",
            st["Equacao"]
        ))
        story.append(Paragraph(
            "<b>(c)</b> A indutância L e a energia magnética total W, bem como as parcelas armazenadas "
            "no núcleo (W<sub>fe</sub>) e no entreferro (W<sub>g</sub>), são dadas por:",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "L = N·Φ / I = N² / (R<sub>fe</sub> + R<sub>g</sub>) &nbsp;&nbsp;[H], &nbsp;&nbsp;&nbsp; "
            "W = ½ · L · I² &nbsp;&nbsp;[J] &nbsp;&nbsp;&nbsp;&nbsp;(4)",
            st["Equacao"]
        ))
        story.append(Paragraph(
            "W<sub>fe</sub> = ½ · R<sub>fe</sub> · Φ² = (B² / (2 μ<sub>0</sub> μ<sub>r</sub>)) · (A · ℓ<sub>fe</sub>), &nbsp;&nbsp;&nbsp; "
            "W<sub>g</sub> = ½ · R<sub>g</sub> · Φ² = (B² / (2 μ<sub>0</sub>)) · (A · g) &nbsp;&nbsp;&nbsp;&nbsp;(5)",
            st["Equacao"]
        ))
        story.append(Paragraph(
            "Essas expressões são válidas exclusivamente em regime magnetostático, na região linear "
            "(B ≤ B<sub>limite</sub>) e sob ausência de saturação, histerese, dispersão e espraiamento.",
            st["Corpo"]
        ))

        # 2.2 Passo 2
        story.append(Paragraph("2.2 Passo 2 – Previsões (antes de rodar o código)", st["H2"]))
        story.append(Paragraph(
            "<b>(a) Efeito de aumentar g:</b> Como R<sub>g</sub> = g/(μ<sub>0</sub>A) cresce "
            "linearmente com g e o entreferro tem permeabilidade μ<sub>0</sub> (muito menor que "
            "μ<sub>0</sub>μ<sub>r</sub> do núcleo), aumentar g eleva fortemente a relutância total R. "
            "Para força magnetomotriz NI fixa, Φ e L reduzem-se de forma hiperbólica (proporcional a 1/(ℓ<sub>fe</sub>/μ<sub>r</sub> + g)).",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "<b>(b) Efeito de aumentar N (com I fixo):</b> Como Φ é proporcional a N e B = Φ/A, o campo B cresce "
            "linearmente com N. Já a indutância L = N²/R cresce quadraticamente com N, tornando o "
            "aumento de espiras um recurso eficaz para elevar L, embora aproxime B do limite do material.",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "<b>(c) Influência de μ<sub>r</sub> e do limite de B:</b> Uma permeabilidade relativa "
            "μ<sub>r</sub> maior reduz R<sub>fe</sub>, elevando Φ, L e B para um mesmo conjunto "
            "(N, I, g). Todavia, maior μ<sub>r</sub> não garante configuração válida porque, se o "
            "material possuir limite de B baixo (caso da ferrite, 0,35 T), o aumento de Φ pode fazer "
            "com que B ultrapasse 80% do limite (R2) ou até o limite de validade linear.",
            st["Corpo"]
        ))

        # 2.3 Passo 3
        story.append(Paragraph("2.3 Passo 3 – Implementação e validação", st["H2"]))
        story.append(Paragraph(
            "O programa foi estruturado em Python com funções dedicadas por passo: "
            "<b>(a)</b> <i>calcular_relutancias_e_B</i> retorna R<sub>fe</sub>, R<sub>g</sub>, "
            "R<sub>total</sub> e B; <b>(b)</b> <i>calcular_fluxo_indutancia_energia</i> calcula "
            "Φ, L, W, W<sub>fe</sub> e W<sub>g</sub>; e <b>(c)</b> <i>verificar_limites</i> avalia "
            "R1 (L ≥ 50,0 mH), R2 (B ≤ 0,80·B<sub>lim</sub>) e a validade linear (B ≤ B<sub>lim</sub>). "
            "Utilizou-se a biblioteca <b>NumPy</b> para operações vetoriais precisas sobre arranjos "
            "de entreferro e constante π, e a biblioteca <b>Matplotlib</b> para gerar os gráficos "
            "padronizados G1, G2 e G3 em alta resolução. A Figura 2 apresenta o fluxograma do algoritmo.",
            st["Corpo"]
        ))

        story.append(KeepTogether([
            Image(img_flux, width=W_UTIL * 0.86, height=W_UTIL * 0.54),
            Paragraph("Figura 2 – Fluxograma do algoritmo implementado para os Passos 3 a 6.", st["Legenda"])
        ]))

        story.append(Paragraph(
            "A validação numérica (Tabela 3) confrontou o modelo com a expressão analítica sem "
            "entreferro (g = 0, aço-silício, N = 200) e verificou a Lei de Ampère e a conservação "
            "de energia (ferrite, g = 0,10 mm, N = 200). Os resíduos encontram-se na ordem da "
            "precisão de ponto flutuante (≤ 10<sup>−14</sup> %).",
            st["Corpo"]
        ))

        tab3 = [
            ["Caso de Validação", "Valor Calculado", "Valor de Referência", "Resíduo Absoluto", "Erro Relativo"],
            ["g = 0 (Aço-silício, N=200)", "B = 0,628319 T", "μ<sub>0</sub>μ<sub>r</sub>NI/ℓ<sub>fe</sub> = 0,628319 T", "0,00×10<sup>0</sup> T", "0,00 %"],
            ["Lei de Ampère (Ferrite, g=0,10 mm)", "H<sub>fe</sub>ℓ<sub>fe</sub>+H<sub>g</sub>g = 80,0000 A·esp", "NI = 80,0000 A·esp", "0,00×10<sup>0</sup> A·esp", "0,00 %"],
            ["Energia Total (Ferrite, g=0,10 mm)", "W<sub>fe</sub>+W<sub>g</sub> = 5,7696 mJ", "½LI² = 5,7696 mJ", "1,73×10<sup>−18</sup> J", "3,01×10<sup>−14</sup> %"],
        ]
        story.append(KeepTogether([
            Paragraph("Tabela 3 – Resíduos e erros relativos da validação numérica do Passo 3.", st["Legenda"]),
            fazer_tabela(tab3, [W_UTIL*0.26, W_UTIL*0.22, W_UTIL*0.22, W_UTIL*0.16, W_UTIL*0.14], st),
            Spacer(1, 0.3 * cm)
        ]))

        # 2.4 Passo 4
        story.append(Paragraph("2.4 Passo 4 – Análise da configuração inicial", st["H2"]))
        story.append(Paragraph(
            "<b>(a)</b> Para a configuração inicial (ferrite, μ<sub>r</sub> = 2200, N = 200, "
            "g = 0,10 mm, I = 0,40 A), os valores obtidos estão reunidos na Tabela 4. As densidades "
            "de energia calculadas foram w<sub>fe</sub> = B²/(2μ<sub>0</sub>μ<sub>r</sub>) = "
            "41,8087 J/m³ e w<sub>g</sub> = B²/(2μ<sub>0</sub>) = 91 979,1815 J/m³. Multiplicando "
            "pelos respectivos volumes (V<sub>fe</sub> = 7,20×10<sup>−5</sup> m³ e V<sub>g</sub> = "
            "3,00×10<sup>−8</sup> m³), obtêm-se W<sub>fe</sub> = 3,0102 mJ e W<sub>g</sub> = "
            "2,7594 mJ, confirmando exatamente as parcelas obtidas via relutâncias.",
            st["Corpo"]
        ))

        tab4 = [
            ["Grandeza", "Nominal (g = 0,10 mm)", "Com Tolerância (g = 0,25 mm)"],
            ["R<sub>fe</sub> / R<sub>g</sub> (H<sup>−1</sup>)", "2,8937×10<sup>5</sup> / 2,6526×10<sup>5</sup>", "2,8937×10<sup>5</sup> / 6,6315×10<sup>5</sup>"],
            ["Fluxo Φ (Wb)", "1,4424×10<sup>−4</sup>", "8,3988×10<sup>−5</sup>"],
            ["Densidade de fluxo B (T)", "<b>0,4808 (INVÁLIDO &gt; 0,35 T)</b>", "0,27996 (≤ 0,28 T; passa R2)"],
            ["Intensidades H<sub>fe</sub> / H<sub>g</sub> (A/m)", "173,9130 / 382 608,6957", "101,2706 / 222 785,2293"],
            ["Indutância L (mH)", "72,1200 (passa R1)", "<b>41,9939 (viola R1 &lt; 50 mH)</b>"],
            ["Energia total W (mJ)", "5,7696", "3,3595"],
            ["W<sub>fe</sub> (mJ) / W<sub>g</sub> (mJ)", "3,0102 (52,17%) / 2,7594 (47,83%)", "1,0206 (30,38%) / 2,3389 (69,62%)"],
        ]
        story.append(KeepTogether([
            Paragraph("Tabela 4 – Resultados da configuração inicial (Ferrite, N = 200) nas duas folgas.", st["Legenda"]),
            fazer_tabela(tab4, [W_UTIL * 0.34, W_UTIL * 0.33, W_UTIL * 0.33], st),
            Spacer(1, 0.3 * cm)
        ]))

        story.append(Paragraph(
            "<b>(b)</b> A Figura 3 (gráfico G1) exibe o comportamento de L e B em função de g "
            "entre 0,05 mm e 0,40 mm, com destaque para a folga nominal (0,10 mm), o limite R1 "
            "(50,0 mH), o limite R2 da ferrite (0,28 T) e o limite de validade linear (0,35 T).",
            st["Corpo"]
        ))
        img_g1 = os.path.join(PASTA_TRABALHO, "G1.png")
        story.append(KeepTogether([
            Image(img_g1, width=W_UTIL, height=W_UTIL * 0.41),
            Paragraph("Figura 3 (G1) – Indutância L e densidade de fluxo B versus entreferro g na configuração inicial.", st["Legenda"])
        ]))

        story.append(Paragraph(
            "<b>(c)</b> Com a folga acrescida da tolerância (g = 0,25 mm), a relutância do entreferro "
            "mais que dobra (de 2,6526×10<sup>5</sup> para 6,6315×10<sup>5</sup> H<sup>−1</sup>), "
            "reduzindo L para 41,9939 mH (violando R1) e B para 0,27996 T (aprovado em R2 por margem "
            "mínima de 0,00004 T). Como R<sub>g</sub> passa a dominar a relutância total e "
            "W<sub>g</sub>/W<sub>fe</sub> = R<sub>g</sub>/R<sub>fe</sub>, a fração de energia "
            "armazenada no entreferro sobe de 47,83% para 69,62%.",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "<b>(d)</b> Na condição nominal (g = 0,10 mm), o valor formal B = 0,4808 T ultrapassa o "
            "limite linear da ferrite (0,35 T). Esses resultados (assim como Φ = 1,4424×10<sup>−4</sup> Wb "
            "e L = 72,1200 mH decorrentes da mesma extrapolação) não representam operação real, pois "
            "acima do limite ocorre saturação magnética: μ<sub>r</sub> cai drasticamente e a relação "
            "B = μH deixa de ser linear.",
            st["Corpo"]
        ))

        # 2.5 Passo 5
        story.append(Paragraph("2.5 Passo 5 – Investigação de uma anomalia na montagem", st["H2"]))
        story.append(Paragraph(
            "<b>(a)</b> Isolando g em L = N² / (ℓ<sub>fe</sub>/(μ<sub>0</sub>μ<sub>r</sub>A) + g/(μ<sub>0</sub>A)), "
            "obtém-se a expressão da folga equivalente sob μ<sub>r</sub> constante:",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "g = μ<sub>0</sub> · A · (N² / L) − (ℓ<sub>fe</sub> / μ<sub>r</sub>) &nbsp;&nbsp;[m] &nbsp;&nbsp;&nbsp;&nbsp;(6)",
            st["Equacao"]
        ))
        story.append(Paragraph(
            "<b>(b)</b> Para L = 42,0 mH, N = 200 e μ<sub>r</sub> = 2200, a Equação (6) fornece "
            "<b>g<sub>eq</sub> = 0,2499 mm</b>. Esse valor é 0,1499 mm maior que a folga nominal "
            "(0,10 mm), coincidindo praticamente com a condição nominal mais a tolerância máxima "
            "de montagem (0,10 + 0,15 = 0,25 mm).",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "<b>(c)</b> Para g<sub>eq</sub> = 0,2499 mm, obtém-se <b>B = 0,2800 T</b>, valor que "
            "respeita o limite de validade linear (0,35 T), ao contrário da condição nominal formal "
            "(B = 0,4808 T, inválida). A Tabela 5 compara as energias nas duas condições.",
            st["Corpo"]
        ))

        tab5 = [
            ["Condição", "B (T)", "W<sub>fe</sub> (mJ)", "W<sub>g</sub> (mJ)", "W<sub>total</sub> (mJ)", "Fração no Entreferro"],
            ["Nominal (g = 0,10 mm)", "<b>0,4808 (Inválido &gt; 0,35)</b>", "3,0102*", "2,7594*", "5,7696*", "47,83 %"],
            ["Estimada (g<sub>eq</sub> = 0,2499 mm)", "0,2800 (Válido)", "1,0209", "2,3391", "3,3600", "69,62 %"],
        ]
        story.append(KeepTogether([
            Paragraph("Tabela 5 – Comparação energética entre condição nominal e folga estimada (*valores extrapolados fora da região linear).", st["Legenda"]),
            fazer_tabela(tab5, [W_UTIL*0.24, W_UTIL*0.20, W_UTIL*0.13, W_UTIL*0.13, W_UTIL*0.14, W_UTIL*0.16], st),
            Spacer(1, 0.3 * cm)
        ]))

        story.append(Paragraph(
            "<b>(d)</b> Uma medida isolada de indutância incremental (42,0 mH) não prova a existência "
            "de uma folga de 0,25 mm porque L depende de múltiplos parâmetros acoplados (N, μ<sub>r</sub>, "
            "A, ℓ<sub>fe</sub>, g). Duas outras causas físicas possíveis para a queda de L são: "
            "(1) redução efetiva da permeabilidade diferencial μ<sub>r</sub> devido à saturação "
            "parcial na polarização de 0,40 A ou a tensões mecânicas no núcleo; e (2) erro no número "
            "de espiras efetivas ou espira em curto parcial. Como dado adicional necessário, deve-se "
            "medir diretamente a folga mecânica com calibre de lâminas ou levantar a curva B–H / L(I) "
            "em função da corrente CC de polarização.",
            st["Corpo"]
        ))

        # 2.6 Passo 6
        story.append(Paragraph("2.6 Passo 6 – Decisão de projeto: material e enrolamento", st["H2"]))
        story.append(Paragraph(
            "<b>(a)</b> Na configuração inicial (ferrite, N = 200), a condição nominal (0,10 mm) "
            "atende R1 (72,1200 mH ≥ 50 mH), mas viola R2 e a validade linear (0,4808 T &gt; 0,35 T). "
            "Já a condição com tolerância (0,25 mm) atende R2 (0,27996 T ≤ 0,28 T), mas viola R1 "
            "(41,9939 mH &lt; 50 mH). Logo, a configuração inicial é reprovada.",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "<b>(b)</b> Realizou-se a varredura com laços simples para os 3 materiais, N = {120, 140, "
            "..., 260} e g<sub>nom</sub> = {0,05; 0,10; ...; 0,25} mm, exigindo R1, R2 e validade "
            "linear simultaneamente em g<sub>nom</sub> e em g<sub>nom</sub> + 0,15 mm. A <b>Ferrite</b> "
            "e o <b>Pó de ferro</b> não apresentaram <b>nenhuma</b> configuração válida. Apenas o "
            "<b>Aço-silício</b> produziu 6 combinações válidas, listadas na Tabela 6. A Figura 4 (G2) "
            "ilustra o desempenho dos três materiais para N = 220 espiras.",
            st["Corpo"]
        ))

        tab6 = [
            ["Material", "N", "g<sub>nom</sub> (mm)", "L<sub>nom</sub> (mH)", "B<sub>nom</sub> (T)", "L<sub>tol</sub> (mH)", "B<sub>tol</sub> (T)"],
            ["Aço-silício", "220", "0,05", "86,8875", "0,5266", "50,6844", "0,3072"],
            ["Aço-silício", "240", "0,05", "103,4033", "0,5745", "60,3186", "0,3351"],
            ["Aço-silício", "240", "0,10", "83,5180", "0,4640", "52,9627", "0,2942"],
            ["Aço-silício", "260", "0,05", "121,3552", "0,6223", "70,7906", "0,3630"],
            ["Aço-silício", "260", "0,10", "98,0177", "0,5027", "62,1576", "0,3188"],
            ["Aço-silício", "260", "0,15", "82,2084", "0,4216", "55,4013", "0,2841"],
        ]
        story.append(KeepTogether([
            Paragraph("Tabela 6 – Única tabela de configurações válidas (Ferrite e Pó de ferro: nenhuma configuração válida).", st["Legenda"]),
            fazer_tabela(tab6, [W_UTIL*0.18, W_UTIL*0.09, W_UTIL*0.13, W_UTIL*0.15, W_UTIL*0.15, W_UTIL*0.15, W_UTIL*0.15], st),
            Spacer(1, 0.3 * cm)
        ]))

        img_g2 = os.path.join(PASTA_TRABALHO, "G2.png")
        story.append(KeepTogether([
            Image(img_g2, width=W_UTIL, height=W_UTIL * 0.42),
            Paragraph("Figura 4 (G2) – Indutância L (com tolerância) e campo B (nominal) em função de g<sub>nom</sub> para N = 220.", st["Legenda"])
        ]))

        story.append(Paragraph(
            "<b>(c)</b> Seguindo o critério de priorizar o menor número de espiras (sem empate em "
            "N = 220), a configuração final escolhida é: <b>Aço-silício, N = 220 espiras e "
            "g<sub>nom</sub> = 0,05 mm</b>. Na condição nominal (g = 0,05 mm), obtém-se L = 86,8875 mH, "
            "B = 0,5266 T e W = 6,9510 mJ; na condição com tolerância (g = 0,20 mm), obtém-se "
            "L = 50,6844 mH (margem de apenas 0,6844 mH acima de R1 = 50,0 mH), B = 0,3072 T (bem "
            "abaixo de R2 = 1,12 T) e W = 4,0547 mJ. Em relação ao projeto inicial (N = 200), "
            "foram <b>acrescentadas 20 espiras</b>.",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "<b>(d)</b> A Figura 5 (G3) compara as curvas de L e B × g das configurações inicial e "
            "final. Observa-se que o aço-silício possui ampla folga em B em relação ao seu limite R2 "
            "(1,12 T), confirmando a previsão do Passo 2(c) de que maior limite de B pesa mais que "
            "um μ<sub>r</sub> ligeiramente superior (2200 vs. 1500). Para aplicar essa análise a um "
            "transformador real em CA, duas limitações centrais são: (1) ausência de perdas no núcleo "
            "(histerese e correntes parasitas em aço-silício maciço ou laminado); e (2) desconsideração "
            "da reatância de dispersão e da corrente de magnetização senoidal não linear.",
            st["Corpo"]
        ))
        img_g3 = os.path.join(PASTA_TRABALHO, "G3.png")
        story.append(KeepTogether([
            Image(img_g3, width=W_UTIL, height=W_UTIL * 0.42),
            Paragraph("Figura 5 (G3) – Comparação gráfica de L e B × g entre as configurações inicial e final.", st["Legenda"])
        ]))

        # 3 ANÁLISE CRÍTICA
        story.append(Paragraph("3 Análise crítica", st["H1"]))
        story.append(Paragraph(
            "O confronto entre as previsões do Passo 2 e os resultados dos Passos 4 a 6 confirma "
            "todas as tendências físicas previstas: o aumento de g reduziu Φ, L e B (Passo 4c), "
            "elevando a fração de energia no entreferro de 47,83% para 69,62%; o aumento de N de 200 "
            "para 220 elevou L quadraticamente; e a comparação entre materiais demonstrou que a "
            "ferrite (μ<sub>r</sub> = 2200), apesar da maior permeabilidade, falha devido ao baixo "
            "limite de fluxo (0,35 T), enquanto o pó de ferro (μ<sub>r</sub> = 125) não atinge R1 "
            "com até 260 espiras.",
            st["Corpo"]
        ))
        story.append(Paragraph(
            "Quanto aos limites do modelo, a aproximação linear superestima Φ, L e B quando B &gt; B<sub>lim</sub> "
            "(caso da ferrite nominal com B = 0,4808 T), pois ignora a saturação da curva B–H. "
            "Além disso, na configuração final escolhida (Aço-silício, N = 220, g<sub>nom</sub> = 0,05 mm), "
            "a indutância sob tolerância (50,6844 mH) supera o requisito R1 por uma margem estreita "
            "de 0,6844 mH (1,37%); caso o processo produtivo apresente folga ligeiramente acima de "
            "+0,15 mm ou dispersão de fluxo, o projeto ficaria abaixo de 50,0 mH, sendo N = 240 uma "
            "alternativa mais conservadora se o custo de cobre permitir. Por fim, a hipótese de "
            "folga equivalente no Passo 5(d) evidencia que parâmetros concentrados em um único ensaio "
            "não identificam univocamente defeitos físicos sem medições complementares em CA ou "
            "inspeção geométrica.",
            st["Corpo"]
        ))

        # 4 CONCLUSÕES
        story.append(Paragraph("4 Conclusões", st["H1"]))
        story.append(Paragraph(
            "O estudo magnetostático permitiu modelar, validar e otimizar o núcleo do transformador "
            "de isolamento para os requisitos de ensaio propostos. A validação numérica apresentou "
            "resíduos compatíveis com precisão de máquina (≤ 10<sup>−14</sup> %). Verificou-se que "
            "a configuração inicial de ferrite (N = 200, g = 0,10 mm) é inviável por operar fora da "
            "validade linear na condição nominal (B = 0,4808 T &gt; 0,35 T) e violar R1 na condição "
            "com tolerância (L = 41,9939 mH &lt; 50,0 mH). Após varredura completa, selecionou-se o "
            "<b>aço-silício com N = 220 espiras (+20 espiras) e g<sub>nom</sub> = 0,05 mm</b>, que "
            "atende R1 e R2 em ambas as condições (L<sub>nom</sub> = 86,8875 mH, L<sub>tol</sub> = "
            "50,6844 mH, B<sub>nom</sub> = 0,5266 T, B<sub>tol</sub> = 0,3072 T), observando-se "
            "contudo a estreita margem de 0,6844 mH no limite inferior de indutância.",
            st["Corpo"]
        ))

        # REFERÊNCIAS
        story.append(Paragraph("Referências", st["H1"]))
        story.append(Paragraph(
            "FITZGERALD, A. E.; KINGSLEY JR., C.; UMANS, S. D. <b>Máquinas elétricas</b>: com "
            "introdução à eletrônica de potência. 7. ed. Porto Alegre: AMGH, 2014.",
            st["Ref"]
        ))
        story.append(Paragraph(
            "PASSATUTO, L. A. T. <b>FEELT31405 – Eletromagnetismo</b>: slides das aulas de "
            "magnetostática e circuitos magnéticos. Uberlândia: UFU/FEELT, 2026.",
            st["Ref"]
        ))
        story.append(Paragraph(
            "SADIKU, M. N. O. <b>Elementos de eletromagnetismo</b>. 5. ed. Porto Alegre: Bookman, 2012.",
            st["Ref"]
        ))

        doc.build(story, onFirstPage=desenhar_cabecalho_rodape, onLaterPages=desenhar_cabecalho_rodape)
        print(f"PDF gerado com sucesso em: {PDF_SAIDA}")


if __name__ == "__main__":
    construir_pdf()
