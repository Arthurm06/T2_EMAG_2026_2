"""Trabalho 1 de Eletromagnetismo: sonda capacitiva de nivel.

Autores: Arthur Montes Cuoco e Luis Gustavo Oliveira Sena
Dependencias: numpy e matplotlib
Execucao: python T1_EM_ARTHUR_LUIS.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Constantes e dimensoes da sonda, em unidades do SI.
EPS_0 = 8.854e-12       # permissividade do vacuo (F/m)
H = 0.80                # comprimento util da sonda (m)

# Os diametros informados no enunciado sao 10 mm e 30 mm.
a = 0.0050              # raio da haste central (m) = 5.0 mm
b = 0.0150              # raio interno do tubo externo (m) = 15.0 mm

# Capa isolante inicial.
t_init = 0.00050        # espessura inicial PTFE: 0.50 mm (m)
eps_ptfe = 2.1          # permissividade relativa do PTFE
eps_poliimida = 3.4     # poliimida (passo 6)
eps_epoxi = 3.6         # epoxi (passo 6)

# Permissividades relativas dos meios.
eps_ar = 1.0
eps_oleo = 2.2
eps_agua = 80.0

# Especificacoes da eletronica.
res_eletronica = 0.1e-12    # resolucao de 0.1 pF (F)
fundo_escala = 150.0e-12    # fundo de escala de 150 pF (F)


def fmt_virgula(x, pos):
    """Formata os valores dos eixos com virgula decimal."""
    if abs(x) < 1e-12:
        return '0'
    return f"{x:g}".replace('.', ',')

formatter_virgula = FuncFormatter(fmt_virgula)


# Passo 1 - Modelagem fisica.
def passo1():
    print("=" * 60)
    print("Passo 1: Modelagem fisica da sonda e hipoteses")
    print("=" * 60)
    print("1. Regioes geometricas:")
    print("   - Haste condutora interna: r = a = 5,0 mm")
    print("   - Capa isolante protetora: de r = a ate a + t")
    print("   - Meio fluido (ar, oleo ou agua decantada): de a + t ate b = 15,0 mm")
    print("   - Tubo condutor externo (vazado): r = b")
    print("\n2. Condicoes de fronteira e associacao:")
    print("   - Direcao radial: continuidade da componente normal de D (sem cargas livres na interface).")
    print("     O fluxo de D e radial e unico atravessando a capa e o fluido -> associacao em SERIE (Eq. 1 e 2).")
    print("   - Direcao axial: continuidade de E tangencial nas interfaces horizontais.")
    print("     A diferenca de potencial aplicada e a mesma (5 V) em todas as colunas de liquido/ar -> associacao em PARALELO (Eq. 3, 4 e 5).")
    print("\n3. Hipoteses adotadas:")
    print("   - Regime quase-estatico (aproximacao eletrostatica valida em baixa frequencia).")
    print("   - Meios lineares, homogeneos, isotropicos e sem perdas.")
    print("   - Superficies de separacao planas e horizontais (efeitos de menisco/ondas desprezados).")
    print("   - Efeitos de borda e capacitancias parasitas de cabos despreziveis.")
    print("   - Sonda perfeitamente concentrica e vertical; condutores ideais (equipotenciais).")
    print("-" * 60 + "\n")


# Passo 2 - Previsoes fisicas.
def passo2():
    print("=" * 60)
    print("Passo 2: Previsoes fisicas (antes de rodar os calculos)")
    print("=" * 60)
    print("(a) Curva C(h) com oleo limpo:")
    print("    Sera uma reta perfeitamente linear, pois resulta da combinacao em paralelo")
    print("    de duas colunas (oleo e ar) cujos comprimentos variam linearmente com h.")
    print("(b) Aumento da espessura da capa (t):")
    print("    Reduz a capacitancia por unidade de comprimento e a diferenca entre C'_oleo e C'_ar,")
    print("    portanto a sensibilidade S diminui e a resolucao Delta_h_min piora (aumenta em mm).")
    print("(c) Presenca de agua decantada (hw):")
    print("    Como eps_r da agua e 80 (muito superior a 2,2 do oleo), a presenca de agua eleva")
    print("    bastante a capacitancia. A sonda indicara um nivel MUITO MAIOR que o real.")
    print("    1 cm de agua contribui muito mais para C do que 1 cm de oleo.")
    print("-" * 60 + "\n")


# Passo 3 - Funcoes de modelagem e validacao.
def cap_por_comprimento(raios, eps_r):
    """Calcula a capacitancia por metro de camadas coaxiais em serie."""
    r = np.asarray(raios, dtype=float)
    eps = np.asarray(eps_r, dtype=float)
    # somatorio de (1/eps_k) * ln(r_{k+1} / r_k)
    denominador = np.sum((1.0 / eps) * np.log(r[1:] / r[:-1]))
    return float(2.0 * np.pi * EPS_0 / denominador)


def capacitancia_total(h, hw, eps_capa, t):
    """Calcula a capacitancia total dos trechos de agua, oleo e ar."""
    raios = [a, a + t, b]
    c_ar = cap_por_comprimento(raios, [eps_capa, eps_ar])
    c_oleo = cap_por_comprimento(raios, [eps_capa, eps_oleo])
    c_agua = cap_por_comprimento(raios, [eps_capa, eps_agua])

    # Os trechos verticais ficam associados em paralelo.
    return c_agua * hw + c_oleo * (h - hw) + c_ar * (H - h)


def nivel_indicado(C_medida, eps_capa, t):
    """Inverte a calibracao de oleo limpo para obter o nivel indicado."""
    raios = [a, a + t, b]
    c_ar = cap_por_comprimento(raios, [eps_capa, eps_ar])
    c_oleo = cap_por_comprimento(raios, [eps_capa, eps_oleo])

    c_vazio = c_ar * H
    sensibilidade = c_oleo - c_ar
    return (C_medida - c_vazio) / sensibilidade


def passo3():
    print("=" * 60)
    print("Passo 3: Validacao do modelo (cabo bicamada Aula 08)")
    print("=" * 60)

    # Dados do problema final da Aula 08:
    r_val = [0.001, 0.003, 0.005]  # raios 1 mm, 3 mm e 5 mm
    eps_val = [2.1, 2.3]
    c_ref = 74.6482e-12            # ~74,6 pF/m

    c_calc = cap_por_comprimento(r_val, eps_val)
    erro_rel = abs(c_calc - c_ref) / c_ref * 100.0

    print(f"{'Grandeza':<25} | {'Obtido':<12} | {'Referencia':<12} | {'Erro Rel. (%)':<10}")
    print("-" * 65)
    print(f"{'C/L (pF/m)':<25} | {c_calc * 1e12:<12.4f} | {c_ref * 1e12:<12.4f} | {erro_rel:<10.4f}")

    assert erro_rel < 0.05, f"Erro na validacao do Passo 3: {erro_rel:.4f}%"
    print("Resultado: Validacao aprovada (assert OK).\n")


# Passo 4 - Calibracao e leituras de campo.
def passo4():
    print("=" * 60)
    print("Passo 4: Curva de calibracao (oleo limpo, config inicial)")
    print("=" * 60)

    raios_init = [a, a + t_init, b]
    cp_ar = cap_por_comprimento(raios_init, [eps_ptfe, eps_ar])
    cp_oleo = cap_por_comprimento(raios_init, [eps_ptfe, eps_oleo])
    cp_agua = cap_por_comprimento(raios_init, [eps_ptfe, eps_agua])

    # (a) Capacitancias caracteristicas e sensibilidade.
    c_vazio = cp_ar * H
    c_cheio = cp_oleo * H
    S_si = cp_oleo - cp_ar
    S_pf_cm = S_si * 1e12 / 100.0

    print(f"Passo 4 (a): C_vazio  = {c_vazio * 1e12:.4f} pF")
    print(f"Passo 4 (a): C_cheio  = {c_cheio * 1e12:.4f} pF")
    print(f"Passo 4 (a): Sensibilidade S = {S_pf_cm:.4f} pF/cm ({S_si * 1e12:.4f} pF/m)")
    print(f"            (C'_ar = {cp_ar * 1e12:.4f} pF/m, C'_oleo = {cp_oleo * 1e12:.4f} pF/m, C'_agua = {cp_agua * 1e12:.4f} pF/m)")

    # Verificacoes dos valores de referencia.
    assert abs(c_vazio * 1e12 - 42.4388) < 0.01
    assert abs(c_cheio * 1e12 - 88.7559) < 0.01
    assert abs(S_pf_cm - 0.5790) < 0.005

    # (b) Teste numerico de linearidade.
    h_vetor = np.linspace(0, H, 100)
    c_vetor = capacitancia_total(h_vetor, 0, eps_ptfe, t_init)
    c_reta = c_vazio + S_si * h_vetor
    desvio_max = np.max(np.abs(c_vetor - c_reta))
    r2 = 1.0 - np.sum((c_vetor - c_reta)**2) / np.sum((c_vetor - np.mean(c_vetor))**2)

    print(f"Passo 4 (b): Desvio maximo da reta = {desvio_max:.4e} F (R2 = {r2:.4f})")
    print("             Explicacao: A resposta e perfeitamente linear porque a capacitancia equivale")
    print("             a soma de duas colunas associadas em paralelo com comprimentos lineares em h.")

    # (c) Niveis para as leituras de campo.
    leituras = [54.0e-12, 68.5e-12, 83.0e-12]
    nomes_l = ['L1', 'L2', 'L3']
    h_leituras = []
    for nome, l in zip(nomes_l, leituras):
        h_l = nivel_indicado(l, eps_ptfe, t_init)
        h_leituras.append(h_l)
        print(f"Passo 4 (c): {nome} ({l*1e12:.1f} pF) -> h = {h_l:.4f} m ({h_l*100:.4f} cm)")

    assert abs(h_leituras[0] - 0.1997) < 0.001
    assert abs(h_leituras[1] - 0.4501) < 0.001
    assert abs(h_leituras[2] - 0.7006) < 0.001

    # (d) Menor variacao de nivel distinguivel.
    dh_min = res_eletronica / S_si
    dh_min_mm = dh_min * 1000.0
    print(f"Passo 4 (d): Delta_h_min = {dh_min_mm:.4f} mm ({dh_min:.4e} m)")
    assert abs(dh_min_mm - 1.7272) < 0.005

    # Grafico G1.
    plt.figure(figsize=(7.5, 5))
    h_plot = np.linspace(0, H, 200)
    c_plot_pf = capacitancia_total(h_plot, 0, eps_ptfe, t_init) * 1e12

    plt.plot(h_plot, c_plot_pf, color='royalblue', lw=2, label='Curva de calibracao C(h)')
    plt.scatter([0], [c_vazio * 1e12], color='tab:orange', s=50, zorder=4,
                label=f'C_vazio = {c_vazio*1e12:.4f} pF')
    plt.scatter([H], [c_cheio * 1e12], color='tab:green', s=50, zorder=4,
                label=f'C_cheio = {c_cheio*1e12:.4f} pF')

    cores = ['red', 'purple', 'teal']
    for idx, (hl, l_val, rot) in enumerate(zip(h_leituras, leituras, nomes_l)):
        plt.scatter([hl], [l_val * 1e12], color=cores[idx], s=40, zorder=5,
                    label=f'{rot} = {l_val*1e12:.1f} pF (h = {hl:.4f} m)')
        plt.vlines(hl, c_vazio * 1e12, l_val * 1e12, colors=cores[idx], linestyles=':')
        plt.hlines(l_val * 1e12, 0, hl, colors=cores[idx], linestyles=':')

    plt.title('G1: Curva de Calibração da Sonda (Óleo Limpo - Configuração Inicial)')
    plt.xlabel('Nível de líquido h (m)')
    plt.ylabel('Capacitância total C (pF)')
    plt.gca().xaxis.set_major_formatter(formatter_virgula)
    plt.gca().yaxis.set_major_formatter(formatter_virgula)
    plt.xlim(-0.02, H + 0.03)
    plt.ylim(c_vazio * 1e12 - 5, c_cheio * 1e12 + 6)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='lower right', fontsize=8.5)
    plt.tight_layout()
    plt.savefig('G1.png', dpi=200)
    plt.close()
    print("Salvo: G1.png\n")

    return cp_ar, cp_oleo, cp_agua, c_vazio, c_cheio, S_si


# Passo 5 - Investigacao da anomalia com agua decantada.
def passo5(cp_ar, cp_oleo, cp_agua, c_vazio, c_cheio, S_si):
    print("=" * 60)
    print("Passo 5: Anomalia com agua decantada (config inicial)")
    print("=" * 60)

    h_real = 0.45
    c_med = 85.5e-12

    # (a) Nivel indicado e erro.
    h_ind = nivel_indicado(c_med, eps_ptfe, t_init)
    erro = h_ind - h_real

    print(f"Passo 5 (a): Nivel indicado h_ind = {h_ind:.4f} m ({h_ind*100:.4f} cm)")
    print(f"Passo 5 (a): Erro de medicao       = {erro:+.4f} m ({erro*100:+.4f} cm)")
    assert abs(h_ind - 0.7438) < 0.001
    assert abs(erro - 0.2938) < 0.001

    # (b) Espessura de agua hw coerente.
    hw_calc = (c_med - c_vazio - S_si * h_real) / (cp_agua - cp_oleo)
    print(f"Passo 5 (b): Camada de agua hw    = {hw_calc:.4f} m ({hw_calc*100:.4f} cm)")
    assert abs(hw_calc - 0.0200) < 0.001

    # (c) Limites de hw e extrapolacao.
    c_045_0 = cp_oleo * h_real + cp_ar * (H - h_real)
    hw_lim_cheio = (c_cheio - c_045_0) / (cp_agua - cp_oleo)
    hw_lim_150 = (fundo_escala - c_045_0) / (cp_agua - cp_oleo)

    print(f"Passo 5 (c): C(0,45; 0)           = {c_045_0 * 1e12:.4f} pF")
    print(f"Passo 5 (c): hw para C > C_cheio  = {hw_lim_cheio * 100:.4f} cm ({hw_lim_cheio:.4f} m)")
    print(f"Passo 5 (c): hw para C > 150 pF   = {hw_lim_150 * 100:.4f} cm ({hw_lim_150:.4f} m)")

    assert abs(c_045_0 * 1e12 - 68.4922) < 0.01
    assert abs(hw_lim_cheio * 100 - 2.3856) < 0.01
    assert abs(hw_lim_150 * 100 - 9.5957) < 0.01

    # Erro com 1 cm de agua.
    c_1cm = capacitancia_total(h_real, 0.01, eps_ptfe, t_init)
    erro_1cm = nivel_indicado(c_1cm, eps_ptfe, t_init) - h_real
    print(f"Passo 5 (c): Erro por 1 cm de agua = {erro_1cm:+.4f} m ({erro_1cm*100:+.4f} cm)")

    # (d) Observacao sobre agua real.
    print("\nPasso 5 (d): [Nota sobre agua real com perdas]")
    print("             A agua livre decantada possui condutividade ionica (sigma > 0).")
    print("             Em baixa frequencia, a corrente de conducao pode superar a de deslocamento,")
    print("             gerando perdas dieletricas e alterando a impedancia lida pela ponte medidora.")
    print("             A discussao teorica aprofundada consta no relatorio.")

    # Grafico G2.
    plt.figure(figsize=(7.5, 5))
    hw_sweep = np.linspace(0, 0.10, 200)
    c_hw = capacitancia_total(h_real, hw_sweep, eps_ptfe, t_init)
    erro_hw = nivel_indicado(c_hw, eps_ptfe, t_init) - h_real

    plt.plot(hw_sweep * 100, erro_hw, color='crimson', lw=2, label='Erro (extrapolacao matematica)')
    plt.axvline(hw_lim_cheio * 100, color='darkorange', linestyle='--', lw=1.5,
                label=f'hw (C > C_cheio) = {hw_lim_cheio*100:.2f} cm')
    plt.axvline(hw_lim_150 * 100, color='purple', linestyle='-.', lw=1.5,
                label=f'hw (C > 150 pF) = {hw_lim_150*100:.2f} cm')
    plt.scatter([hw_calc * 100], [erro], color='blue', s=45, zorder=5,
                label=f'Ponto medido (hw = {hw_calc*100:.2f} cm, erro = {erro:+.4f} m)')

    plt.title('G2: Erro de Indicação de Nível versus Espessura de Água (h = 0,45 m)')
    plt.xlabel('Espessura da camada de água decantada hw (cm)')
    plt.ylabel('Erro de indicação h_ind - h_real (m)')
    plt.gca().xaxis.set_major_formatter(formatter_virgula)
    plt.gca().yaxis.set_major_formatter(formatter_virgula)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left', fontsize=8.5)
    plt.tight_layout()
    plt.savefig('G2.png', dpi=200)
    plt.close()
    print("Salvo: G2.png\n")

    return erro_1cm


# Passo 6 - Revisao de projeto da capa isolante.
def passo6(erro_1cm_init):
    print("=" * 60)
    print("Passo 6: Revisao da capa isolante da sonda")
    print("=" * 60)

    # (a) Verificacao da configuracao inicial.
    raios_init = [a, a + t_init, b]
    cp_ar_init = cap_por_comprimento(raios_init, [eps_ptfe, eps_ar])
    cp_oleo_init = cap_por_comprimento(raios_init, [eps_ptfe, eps_oleo])
    cp_agua_init = cap_por_comprimento(raios_init, [eps_ptfe, eps_agua])

    # R1: conservador cheio com 10 cm de agua.
    c_max_init = cp_agua_init * 0.10 + cp_oleo_init * (H - 0.10)
    dh_min_init_mm = (res_eletronica / (cp_oleo_init - cp_ar_init)) * 1000.0

    stat_r1_init = "APROVADO" if c_max_init <= fundo_escala else "REPROVADO"
    stat_r2_init = "APROVADO" if dh_min_init_mm <= 1.8 else "REPROVADO"

    print("Passo 6 (a): Verificacao da config inicial:")
    print(f"             C_max (R1 <= 150 pF) = {c_max_init * 1e12:.4f} pF -> {stat_r1_init}")
    print(f"             Delta_h (R2 <= 1,8 mm) = {dh_min_init_mm:.4f} mm -> {stat_r2_init}")

    assert abs(c_max_init * 1e12 - 173.6982) < 0.01
    assert stat_r1_init == "REPROVADO"
    assert stat_r2_init == "APROVADO"

    # (b) Varredura de materiais e espessuras.
    materiais = {
        'PTFE': eps_ptfe,
        'Poliimida': eps_poliimida,
        'Epoxi': eps_epoxi
    }
    t_vetor = np.round(np.arange(0.00020, 0.0010001, 0.00001), 5)

    dados_plot = {}
    validas = []

    for nome_mat, eps_mat in materiais.items():
        c_max_vals = []
        dh_vals = []
        s_vals = []

        for t_val in t_vetor:
            raios_sw = [a, a + t_val, b]
            c_ar_sw = cap_por_comprimento(raios_sw, [eps_mat, eps_ar])
            c_oleo_sw = cap_por_comprimento(raios_sw, [eps_mat, eps_oleo])
            c_agua_sw = cap_por_comprimento(raios_sw, [eps_mat, eps_agua])

            # R1: capacitancia maxima na condicao mais severa.
            c_max_sw = c_agua_sw * 0.10 + c_oleo_sw * (H - 0.10)
            # R2: menor variacao detectavel com oleo limpo.
            s_sw = c_oleo_sw - c_ar_sw
            s_cm = s_sw * 1e12 / 100.0
            dh_sw_mm = (res_eletronica / s_sw) * 1000.0

            r1_ok = (c_max_sw <= fundo_escala)
            r2_ok = (dh_sw_mm <= 1.8)

            reg = {
                'mat': nome_mat, 'eps': eps_mat,
                't_mm': t_val * 1000.0, 't_m': t_val,
                'C_max': c_max_sw * 1e12, 'dh_min': dh_sw_mm,
                'S_cm': s_cm, 'valido': r1_ok and r2_ok
            }
            if r1_ok and r2_ok:
                validas.append(reg)

            c_max_vals.append(c_max_sw * 1e12)
            dh_vals.append(dh_sw_mm)
            s_vals.append(s_cm)

        dados_plot[nome_mat] = {
            'C_max': np.array(c_max_vals),
            'dh_min': np.array(dh_vals),
            'S': np.array(s_vals)
        }

    # (c) Escolha da maior sensibilidade entre as configuracoes validas.
    print(f"\nPasso 6 (c): Configuracoes que atendem R1 e R2: {len(validas)}")
    validas.sort(key=lambda x: x['S_cm'], reverse=True)
    escolhida = validas[0]

    print("\nTabela de configuracoes validas:")
    print(f"{'Material':<12} | {'t (mm)':<8} | {'C_max (pF)':<12} | {'Delta_h (mm)':<12} | {'S (pF/cm)':<10}")
    print("-" * 65)
    for v in validas:
        print(f"{v['mat']:<12} | {v['t_mm']:<8.2f} | {v['C_max']:<12.4f} | {v['dh_min']:<12.4f} | {v['S_cm']:<10.4f}")

    print("\n--> Configuracao final selecionada:")
    print(f"    Material : {escolhida['mat']} (eps_r = {escolhida['eps']:.1f})")
    print(f"    Espessura: t = {escolhida['t_mm']:.2f} mm")
    print(f"    C_max    : {escolhida['C_max']:.4f} pF (R1 <= 150 pF: OK)")
    print(f"    Delta_h  : {escolhida['dh_min']:.4f} mm (R2 <= 1,8 mm: OK)")
    print(f"    Sensib. S: {escolhida['S_cm']:.4f} pF/cm")

    # (d) Recalibracao da configuracao final.
    t_fin = escolhida['t_m']
    eps_fin = escolhida['eps']
    raios_fin = [a, a + t_fin, b]

    cp_ar_fin = cap_por_comprimento(raios_fin, [eps_fin, eps_ar])
    cp_oleo_fin = cap_por_comprimento(raios_fin, [eps_fin, eps_oleo])
    c_vazio_fin = cp_ar_fin * H
    c_cheio_fin = cp_oleo_fin * H
    S_fin_si = cp_oleo_fin - cp_ar_fin

    # Erro com 1 cm de agua na configuracao final.
    c_1cm_fin = capacitancia_total(0.45, 0.01, eps_fin, t_fin)
    erro_1cm_fin = nivel_indicado(c_1cm_fin, eps_fin, t_fin) - 0.45

    print("\nPasso 6 (d): Comparacao Config. Inicial vs. Config. Final:")
    print(f"{'Item':<28} | {'Inicial (PTFE 0,50mm)':<22} | {'Final (PTFE 0,73mm)':<22}")
    print("-" * 78)
    print(f"{'C_vazio (pF)':<28} | {cp_ar_init * H * 1e12:<22.4f} | {c_vazio_fin * 1e12:<22.4f}")
    print(f"{'C_cheio (pF)':<28} | {cp_oleo_init * H * 1e12:<22.4f} | {c_cheio_fin * 1e12:<22.4f}")
    print(f"{'S (pF/cm)':<28} | {(cp_oleo_init - cp_ar_init)*1e12/100:<22.4f} | {S_fin_si * 1e12 / 100:<22.4f}")
    print(f"{'Delta_h_min (mm)':<28} | {dh_min_init_mm:<22.4f} | {escolhida['dh_min']:<22.4f}")
    print(f"{'C_max (condicao R1) (pF)':<28} | {c_max_init * 1e12:<22.4f} | {escolhida['C_max']:<22.4f}")
    print(f"{'Erro p/ 1 cm agua (m)':<28} | {erro_1cm_init:<+22.4f} | {erro_1cm_fin:<+22.4f}")
    print(f"Reducao no impacto da agua: {(1 - erro_1cm_fin/erro_1cm_init)*100:.2f}%")

    # Grafico G3.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    t_mm_plot = t_vetor * 1000.0

    estilos = {'PTFE': ('blue', '-'), 'Poliimida': ('green', '--'), 'Epoxi': ('magenta', '-.')}
    for mat, (cor, traço) in estilos.items():
        ax1.plot(t_mm_plot, dados_plot[mat]['C_max'], label=mat, color=cor, linestyle=traço)
        ax2.plot(t_mm_plot, dados_plot[mat]['dh_min'], label=mat, color=cor, linestyle=traço)

    ax1.axhline(150.0, color='red', linestyle=':', label='Limite R1 (150 pF)')
    ax1.set_title('Capacitância Máxima (R1) vs. Espessura')
    ax1.set_xlabel('Espessura da capa t (mm)')
    ax1.set_ylabel('C_máx na condição mais crítica (pF)')
    ax1.xaxis.set_major_formatter(formatter_virgula)
    ax1.yaxis.set_major_formatter(formatter_virgula)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='upper right', fontsize=8.5)

    ax2.axhline(1.8, color='red', linestyle=':', label='Limite R2 (1,8 mm)')
    ax2.set_title('Resolução Mínima (R2) vs. Espessura')
    ax2.set_xlabel('Espessura da capa t (mm)')
    ax2.set_ylabel('Delta_h_mín com óleo limpo (mm)')
    ax2.xaxis.set_major_formatter(formatter_virgula)
    ax2.yaxis.set_major_formatter(formatter_virgula)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(loc='upper left', fontsize=8.5)

    plt.suptitle('G3: Varredura de Materiais e Espessuras da Capa Isolante')
    plt.tight_layout()
    plt.savefig('G3.png', dpi=200)
    plt.close()
    print("Salvo: G3.png")

    # Grafico G4.
    plt.figure(figsize=(7.5, 5.2))
    cenarios_hw = [0.0, 0.01, 0.05]
    cores_cen = ['navy', 'darkorange', 'purple']

    for hw_val, cor in zip(cenarios_hw, cores_cen):
        # O nivel total precisa ser maior ou igual a hw.
        h_range = np.linspace(hw_val, H, 200)
        c_i = capacitancia_total(h_range, hw_val, eps_ptfe, t_init) * 1e12
        c_f = capacitancia_total(h_range, hw_val, eps_fin, t_fin) * 1e12

        lbl_i = f'Inicial: hw = {int(hw_val*100)} cm'
        lbl_f = f'Final: hw = {int(hw_val*100)} cm'
        plt.plot(h_range, c_i, color=cor, linestyle='-', lw=1.8, label=lbl_i)
        plt.plot(h_range, c_f, color=cor, linestyle='--', lw=1.8, label=lbl_f)

    plt.axhline(150.0, color='red', linestyle=':', label='Fundo de escala (150 pF)')
    plt.title('G4: Comparação C x h (Inicial contínua vs Final tracejada)')
    plt.xlabel('Nível total de líquido h (m)')
    plt.ylabel('Capacitância total C (pF)')
    plt.gca().xaxis.set_major_formatter(formatter_virgula)
    plt.gca().yaxis.set_major_formatter(formatter_virgula)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left', fontsize=8.5, ncol=2)
    plt.tight_layout()
    plt.savefig('G4.png', dpi=200)
    plt.close()
    print("Salvo: G4.png\n")


# Execucao sequencial.
def main():
    print("Iniciando execucao do script de Eletromagnetismo...\n")
    passo1()
    passo2()
    passo3()
    cp_ar, cp_oleo, cp_agua, c_vazio, c_cheio, S_si = passo4()
    erro_1cm_init = passo5(cp_ar, cp_oleo, cp_agua, c_vazio, c_cheio, S_si)
    passo6(erro_1cm_init)
    print("Processamento finalizado com sucesso!")


if __name__ == "__main__":
    main()
