# T2_EMAG_2026_2 — Trabalho 2 de Eletromagnetismo (FEELT31405)

Análise magnetostática do núcleo magnético de um transformador de isolamento com entreferro (UFU / FEELT, 2026-2).

- **Disciplina:** Eletromagnetismo (`FEELT31405`)
- **Professor:** Luiz Arthur Tarralo Passatuto
- **Turma:** `FEELT31411`
- **Data de entrega:** `08/12/2026`
- **Integrantes:**
  - Arthur Montes Cuoco — `12411EEL028`
  - Luis Gustavo Oliveira Sena — `12211FIS210`

---

## Estrutura dos Arquivos

| Arquivo | Descrição |
|---|---|
| `T2_EM_ARTHUR_LUIS.py` | Script principal do trabalho (Passos 3 a 6): validação numérica, cálculo da configuração inicial, investigação de folga equivalente, varredura de projeto e geração dos gráficos `G1.png`, `G2.png` e `G3.png`. |
| `gerar_relatorio_pdf.py` | Script independente que gera o esquema do núcleo, o fluxograma e compila o relatório oficial em PDF (`T2_EM_ARTHUR_LUIS.pdf`). |
| `T2_EM_ARTHUR_LUIS.pdf` | Relatório final em formato PDF (A4, Times New Roman 12 pt, espaçamento 1,5). |
| `G1.png`, `G2.png`, `G3.png` | Gráficos obrigatórios gerados por `T2_EM_ARTHUR_LUIS.py`. |
| `Trabalho_2_Eletromagnetismo_Nucleo_Transformador.pdf` | Enunciado oficial do trabalho. |
| `briefing_Trabalho2_Eletromagnetismo.md` | Briefing e checklist de referência. |

---

## Dependências

- Python 3.x
- `numpy`
- `matplotlib`
- `reportlab` (apenas para `gerar_relatorio_pdf.py`)

Instalação rápida:

```bash
pip install numpy matplotlib reportlab
```

---

## Como Executar

1. **Executar os cálculos e gerar os gráficos (`G1.png`, `G2.png`, `G3.png`):**

   ```bash
   python T2_EM_ARTHUR_LUIS.py
   ```

2. **Gerar o relatório em PDF (`T2_EM_ARTHUR_LUIS.pdf`):**

   ```bash
   python gerar_relatorio_pdf.py
   ```

---
