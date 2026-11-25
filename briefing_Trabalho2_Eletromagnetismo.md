# BRIEFING — Trabalho 2 de Eletromagnetismo (FEELT31405, UFU/FEELT, 2026-2)

> Documento-base para outra IA começar o trabalho. Leia tudo antes de gerar código ou relatório.
> Tema: **Análise do núcleo magnético de um transformador de isolamento** (magnetostática, circuito magnético com entreferro).
> Prof.: Luiz Arthur Tarralo Passatuto. Trabalho em dupla ou trio.

---

## 0. Dados que o aluno ainda precisa fornecer (NÃO inventar)

- Nomes completos e matrículas de todos os integrantes
- Turma
- Data de entrega / data do relatório
- Nome da equipe (para o nome dos arquivos)
- Linguagem escolhida (Python é a sugestão padrão; matplotlib + numpy)

---

## 1. Entregas

1. **Código-fonte** (Python, MATLAB, C++ etc.)
2. **Relatório em PDF**

**Nome dos arquivos:** `T2_EM_PRIMEIROS_NOMES_EQUIPE` (sem acentos, sem espaços, separar com `_`).
**Envio:** Teams da disciplina, aba Trabalhos, até 23:59 da data indicada.

### Requisitos do código
- Cabeçalho em comentário: disciplina, turma, nº do trabalho, data, nomes completos e matrículas.
- Comentários nas linhas não triviais e onde usar pacotes; dependências e modo de execução em comentário.
- **Uma função por passo**, bem identificadas, nomes significativos.
- Executar do início ao fim **sem intervenção**, gerando G1, G2, G3 e imprimindo resultados numéricos identificados como **"Passo N (item)"**.
- Código e texto devem ser de autoria própria.

### Formato do relatório
- PDF, A4, margens 2,5 cm, Times New Roman ou Arial 12 pt, espaçamento 1,5, texto justificado, legendas 10 pt.
- **6 a 10 páginas** da Introdução às Referências (capa e apêndice não contam).
- **Capa:** título, disciplina, professor, turma, semestre, nomes completos e matrículas, data.
- **Estrutura:** 1 Introdução (contexto, objetivos, esquema do núcleo identificando bobina e entreferro, com cotas e hipóteses) → 2 Desenvolvimento (uma subseção por passo, **mesmo número e título do roteiro**; abrir com **quadro-resumo**: passo, resultado principal, figura/tabela) → 3 Análise crítica → 4 Conclusões → Referências → Apêndice (opcional).
- Cada item (a), (b)... respondido de forma identificável, com valores finais em tabela ou frase explícita.
- Figuras, tabelas e equações **numeradas, com legenda e citadas no texto**. Eixos rotulados com grandeza e unidade SI. **Decimais com vírgula** no relatório.
- Passo 3 deve incluir **fluxograma ou pseudocódigo** + justificativa das bibliotecas.
- Referências em **ABNT NBR 6023**, mínimo 3, incluindo o **livro-texto da disciplina** e os **slides das aulas**; todas citadas no texto.
- Análise crítica (Seção 3): confronto previsões × resultados; limites da aproximação linear, da folga equivalente e da aplicação a transformador real.

### Pesos de avaliação
Script 40% (clareza 10, funções/correção 20, saídas 10) · Relatório 60% (documento 8, figuras/tabelas 8, apresentação do problema 8, desenvolvimento e análise crítica 20, resultados 12, referências 4).

---

## 2. Dados do problema

| Grandeza | Valor |
|---|---|
| Comprimento médio do núcleo | ℓfe = 0,24 m |
| Área transversal (núcleo e entreferro) | A = 3,00 cm² = 3,00×10⁻⁴ m² |
| Bobina / corrente de ensaio | N inicial = 200 espiras; I = 0,40 A (contínua) |
| Entreferro | g inicial = 0,10 mm; acréscimo possível Δg = 0,15 mm (tolerância) |
| Materiais (μr; limite de B) | Ferrite: 2200; 0,35 T · Aço-silício: 1500; 1,40 T · Pó de ferro: 125; 0,90 T |
| μ0 | 4π×10⁻⁷ H/m |
| Requisitos | **R1:** L ≥ 50,0 mH · **R2:** B ≤ 80% do limite do material |

**Hipóteses:** magnetostática; materiais lineares, homogêneos e isotrópicos *enquanto B ≤ limite*; μ_ar = μ0; seção constante; campo uniforme no núcleo e no entreferro; sem dispersão, histerese, correntes parasitas ou espraiamento. Limites de B são critérios didáticos. **Resultados acima do limite são extrapolações inválidas do modelo linear.**
A corrente de 0,40 A é imposta pela fonte do ensaio (não é a corrente de magnetização de um transformador na rede). Não se calcula tensão induzida, perdas em CA, rendimento ou EMI.

