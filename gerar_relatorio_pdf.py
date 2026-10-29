# -*- coding: utf-8 -*-
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
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#444444"))

        if self._pageNumber >= 3:
            cabecalho = "FEELT31405 – Eletromagnetismo | Trabalho 1: Sonda Capacitiva no Conservador"
            self.drawString(2.5 * cm, 29.7 * cm - 1.6 * cm, cabecalho)
            self.setStrokeColor(colors.HexColor("#B0BEC5"))
            self.setLineWidth(0.6)
            self.line(2.5 * cm, 29.7 * cm - 1.75 * cm, 21.0 * cm - 2.5 * cm, 29.7 * cm - 1.75 * cm)

        if self._pageNumber >= 3:
            num_str = f"{self._pageNumber}"
            self.drawRightString(21.0 * cm - 2.5 * cm, 1.4 * cm, num_str)

        self.restoreState()


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

    style_corpo = ParagraphStyle(
        'CorpoTexto',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        alignment=4,
        spaceAfter=5,
        firstLineIndent=1.0 * cm
    )

    style_corpo_sem_recuo = ParagraphStyle(
        'CorpoTextoSemRecuo',
        parent=style_corpo,
        firstLineIndent=0
    )

    style_h1 = ParagraphStyle(
        'Titulo1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True,
        textColor=colors.HexColor("#0D233A")
    )

    style_h2 = ParagraphStyle(
        'Titulo2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
        textColor=colors.HexColor("#1A365D")
    )

    style_legenda = ParagraphStyle(
        'Legenda',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        alignment=1,
        spaceBefore=2,
        spaceAfter=6,
        textColor=colors.HexColor("#333333")
    )

    style_tabela = ParagraphStyle(
        'TabelaTexto',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        alignment=1
    )

    style_tabela_esq = ParagraphStyle(
        'TabelaTextoEsq',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        alignment=0
    )

    style_tabela_header = ParagraphStyle(
        'TabelaHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        alignment=1,
        textColor=colors.whitesmoke
    )

    style_code_box = ParagraphStyle(
        'CodeBox',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        spaceBefore=2,
        spaceAfter=4
    )

    story = []

    # PAGINA 1: CAPA
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph(
        "<para align='center'><b>UNIVERSIDADE FEDERAL DE UBERLÂNDIA</b><br/>"
        "FACULDADE DE ENGENHARIA ELÉTRICA – FEELT<br/>"
        "CURSO DE ENGENHARIA ELÉTRICA</para>",
        ParagraphStyle('CapaH1', fontName='Helvetica-Bold', fontSize=11, leading=15, alignment=1)
    ))
    story.append(Spacer(1, 4.0 * cm))

    story.append(Paragraph(
        "<para align='center'>"
        "<font size='11'><b>FEELT31405 – ELETROMAGNETISMO (2026-2)</b></font><br/><br/>"
        "<font size='14'><b>TRABALHO 1</b></font><br/><br/>"
        "<font size='13'><b>SONDA CAPACITIVA DE NÍVEL NO CONSERVADOR DE UM TRANSFORMADOR</b></font><br/>"
        "<font size='9.5'><i>Modelagem Eletrostática Analítica, Validação Computacional e Revisão de Projeto</i></font>"
        "</para>",
        ParagraphStyle('CapaTit', fontName='Helvetica', fontSize=11, leading=16, alignment=1)
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
        ParagraphStyle('CapaAut', fontName='Helvetica', fontSize=9.5, leading=14, alignment=1)
    ))
    story.append(Spacer(1, 3.2 * cm))

    story.append(Paragraph(
        "<para align='center'><b>Uberlândia – MG</b><br/>29 de outubro de 2026</para>",
        ParagraphStyle('CapaData', fontName='Helvetica', fontSize=9.5, leading=13, alignment=1)
    ))
    story.append(PageBreak())

    # PAGINA 2: SUMÁRIO
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
        ("<b>4 CONCLUSÕES</b>", "10"),
        ("<b>REFERÊNCIAS</b>", "10")
    ]
    t_sum_data = [[Paragraph(tit, style_corpo_sem_recuo), Paragraph(pag, ParagraphStyle('SumPag', fontName='Helvetica-Bold', fontSize=9.5, alignment=2))] for tit, pag in sumario_linhas]
    t_sum = Table(t_sum_data, colWidths=[14.2 * cm, 1.8 * cm])
    t_sum.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor("#EEEEEE")),
    ]))
    story.append(t_sum)
    story.append(PageBreak())

    # PAGINA 3: 1 INTRODUÇÃO
    story.append(Paragraph("1 Introdução", style_h1))
    story.append(Paragraph(
        "Transformadores de potência imersos em óleo constituem equipamentos vitais nos sistemas de transmissão e distribuição de energia elétrica. O óleo mineral isolante desempenha dupla função: promover a rigidez dielétrica necessária para suportar elevados gradientes de potencial e atuar como fluido térmico condutor de calor. Em regime operacional contínuo, as flutuações de carga e de temperatura ambiente causam dilatações e contrações volumétricas no óleo, as quais são acomodadas por um vaso de expansão superior denominado <i>conservador de óleo</i>. O monitoramento contínuo e rigoroso do nível de fluido no conservador é indispensável para prevenir sinistros: o nível excessivamente baixo desassiste os enrolamentos, propiciando descargas parciais e queima do isolamento celulósico, ao passo que níveis anormais provocam transbordamento do dielétrico aquecido.",
        style_corpo
    ))
    story.append(Paragraph(
        "Dentre as tecnologias de instrumentação industrial para medição de nível, destacam-se as sondas capacitivas coaxiais. O princípio operacional reside na dependência funcional entre a capacitância estática do sensor e as propriedades dielétricas dos fluidos presentes no espaço intereletródico. A sonda objeto deste estudo é instalada verticalmente cobrindo toda a faixa útil de operação (comprimento H = 0,80 m), sendo constituída por dois condutores coaxiais concêntricos: uma haste central metálica de raio a = 5,0 mm (diâmetro 10,0 mm) protegida por uma capa isolante de politetrafluoretileno (PTFE, permissividade relativa ε_r,capa = 2,1 e espessura inicial t = 0,50 mm, determinando raio externo a + t = 5,5 mm) e um tubo externo metálico vazado aterrado com raio interno b = 15,0 mm (diâmetro interno 30,0 mm). A unidade eletrônica aplica tensão de 5 V de amplitude em baixa frequência e afere a capacitância com resolução de 0,1 pF e fundo de escala de 150 pF.",
        style_corpo
    ))

    if os.path.exists("figura1_esquema.jpeg"):
        img_fig1 = Image("figura1_esquema.jpeg", width=12.0 * cm, height=5.2 * cm)
        story.append(KeepTogether([
            Spacer(1, 0.1 * cm),
            img_fig1,
            Paragraph("Figura 1 – Esquema geométrico da sonda coaxial no interior do conservador: corte longitudinal (com cotas de água decantada hw e óleo) e corte transversal.", style_legenda)
        ]))

    story.append(Paragraph(
        "Com a operação contínua, o ar admitido pelo respiro condensa umidade atmosférica, formando no fundo do vaso uma camada de água decantada (espessura hw) sob o óleo (faixa hw a h). Como a constante dielétrica da água (ε_r = 80) supera enormemente a do óleo mineral (ε_r = 2,2), a presença de água altera drasticamente o sinal elétrico lido. Este trabalho tem como objetivos modelar analiticamente a capacitância da sonda via equações de Maxwell, validar um algoritmo computacional em Python, investigar quantitativamente a anomalia gerada por água decantada e redimensionar a capa isolante para garantir a conformidade operacional.",
        style_corpo
    ))
    story.append(PageBreak())

    # PAGINA 4: 2 DESENVOLVIMENTO (Passo 1 e Quadro-Resumo)
    story.append(Paragraph("2 Desenvolvimento", style_h1))
    story.append(Paragraph(
        "Esta seção apresenta a modelagem eletrostática e as simulações computacionais estruturadas em seis etapas consecutivas, iniciadas pelo quadro-resumo dos resultados na Tabela 1.",
        style_corpo
    ))

    quadro_resumo_data = [
        [Paragraph("Passo", style_tabela_header), Paragraph("Resultado Principal Obtido", style_tabela_header), Paragraph("Saída Associada", style_tabela_header)],
        [Paragraph("Passo 1", style_tabela), Paragraph("Modelagem analítica comprovando série na radial e paralelo na vertical", style_tabela_esq), Paragraph("Figura 1 / Eq. (1)-(3)", style_tabela)],
        [Paragraph("Passo 2", style_tabela), Paragraph("Previsões teóricas de linearidade, atenuação por espessura t e desvio positivo por hw", style_tabela_esq), Paragraph("Texto dedutivo", style_tabela)],
        [Paragraph("Passo 3", style_tabela), Paragraph("Implementação em Python validada com cabo bicamada (C' = 74,6482 pF/m, erro 0,00%)", style_tabela_esq), Paragraph("Tabela 2 / Pseudocódigo", style_tabela)],
        [Paragraph("Passo 4", style_tabela), Paragraph("Calibração óleo limpo: C_vazio = 42,4388 pF, C_cheio = 88,7559 pF, S = 0,5790 pF/cm", style_tabela_esq), Paragraph("Tabela 3 / Figura 2 (G1)", style_tabela)],
        [Paragraph("Passo 5", style_tabela), Paragraph("Anomalia de campo: hw = 2,00 cm induz erro de +29,38 cm; saturação em hw = 9,60 cm", style_tabela_esq), Paragraph("Tabela 4 / Figura 3 (G2)", style_tabela)],
        [Paragraph("Passo 6", style_tabela), Paragraph("Revisão de projeto: PTFE com t = 0,73 mm atende R1 (149,84 pF) e R2 (1,77 mm), atenuando erro por água em 26,2%", style_tabela_esq), Paragraph("Tab. 5-6 / Fig. 4-5 (G3-G4)", style_tabela)]
    ]
    t_qr = Table(quadro_resumo_data, colWidths=[2.2 * cm, 10.4 * cm, 3.4 * cm])
    t_qr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_qr)
    story.append(Paragraph("Tabela 1 – Quadro-resumo do desenvolvimento: etapas, entregas principais e correspondência de saídas.", style_legenda))
    story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph("2.1 Passo 1 – Modelagem Física", style_h2))
    story.append(Paragraph(
        "<b>(a) Regiões materiais:</b> Na coordenada axial z (0 ≤ z ≤ H), a sonda compreende: (1) coluna inferior alagada por água decantada (0 a hw); (2) coluna intermediária de óleo isolante (hw a h); e (3) coluna superior de ar (h a H). Na seção radial transversal, identificam-se duas camadas cilíndricas coaxiais: a camada interna (haste r = a até a + t) formada pela capa sólida (ε_r,capa); e a camada anular externa (a + t até r = b) preenchida pelo fluido circundante (ar, óleo ou água).",
        style_corpo
    ))
    story.append(Paragraph(
        "<b>(b) Condições de fronteira e associação:</b> Na interface cilíndrica entre a capa sólida e o meio fluido (r = a + t), a ausência de cargas livres superficiais (ρ_s = 0) impõe a continuidade rigorosa da componente normal do deslocamento elétrico pela Lei de Gauss: D_1n = D_2n. Pela simetria cilíndrica axial, as linhas de campo são puramente radiais, de modo que o mesmo fluxo de deslocamento atravessa sequencialmente ambas as camadas dielétricas. Como a diferença de potencial total V aplicada entre a haste e o tubo é a soma das quedas de tensão radiais de cada dielétrico (V = V_capa + V_meio), a associação radial configura estritamente uma associação em <b>SÉRIE</b>. Por outro lado, nas interfaces horizontais que separam os fluidos (z = hw e z = h), a condição de contorno eletrostática assegura a continuidade da componente tangencial do campo elétrico: E_1t = E_2t. Haste e tubo são condutores ideais equipotenciais, impondo a mesma d.d.p. V = 5 V a todas as colunas ao longo da altura H. Como a carga total armazenada é a soma direta das cargas em cada trecho (Q = Σ Q_i), a combinação axial opera em <b>PARALELO</b>.",
        style_corpo
    ))
    story.append(Paragraph(
        "<b>(c) Dedução analítica:</b> Aplicando a Lei de Gauss para uma superfície gaussiana cilíndrica de raio r e comprimento unitário, D_r(r) = q' / (2π r) e E_r(r) = q' / (2π ε_0 ε_r r). Integrando o campo elétrico de r = a até r = b para a estrutura bicamada, a capacitância por unidade de comprimento C' = q'/V [F/m] é dada por:",
        style_corpo
    ))
    story.append(Paragraph(
        "<para align='center'><b>C' = 2π ε₀ / [ (1 / ε_{r,capa}) · ln((a + t) / a) + (1 / ε_{r,meio}) · ln(b / (a + t)) ]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(1)</b></para>",
        style_corpo_sem_recuo
    ))
    story.append(Paragraph(
        "Pela associação em paralelo ao longo da altura útil H, a capacitância total com água decantada (0 ≤ hw ≤ h ≤ H) e com óleo limpo (hw = 0) resultam, respectivamente, em:",
        style_corpo
    ))
    story.append(Paragraph(
        "<para align='center'><b>C(h, hw) = C'_água · hw + C'_óleo · (h − hw) + C'_ar · (H − h)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(2)</b></para>"
        "<para align='center'><b>C(h) = C'_ar · H + (C'_óleo − C'_ar) · h&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(3)</b></para>",
        style_corpo_sem_recuo
    ))
    story.append(PageBreak())

    # PAGINA 5: 2.2 Passo 2 e 2.3 Passo 3
    story.append(Paragraph("2.2 Passo 2 – Previsões Físicas", style_h2))
    story.append(Paragraph(
        "Antes da compilação numérica, formularam-se três previsões teóricas fundamentadas na física eletrostática:<br/>"
        "• <b>(a) Forma de C(h) com óleo limpo:</b> Será uma reta linear perfeita com coeficiente angular positivo constante S = C'_óleo − C'_ar e intercepto C_vazio = C'_ar · H, pois a variação de nível corresponde à substituição volumétrica linear de ar por óleo.<br/>"
        "• <b>(b) Efeito da espessura da capa (t):</b> O aumento de t substitui fluido externo por PTFE (ε_r = 2,1). Como em circuitos série a capacitância equivalente é governada pela menor permissividade relativa, aumentar t reduz o contraste entre ar e óleo, diminuindo a sensibilidade S e degradando a resolução mínima detectável Δh_mín.<br/>"
        "• <b>(c) Efeito da água decantada:</b> Com permissividade ε_r = 80 contra ε_r = 2,2 do óleo, a água decantada eleva brutalmente a capacitância C(h, hw). O algoritmo de calibração de óleo limpo interpretará esse acréscimo como uma grande coluna de óleo, indicando um nível MUITO MAIOR que o real. Cada centímetro de água adiciona muito mais capacitância do que 1 cm de óleo.",
        style_corpo
    ))

    story.append(Paragraph("2.3 Passo 3 – Implementação Algorítmica e Validação", style_h2))
    story.append(Paragraph(
        "A modelagem foi programada em Python empregando duas bibliotecas especializadas: (1) <b>numpy</b>, utilizada para cômputo vetorizado eficiente das capacitâncias lineares, arrays de alturas h e hw e matrizes de varredura de materiais e espessuras sem loops lentos; e (2) <b>matplotlib.pyplot</b> (com FuncFormatter), para geração e formatação técnica dos gráficos G1 a G4 com vírgula decimal nos eixos conforme o padrão ABNT. A lógica operacional do código é expressa no pseudocódigo a seguir:",
        style_corpo
    ))

    pseudocodigo_lines = [
        "Algoritmo: Sonda_Capacitiva_Coaxial",
        "Entradas: a = 5 mm, b = 15 mm, H = 0,80 m, eps_r = {ar: 1, oleo: 2.2, agua: 80}",
        "Funcao cap_por_comprimento(raios, eps_camadas):",
        "    denominador = sum([ (1/eps_camadas[k]) * ln(raios[k+1] / raios[k]) ])",
        "    retorne 2 * pi * EPSILON_0 / denominador",
        "Funcao capacitancia_total(h, hw, eps_capa, t):",
        "    C_ar = cap_por_comprimento([a, a+t, b], [eps_capa, eps_ar])",
        "    C_oleo = cap_por_comprimento([a, a+t, b], [eps_capa, eps_oleo])",
        "    C_agua = cap_por_comprimento([a, a+t, b], [eps_capa, eps_agua])",
        "    retorne C_agua * hw + C_oleo * (h - hw) + C_ar * (H - h)",
        "Funcao nivel_indicado(C_medida, eps_capa, t):",
        "    retorne (C_medida - C_ar * H) / (C_oleo - C_ar)  # sem clip para extrapolacao",
        "Executar validacao com cabo bicamada da Aula 08 (assert erro < 0.01%)",
        "Fim_Algoritmo"
    ]
    story.append(Paragraph("<br/>".join(pseudocodigo_lines).replace(" ", "&nbsp;"), style_code_box))

    story.append(Paragraph(
        "A validação da função cap_por_comprimento confrontou os resultados com o exercício do cabo coaxial bicamada da Aula 08 (raios de 1,0 mm, 3,0 mm e 5,0 mm com permissividades relativas 2,1 e 2,3). Os resultados constam na Tabela 2, acusando exatidão analítica plena.",
        style_corpo
    ))

    tab_val_data = [
        [Paragraph("Parâmetro de Teste", style_tabela_header), Paragraph("Valor Teórico Analítico", style_tabela_header), Paragraph("Valor Computado", style_tabela_header), Paragraph("Erro Relativo (%)", style_tabela_header)],
        [Paragraph("Capacitância linear C' (Aula 08)", style_tabela_esq), Paragraph("74,6482 pF/m", style_tabela), Paragraph("74,6482 pF/m", style_tabela), Paragraph("0,0000 %", style_tabela)]
    ]
    t_val = Table(tab_val_data, colWidths=[5.5 * cm, 4.0 * cm, 4.0 * cm, 2.5 * cm])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_val)
    story.append(Paragraph("Tabela 2 – Validação da rotina de cálculo de capacitância coaxial bicamada com dados da Aula 08.", style_legenda))
    story.append(PageBreak())

    # PAGINA 6: 2.4 Passo 4
    story.append(Paragraph("2.4 Passo 4 – Curva de Calibração e Leitura de Campo", style_h2))
    story.append(Paragraph(
        "Avaliando a sonda na configuração inicial de projeto (haste a = 5,0 mm, tubo b = 15,0 mm, capa de PTFE t = 0,50 mm, ε_r = 2,1 e hw = 0), computaram-se as capacitâncias por unidade de comprimento: C'_ar = 53,0485 pF/m, C'_óleo = 110,9449 pF/m e C'_água = 960,3682 pF/m. A Tabela 3 consolida os parâmetros de calibração obtidos e a conversão das leituras de campo.",
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
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_cal)
    story.append(Paragraph("Tabela 3 – Parâmetros de calibração para óleo limpo e conversão das leituras normais de campo.", style_legenda))

    story.append(Paragraph(
        "<b>Verificação de linearidade:</b> O teste numérico comprovou desvio máximo da reta teórica inferior a 1,3 × 10⁻²⁶ F e R² = 1,0000. Fisicamente, como os trechos longitudinais estão associados em paralelo sob mesma d.d.p., substituir um comprimento infinitesimal de ar por óleo incrementa a capacitância total por uma taxa perfeitamente constante dC/dh = S = 0,5790 pF/cm em todo o intervalo.",
        style_corpo
    ))

    if os.path.exists("G1.png"):
        img_g1 = Image("G1.png", width=12.2 * cm, height=6.2 * cm)
        story.append(KeepTogether([
            Spacer(1, 0.1 * cm),
            img_g1,
            Paragraph("Figura 2 – Curva de calibração da sonda C(h) para óleo limpo na configuração inicial (G1), destacando C_vazio, C_cheio e as leituras normais L1, L2 e L3.", style_legenda)
        ]))
    story.append(PageBreak())

    # PAGINA 7: 2.5 Passo 5
    story.append(Paragraph("2.5 Passo 5 – Investigação de Anomalia: Água Decantada", style_h2))
    story.append(Paragraph(
        "Durante inspeção de campo, a verificação física manual por vareta indicou nível real de líquido h_real = 0,45 m, enquanto o sensor acusou capacitância anômala de C = 85,5 pF.<br/>"
        "• <b>(a) Nível indicado e erro de indicação:</b> Pela função inversa de projeto (Eq. 3), o sistema interpretou a medição como h_ind = 0,7438 m (74,38 cm). O erro de medição resultou em <b>Erro = +0,2938 m (+29,38 cm)</b>, superestimando o nível em +65,3%. Esse erro positivo é crítico, pois mascara um nível de óleo potencialmente perigoso no conservador.<br/>"
        "• <b>(b) Determinação da lâmina de água hw:</b> Isolando hw na Equação (2) com h = 0,45 m e C = 85,5 pF, encontrou-se <b>hw = 0,0200 m (2,00 cm)</b>. Uma lâmina de apenas 2 cm de água foi responsável por falsear o nível em quase 30 cm de óleo.<br/>"
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
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_ano)
    story.append(Paragraph("Tabela 4 – Comportamento da sonda em função da lâmina de água decantada (h = 0,45 m).", style_legenda))

    if os.path.exists("G2.png"):
        img_g2 = Image("G2.png", width=12.2 * cm, height=6.0 * cm)
        story.append(KeepTogether([
            Spacer(1, 0.1 * cm),
            img_g2,
            Paragraph("Figura 3 – Erro de indicação de nível hind − hreal versus espessura de água hw para h = 0,45 m (G2), com marcadores de C_cheio e saturação em 150 pF.", style_legenda)
        ]))

    story.append(Paragraph(
        "<b>(d) Hipótese de água sem perdas:</b> A água decantada em equipamentos reais contém eletrólitos dissolvidos (condutividade σ > 0). Sob excitação em 60 Hz, a densidade de corrente é J = (σ + jωε)E. A tangente de perdas tan δ = σ / (ωε) excede enormemente a unidade, caracterizando comportamento condutor predominante (σ >> ωε). O tempo de relaxação dielétrica τ = ε/σ torna-se desprezível, fazendo com que cargas livres blindem o campo elétrico no interior do líquido. A água atua como uma extensão condutora do tubo externo conectada diretamente à capa de PTFE, introduzindo corrente resistiva e alterando a impedância complexa vista pelo circuito.",
        style_corpo
    ))
    story.append(PageBreak())

    # PAGINA 8: 2.6 Passo 6 (Varredura e Escolha)
    story.append(Paragraph("2.6 Passo 6 – Decisão de Projeto: Revisão da Capa Isolante", style_h2))
    story.append(Paragraph(
        "Para impedir a saturação e otimizar o instrumento, reavaliou-se a capa isolante considerando três materiais: PTFE (ε_r = 2,1), Poliimida (ε_r = 3,4) e resina Epóxi (ε_r = 3,6), com espessuras t de 0,20 mm a 1,00 mm (passo 0,01 mm), submetidos aos seguintes critérios:<br/>"
        "• <b>Requisito R1 (Fundo de Escala):</b> C_máx ≤ 150 pF na condição mais severa de tanque cheio (h = H = 0,80 m) com 10 cm de água (hw = 0,10 m).<br/>"
        "• <b>Requisito R2 (Resolução Mínima):</b> Menor variação detectável Δh_mín ≤ 1,8 mm com óleo limpo.<br/>"
        "<b>(a) Avaliação inicial:</b> Para a configuração de projeto (PTFE, t = 0,50 mm), obteve-se C_máx = 960,3682 · 0,10 + 110,9449 · 0,70 = <b>173,6982 pF</b> (> 150 pF, <b>REPROVADO em R1</b>) e Δh_mín = <b>1,7272 mm</b> (≤ 1,8 mm, <b>APROVADO em R2</b>). A capa original satura a eletrônica.<br/>"
        "<b>(b) Varredura paramétrica:</b> A Tabela 5 consolida os dados representativos da varredura executada em Python.",
        style_corpo
    ))

    tab_var_data = [
        [Paragraph("Material Dielétrico", style_tabela_header), Paragraph("t (mm)", style_tabela_header), Paragraph("C_máx (pF) [R1 ≤ 150]", style_tabela_header), Paragraph("Δh_mín (mm) [R2 ≤ 1,8]", style_tabela_header), Paragraph("Sensib. S (pF/cm)", style_tabela_header), Paragraph("Status Global", style_tabela_header)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,20", style_tabela), Paragraph("239,9512", style_tabela), Paragraph("1,6324", style_tabela), Paragraph("0,6126", style_tabela), Paragraph("Reprovado (R1)", style_tabela)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,50", style_tabela), Paragraph("173,6982", style_tabela), Paragraph("1,7272", style_tabela), Paragraph("0,5790", style_tabela), Paragraph("Reprovado (R1)", style_tabela)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,73", style_tabela), Paragraph("149,8448", style_tabela), Paragraph("1,7670", style_tabela), Paragraph("0,5659", style_tabela), Paragraph("<b>APROVADO (Ótimo)</b>", style_tabela)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,80", style_tabela), Paragraph("144,8719", style_tabela), Paragraph("1,7795", style_tabela), Paragraph("0,5620", style_tabela), Paragraph("Aprovado", style_tabela)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,91", style_tabela), Paragraph("138,3767", style_tabela), Paragraph("1,7993", style_tabela), Paragraph("0,5558", style_tabela), Paragraph("Aprovado", style_tabela)],
        [Paragraph("PTFE (ε_r = 2,1)", style_tabela_esq), Paragraph("0,95", style_tabela), Paragraph("136,3390", style_tabela), Paragraph("1,8066", style_tabela), Paragraph("0,5535", style_tabela), Paragraph("Reprovado (R2)", style_tabela)],
        [Paragraph("Poliimida (ε_r = 3,4)", style_tabela_esq), Paragraph("0,80", style_tabela), Paragraph("169,3810", style_tabela), Paragraph("1,7320", style_tabela), Paragraph("0,5774", style_tabela), Paragraph("Reprovado (R1)", style_tabela)],
        [Paragraph("Epóxi (ε_r = 3,6)", style_tabela_esq), Paragraph("0,80", style_tabela), Paragraph("172,9510", style_tabela), Paragraph("1,6320", style_tabela), Paragraph("0,6127", style_tabela), Paragraph("Reprovado (R1)", style_tabela)]
    ]
    t_var = Table(tab_var_data, colWidths=[3.8 * cm, 1.5 * cm, 3.2 * cm, 3.2 * cm, 2.5 * cm, 2.8 * cm])
    t_var.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_var)
    story.append(Paragraph("Tabela 5 – Amostra representativa da varredura paramétrica de materiais e espessuras da capa isolante.", style_legenda))

    if os.path.exists("G3.png"):
        img_g3 = Image("G3.png", width=13.5 * cm, height=5.8 * cm)
        story.append(KeepTogether([
            Spacer(1, 0.1 * cm),
            img_g3,
            Paragraph("Figura 4 – Varredura paramétrica (G3): Painel 1 apresenta C_máx versus t com limite de 150 pF (R1); Painel 2 apresenta Δh_mín versus t com limite de 1,8 mm (R2).", style_legenda)
        ]))

    story.append(Paragraph(
        "<b>(c) Escolha técnica e compromisso de projeto:</b> Poliimida e Epóxi foram reprovados para qualquer espessura até 1,00 mm em R1 devido à alta permissividade (ε_r ≥ 3,4). Para o PTFE, identificaram-se 19 soluções viáveis na faixa t ∈ [0,73 mm; 0,91 mm]. Selecionou-se a espessura <b>t = 0,73 mm em PTFE</b>, pois atende simultaneamente aos requisitos R1 (C_máx = 149,8448 pF ≤ 150 pF) e R2 (Δh_mín = 1,7670 mm ≤ 1,8 mm) e <b>maximiza a sensibilidade ao nível de óleo (S = 0,5659 pF/cm)</b> entre todas as soluções viáveis.",
        style_corpo
    ))
    story.append(PageBreak())

    # PAGINA 9: 2.6 Passo 6 (Comparativo e G4)
    story.append(Paragraph(
        "<b>(d) Comparativo entre configurações:</b> A Tabela 6 sintetiza o confronto direto de desempenho entre a configuração inicial e a final otimizada.",
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
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_comp)
    story.append(Paragraph("Tabela 6 – Confronto comparativo de desempenho metrológico: configuração inicial versus configuração final otimizada.", style_legenda))

    if os.path.exists("G4.png"):
        img_g4 = Image("G4.png", width=12.2 * cm, height=6.2 * cm)
        story.append(KeepTogether([
            Spacer(1, 0.1 * cm),
            img_g4,
            Paragraph("Figura 5 – Curvas de capacitância C versus nível total h para lâminas de água hw = 0, 1 cm e 5 cm (G4): comparação entre configuração inicial (linha contínua) e final (tracejada).", style_legenda)
        ]))

    story.append(Paragraph(
        "A Figura 5 (G4) evidencia que a capa de PTFE com t = 0,73 mm mantém excelente linearidade e paralelismo nas curvas C × h para diferentes espessuras de água hw, enquanto desloca as curvas para patamares inferiores de capacitância. Esse recuo garante margem operacional segura frente à linha limite de fundo de escala de 150 pF, reduzindo a vulnerabilidade da instrumentação à água decantada em 26,24%.",
        style_corpo
    ))
    story.append(PageBreak())

    # PAGINA 10: 3 ANÁLISE CRÍTICA, 4 CONCLUSÕES E REFERÊNCIAS
    story.append(Paragraph("3 Análise Crítica", style_h1))
    story.append(Paragraph(
        "O confronto entre as previsões formuladas no Passo 2 e os resultados das simulações comprovou total coerência físico-matemática: a linearidade de C(h) foi assegurada com R² = 1,0000, o aumento da espessura t reduziu moderadamente a sensibilidade S e atenuou a capacitância de saturação, e o impacto anômalo da água livre foi confirmado pelo erro positivo expressivo de +29,38 cm.",
        style_corpo
    ))
    story.append(Paragraph(
        "Entretanto, a aplicação prática em transformadores de subestação envolve restrições decorrentes das hipóteses simplificadoras:<br/>"
        "1. <b>Efeitos de borda e parasitas:</b> O campo tridimensional disperso nos extremos da sonda e as capacitâncias parasitas dos cabos blindados de conexão introduzem um offset aditivo que deve ser compensado por calibração de zero no comissionamento.<br/>"
        "2. <b>Excentricidade radial:</b> Qualquer desalinhamento mecânico do eixo da haste central aproxima localmente os eletrodos, elevando a capacitância e o campo elétrico radial.<br/>"
        "3. <b>Sensibilidade térmica:</b> A temperatura do óleo (20 °C a 90 °C) provoca dilatação volumétrica e decréscimo térmico da constante dielétrica do óleo mineral (cerca de −0,001/°C), exigindo sensores PT100 auxiliares para compensação dinâmica.<br/>"
        "4. <b>Perdas dielétricas da água:</b> Como a água é condutora (σ > 0), a ponte de medição mede admitância complexa Y = G + jωC. Em baixa frequência, a corrente resistiva de fuga pode sobrecarregar o circuito de medição.",
        style_corpo
    ))

    story.append(Paragraph("4 Conclusões", style_h1))
    story.append(Paragraph(
        "Este trabalho desenvolveu a modelagem analítica e computacional completa de uma sonda capacitiva coaxial para conservadores de transformadores de potência. O algoritmo implementado em Python foi validado com erro nulo frente ao modelo de referência da Aula 08. Constatou-se que a configuração inicial em PTFE de 0,50 mm viola a segurança operacional ao atingir C_máx = 173,70 pF em presença de 10 cm de água decantada.<br/>"
        "A revisão de projeto selecionou com sucesso o <b>PTFE com espessura otimizada t = 0,73 mm</b>, que atende rigorosamente a R1 (C_máx = 149,84 pF ≤ 150 pF) e R2 (Δh_mín = 1,77 mm ≤ 1,8 mm), maximizando a sensibilidade útil ao óleo (S = 0,5659 pF/cm) e <b>reduzindo em 26,24% a interferência de água decantada</b>. A solução garante confiabilidade metrológica à proteção do transformador.",
        style_corpo
    ))

    story.append(Paragraph("Referências", style_h1))
    story.append(Paragraph(
        "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. <b>NBR 5356-2</b>: Transformadores de potência - Parte 2: Elevação de temperatura. Rio de Janeiro: ABNT, 2008.<br/>"
        "HAYT JR., William H.; BUCK, John A. <b>Eletromagnetismo</b>. 8. ed. Porto Alegre: AMGH, 2013.<br/>"
        "KUFFEL, E.; ZAENGL, W. S.; KUFFEL, J. <b>High Voltage Engineering: Fundamentals</b>. 2. ed. Oxford: Newnes, 2000.<br/>"
        "PASSATUTO, Luiz Arthur Tarralo. <b>Slides das aulas da disciplina FEELT31405 – Eletromagnetismo</b>. Uberlândia: Faculdade de Engenharia Elétrica, Universidade Federal de Uberlândia, 2026. Material didático.",
        style_corpo_sem_recuo
    ))

    doc.build(story, canvasmaker=ABNTNumberedCanvas)
    print(f"Relatório ABNT compilado com sucesso: {pdf_filename}")


if __name__ == "__main__":
    compilar_relatorio()

