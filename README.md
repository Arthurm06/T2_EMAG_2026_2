# Trabalho 1 - Eletromagnetismo

## Identificação

- **Disciplina:** FEELT31405 - Eletromagnetismo (2026-2)
- **Trabalho:** 1
- **Tema:** Sonda capacitiva de nível no conservador de um transformador
- **Data de entrega:** 03/11/2026
- **Autores:** Arthur Montes Cuoco e Luis Gustavo Oliveira Sena
- **Matrículas:** 12411EEL028 e matrícula de Luis Gustavo Oliveira Sena (informar)

## Objetivo

Modelar uma sonda capacitiva coaxial para medir o nível de óleo, investigar o
efeito de água decantada na indicação e revisar a capa isolante para atender
às restrições de fundo de escala e resolução da eletrônica.

O modelo considera a associação em série das camadas radiais e em paralelo
dos trechos ao longo da altura da sonda. São adotadas as hipóteses de regime
eletrostático ou quase-estático, meios lineares, homogêneos, isotrópicos e sem
perdas, interfaces planas e horizontais, além da desprezibilidade dos efeitos
de borda e das capacitâncias parasitas.

## Organização do trabalho

O programa executa todos os passos sequencialmente, identifica os resultados
no terminal e gera os gráficos obrigatórios:

1. **Passo 1:** modelagem física, hipóteses e associações série/paralelo.
2. **Passo 2:** previsões sobre a curva de capacitância, a capa e a água.
3. **Passo 3:** funções do modelo e validação de `C/L` para uma sonda de duas camadas.
4. **Passo 4:** calibração com óleo limpo, sensibilidade, leituras L1, L2 e L3 e resolução.
5. **Passo 5:** análise da água decantada, erro de indicação e extrapolação da calibração.
6. **Passo 6:** varredura de PTFE, poliimida e epóxi, com espessuras de 0,2 a 1,0 mm,
   verificação das restrições R1 e R2 e escolha da configuração final.

## Dados principais

- Comprimento útil: `H = 0,80 m`
- Raio da haste: `a = 5,0 mm`
- Raio interno do tubo: `b = 15,0 mm`
- Capa inicial: PTFE, `t = 0,50 mm`, `epsilon_r = 2,1`
- Permissividades relativas: ar `1,0`, óleo `2,2` e água `80`
- Resolução da eletrônica: `0,1 pF`
- Fundo de escala: `150 pF`

## Dependências

- Python 3
- `numpy`
- `matplotlib`

Instalação:

```bash
pip install numpy matplotlib
```

## Execução

Na pasta do projeto, execute:

```bash
python T1_EM_ARTHUR_LUIS.py
```

O programa roda do início ao fim sem intervenção, imprime os resultados dos
Passos 1 a 6 e salva os gráficos `G1.png`, `G2.png`, `G3.png` e `G4.png`.

## Gráficos gerados

- **G1:** curva `C x h` para óleo limpo, com `C_vazio`, `C_cheio` e L1-L3.
- **G2:** erro de indicação em função da altura da água para `h = 0,45 m`.
- **G3:** varredura de `C_max` e da menor variação de nível para os três materiais.
- **G4:** comparação entre as configurações inicial e final para `h_w = 0`, 1 e 5 cm.

## Relatório em PDF

O arquivo `gerar_relatorio_pdf.py` compila o relatório técnico em PDF usando
`reportlab`. Para executá-lo, instale também a dependência e rode:

```bash
pip install reportlab
python gerar_relatorio_pdf.py
```

O relatório utiliza as figuras geradas pelo programa principal e apresenta a
metodologia, o fluxograma ou pseudocódigo, as tabelas, os resultados, a análise
crítica, as conclusões e as referências conforme as exigências do trabalho.