**Modelo (circuito magnético em série):**
- Rfe = ℓfe/(μ0 μr A) · Rg = g/(μ0 A) · R = Rfe + Rg
- Φ = NI/R · B = Φ/A · L = NΦ/I = N²/R · W = LI²/2
- Hfe = B/(μ0 μr) · Hg = B/μ0 · verificação: Hfe·ℓfe + Hg·g = NI
- Wfe = ½·Rfe·Φ² · Wg = ½·Rg·Φ² · densidade de energia w = B²/(2μ) × volume (A·ℓfe e A·g)

---

## 3. Roteiro dos 6 passos

**Passo 1 – Modelagem física (à mão).**
(a) Esboço do circuito: bobina, sentido do fluxo, percurso no núcleo, entreferro, área; explicar condições para mesmo fluxo nas duas regiões. (b) Lei de Ampère + B = μH → H no núcleo e no entreferro, relutâncias parciais, Φ em função de N, I, μr, g, A, ℓfe. (c) L = NΦ/I, W = LI²/2, parcelas de energia no núcleo e no entreferro; condições de validade.

**Passo 2 – Previsões (ANTES de rodar o código).**
Registrar e justificar fisicamente: (a) efeito de aumentar g sobre Φ e L; (b) efeito de aumentar N (I fixo) sobre B e L; (c) influência de μr e do limite de B na escolha do material; por que maior μr não garante configuração válida. **Confrontar depois com os Passos 4 a 6.**

**Passo 3 – Implementação e validação.**
Funções para: (a) relutâncias e B; (b) Φ, L, W com energias no núcleo e no entreferro; (c) verificação dos limites de campo e de indutância. Validar:
- g = 0, aço-silício, N = 200: comparar B com μ0·μr·N·I/ℓfe;
- qualquer g: verificar numericamente Hfe·ℓfe + Hg·g = NI e W = Wfe + Wg.
Apresentar **tabela de resíduos/erros relativos com valores e unidades**. Incluir fluxograma/pseudocódigo e justificativa das bibliotecas.

**Passo 4 – Configuração inicial (ferrite, N = 200, g = 0,10 mm).**
(a) B, Hfe, Hg, Φ, L, W, as duas parcelas de energia, densidade de energia em cada região e verificação via volumes. (b) **G1:** L e B × g, de 0,05 a 0,40 mm, N e I fixos; marcar g = 0,10 mm, limite R1, limite R2 da ferrite e limite de validade linear. (c) Repetir com g = 0,25 mm; comparar com nominal e explicar a mudança na distribuição de energia. (d) Apontar quais resultados ultrapassam o limite de validade linear e por que não são previsões de operação real.

**Passo 5 – Anomalia na montagem.**
Ensaio com pequenas variações em torno de 0,40 A deu L incremental = 42,0 mH (no modelo linear coincide com L = NΦ/I; valor formal nominal = 72,1 mH). Hipótese: aumento da folga, com μr constante. (a) Expressão da folga equivalente g a partir de L medido. (b) Calcular g para 42,0 mH e comparar com nominal e tolerância. (c) B para a folga estimada e comparação com o nominal; **tabela com as duas condições** (energia no núcleo, no entreferro, total, fração no entreferro); marcar o que ultrapassa o limite linear. (d) Por que a medida de L isolada não prova a folga; ≥ 2 outras causas possíveis; um dado adicional necessário.

**Passo 6 – Decisão de projeto.**
Materiais: os 3. N = 120, 140, ..., 260. gnom = 0,05, 0,10, ..., 0,25 mm. Junta montada pode ter até +0,15 mm. Atender **R1 e R2 nas condições nominal e com tolerância**, usando só resultados dentro da validade linear. Priorizar o **menor N**; em empate, justificar gnom.
(a) Verificar R1/R2 na configuração inicial nas duas folgas. (b) Varredura com laços simples; **uma única tabela** só com configurações válidas (material, N, gnom, L e B nas duas condições); registrar materiais sem configuração válida. (c) Configuração final justificada: N, gnom, material, L, B, W nas duas condições + espiras poupadas/acrescentadas. (d) **G3:** L e B × g comparando inicial e final; confrontar com Passo 2; ≥ 2 limitações para transformador real em CA.

### Gráficos obrigatórios (gerados pelo código; título, eixos com unidade, legenda se >1 curva; dois painéis cada)
- **G1:** L e B × g, núcleo inicial, com folga nominal e limites (Passo 4b).
- **G2:** para **N = 220**: L na folga *com tolerância* e B na folga *nominal*, × gnom, por material, com R1 e R2 (Passo 6b).
- **G3:** L e B × g, configurações inicial e final, indicando limites (Passo 6d).

---

## 4. Valores de referência (pré-calculados para conferência — o código deve reproduzi-los)

Modelo linear, μ0 = 4π×10⁻⁷, ℓfe = 0,24 m, A = 3,00×10⁻⁴ m², I = 0,40 A.

**Ferrite, N = 200, g = 0,10 mm (nominal):**
- Rfe ≈ 2,8937×10⁵ H⁻¹ · Rg ≈ 2,6526×10⁵ H⁻¹
- Φ ≈ 1,4424×10⁻⁴ Wb · **B ≈ 0,4808 T** (> 0,35 T → **fora da validade linear**) · **L ≈ 72,1200 mH** · W ≈ 5,7696 mJ
- Wfe ≈ 3,0102 mJ · Wg ≈ 2,7594 mJ

