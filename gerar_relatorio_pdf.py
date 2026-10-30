# -*- coding: utf-8 -*-
"""
Script de compilacao do Relatorio Tecnico ABNT em PDF.
Trabalho 1 - FEELT31405 - Eletromagnetismo (2026-2) - UFU
Autores: Arthur Montes Cuoco e Luis Gustavo Oliveira Sena

PADRAO RIGOROSO EXIGIDO PELO PROFESSOR:
- Fonte do texto: Arial / Helvetica corpo 12 pt, espacamento 1,5 (leading = 16.5 pt), justificado
- Legendas das figuras e tabelas: 10 pt
- Margens: 2,5 cm em todas as bordas
- Paginas dedicadas: 3 Analise Critica (Pag 10), 4 Conclusoes (Pag 11), Referencias (Pag 12)
- Extensao da Introducao as Referencias: EXATAMENTE 10 PAGINAS (cumprindo a regra de 6 a 10 paginas).
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak
)
from reportlab.pdfgen import canvas

class ABNTNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        if self._pageNumber <= 2:
            return

        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#333333"))

        # Numeracao ABNT: canto superior direito a 2 cm da borda superior
        num_str = f"{self._pageNumber}"
        self.drawRightString(21.0 * cm - 2.5 * cm, 29.7 * cm - 1.8 * cm, num_str)

        self.restoreState()


def gerar_figura_equacoes():
    """Gera figura contendo as equações analíticas (1), (2) e (3) em alta resolução com notação matemática rigorosa."""
    import matplotlib.pyplot as plt
    caminho = "equacoes_modelo.png"
    fig = plt.figure(figsize=(7.2, 1.8), dpi=300)
    ax = fig.add_subplot(111)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    eq1 = r"$C' = \frac{2\pi\,\varepsilon_0}{\frac{1}{\varepsilon_{r,\mathrm{capa}}}\ln\left(\frac{a+t}{a}\right) + \frac{1}{\varepsilon_{r,\mathrm{meio}}}\ln\left(\frac{b}{a+t}\right)}$"
    eq2 = r"$C(h,\,h_w) = C'_{\mathrm{água}}\cdot h_w + C'_{\mathrm{óleo}}\cdot (h - h_w) + C'_{\mathrm{ar}}\cdot (H - h)$"
    eq3 = r"$C(h) = C'_{\mathrm{ar}}\cdot H + \left(C'_{\mathrm{óleo}} - C'_{\mathrm{ar}}\right)\cdot h$"

    ax.text(0.46, 0.77, eq1, fontsize=11.5, ha='center', va='center')
    ax.text(0.99, 0.77, "(1)", fontsize=11, ha='right', va='center', weight='bold')

    ax.text(0.46, 0.40, eq2, fontsize=11, ha='center', va='center')
    ax.text(0.99, 0.40, "(2)", fontsize=11, ha='right', va='center', weight='bold')

    ax.text(0.46, 0.12, eq3, fontsize=11, ha='center', va='center')
    ax.text(0.99, 0.12, "(3)", fontsize=11, ha='right', va='center', weight='bold')

    plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    plt.savefig(caminho, dpi=300, bbox_inches='tight', pad_inches=0.04, facecolor='white')
    plt.close()
    return caminho


def compilar_relatorio():
    pdf_filename = "T1_EM_ARTHUR_LUIS.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm
    )

    styles = getSampleStyleSheet()

    # Estilos ABNT estritos: corpo 12 pt e entrelinha 1,5 (16.5 pt)
    style_corpo = ParagraphStyle(
        'CorpoTexto12',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16.5,
        alignment=4, # Justificado
        spaceAfter=4.5,
        firstLineIndent=1.25 * cm
    )

    style_corpo_sem_recuo = ParagraphStyle(
        'CorpoTextoSemRecuo12',
        parent=style_corpo,
        firstLineIndent=0
    )

    style_h1 = ParagraphStyle(
        'Titulo1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True,
        textColor=colors.HexColor("#0D233A")
    )

    style_h2 = ParagraphStyle(
        'Titulo2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15.5,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True,
        textColor=colors.HexColor("#1A365D")
    )

    # Legendas com 10 pt conforme regra expressa do professor
    style_legenda = ParagraphStyle(
        'Legenda10',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        alignment=1, # Centralizado
        spaceBefore=2,
        spaceAfter=4,
        textColor=colors.HexColor("#222222")
    )

    style_tabela = ParagraphStyle(
        'TabelaTexto',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=10.5,
        alignment=1
    )

    style_tabela_esq = ParagraphStyle(
        'TabelaTextoEsq',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=10.5,
        alignment=0
    )

    style_tabela_header = ParagraphStyle(
        'TabelaHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        alignment=1,
        textColor=colors.whitesmoke
    )

    style_code_box = ParagraphStyle(
        'CodeBox',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.8,
        leading=9.5,
        spaceBefore=2,
        spaceAfter=3
    )

    story = []

    # =========================================================================
    # PAGINA 1: CAPA
    # =========================================================================
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph(
        "<para align='center'><b>UNIVERSIDADE FEDERAL DE UBERLÂNDIA</b><br/>"
        "FACULDADE DE ENGENHARIA ELÉTRICA – FEELT<br/>"
        "CURSO DE ENGENHARIA ELÉTRICA</para>",
        ParagraphStyle('CapaH1', fontName='Helvetica-Bold', fontSize=12, leading=16, alignment=1)
    ))
    story.append(Spacer(1, 4.0 * cm))

    story.append(Paragraph(
        "<para align='center'>"
        "<font size='12'><b>FEELT31405 – ELETROMAGNETISMO (2026-2)</b></font><br/><br/>"
        "<font size='15'><b>TRABALHO 1</b></font><br/><br/>"
        "<font size='13.5'><b>SONDA CAPACITIVA DE NÍVEL NO CONSERVADOR DE UM TRANSFORMADOR</b></font><br/>"
        "<font size='10.5'><i>Modelagem Eletrostática Analítica, Validação Computacional e Revisão de Projeto</i></font>"
        "</para>",
        ParagraphStyle('CapaTit', fontName='Helvetica', fontSize=12, leading=17, alignment=1)
    ))
    story.append(Spacer(1, 4.2 * cm))

    story.append(Paragraph(
        "<para align='center'>"
        "<b>Equipe de Engenharia / Autores:</b><br/>"
        "Arthur Montes Cuoco – Matrícula: 12411EEL028<br/>"
        "Luis Gustavo Oliveira Sena – Matrícula: [MATRÍCULA]<br/><br/>"
        "<b>Professor Responsável:</b><br/>"
        "Prof. Dr. Luiz Arthur Tarralo Passatuto<br/>"
        "Turma: Turma 1"
        "</para>",
        ParagraphStyle('CapaAut', fontName='Helvetica', fontSize=10.5, leading=15, alignment=1)
    ))
    story.append(Spacer(1, 3.2 * cm))

    story.append(Paragraph(
        "<para align='center'><b>Uberlândia – MG</b><br/>29 de outubro de 2026</para>",
        ParagraphStyle('CapaData', fontName='Helvetica', fontSize=10.5, leading=14, alignment=1)
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGINA 2: SUMÁRIO
    # =========================================================================
    story.append(Paragraph("<b>SUMÁRIO</b>", ParagraphStyle('SumTit', fontName='Helvetica-Bold', fontSize=13, leading=17, alignment=1)))
    story.append(Spacer(1, 0.6 * cm))

    sumario_linhas = [
        ("<b>1 INTRODUÇÃO</b>", "3"),
        ("<b>2 DESENVOLVIMENTO</b>", "4"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Passo 1 – Modelagem Física", "4"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Passo 2 – Previsões Físicas", "5"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Passo 3 – Implementação Algorítmica e Validação", "5"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.4 Passo 4 – Curva de Calibração e Leituras de Campo", "6"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.5 Passo 5 – Investigação de Anomalia: Água Decantada", "7"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.6 Passo 6 – Decisão de Projeto: Revisão da Capa Isolante", "8"),
        ("<b>3 ANÁLISE CRÍTICA</b>", "10"),
        ("<b>4 CONCLUSÕES</b>", "11"),
        ("<b>REFERÊNCIAS</b>", "12")
    ]
    t_sum_data = [[Paragraph(tit, style_corpo_sem_recuo), Paragraph(pag, ParagraphStyle('SumPag', fontName='Helvetica-Bold', fontSize=11, alignment=2))] for tit, pag in sumario_linhas]
    t_sum = Table(t_sum_data, colWidths=[14.2 * cm, 1.8 * cm])
    t_sum.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor("#EEEEEE")),
    ]))
    story.append(t_sum)
    story.append(PageBreak())

    # =========================================================================
    # PAGINA 3: 1 INTRODUÇÃO
    # =========================================================================
    story.append(Paragraph("1 Introdução", style_h1))
    story.append(Paragraph(
        "Transformadores de potência imersos em óleo constituem ativos fundamentais na infraestrutura de transmissão e distribuição de energia. O óleo mineral desempenha papel duplo de isolamento dielétrico e refrigeração térmica. Variações diárias de carga e temperatura exigem um vaso de expansão superior, o <i>conservador de óleo</i>, para acomodar a dilatação do fluido. O monitoramento contínuo desse nível é essencial: níveis insuficientes expõem os enrolamentos ao ar, provocando descargas parciais e queima do isolamento, enquanto níveis anormais causam transbordamentos perigosos.",
        style_corpo
    ))
    story.append(Paragraph(
        "A sonda capacitiva coaxial analisada opera na vertical ao longo de toda a faixa útil de operação (H = 0,80 m), próxima ao fundo do conservador. Ela é formada por dois condutores coaxiais concêntricos: uma haste central metálica de raio a = 5,0 mm (diâmetro 10,0 mm) com capa protetora de PTFE de espessura t = 0,50 mm (ε_r,capa = 2,1, raio externo a + t = 5,5 mm) e um tubo externo vazado de raio interno b = 15,0 mm (diâmetro interno 30,0 mm). A unidade eletrônica aplica 5 V de amplitude em baixa frequência, com resolução de 0,1 pF e fundo de escala de 150 pF.",
        style_corpo
    ))

    if os.path.exists("figura1_esquema.jpeg"):
        img_fig1 = Image("figura1_esquema.jpeg", width=11.5 * cm, height=4.5 * cm)
        story.append(KeepTogether([
            Spacer(1, 0.1 * cm),
            img_fig1,
            Paragraph("Figura 1 – Esquema geométrico da sonda coaxial no conservador: corte longitudinal (com lâmina hw e óleo) e transversal.", style_legenda)
        ]))

    story.append(Paragraph(
        "A respiração do conservador introduz umidade, que condensa e decanta no fundo formando uma camada de água de espessura hw. Como a constante dielétrica da água (ε_r = 80) supera muito a do óleo (ε_r = 2,2), essa lâmina altera severamente o sinal lido. Este trabalho modela o sistema via equações de Maxwell, valida um código em Python, analisa os erros por água e redimensiona a capa isolante para garantir a segurança operacional.",
        style_corpo
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGINA 4: 2 DESENVOLVIMENTO (Quadro-Resumo e Passo 1)
    # =========================================================================
    story.append(Paragraph("2 Desenvolvimento", style_h1))
    story.append(Paragraph(
        "A modelagem eletrostática e as simulações computacionais foram desenvolvidas em seis passos sequenciais. A Tabela 1 abre a seção com o quadro-resumo das etapas e resultados obtidos.",
        style_corpo
    ))

    quadro_resumo_data = [
        [Paragraph("Passo", style_tabela_header), Paragraph("Resultado Principal Obtido", style_tabela_header), Paragraph("Saída Associada", style_tabela_header)],
        [Paragraph("Passo 1", style_tabela), Paragraph("Modelagem analítica comprovando série na radial e paralelo na vertical", style_tabela_esq), Paragraph("Figura 1 / Eq. (1)-(3)", style_tabela)],
        [Paragraph("Passo 2", style_tabela), Paragraph("Previsões teóricas de linearidade, atenuação por espessura t e desvio positivo por hw", style_tabela_esq), Paragraph("Texto dedutivo", style_tabela)],
        [Paragraph("Passo 3", style_tabela), Paragraph("Código Python validado com cabo bicamada (C' = 74,6482 pF/m, erro 0,00%)", style_tabela_esq), Paragraph("Tabela 2 / Pseudocódigo", style_tabela)],
        [Paragraph("Passo 4", style_tabela), Paragraph("Calibração óleo limpo: C_vazio = 42,4388 pF, C_cheio = 88,7559 pF, S = 0,5790 pF/cm", style_tabela_esq), Paragraph("Tabela 3 / Figura 2 (G1)", style_tabela)],
        [Paragraph("Passo 5", style_tabela), Paragraph("Anomalia: hw = 2,00 cm gera erro de +29,38 cm; saturação em hw = 9,60 cm", style_tabela_esq), Paragraph("Tabela 4 / Figura 3 (G2)", style_tabela)],
        [Paragraph("Passo 6", style_tabela), Paragraph("Revisão: PTFE com t = 0,73 mm atende R1 (149,84 pF) e R2 (1,77 mm), atenuando erro em 26,2%", style_tabela_esq), Paragraph("Tab. 5-6 / Fig. 4-5 (G3-G4)", style_tabela)]
    ]
    t_qr = Table(quadro_resumo_data, colWidths=[2.2 * cm, 10.4 * cm, 3.4 * cm])
    t_qr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_qr)
    story.append(Paragraph("Tabela 1 – Quadro-resumo do desenvolvimento: etapas, principais entregas e figuras/tabelas.", style_legenda))
    story.append(Spacer(1, 0.1 * cm))

    story.append(Paragraph("2.1 Passo 1 – Modelagem Física", style_h2))
    story.append(Paragraph(
        "<b>(a) Regiões materiais:</b> Verticalmente (z), há três trechos: água (0 a hw), óleo (hw a h) e ar (h a H). Radialmente (r), há duas camadas cilíndricas: capa sólida (a ≤ r ≤ a + t) e meio fluido (a + t ≤ r ≤ b).",
        style_corpo
    ))
    story.append(Paragraph(
        "<b>(b) Condições de fronteira e associação:</b> Na interface radial (r = a + t), a ausência de cargas livres impõe D_1n = D_2n. O fluxo radial único de D atravessa sequencialmente capa e fluido, somando as quedas de potencial (V = V_capa + V_meio) e caracterizando associação em <b>SÉRIE</b>. Nas interfaces horizontais (z = hw e z = h), a continuidade de E_t e os condutores equipotenciais aplicam a mesma tensão V = 5 V em todas as colunas, combinando-as em <b>PARALELO</b> (Q = Σ Q_i).",
        style_corpo
    ))
    story.append(Paragraph(
        "<b>(c) Dedução analítica:</b> Aplicando a Lei de Gauss cilíndrica D_r = q' / (2π r) e integrando o campo elétrico radial E_r = D_r / ε, a capacitância linear C' = q'/V [F/m] e a capacitância total C [F] associada às colunas de fluido resultam nas Equações (1), (2) e (3):",
        style_corpo
    ))
    img_eqs = gerar_figura_equacoes()
    story.append(Spacer(1, 0.15 * cm))
    story.append(Image(img_eqs, width=15.5 * cm, height=3.87 * cm))
    story.append(PageBreak())

    # =========================================================================
    # PAGINA 5: 2.2 Passo 2 e 2.3 Passo 3
    # =========================================================================
    story.append(Paragraph("2.2 Passo 2 – Previsões Físicas", style_h2))
    story.append(Paragraph(
        "Antes das simulações, estabeleceram-se três previsões físicas fundamentadas no eletromagnetismo:<br/>"
        "• <b>(a) Forma de C(h) com óleo limpo:</b> Reta linear ideal com inclinação S = C'_óleo − C'_ar > 0 e intercepto C_vazio = C'_ar · H, pois a altura varia substituindo uniformemente coluna de ar por óleo.<br/>"
        "• <b>(b) Efeito da espessura da capa (t):</b> Aumentar t expande a fração de PTFE (ε_r = 2,1). Como a associação série é governada pelo menor ε_r, a capacitância equivalente diminui, atenuando a sensibilidade S e piorando a resolução mínima detectável Δh_mín.<br/>"
        "• <b>(c) Efeito da água decantada (hw):</b> Pela alta permissividade da água (ε_r = 80 >> 2,2), C(h, hw) cresce drasticamente. A calibração de óleo limpo interpretará esse valor como excesso de óleo, indicando nível muito maior que o real (erro positivo severo). Cada centímetro de água adiciona muito mais capacitância do que 1 cm de óleo.",
        style_corpo
    ))

    story.append(Paragraph("2.3 Passo 3 – Implementação Algorítmica e Validação", style_h2))
    story.append(Paragraph(
        "O modelo foi programado em Python usando <b>numpy</b> (cálculo matricial vetorizado das camadas e varreduras paramétricas sem loops lentos) e <b>matplotlib</b> (gráficos G1 a G4 com vírgula decimal ABNT via FuncFormatter). O algoritmo estruturado opera conforme o pseudocódigo abaixo:",
        style_corpo
    ))

    pseudocodigo_lines = [
        "Algoritmo: Sonda_Capacitiva_Coaxial",
        "Entradas: a = 5 mm, b = 15 mm, H = 0,80 m, eps_r = {ar: 1, oleo: 2.2, agua: 80}",
        "Funcao cap_por_comprimento(raios, eps_camadas):",
        "    retorne 2 * pi * EPSILON_0 / sum([ (1/eps_camadas[k]) * ln(raios[k+1] / raios[k]) ])",
        "Funcao capacitancia_total(h, hw, eps_capa, t):",
        "    retorne C_agua * hw + C_oleo * (h - hw) + C_ar * (H - h)",
        "Funcao nivel_indicado(C_medida, eps_capa, t):",
        "    retorne (C_medida - C_ar * H) / (C_oleo - C_ar)  # linear, sem clip",
        "Validar com cabo bicamada da Aula 08 (assert erro < 0.01%)",
        "Fim_Algoritmo"
    ]
    story.append(Paragraph("<br/>".join(pseudocodigo_lines).replace(" ", "&nbsp;"), style_code_box))

    story.append(Paragraph(
        "A validação da função cap_por_comprimento com o cabo coaxial bicamada da Aula 08 (raios 1,0, 3,0 e 5,0 mm com ε_r de 2,1 e 2,3) comprovou exatidão analítica plena, conforme a Tabela 2.",
        style_corpo
    ))

    tab_val_data = [
        [Paragraph("Parâmetro de Validação", style_tabela_header), Paragraph("Valor Analítico Teórico", style_tabela_header), Paragraph("Valor Computado no Código", style_tabela_header), Paragraph("Erro Relativo (%)", style_tabela_header)],
        [Paragraph("Capacitância linear C' (Aula 08)", style_tabela_esq), Paragraph("74,6482 pF/m", style_tabela), Paragraph("74,6482 pF/m", style_tabela), Paragraph("0,0000 %", style_tabela)]
    ]
    t_val = Table(tab_val_data, colWidths=[5.5 * cm, 4.0 * cm, 4.0 * cm, 2.5 * cm])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
    ]))
    story.append(t_val)
    story.append(Paragraph("Tabela 2 – Validação da capacitância linear coaxial bicamada com dados de referência da Aula 08.", style_legenda))
    story.append(PageBreak())

    # =========================================================================
    # PAGINA 6: 2.4 Passo 4
    # =========================================================================
    story.append(Paragraph("2.4 Passo 4 – Curva de Calibração e Leitura de Campo", style_h2))
    story.append(Paragraph(
        "Para a sonda na configuração inicial (PTFE t = 0,50 mm, ε_r = 2,1 e hw = 0), computaram-se C'_ar = 53,0485 pF/m, C'_óleo = 110,9449 pF/m e C'_água = 960,3682 pF/m. A Tabela 3 sumariza os parâmetros de calibração e a conversão das leituras de campo.",
        style_corpo
    ))

    tab_cal_data = [
        [Paragraph("Parâmetro / Medição de Campo", style_tabela_header), Paragraph("Expressão Analítica", style_tabela_header), Paragraph("Valor Numérico", style_tabela_header), Paragraph("Unidade", style_tabela_header)],
        [Paragraph("Capacitância com sonda vazia (C_vazio)", style_tabela_esq), Paragraph("C'_ar · H", style_tabela), Paragraph("42,4388", style_tabela), Paragraph("pF", style_tabela)],
        [Paragraph("Capacitância com sonda cheia (C_cheio)", style_tabela_esq), Paragraph("C'_óleo · H", style_tabela), Paragraph("88,7559", style_tabela), Paragraph("pF", style_tabela)],
        [Paragraph("Sensibilidade ao nível de óleo (S)", style_tabela_esq), Paragraph("C'_óleo − C'_ar", style_tabela), Paragraph("0,5790", style_tabela), Paragraph("pF/cm", style_tabela)],
        [Paragraph("Menor variação distinguível (Δh_mín)", style_tabela_esq), Paragraph("0,1 pF / S", style_tabela), Paragraph("1,7272", style_tabela), Paragraph("mm", style_tabela)],
        [Paragraph("Nível para leitura L1 = 54,0 pF", style_tabela_esq), Paragraph("(L1 − C_vazio) / S", style_tabela), Paragraph("0,1997", style_tabela), Paragraph("m", style_tabela)],
        [Paragraph("Nível para leitura L2 = 68,5 pF", style_tabela_esq), Paragraph("(L2 − C_vazio) / S", style_tabela), Paragraph("0,4501", style_tabela), Paragraph("m", style_tabela)],
        [Paragraph("Nível para leitura L3 = 83,0 pF", style_tabela_esq), Paragraph("(L3 − C_vazio) / S", style_tabela), Paragraph("0,7006", style_tabela), Paragraph("m", style_tabela)]
    ]
    t_cal = Table(tab_cal_data, colWidths=[6.0 * cm, 3.8 * cm, 3.7 * cm, 2.5 * cm])
    t_cal.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_cal)
    story.append(Paragraph("Tabela 3 – Parâmetros de calibração para óleo limpo e conversão das leituras normais de campo.", style_legenda))

    story.append(Paragraph(
        "<b>Linearidade:</b> O teste numérico comprovou desvio máximo da reta inferior a 1,3 × 10<sup>-26</sup> F e R<sup>2</sup> = 1,0000. Fisicamente, trechos paralelos somam capacitâncias estritamente proporcionais ao deslocamento dh, mantendo dC/dh = S constante.",
        style_corpo
    ))

    if os.path.exists("G1.png"):
        img_g1 = Image("G1.png", width=11.5 * cm, height=5.2 * cm)
        story.append(KeepTogether([
            Spacer(1, 0.1 * cm),
            img_g1,
            Paragraph("Figura 2 – Curva de calibração da sonda C(h) para óleo limpo na configuração inicial (G1), destacando C_vazio, C_cheio e as leituras normais L1, L2 e L3.", style_legenda)
        ]))
    story.append(PageBreak())

    # =========================================================================
    # PAGINA 7: 2.5 Passo 5
    # =========================================================================
    story.append(Paragraph("2.5 Passo 5 – Investigação de Anomalia: Água Decantada", style_h2))
    story.append(Paragraph(
        "Na inspeção de campo, a vareta indicou nível real h_real = 0,45 m, enquanto a unidade registrou C = 85,5 pF.<br/>"
        "• <b>(a) Nível indicado e erro:</b> Pela função inversa (Eq. 3), obteve-se h_ind = 0,7438 m (74,38 cm). O erro de medição foi de <b>Erro = +0,2938 m (+29,38 cm)</b> (+65,3%), superestimando perigosamente o volume de óleo.<br/>"
        "• <b>(b) Lâmina de água:</b> Isolando hw na Equação (2), obteve-se <b>hw = 0,0200 m (2,00 cm)</b>. Apenas 2 cm de água no fundo foram capazes de falsear a indicação em quase 30 cm de óleo.<br/>"
        "• <b>(c) Análise paramétrica e saturação:</b> A Tabela 4 sintetiza a evolução da capacitância e do erro com a lâmina de água.",
        style_corpo
    ))

    tab_ano_data = [
        [Paragraph("Condição de Operação", style_tabela_header), Paragraph("Água hw (cm)", style_tabela_header), Paragraph("Capacitância C (pF)", style_tabela_header), Paragraph("Nível Indicado hind (m)", style_tabela_header), Paragraph("Erro Absoluto (cm)", style_tabela_header)],
        [Paragraph("Sem água (referência)", style_tabela_esq), Paragraph("0,00", style_tabela), Paragraph("68,4922", style_tabela), Paragraph("0,4500", style_tabela), Paragraph("0,00", style_tabela)],
        [Paragraph("Taxa por 1 cm de água", style_tabela_esq), Paragraph("1,00", style_tabela), Paragraph("76,9864", style_tabela), Paragraph("0,5968", style_tabela), Paragraph("+14,67", style_tabela)],
        [Paragraph("Ponto da inspeção", style_tabela_esq), Paragraph("2,00", style_tabela), Paragraph("85,4806", style_tabela), Paragraph("0,7438", style_tabela), Paragraph("+29,38", style_tabela)],
        [Paragraph("Ponto C = C_cheio", style_tabela_esq), Paragraph("2,39", style_tabela), Paragraph("88,7559", style_tabela), Paragraph("0,8000", style_tabela), Paragraph("+35,00", style_tabela)],
        [Paragraph("Saturação eletrônica 150 pF", style_tabela_esq), Paragraph("9,60", style_tabela), Paragraph("150,0000", style_tabela), Paragraph("1,8578", style_tabela), Paragraph("+140,78", style_tabela)]
    ]
    t_ano = Table(tab_ano_data, colWidths=[4.5 * cm, 2.5 * cm, 3.2 * cm, 3.3 * cm, 2.5 * cm])
    t_ano.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_ano)
    story.append(Paragraph("Tabela 4 – Comportamento da sonda em função da lâmina de água decantada (h = 0,45 m).", style_legenda))

    if os.path.exists("G2.png"):
        img_g2 = Image("G2.png", width=11.5 * cm, height=5.2 * cm)
        story.append(KeepTogether([
            Spacer(1, 0.1 * cm),
            img_g2,
            Paragraph("Figura 3 – Erro de indicação de nível hind − hreal versus espessura de água hw para h = 0,45 m (G2), com marcadores de C_cheio e saturação em 150 pF.", style_legenda)
        ]))

    story.append(Paragraph(
        "<b>(d) Água com perdas:</b> A água decantada contém íons dissolvidos (condutividade σ > 0). Sob 60 Hz, o regime é condutivo (σ >> ωε), com corrente de condução predominante. O tempo de relaxação τ = ε/σ é desprezível, blindando o campo no líquido e atuando como um condutor em série com a capa de PTFE. A condutância resistiva associada altera a impedância complexa lida pela ponte de medição.",
        style_corpo
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGINA 8: 2.6 Passo 6 (Varredura, G3 e Escolha Técnica em uma única página)
    # =========================================================================
    story.append(Paragraph("2.6 Passo 6 – Decisão de Projeto: Revisão da Capa Isolante", style_h2))
    story.append(Paragraph(
        "Reavaliou-se a capa considerando PTFE (ε_r = 2,1), Poliimida (ε_r = 3,4) e Epóxi (ε_r = 3,6), com t de 0,20 a 1,00 mm, sob dois critérios: <b>R1</b> (C_máx ≤ 150 pF com tanque cheio e hw = 10 cm) e <b>R2</b> (Δh_mín ≤ 1,8 mm com óleo limpo). A capa inicial (PTFE t = 0,50 mm) obteve C_máx = <b>173,6982 pF</b> (<b>REPROVADO em R1</b>) e Δh_mín = <b>1,7272 mm</b> (<b>APROVADO em R2</b>).",
        style_corpo
    ))

    tab_var_data = [
        [Paragraph("Material", style_tabela_header), Paragraph("t (mm)", style_tabela_header), Paragraph("C_máx (pF) [R1 ≤ 150]", style_tabela_header), Paragraph("Δh_mín (mm) [R2 ≤ 1,8]", style_tabela_header), Paragraph("S (pF/cm)", style_tabela_header), Paragraph("Status", style_tabela_header)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,20", style_tabela), Paragraph("239,9512", style_tabela), Paragraph("1,6324", style_tabela), Paragraph("0,6126", style_tabela), Paragraph("Reprov. (R1)", style_tabela)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,50", style_tabela), Paragraph("173,6982", style_tabela), Paragraph("1,7272", style_tabela), Paragraph("0,5790", style_tabela), Paragraph("Reprov. (R1)", style_tabela)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,73", style_tabela), Paragraph("149,8448", style_tabela), Paragraph("1,7670", style_tabela), Paragraph("0,5659", style_tabela), Paragraph("<b>APROV. (Ótimo)</b>", style_tabela)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,80", style_tabela), Paragraph("144,8719", style_tabela), Paragraph("1,7795", style_tabela), Paragraph("0,5620", style_tabela), Paragraph("Aprovado", style_tabela)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,91", style_tabela), Paragraph("138,3767", style_tabela), Paragraph("1,7993", style_tabela), Paragraph("0,5558", style_tabela), Paragraph("Aprovado", style_tabela)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,95", style_tabela), Paragraph("136,3390", style_tabela), Paragraph("1,8066", style_tabela), Paragraph("0,5535", style_tabela), Paragraph("Reprov. (R2)", style_tabela)],
        [Paragraph("Poliimida (ε_r = 3,4)", style_tabela_esq), Paragraph("0,80", style_tabela), Paragraph("169,3810", style_tabela), Paragraph("1,7320", style_tabela), Paragraph("0,5774", style_tabela), Paragraph("Reprov. (R1)", style_tabela)],
        [Paragraph("Epóxi (ε_r = 3,6)", style_tabela_esq), Paragraph("0,80", style_tabela), Paragraph("172,9510", style_tabela), Paragraph("1,6320", style_tabela), Paragraph("0,6127", style_tabela), Paragraph("Reprov. (R1)", style_tabela)]
    ]
    t_var = Table(tab_var_data, colWidths=[3.5 * cm, 1.4 * cm, 3.3 * cm, 3.3 * cm, 2.3 * cm, 2.7 * cm])
    t_var.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_var)
    story.append(Paragraph("Tabela 5 – Amostra representativa da varredura paramétrica de materiais e espessuras da capa isolante.", style_legenda))

    if os.path.exists("G3.png"):
        img_g3 = Image("G3.png", width=12.5 * cm, height=4.5 * cm)
        story.append(KeepTogether([
            Spacer(1, 0.05 * cm),
            img_g3,
            Paragraph("Figura 4 – Varredura paramétrica (G3): Painel 1 (C_máx vs t, limite 150 pF) e Painel 2 (Δh_mín vs t, limite 1,8 mm).", style_legenda)
        ]))

    story.append(Paragraph(
        "<b>Escolha técnica:</b> Poliimida e Epóxi reprovaram em R1 em toda a faixa por sua alta constante (ε_r ≥ 3,4). Para o PTFE, encontraram-se 19 soluções viáveis (t ∈ [0,73 mm; 0,91 mm]). Selecionou-se <b>t = 0,73 mm em PTFE</b>, pois cumpre R1 (C_máx = 149,8448 pF) e R2 (Δh_mín = 1,7670 mm) e <b>maximiza a sensibilidade ao óleo (S = 0,5659 pF/cm)</b>.",
        style_corpo
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGINA 9: 2.6 Passo 6 cont. (Comparativo e G4)
    # =========================================================================
    story.append(Paragraph(
        "<b>(d) Comparativo de desempenho:</b> A Tabela 6 sintetiza a comparação direta entre as configurações inicial e final otimizada.",
        style_corpo
    ))

    tab_comp_data = [
        [Paragraph("Parâmetro de Desempenho", style_tabela_header), Paragraph("Configuração Inicial (PTFE, 0,50 mm)", style_tabela_header), Paragraph("Configuração Final (PTFE, 0,73 mm)", style_tabela_header), Paragraph("Variação Relativa (%)", style_tabela_header)],
        [Paragraph("Capacitância linear no ar (C'_ar)", style_tabela_esq), Paragraph("53,0485 pF/m", style_tabela), Paragraph("54,1567 pF/m", style_tabela), Paragraph("+2,09 %", style_tabela)],
        [Paragraph("Capacitância linear no óleo (C'_óleo)", style_tabela_esq), Paragraph("110,9449 pF/m", style_tabela), Paragraph("110,7490 pF/m", style_tabela), Paragraph("−0,18 %", style_tabela)],
        [Paragraph("Capacitância linear na água (C'_água)", style_tabela_esq), Paragraph("960,3682 pF/m", style_tabela), Paragraph("723,2052 pF/m", style_tabela), Paragraph("−24,70 %", style_tabela)],
        [Paragraph("Capacitância com sonda vazia (C_vazio)", style_tabela_esq), Paragraph("42,4388 pF", style_tabela), Paragraph("43,3254 pF", style_tabela), Paragraph("+2,09 %", style_tabela)],
        [Paragraph("Capacitância com sonda cheia (C_cheio)", style_tabela_esq), Paragraph("88,7559 pF", style_tabela), Paragraph("88,5992 pF", style_tabela), Paragraph("−0,18 %", style_tabela)],
        [Paragraph("Sensibilidade ao nível de óleo (S)", style_tabela_esq), Paragraph("0,5790 pF/cm", style_tabela), Paragraph("0,5659 pF/cm", style_tabela), Paragraph("−2,26 %", style_tabela)],
        [Paragraph("Menor variação distinguível (Δh_mín)", style_tabela_esq), Paragraph("1,7272 mm", style_tabela), Paragraph("1,7670 mm", style_tabela), Paragraph("+2,30 %", style_tabela)],
        [Paragraph("Capacitância máxima crítica (C_máx)", style_tabela_esq), Paragraph("173,6982 pF (Reprovado)", style_tabela), Paragraph("149,8448 pF (Aprovado)", style_tabela), Paragraph("−13,73 % (Segurança)", style_tabela)],
        [Paragraph("Erro por 1 cm de água decantada", style_tabela_esq), Paragraph("+14,67 cm (+0,1467 m)", style_tabela), Paragraph("+10,82 cm (+0,1082 m)", style_tabela), Paragraph("−26,24 % (Atenuação)", style_tabela)]
    ]
    t_comp = Table(tab_comp_data, colWidths=[5.5 * cm, 4.3 * cm, 4.3 * cm, 2.9 * cm])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_comp)
    story.append(Paragraph("Tabela 6 – Confronto comparativo de desempenho metrológico: configuração inicial versus configuração final otimizada.", style_legenda))

    if os.path.exists("G4.png"):
        img_g4 = Image("G4.png", width=11.5 * cm, height=5.5 * cm)
        story.append(KeepTogether([
            Spacer(1, 0.1 * cm),
            img_g4,
            Paragraph("Figura 5 – Curvas de capacitância C versus nível total h para lâminas de água hw = 0, 1 cm e 5 cm (G4): comparação entre configuração inicial (linha contínua) e final (tracejada).", style_legenda)
        ]))

    story.append(Paragraph(
        "A Figura 5 (G4) evidencia que a capa de PTFE com t = 0,73 mm preserva a linearidade e o paralelismo das curvas C × h, enquanto desloca as leituras para níveis inferiores de capacitância. Isso garante margem segura abaixo do fundo de escala de 150 pF, reduzindo a vulnerabilidade à água em 26,24%.",
        style_corpo
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGINA 10: 3 ANÁLISE CRÍTICA (PÁGINA DEDICADA COMPACTA)
    # =========================================================================
    story.append(Paragraph("3 Análise Crítica", style_h1))
    story.append(Paragraph(
        "A confrontação sistemática entre a modelagem analítica e as restrições práticas de sistemas de instrumentação em subestações permite balizar com clareza o alcance e a validade das soluções propostas.",
        style_corpo
    ))

    story.append(Paragraph("3.1 Confronto entre Previsões Teóricas e Resultados Numéricos", style_h2))
    story.append(Paragraph(
        "Os resultados obtidos ratificaram integralmente as previsões qualitativas do Passo 2:<br/>"
        "• <b>Linearidade com óleo limpo:</b> Confirmou-se rigorosamente (R<sup>2</sup> = 1,0000 e resíduo &lt; 1,3 × 10<sup>-26</sup> F), comprovando que o campo eletrostático radial permanece invariante com a ascensão do líquido.<br/>"
        "• <b>Impacto da espessura da capa:</b> Aumentar t de 0,50 para 0,73 mm reduziu levemente a sensibilidade ao óleo (−2,26%), mas aliviou de forma decisiva a capacitância de saturação (−13,73%), validando a previsão sobre o efeito limitador do PTFE em circuito série.<br/>"
        "• <b>Severidade da contaminação aquosa:</b> Confirmou-se a indução de erro positivo drástico (+29,38 cm por 2 cm de água), falseando a medição em mais de 65% e comprovando o alto risco que a água livre representa para o diagnóstico térmico do transformador.",
        style_corpo
    ))

    story.append(Paragraph("3.2 Limitações do Modelo Físico e Fontes de Erro em Sondas Reais", style_h2))
    story.append(Paragraph(
        "Em ambiente de subestação, o comportamento real da sonda desvia do modelo ideal por quatro causas:<br/>"
        "1. <b>Efeitos de Borda e Capacitâncias Parasitas:</b> O modelo bidimensional despreza as linhas de campo tridimensionais nas extremidades. Além disso, o cabo blindado de conexão soma capacitâncias parasitas (10 a 30 pF) em paralelo, exigindo calibração de zero no comissionamento.<br/>"
        "2. <b>Excentricidade Mecânica:</b> Vibrações do transformador podem causar desalinhamento entre haste e tubo. Como o campo varia com 1/r, condutores excêntricos sempre elevam a capacitância frente ao valor concêntrico ideal.<br/>"
        "3. <b>Sensibilidade Térmica:</b> A temperatura no conservador varia de 20 °C a 90 °C. O decréscimo térmico da permissividade do óleo (dε_r/dT ≈ −0,001/°C) altera C_vazio e S, exigindo compensação térmica com PT100 auxiliar.<br/>"
        "4. <b>Condutividade e Perdas na Água:</b> A água decantada contém íons dissolvidos (σ > 0). Em 60 Hz, o regime é fortemente condutivo (σ >> ωε), atuando como condutor resistivo. A corrente de fuga associada altera a impedância complexa vista pela ponte, impondo defasamento não contemplado pelo modelo eletrostático estático.",
        style_corpo
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGINA 11: 4 CONCLUSÕES (PÁGINA DEDICADA)
    # =========================================================================
    story.append(Paragraph("4 Conclusões", style_h1))
    story.append(Paragraph(
        "Este trabalho desenvolveu com sucesso a modelagem eletrostática analítica, a validação numérica e o redimensionamento de engenharia de uma sonda capacitiva coaxial para controle contínuo de nível de óleo no conservador de transformadores de potência.",
        style_corpo
    ))
    story.append(Paragraph(
        "As condições de fronteira eletrostáticas de Maxwell comprovaram a fundamentação física da combinação de capacitâncias: associação em <b>série</b> na direção radial (continuidade da componente normal de D) e associação em <b>paralelo</b> ao longo da altura útil (continuidade da componente tangencial de E e superfícies condutoras equipotenciais sob tensão comum de 5 V).",
        style_corpo
    ))
    story.append(Paragraph(
        "O código desenvolvido em Python demonstrou exatidão analítica plena, sendo validado com erro relativo de 0,0000% frente à geometria bicamada da Aula 08. Na configuração com óleo limpo, a sonda exibiu resposta perfeitamente linear (R² = 1,0000), garantindo resolução de 1,7272 mm.",
        style_corpo
    ))
    story.append(Paragraph(
        "A investigação da anomalia revelou a vulnerabilidade crítica do sensor à presença de água livre decantada. Devido à sua altíssima permissividade (ε_r = 80), uma lâmina de apenas 2,00 cm no fundo do vaso induziu erro positivo de <b>+29,38 cm</b> no nível de óleo (+65,3%), criando uma falsa impressão de conservador abastecido enquanto os enrolamentos podem estar perigosamente desnudados.",
        style_corpo
    ))
    story.append(Paragraph(
        "Constatou-se também que a geometria inicial (PTFE t = 0,50 mm) é inviável em condições severas de contaminação, pois atinge C_máx = <b>173,70 pF</b> sob 10 cm de água, violando o fundo de escala de 150 pF da eletrônica (R1). A varredura de materiais demonstrou que Poliimida (ε_r = 3,4) e Epóxi (ε_r = 3,6) são inviáveis por violarem R1 em qualquer espessura.",
        style_corpo
    ))
    story.append(Paragraph(
        "A revisão de projeto identificou o <b>PTFE com espessura otimizada de t = 0,73 mm</b> como a solução de engenharia perfeita. Essa configuração atende simultaneamente aos requisitos R1 (C_máx = 149,84 pF ≤ 150 pF) e R2 (Δh_mín = 1,77 mm ≤ 1,8 mm), <b>maximizando a sensibilidade ao óleo (S = 0,5659 pF/cm)</b> e proporcionando <b>atenuação de 26,24% na sensibilidade à água decantada</b> (reduzindo a taxa de erro de +14,67 cm para +10,82 cm por cm de água).",
        style_corpo
    ))
    story.append(Paragraph(
        "Conclui-se que o redimensionamento eletrostático soluciona de forma robusta e econômica os limites da instrumentação, recomendando-se ainda para operação em campo rotinas de purga periódica de água decantada e compensação digital de temperatura para assegurar a confiabilidade do transformador.",
        style_corpo
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGINA 12: REFERÊNCIAS (PÁGINA DEDICADA)
    # =========================================================================
    story.append(Paragraph("Referências", style_h1))
    story.append(Spacer(1, 0.5 * cm))

    referencias_abnt = [
        "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. <b>NBR 5356-2</b>: Transformadores de potência - Parte 2: Elevação de temperatura. Rio de Janeiro: ABNT, 2008.",
        "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. <b>NBR 10576</b>: Óleo mineral isolante de equipamentos elétricos - Guia para amostragem, manuseio e ensaios. Rio de Janeiro: ABNT, 2017.",
        "BAXTER, Larry K. <b>Capacitive Sensors: Design and Applications</b>. New York: IEEE Press / John Wiley & Sons, 1997.",
        "HAYT JR., William H.; BUCK, John A. <b>Eletromagnetismo</b>. 8. ed. Porto Alegre: AMGH, 2013.",
        "KUFFEL, E.; ZAENGL, W. S.; KUFFEL, J. <b>High Voltage Engineering: Fundamentals</b>. 2. ed. Oxford: Newnes, 2000.",
        "PASSATUTO, Luiz Arthur Tarralo. <b>Slides das aulas da disciplina FEELT31405 – Eletromagnetismo</b>. Uberlândia: Faculdade de Engenharia Elétrica, Universidade Federal de Uberlândia, 2026. Material didático.",
        "SADIKU, Matthew N. O. <b>Elementos de Eletromagnetismo</b>. 5. ed. Porto Alegre: Bookman, 2012."
    ]

    for ref in referencias_abnt:
        p_ref = Paragraph(ref, ParagraphStyle('RefABNT12', fontName='Helvetica', fontSize=10.5, leading=14.5, alignment=0, spaceAfter=14))
        story.append(p_ref)

    story.append(Spacer(1, 2.0 * cm))
    story.append(Paragraph(
        "<para align='center'><font size='9' color='#666666'><i>Relatório técnico formatado em conformidade com as normas ABNT NBR 6023 e as diretrizes da disciplina FEELT31405 (UFU / 2026-2).</i></font></para>",
        style_corpo_sem_recuo
    ))

    doc.build(story, canvasmaker=ABNTNumberedCanvas)
    print(f"Relatório ABNT com fonte 12 compilado com sucesso: {pdf_filename}")


if __name__ == "__main__":
    compilar_relatorio()
