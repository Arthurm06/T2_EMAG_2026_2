"""
===============================================================================
Trabalho 2 – Análise do Núcleo Magnético de um Transformador de Isolamento
Disciplina : Eletromagnetismo (FEELT31405, UFU / FEELT, 2026-2)
Professor  : Luiz Arthur Tarralo Passatuto
Turma      : FEELT31411
Data       : 08/12/2026
Integrantes:
  - Arthur Montes Cuoco - 12411EEL028
  - Luis Gustavo Oliveira Sena - 12211FIS210

Dependências:
  - Python 3.x
  - numpy       (cálculo numérico e vetorial)
  - matplotlib  (geração dos gráficos G1, G2 e G3)

Modo de execução:
  python T2_EM_ARTHUR_LUIS.py

Ao ser executado do início ao fim sem intervenção, o script imprime os
resultados numéricos identificados como "Passo N (item)" e gera os gráficos
G1.png, G2.png e G3.png no diretório de trabalho.
===============================================================================
"""

import os
import numpy as np              # Operações matemáticas e vetores para curvas
import matplotlib.pyplot as plt # Plotagem dos gráficos obrigatórios G1, G2 e G3
import matplotlib.ticker as ticker

# Configuração global do matplotlib para usar vírgula como separador decimal
plt.rcParams["axes.formatter.use_locale"] = False
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.size"] = 10

# -----------------------------------------------------------------------------
# Parâmetros físicos e geométricos do problema (Tabela 1 do roteiro)
# -----------------------------------------------------------------------------
MU0 = 4.0 * np.pi * 1e-7        # Permeabilidade magnética do vácuo [H/m]
L_FE = 0.24                     # Comprimento médio do percurso no núcleo [m]
AREA = 3.00e-4                  # Área da seção transversal (3,00 cm²) [m²]
I_ENSAIO = 0.40                 # Corrente contínua imposta no ensaio [A]
N_INICIAL = 200                 # Número de espiras da configuração inicial
G_INICIAL = 0.10e-3             # Entreferro nominal inicial (0,10 mm) [m]
DELTA_G = 0.15e-3               # Acréscimo máximo de tolerância na junta [m]
L_MIN_R1 = 50.0e-3              # Requisito R1: indutância mínima (50,0 mH) [H]
FATOR_R2 = 0.80                 # Requisito R2: B <= 80% do limite do material

# Dicionário com propriedades dos três materiais hipotéticos de referência
MATERIAIS = {
    "Ferrite":     {"mu_r": 2200.0, "B_lim": 0.35},
    "Aço-silício": {"mu_r": 1500.0, "B_lim": 1.40},
    "Pó de ferro": {"mu_r": 125.0,  "B_lim": 0.90},
}


def fmt(valor: float, casas: int = 4) -> str:
    """Formata número float com vírgula decimal para exibição padronizada."""
    return f"{valor:.{casas}f}".replace(".", ",")


def formatador_virgula(x, pos):
    """Formatter do matplotlib para exibir eixos numéricos com vírgula."""
    return f"{x:g}".replace(".", ",")


# -----------------------------------------------------------------------------
# Funções do modelo físico (Passo 3a, 3b, 3c)
# -----------------------------------------------------------------------------

def calcular_relutancias_e_B(N: int, mu_r: float, g: float,
                             I: float = I_ENSAIO,
                             l_fe: float = L_FE,
                             A: float = AREA) -> tuple:
    """Passo 3 (a): Calcula relutâncias parciais, total e densidade de fluxo B.

    Retorna (R_fe, R_g, R_total, B) em unidades do SI ([H^-1], [H^-1], [H^-1], [T]).
    """
    R_fe = l_fe / (MU0 * mu_r * A)     # Relutância do núcleo [H^-1]
    R_g = g / (MU0 * A)                # Relutância do entreferro [H^-1]
    R_total = R_fe + R_g               # Associação série no circuito magnético
    phi = (N * I) / R_total            # Fluxo magnético [Wb]
    B = phi / A                        # Densidade de fluxo uniforme na seção [T]
    return R_fe, R_g, R_total, B