**Ferrite, N = 200, g = 0,25 mm (com tolerância):**
- **B ≈ 0,27996 T** (≤ 0,28 T = 80% de 0,35 T → R2 passa por margem ínfima; cuidado com arredondamento na comparação) · **L ≈ 42,0 mH** (< 50 mH → viola R1)
- W ≈ 3,3595 mJ · Wfe ≈ 1,0206 mJ · Wg ≈ 2,3389 mJ

**Passo 5:** folga equivalente para L = 42,0 mH ≈ **0,2499 mm ≈ 0,25 mm**, ou seja, coincide com a folga nominal + tolerância (0,10 + 0,15). B ≈ 0,2800 T.

**Passo 6 (varredura, critérios R1 e R2 nas duas folgas, B também ≤ limite):**
- Ferrite: **nenhuma** configuração válida. Pó de ferro: **nenhuma** configuração válida.
- Aço-silício, válidas: (220, 0,05), (240, 0,05), (240, 0,10), (260, 0,05), (260, 0,10), (260, 0,15).
- **Escolha esperada: aço-silício, N = 220, gnom = 0,05 mm** (menor N; sem empate em N = 220). L ≈ 86,8875 mH (nominal) e ≈ 50,6844 mH (com tolerância); B ≈ 0,5266 T e ≈ 0,3072 T. Em relação à configuração inicial (N = 200), são **20 espiras acrescentadas** (não poupadas); atenção ao sinal ao redigir.
- Margem de R1 com tolerância é pequena (≈ 0,6844 mH); comentar isso.

> Conferir tudo rodando o código; esses números são só uma checagem independente.

---

## 5. ERROS DO TRABALHO ANTERIOR A NÃO REPETIR

Comentários recebidos no trabalho anterior (capacitância / geometria coaxial), generalizados como checklist:

1. **Dedução matemática correta:** conferir integrais e logaritmos (ex.: o termo era ln(b/a), não outra forma); definir corretamente grandezas por unidade de comprimento (ex.: C' = C/L). Ao somar camadas/regiões, não repetir parcelas nem omitir termos (ex.: permissividade excedente no numerador e termo logarítmico faltando). **Aqui:** revisar as deduções de Rfe, Rg, Φ, L, Wfe, Wg com cuidado, incluindo unidades.
2. **Tabelas recalculadas a partir do próprio código.** Nenhum número de tabela pode ser "estimado à mão" ou ficar desatualizado em relação ao script. Gerar as tabelas do relatório com a saída do código.
3. **Validação com referência e tolerância explícitas.** Se usar um valor de referência diferente do solicitado, explicar a substituição ou mostrar a comparação com o valor pedido. Mostrar o erro relativo. **Usar a mesma tolerância no relatório, no pseudocódigo e no programa.**
4. **Não afirmar mais do que o modelo demonstra.** Ex.: linearidade de uma curva não prova que o campo permanece inalterado; variar uma propriedade do meio não altera o que não depende dela. **Aqui:** não confundir L medido com prova de folga (Passo 5d); não tratar resultados acima do limite de B como previsão real.
5. **Qualificar linguagem forte.** Evitar "solução de engenharia perfeita", "margem segura" etc. Se a configuração passa por pouco (ex.: L com tolerância ≈ 50,68 mH), dizer a folga numérica real. **Valores adicionais assumidos (frequência, temperatura, etc.) devem ser rotulados como hipóteses ou fundamentos.**
6. **Formalidades:** numeração de figuras sem repetição (inclusive nos apêndices); **todas as referências citadas no texto**; **cabeçalho do código completo** (disciplina, turma, trabalho, data, nomes, matrículas).

---

## 6. Checklist final antes de entregar

- [ ] Cabeçalho do código completo; roda sem intervenção; imprime "Passo N (item)"; gera G1, G2, G3
- [ ] Validação do Passo 3 com tabela de resíduos (valores e unidades)
- [ ] Todos os resultados do relatório vêm da saída do código (4 casas decimais, vírgula decimal no PDF)
- [ ] Quadro-resumo abrindo a Seção 2; subseções com mesmo número/título dos passos
- [ ] Previsões do Passo 2 escritas *antes* e confrontadas na Seção 3
- [ ] Resultados fora da validade linear marcados explicitamente (ferrite nominal: B ≈ 0,4808 T > 0,35 T)
- [ ] 6 a 10 páginas, Times/Arial 12, 1,5, justificado, margens 2,5 cm, legendas 10 pt
- [ ] ≥ 3 referências ABNT (livro-texto + slides), todas citadas no texto
- [ ] Figuras/tabelas/equações numeradas sem repetição e citadas no texto
- [ ] Linguagem sem exageros; hipóteses adicionais rotuladas
- [ ] Nome dos arquivos no padrão T2_EM_PRIMEIROS_NOMES_EQUIPE
