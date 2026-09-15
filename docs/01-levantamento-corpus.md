# Levantamento e Dimensionamento do Corpus

**Data do levantamento:** 2026-09-15
**Método:** busca web + consulta às páginas oficiais (Planalto, CGIBS, Portal NF-e, CCiF)
**Status:** levantamento inicial — contagens de artigos vêm de fontes secundárias e precisam de conferência
contra o texto oficial na etapa de ingestão.

> **Aviso:** o `PROJETO.md` foi escrito quando o PLP 108/2024 ainda tramitava e os regulamentos não existiam.
> Este documento substitui o dimensionamento daquele arquivo.

---

## 1. Núcleo normativo — Dataset (a)

| # | Norma | Publicação | Artigos | Anexos | Papel no grafo |
|---|---|---|---|---|---|
| 1 | **EC 132/2023** | 20/12/2023 | ~20 | — | Raiz da hierarquia; altera a CF |
| 2 | **LC 214/2025** | 16/01/2025 | 499 | 23 | Institui IBS, CBS e IS |
| 3 | **LC 227/2026** (ex-PLP 108/2024) | 13/01/2026 | ~197 | — | Institui o CGIBS, processo adm., ITCMD |
| 4 | **Decreto 12.955/2026** | 29/04/2026 | 620 | 5 | Regulamento da CBS (Receita Federal) |
| 5 | **Resolução CGIBS 6/2026** | 30/04/2026 | 617 | 5 | Regulamento do IBS (CGIBS) |
| 6 | **Portaria Conjunta MF/CGIBS 7/2026** | 04/2026 | a apurar | — | Disposições comuns CBS/IBS |

**Total estimado: ~1.950 artigos** (nível-artigo) ou **6 documentos** (nível-documento).

### Estrutura relevante descoberta

Decreto 12.955/2026 e Resolução CGIBS 6/2026 são **documentos-espelho**: ambos publicados em 30/04/2026,
ambos organizados com um **Livro I de "normas comuns ao IBS e à CBS"** e um Livro II específico do
respectivo tributo. Regulamentam os mesmos artigos da LC 214/2025 a partir de autoridades distintas
(RFB e CGIBS).

Isso cria duas oportunidades não previstas no `PROJETO.md`:
- **conjunto denso e genuíno de arestas** `regulamenta` (regulamento → artigo da LC 214);
- **conjunto natural de validação por alinhamento** (dois nós distintos que regulamentam o mesmo artigo-fonte
  devem ter embeddings próximos) — sem precisar de rotulagem manual.

---

## 2. Documentos técnicos de entidades — Dataset (b)

| Fonte | Volume | Formato | Observação |
|---|---|---|---|
| **CCiF — Notas Técnicas** | **30** (NT I a NT XXX) | PDF | Listagem confirmada na página oficial; datas/links dos PDFs não estão na página de índice |
| **NT 2025.002 (NF-e/NFC-e)** | ~20+ versões (v1.00 03/2025 → v1.51 04/08/2026) | PDF | Série versionada — cada versão é um nó temporal natural |
| **Outras NTs de DF-e** | a apurar (CT-e, NFS-e, NF3-e, etc.) | PDF | Portal NF-e / cronograma RFB |
| **Ato Técnico Conjunto RFB/CGIBS 1/2026** | 1 | — | Ratifica as NTs de documentos fiscais |
| **Entidades setoriais** (CNI, CBIC, Conasems…) | a apurar | PDF/HTML | Coleta manual |

---

## 3. Impacto no desenho do projeto

### 3.1 Tamanho do grafo — resolvido

A preocupação de "grafo pequeno demais para GNN" some no nível-artigo: **~1.950 nós** do núcleo normativo,
antes de qualquer nota técnica. Ordem de grandeza compatível com Cora (2.708 nós), o benchmark do
próprio paper do GraphSAGE.

**Decisão:** granularidade = **artigo**. Documento vira atributo do nó, não nó.

### 3.2 Split temporal — agora natural

| Partição | Documentos | Data |
|---|---|---|
| **Treino** | EC 132/2023 + LC 214/2025 | até 01/2025 |
| **Teste indutivo** | LC 227/2026 | 01/2026 |
| **Teste indutivo** | Decreto 12.955/2026 + Res. CGIBS 6/2026 | 04/2026 |
| **Teste indutivo (stream)** | NT 2025.002 v1.51 e posteriores | 08/2026+ |

Nenhum nó de teste existia no momento do treino — o requisito indutivo é testado com dados reais,
sem simulação artificial de "nó novo". **Split aleatório está descartado**: vazaria informação temporal
e invalidaria a tese central.

### 3.3 Risco novo identificado: vazamento de citação na feature do nó

As arestas do grafo vêm de citações explícitas no texto ("nos termos do art. 12 da Lei Complementar
nº 214, de 2025"). Se a feature do nó for o embedding do texto **bruto**, a string da citação — que É o
rótulo da aresta — entra na feature. O modelo não aprenderia estrutura: leria a resposta.

**Mitigação obrigatória:** mascarar todas as referências normativas explícitas do texto antes de gerar o
embedding de feature (`art. 12 da LC 214/2025` → `<REF>`). A citação passa a existir **apenas como aresta**.
Sem isso, qualquer resultado positivo é artefato.

### 3.4 Consequência sobre a etapa de extração (GLiNER-Relex)

Citações normativas em texto legal brasileiro são altamente padronizadas e extraíveis por **regex** com
precisão próxima de 100%. Isso é bom (ground truth confiável, barato), mas significa que a extração
**não é onde está a contribuição do projeto** — o GLiNER/LLM só se justifica para relações não explícitas
(interpreta, critica, diverge) nas notas técnicas do dataset (b).

**Ponto em aberto para decisão:** ver `docs/02-decisoes-abertas.md`.

---

## 4. Disponibilidade dos textos

| Documento | Fonte | Formato |
|---|---|---|
| EC 132, LC 214, LC 227, Decreto 12.955 | planalto.gov.br | HTML (parseável) |
| Resolução CGIBS 6/2026 | cgibs.gov.br | PDF |
| Notas técnicas CCiF | ccif.com.br | PDF |
| NT 2025.002 e séries DF-e | nfe.fazenda.gov.br | PDF |

**A confirmar:** qualidade do HTML do Planalto para segmentação automática por artigo (é a etapa crítica
de ingestão — 1.950 nós dependem dela).

---

## Fontes

- Sanção do PLP 108/2024 → LC 227/2026: <https://bvp.adv.br/reforma-tributaria-sancao-do-plp-no-108-24-e-conversao-na-lei-complementar-no-227-26-cgibs-ibs/>
- Publicação dos regulamentos: <https://www.mattosfilho.com.br/unico/regulamentos-ibs-cbs/>
- Decreto 12.955/2026 (620 artigos): <https://www2.camara.leg.br/legin/fed/decret/2026/decreto-12955-29-abril-2026-799019-publicacaooriginal-179077-pe.html>
- Resolução CGIBS 6/2026 (617 artigos): <https://www.cgibs.gov.br/upload/arquivos/202604/30084927-res-cgibs-n-6-30-abr-2026-regulamenta-o-ibs.pdf>
- Notas Técnicas CCiF: <https://ccif.com.br/notas-tecnicas-reforma-tributaria/>
- NT 2025.002: <https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=04BIflQt1aY%3D>