def calcular_fluxo_indutancia_energia(N: int, mu_r: float, g: float,
                                      I: float = I_ENSAIO,
                                      l_fe: float = L_FE,
                                      A: float = AREA) -> tuple:
    """Passo 3 (b): Calcula Φ, L, W total e parcelas W_fe e W_g.

    Retorna (Phi, L, W_total, W_fe, W_g) em unidades do SI ([Wb], [H], [J], [J], [J]).
    """
    R_fe, R_g, R_total, _ = calcular_relutancias_e_B(N, mu_r, g, I, l_fe, A)
    phi = (N * I) / R_total            # Fluxo magnético [Wb]
    L = (N ** 2) / R_total             # Indutância L = N*Phi/I = N²/R_total [H]
    W_total = 0.5 * L * (I ** 2)       # Energia magnética total [J]
    W_fe = 0.5 * R_fe * (phi ** 2)     # Parcela de energia no núcleo [J]
    W_g = 0.5 * R_g * (phi ** 2)       # Parcela de energia no entreferro [J]
    return phi, L, W_total, W_fe, W_g


def verificar_limites(L: float, B: float, material: str) -> dict:
    """Passo 3 (c): Verifica requisitos R1, R2 e validade do modelo linear.

    R1: L >= 50,0 mH
    R2: B <= 80% de B_lim
    Validade linear: B <= B_lim
    """
    B_lim = MATERIAIS[material]["B_lim"]
    B_r2 = FATOR_R2 * B_lim
    passa_r1 = bool(L >= L_MIN_R1)
    passa_r2 = bool(B <= B_r2)
    valido_linear = bool(B <= B_lim)
    return {
        "R1": passa_r1,
        "R2": passa_r2,
        "linear": valido_linear,
        "B_lim": B_lim,
        "B_r2": B_r2,
        "ambos": passa_r1 and passa_r2 and valido_linear,
    }


# -----------------------------------------------------------------------------
# Passo 3 – Implementação e validação
# -----------------------------------------------------------------------------

def passo_3_validacao() -> dict:
    """Executa as duas validações exigidas no Passo 3 e imprime os resíduos."""
    print("\n" + "=" * 76)
    print("PASSO 3 – Implementação e validação")
    print("=" * 76)

    # Caso 1: g = 0, aço-silício, N = 200 -> comparar B com μ0*μr*N*I/l_fe
    mu_aco = MATERIAIS["Aço-silício"]["mu_r"]
    _, _, _, B_num = calcular_relutancias_e_B(N_INICIAL, mu_aco, g=0.0)
    B_analitico = MU0 * mu_aco * N_INICIAL * I_ENSAIO / L_FE
    residuo_B = abs(B_num - B_analitico)
    erro_rel_B = (residuo_B / B_analitico) * 100.0

    # Caso 2: g > 0 (ex.: Ferrite, g = 0,10 mm, N = 200) -> Ampère e Energia
    mu_fer = MATERIAIS["Ferrite"]["mu_r"]
    _, _, _, B_f = calcular_relutancias_e_B(N_INICIAL, mu_fer, G_INICIAL)
    phi_f, L_f, W_tot, W_fe, W_g = calcular_fluxo_indutancia_energia(
        N_INICIAL, mu_fer, G_INICIAL
    )
    H_fe = B_f / (MU0 * mu_fer)
    H_g = B_f / MU0
    NI_esp = N_INICIAL * I_ENSAIO
    NI_calc = H_fe * L_FE + H_g * G_INICIAL
    residuo_NI = abs(NI_calc - NI_esp)
    erro_rel_NI = (residuo_NI / NI_esp) * 100.0

    W_soma = W_fe + W_g
    residuo_W = abs(W_tot - W_soma)
    erro_rel_W = (residuo_W / W_tot) * 100.0

    print("Passo 3 (a-c) – Tabela de validação e resíduos:")
    print(f"  1) Caso g = 0 (Aço-silício, N=200): B_func = {fmt(B_num, 6)} T | "
          f"B_ref = {fmt(B_analitico, 6)} T | Resíduo = {residuo_B:.2e} T | "
          f"Erro rel. = {erro_rel_B:.2e} %")
    print(f"  2) Lei de Ampère (Ferrite, g=0,10 mm): Hfe*lfe + Hg*g = {fmt(NI_calc, 6)} A·esp | "
          f"N*I = {fmt(NI_esp, 6)} A·esp | Resíduo = {residuo_NI:.2e} A·esp | "
          f"Erro rel. = {erro_rel_NI:.2e} %")
    print(f"  3) Conservação de energia (Ferrite, g=0,10 mm): W = {fmt(W_tot*1e3, 6)} mJ | "
          f"Wfe + Wg = {fmt(W_soma*1e3, 6)} mJ | Resíduo = {residuo_W:.2e} J | "
          f"Erro rel. = {erro_rel_W:.2e} %")

    return {
        "B_num": B_num, "B_analitico": B_analitico,
        "residuo_B": residuo_B, "erro_rel_B": erro_rel_B,
        "NI_calc": NI_calc, "NI_esp": NI_esp,
        "residuo_NI": residuo_NI, "erro_rel_NI": erro_rel_NI,
        "W_tot": W_tot, "W_soma": W_soma,
        "residuo_W": residuo_W, "erro_rel_W": erro_rel_W,
    }


# -----------------------------------------------------------------------------
# Passo 4 – Análise da configuração inicial e geração de G1
# -----------------------------------------------------------------------------

def gerar_G1(pasta_saida: str) -> str:
    """Passo 4 (b): Gera gráfico G1 (dois painéis: L e B × g, 0,05 a 0,40 mm)."""
    mu_fer = MATERIAIS["Ferrite"]["mu_r"]
    B_lim = MATERIAIS["Ferrite"]["B_lim"]
    B_r2 = FATOR_R2 * B_lim

    g_vals = np.linspace(0.05e-3, 0.40e-3, 200)
    _, _, _, B_vals = calcular_relutancias_e_B(N_INICIAL, mu_fer, g_vals)
    _, L_vals, _, _, _ = calcular_fluxo_indutancia_energia(N_INICIAL, mu_fer, g_vals)

    # Ponto nominal g = 0,10 mm
    _, _, _, B_nom = calcular_relutancias_e_B(N_INICIAL, mu_fer, G_INICIAL)
    _, L_nom, _, _, _ = calcular_fluxo_indutancia_energia(N_INICIAL, mu_fer, G_INICIAL)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.3))

    # Painel 1: Indutância L x g
    ax1.plot(g_vals * 1e3, L_vals * 1e3, color="#1f4e79", lw=2.0, label="L(g) – Ferrite, N=200")
    ax1.axhline(L_MIN_R1 * 1e3, color="#c00000", ls="--", lw=1.4, label="Limite R1 (50,0 mH)")
    ax1.axvline(G_INICIAL * 1e3, color="#548235", ls=":", lw=1.5, label="Folga nominal (0,10 mm)")
    ax1.scatter([G_INICIAL * 1e3], [L_nom * 1e3], color="#548235", zorder=5, s=45)
    ax1.annotate(f"({fmt(0.10, 2)}; {fmt(L_nom*1e3, 2)} mH)",
                 xy=(0.10, L_nom * 1e3), xytext=(0.13, L_nom * 1e3 + 6),
                 fontsize=8.5, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax1.set_title("Indutância L em função do entreferro g")
    ax1.set_xlabel("Entreferro g (mm)")
    ax1.set_ylabel("Indutância L (mH)")
    ax1.grid(True, alpha=0.35)
    ax1.legend(fontsize=8, loc="upper right")
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))

    # Painel 2: Densidade de fluxo B x g
    ax2.plot(g_vals * 1e3, B_vals, color="#bf5700", lw=2.0, label="B(g) – Ferrite, N=200")
    ax2.axhline(B_r2, color="#c00000", ls="--", lw=1.4, label="Limite R2 (0,28 T = 80% B_lim)")
    ax2.axhline(B_lim, color="#7f0000", ls="-.", lw=1.4, label="Validade linear (0,35 T)")
    ax2.axvline(G_INICIAL * 1e3, color="#548235", ls=":", lw=1.5, label="Folga nominal (0,10 mm)")
    ax2.scatter([G_INICIAL * 1e3], [B_nom], color="#548235", zorder=5, s=45)
    ax2.annotate(f"({fmt(0.10, 2)}; {fmt(B_nom, 4)} T)",
                 xy=(0.10, B_nom), xytext=(0.13, B_nom + 0.03),
                 fontsize=8.5, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax2.set_title("Densidade de fluxo B em função do entreferro g")
    ax2.set_xlabel("Entreferro g (mm)")
    ax2.set_ylabel("Densidade de fluxo B (T)")
    ax2.grid(True, alpha=0.35)
    ax2.legend(fontsize=8, loc="upper right")
    ax2.xaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))

    fig.suptitle("G1 – Configuração Inicial (Ferrite, N = 200 espiras, I = 0,40 A)",
                 fontsize=11, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    caminho = os.path.join(pasta_saida, "G1.png")
    plt.savefig(caminho, dpi=300)
    plt.close(fig)
    return caminho


def passo_4_configuracao_inicial(pasta_saida: str) -> dict:
    """Executa o Passo 4 completo (itens a, b, c, d) e gera G1.png."""
    print("\n" + "=" * 76)
    print("PASSO 4 – Análise da configuração inicial (Ferrite, N=200, I=0,40 A)")
    print("=" * 76)

    mu_fer = MATERIAIS["Ferrite"]["mu_r"]

    # (a) Condição nominal g = 0,10 mm
    R_fe, R_g, R_tot, B = calcular_relutancias_e_B(N_INICIAL, mu_fer, G_INICIAL)
    phi, L, W, W_fe, W_g = calcular_fluxo_indutancia_energia(N_INICIAL, mu_fer, G_INICIAL)
    H_fe = B / (MU0 * mu_fer)
    H_g = B / MU0
    w_fe = (B ** 2) / (2.0 * MU0 * mu_fer)  # Densidade de energia no núcleo [J/m³]
    w_g = (B ** 2) / (2.0 * MU0)            # Densidade de energia no entreferro [J/m³]
    vol_fe = AREA * L_FE
    vol_g = AREA * G_INICIAL
    W_fe_vol = w_fe * vol_fe
    W_g_vol = w_g * vol_g

    print("Passo 4 (a) – Condição nominal (g = 0,10 mm):")
    print(f"  R_fe = {R_fe:.4e} H^-1 | R_g = {R_g:.4e} H^-1 | R_total = {R_tot:.4e} H^-1")
    print(f"  Phi = {phi:.4e} Wb | B = {fmt(B, 4)} T | L = {fmt(L*1e3, 4)} mH")
    print(f"  H_fe = {fmt(H_fe, 4)} A/m | H_g = {fmt(H_g, 4)} A/m")
    print(f"  W = {fmt(W*1e3, 4)} mJ | W_fe = {fmt(W_fe*1e3, 4)} mJ ({fmt(W_fe/W*100, 2)}%) | "
          f"W_g = {fmt(W_g*1e3, 4)} mJ ({fmt(W_g/W*100, 2)}%)")
    print(f"  Densidades: w_fe = {fmt(w_fe, 4)} J/m³ | w_g = {fmt(w_g, 4)} J/m³")
    print(f"  Verificação por volume: w_fe*V_fe = {fmt(W_fe_vol*1e3, 4)} mJ | "
          f"w_g*V_g = {fmt(W_g_vol*1e3, 4)} mJ")

    # (b) Gráfico G1
    caminho_g1 = gerar_G1(pasta_saida)
    print(f"Passo 4 (b) – Gráfico G1 salvo em: {caminho_g1}")

    # (c) Condição com tolerância g = 0,25 mm
    g_tol = G_INICIAL + DELTA_G
    R_fe_t, R_g_t, R_tot_t, B_t = calcular_relutancias_e_B(N_INICIAL, mu_fer, g_tol)
    phi_t, L_t, W_t, W_fe_t, W_g_t = calcular_fluxo_indutancia_energia(N_INICIAL, mu_fer, g_tol)

    print("Passo 4 (c) – Condição com tolerância (g = 0,25 mm):")
    print(f"  R_fe = {R_fe_t:.4e} H^-1 | R_g = {R_g_t:.4e} H^-1 | R_total = {R_tot_t:.4e} H^-1")
    print(f"  Phi = {phi_t:.4e} Wb | B = {fmt(B_t, 5)} T | L = {fmt(L_t*1e3, 4)} mH")
    print(f"  W = {fmt(W_t*1e3, 4)} mJ | W_fe = {fmt(W_fe_t*1e3, 4)} mJ ({fmt(W_fe_t/W_t*100, 2)}%) | "
          f"W_g = {fmt(W_g_t*1e3, 4)} mJ ({fmt(W_g_t/W_t*100, 2)}%)")

    # (d) Validade linear
    lim_nom = verificar_limites(L, B, "Ferrite")
    lim_tol = verificar_limites(L_t, B_t, "Ferrite")
    print("Passo 4 (d) – Validade linear:")
    print(f"  Nominal (g=0,10 mm): B = {fmt(B, 4)} T > 0,35 T -> FORA da validade linear "
          f"(extrapolação inválida; não representa operação real).")
    print(f"  Tolerância (g=0,25 mm): B = {fmt(B_t, 5)} T <= 0,35 T -> Dentro da validade linear "
          f"(R2={'PASSA' if lim_tol['R2'] else 'FALHA'}, R1={'PASSA' if lim_tol['R1'] else 'FALHA'}).")

    return {
        "nominal": {"R_fe": R_fe, "R_g": R_g, "R_tot": R_tot, "B": B, "H_fe": H_fe,
                    "H_g": H_g, "phi": phi, "L": L, "W": W, "W_fe": W_fe, "W_g": W_g,
                    "w_fe": w_fe, "w_g": w_g, "lim": lim_nom},
        "tolerancia": {"R_fe": R_fe_t, "R_g": R_g_t, "R_tot": R_tot_t, "B": B_t,
                       "phi": phi_t, "L": L_t, "W": W_t, "W_fe": W_fe_t, "W_g": W_g_t,
                       "lim": lim_tol},
    }


# -----------------------------------------------------------------------------
# Passo 5 – Investigação de uma anomalia na montagem
# -----------------------------------------------------------------------------

def calcular_folga_equivalente(L_medida: float, N: int = N_INICIAL,
                               mu_r: float = MATERIAIS["Ferrite"]["mu_r"]) -> float:
    """Passo 5 (a): Expressão g = μ0*A*(N²/L - l_fe/(μ0*μr*A)) = μ0*A*N²/L - l_fe/μr."""
    R_fe = L_FE / (MU0 * mu_r * AREA)
    R_total = (N ** 2) / L_medida
    R_g = R_total - R_fe
    return R_g * MU0 * AREA


def passo_5_anomalia(res_p4: dict) -> dict:
    """Executa o Passo 5 completo (itens a, b, c, d)."""
    print("\n" + "=" * 76)
    print("PASSO 5 – Investigação de uma anomalia na montagem")
    print("=" * 76)

    L_med = 42.0e-3  # 42,0 mH medida no ensaio
    mu_fer = MATERIAIS["Ferrite"]["mu_r"]

    g_eq = calcular_folga_equivalente(L_med, N_INICIAL, mu_fer)
    _, _, _, B_eq = calcular_relutancias_e_B(N_INICIAL, mu_fer, g_eq)
    _, L_eq, W_eq, W_fe_eq, W_g_eq = calcular_fluxo_indutancia_energia(N_INICIAL, mu_fer, g_eq)

    nom = res_p4["nominal"]
    frac_nom = (nom["W_g"] / nom["W"]) * 100.0
    frac_eq = (W_g_eq / W_eq) * 100.0

    print("Passo 5 (a-b) – Folga equivalente:")
    print(f"  Expressão: g = μ0*A*N²/L - l_fe/μr")
    print(f"  Para L = 42,0 mH -> g_eq = {fmt(g_eq*1e3, 4)} mm "
          f"(nominal: 0,10 mm; nominal + tolerância: 0,25 mm)")

    print("Passo 5 (c) – Comparação Nominal vs. Folga Estimada:")
    print(f"  Nominal (g=0,10 mm): B = {fmt(nom['B'], 4)} T [FORA DA VALIDADE LINEAR] | "
          f"W_fe = {fmt(nom['W_fe']*1e3, 4)} mJ | W_g = {fmt(nom['W_g']*1e3, 4)} mJ | "
          f"W = {fmt(nom['W']*1e3, 4)} mJ | Fração entreferro = {fmt(frac_nom, 2)} %")
    print(f"  Estimada (g={fmt(g_eq*1e3, 4)} mm): B = {fmt(B_eq, 4)} T [VÁLIDO] | "
          f"W_fe = {fmt(W_fe_eq*1e3, 4)} mJ | W_g = {fmt(W_g_eq*1e3, 4)} mJ | "
          f"W = {fmt(W_eq*1e3, 4)} mJ | Fração entreferro = {fmt(frac_eq, 2)} %")
    print("Passo 5 (d) – Limitação da medida isolada de L: outras causas possíveis incluem "
          "redução efetiva de μr (saturação parcial/tensão mecânica) e curto entre espiras "
          "ou erro no número de espiras; dado adicional útil: curva B-H ou medição direta da folga.")

    return {
        "g_eq": g_eq, "B_eq": B_eq, "L_eq": L_eq,
        "W_eq": W_eq, "W_fe_eq": W_fe_eq, "W_g_eq": W_g_eq,
        "frac_nom": frac_nom, "frac_eq": frac_eq,
    }


# -----------------------------------------------------------------------------
# Passo 6 – Decisão de projeto e geração de G2 e G3
# -----------------------------------------------------------------------------

def gerar_G2(pasta_saida: str) -> str:
    """Passo 6 (b): Gera G2 para N=220 (L na folga com tolerância e B na folga nominal)."""
    N_fixo = 220
    g_nom_vals = np.linspace(0.05e-3, 0.25e-3, 150)
    g_tol_vals = g_nom_vals + DELTA_G

    cores = {"Ferrite": "#1f4e79", "Aço-silício": "#2e75b6", "Pó de ferro": "#bf5700"}
    estilos = {"Ferrite": "-", "Aço-silício": "-", "Pó de ferro": "-"}
    cores_mat = {"Ferrite": "#d95f02", "Aço-silício": "#1b9e77", "Pó de ferro": "#7570b3"}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.4))

    for mat, props in MATERIAIS.items():
        mu_r = props["mu_r"]
        B_r2 = FATOR_R2 * props["B_lim"]
        _, L_tol, _, _, _ = calcular_fluxo_indutancia_energia(N_fixo, mu_r, g_tol_vals)
        _, _, _, B_nom = calcular_relutancias_e_B(N_fixo, mu_r, g_nom_vals)

        ax1.plot(g_nom_vals * 1e3, L_tol * 1e3, color=cores_mat[mat], lw=2.0, label=mat)
        ax2.plot(g_nom_vals * 1e3, B_nom, color=cores_mat[mat], lw=2.0, label=f"{mat} (B nom.)")
        ax2.axhline(B_r2, color=cores_mat[mat], ls="--", lw=1.2,
                    label=f"R2 {mat} ({fmt(B_r2, 2)} T)")

    ax1.axhline(L_MIN_R1 * 1e3, color="#c00000", ls="--", lw=1.5, label="Limite R1 (50,0 mH)")
    ax1.set_title("Indutância L (folga com tolerância: g_nom + 0,15 mm)")
    ax1.set_xlabel("Folga nominal g_nom (mm)")
    ax1.set_ylabel("Indutância L (mH)")
    ax1.grid(True, alpha=0.35)
    ax1.legend(fontsize=8, loc="upper right")
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))

    ax2.set_title("Densidade de fluxo B (folga nominal: g_nom)")
    ax2.set_xlabel("Folga nominal g_nom (mm)")
    ax2.set_ylabel("Densidade de fluxo B (T)")
    ax2.grid(True, alpha=0.35)
    ax2.legend(fontsize=7.2, loc="upper right", ncol=1)
    ax2.xaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))

    fig.suptitle("G2 – Desempenho por Material para N = 220 espiras (I = 0,40 A)",
                 fontsize=11, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    caminho = os.path.join(pasta_saida, "G2.png")
    plt.savefig(caminho, dpi=300)
    plt.close(fig)
    return caminho


def gerar_G3(pasta_saida: str, escolha: dict) -> str:
    """Passo 6 (d): Gera G3 comparando configuração inicial e final em função de g."""
    g_vals = np.linspace(0.05e-3, 0.40e-3, 200)

    # Inicial: Ferrite, N = 200
    mu_ini = MATERIAIS["Ferrite"]["mu_r"]
    _, L_ini, _, _, _ = calcular_fluxo_indutancia_energia(N_INICIAL, mu_ini, g_vals)
    _, _, _, B_ini = calcular_relutancias_e_B(N_INICIAL, mu_ini, g_vals)

    # Final: Aço-silício, N = 220, g_nom = 0,05 mm
    mat_f = escolha["material"]
    N_f = escolha["N"]
    g_nom_f = escolha["g_nom"]
    mu_f = MATERIAIS[mat_f]["mu_r"]
    _, L_fin, _, _, _ = calcular_fluxo_indutancia_energia(N_f, mu_f, g_vals)
    _, _, _, B_fin = calcular_relutancias_e_B(N_f, mu_f, g_vals)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.4))

    # Painel 1: L x g
    ax1.plot(g_vals * 1e3, L_ini * 1e3, color="#d95f02", ls="--", lw=2.0,
             label="Inicial (Ferrite, N=200)")
    ax1.plot(g_vals * 1e3, L_fin * 1e3, color="#1b9e77", lw=2.2,
             label=f"Final ({mat_f}, N={N_f})")
    ax1.axhline(L_MIN_R1 * 1e3, color="#c00000", ls=":", lw=1.5, label="Limite R1 (50,0 mH)")
    ax1.scatter([g_nom_f * 1e3, (g_nom_f + DELTA_G) * 1e3],
                [escolha["L_nom"] * 1e3, escolha["L_tol"] * 1e3],
                color="#1b9e77", zorder=5, s=45)
    ax1.set_title("Indutância L × entreferro g (Inicial vs. Final)")
    ax1.set_xlabel("Entreferro g (mm)")
    ax1.set_ylabel("Indutância L (mH)")
    ax1.grid(True, alpha=0.35)
    ax1.legend(fontsize=8, loc="upper right")
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))

    # Painel 2: B x g
    ax2.plot(g_vals * 1e3, B_ini, color="#d95f02", ls="--", lw=2.0,
             label="Inicial (Ferrite, N=200)")
    ax2.plot(g_vals * 1e3, B_fin, color="#1b9e77", lw=2.2,
             label=f"Final ({mat_f}, N={N_f})")
    ax2.axhline(FATOR_R2 * MATERIAIS["Ferrite"]["B_lim"], color="#d95f02", ls=":", lw=1.2,
                label="R2 Ferrite (0,28 T)")
    ax2.axhline(FATOR_R2 * MATERIAIS[mat_f]["B_lim"], color="#1b9e77", ls=":", lw=1.4,
                label=f"R2 {mat_f} (1,12 T)")
    ax2.scatter([g_nom_f * 1e3, (g_nom_f + DELTA_G) * 1e3],
                [escolha["B_nom"], escolha["B_tol"]],
                color="#1b9e77", zorder=5, s=45)
    ax2.set_title("Densidade de fluxo B × entreferro g (Inicial vs. Final)")
    ax2.set_xlabel("Entreferro g (mm)")
    ax2.set_ylabel("Densidade de fluxo B (T)")
    ax2.grid(True, alpha=0.35)
    ax2.legend(fontsize=7.5, loc="upper right")
    ax2.xaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(formatador_virgula))

    fig.suptitle("G3 – Comparação entre Configuração Inicial e Projeto Final",
                 fontsize=11, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    caminho = os.path.join(pasta_saida, "G3.png")
    plt.savefig(caminho, dpi=300)
    plt.close(fig)
    return caminho


def passo_6_decisao_projeto(pasta_saida: str, res_p4: dict) -> dict:
    """Executa o Passo 6 completo (itens a, b, c, d) e gera G2.png e G3.png."""
    print("\n" + "=" * 76)
    print("PASSO 6 – Decisão de projeto: material e enrolamento")
    print("=" * 76)

    # (a) Verificação R1 e R2 na configuração inicial
    nom = res_p4["nominal"]
    tol = res_p4["tolerancia"]
    print("Passo 6 (a) – Verificação na configuração inicial (Ferrite, N=200):")
    print(f"  Nominal (g=0,10 mm): L={fmt(nom['L']*1e3, 4)} mH (R1={nom['lim']['R1']}) | "
          f"B={fmt(nom['B'], 4)} T (R2={nom['lim']['R2']}, linear={nom['lim']['linear']})")
    print(f"  Tolerância (g=0,25 mm): L={fmt(tol['L']*1e3, 4)} mH (R1={tol['lim']['R1']}) | "
          f"B={fmt(tol['B'], 5)} T (R2={tol['lim']['R2']}, linear={tol['lim']['linear']})")

    # (b) Varredura com laços simples
    lista_N = list(range(120, 261, 20))
    lista_g_nom = [round(0.05 * k, 2) * 1e-3 for k in range(1, 6)]

    validas = []
    contagem_por_mat = {mat: 0 for mat in MATERIAIS}

    for mat, props in MATERIAIS.items():
        mu_r = props["mu_r"]
        for N in lista_N:
            for g_nom in lista_g_nom:
                g_tol = g_nom + DELTA_G
                _, _, _, B_nom = calcular_relutancias_e_B(N, mu_r, g_nom)
                _, L_nom, W_nom, _, _ = calcular_fluxo_indutancia_energia(N, mu_r, g_nom)
                _, _, _, B_tol = calcular_relutancias_e_B(N, mu_r, g_tol)
                _, L_tol, W_tol, _, _ = calcular_fluxo_indutancia_energia(N, mu_r, g_tol)

                v_nom = verificar_limites(L_nom, B_nom, mat)
                v_tol = verificar_limites(L_tol, B_tol, mat)

                if v_nom["ambos"] and v_tol["ambos"]:
                    contagem_por_mat[mat] += 1
                    validas.append({
                        "material": mat,
                        "N": N,
                        "g_nom": g_nom,
                        "g_tol": g_tol,
                        "L_nom": L_nom,
                        "B_nom": B_nom,
                        "W_nom": W_nom,
                        "L_tol": L_tol,
                        "B_tol": B_tol,
                        "W_tol": W_tol,
                    })

    print("\nPasso 6 (b) – Configurações válidas simultaneamente (nominal e tolerância):")
    for mat, qtd in contagem_por_mat.items():
        if qtd == 0:
            print(f"  {mat}: NENHUMA configuração válida.")
    print("  Material     | N   | g_nom(mm) | L_nom(mH) | B_nom(T) | L_tol(mH) | B_tol(T)")
    for c in validas:
        print(f"  {c['material']:12s} | {c['N']:3d} | {fmt(c['g_nom']*1e3, 2):>9s} | "
              f"{fmt(c['L_nom']*1e3, 4):>9s} | {fmt(c['B_nom'], 4):>8s} | "
              f"{fmt(c['L_tol']*1e3, 4):>9s} | {fmt(c['B_tol'], 4):>8s}")

    caminho_g2 = gerar_G2(pasta_saida)
    print(f"Passo 6 (b) – Gráfico G2 salvo em: {caminho_g2}")

    # (c) Escolha final: menor N; em caso de empate, menor g_nom
    validas_ordenadas = sorted(validas, key=lambda x: (x["N"], x["g_nom"]))
    escolha = validas_ordenadas[0]
    delta_N = escolha["N"] - N_INICIAL
    margem_r1_tol = (escolha["L_tol"] - L_MIN_R1) * 1e3

    print("\nPasso 6 (c) – Configuração final selecionada:")
    print(f"  Material: {escolha['material']} | N = {escolha['N']} espiras "
          f"({delta_N:+d} espiras em relação a N=200) | g_nom = {fmt(escolha['g_nom']*1e3, 2)} mm")
    print(f"  Nominal (g=0,05 mm): L = {fmt(escolha['L_nom']*1e3, 4)} mH | "
          f"B = {fmt(escolha['B_nom'], 4)} T | W = {fmt(escolha['W_nom']*1e3, 4)} mJ")
    print(f"  Tolerância (g=0,20 mm): L = {fmt(escolha['L_tol']*1e3, 4)} mH "
          f"(margem R1 = {fmt(margem_r1_tol, 4)} mH) | B = {fmt(escolha['B_tol'], 4)} T | "
          f"W = {fmt(escolha['W_tol']*1e3, 4)} mJ")

    # (d) Gráfico G3
    caminho_g3 = gerar_G3(pasta_saida, escolha)
    print(f"Passo 6 (d) – Gráfico G3 salvo em: {caminho_g3}")

    return {
        "validas": validas,
        "contagem": contagem_por_mat,
        "escolha": escolha,
        "delta_N": delta_N,
        "margem_r1_tol": margem_r1_tol,
    }


# -----------------------------------------------------------------------------
# Função principal – executa o roteiro completo sem intervenção
# -----------------------------------------------------------------------------

def main() -> None:
    pasta_saida = os.path.dirname(os.path.abspath(__file__))
    passo_3_validacao()
    res_p4 = passo_4_configuracao_inicial(pasta_saida)
    passo_5_anomalia(res_p4)
    passo_6_decisao_projeto(pasta_saida, res_p4)
    print("\nExecução concluída com sucesso.")


if __name__ == "__main__":
    main()
