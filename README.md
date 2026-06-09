# Guardião do Mar

Sistema de monitoramento do litoral brasileiro para detecção de manchas de óleo no oceano e focos de fogo na vegetação costeira do nordeste brasileiro.

---

## O problema que a aplicação resolve

Em 2019, aconteceu um desastre no litoral do nordeste brasileiro que contaminou mais de 4.000 km de costa com manchas de óleo. Ou seja, muitas costas do litoral foram atingidas, animais foram mortos e muitos pescadores ficaram  prejudicados. E a gente viu que o governo demorou 43 dias para agir, não porque não tinha tecnologia, mas porque não havia uma ferramenta pública que pudesse ser acessada pela propria população para ajudar a identificar as manchas de oleo e focos de fogo e assim pudesse comunicar o governo, colocando a própria população como meio dnessa busca ativa. Pois é a população que está todo dia em contato com o litoral, principalmente as pessoas comerciantes que trabalham no litoral.

O Guardião do Mar resolve esse problema ao usar dados de satélite do IBAMA e do INPE em um painel que qualquer cidadão, pescador, agente ambiental ou gestor público consegue usar sem conhecimento técnico.

---

## Fontes de dados

| Fonte | Dado | Formato | Período |
|-------|------|---------|---------|
| IBAMA — ibama.gov.br/manchasdeoleo | Localidades com manchas de óleo, coordenadas, status e nível de alerta | CSV | Desastre de 2019 |
| INPE — Programa Queimadas | Focos de fogo diários no nordeste brasileiro, risco de fogo, bioma, dias sem chuva | CSV | Mai–Jun 2026 |

---

## Justificativa do framework

O projeto usa **Streamlit** pelos seguintes motivos:

- Suporte nativo a `st.session_state` para gerenciamento de estado entre reruns
- Decorator `@st.cache_data` para evitar recarregamento de dados a cada interação
- Integração direta com Plotly para gráficos interativos com hover e zoom
- Sidebar nativa para filtros interativos
- Ciclo de execução simples e previsível para aplicações de dados

---

## Diagrama de arquitetura

```
guardiao_do_mar/
│
├── app.py                        ← Entrada principal — carrega dados, monta sidebar e navegação
│
├── providers/                    ← Acesso a dados externos
│   ├── provider_oleo.py          ← Carrega e trata CSV do IBAMA (manchas de óleo)
│   └── provider_fogo.py          ← Carrega e trata CSV do INPE (focos de fogo)
│
├── pipelines/                    ← Transformação e agregação de dados
│   └── pipeline_dados.py         ← Filtros por estado/data/risco, contadores, séries temporais
│
├── features/                     ← Telas do dashboard (uma por aba)
│   ├── feature_mapa.py           ← Mapa interativo com manchas de óleo e focos de fogo
│   ├── feature_alertas.py        ← Alertas ativos com confirmação humana
│   ├── feature_historico.py      ← Gráficos históricos de focos por período e estado
│   └── feature_boia.py           ← Monitoramento da boia costeira com sensores IoT
│
├── state/                        ← Gerenciamento de estado
│   └── estado_sessao.py          ← Inicialização e reset do st.session_state
│
├── ui/                           ← Componentes visuais reutilizáveis
│   ├── componente_metrica.py     ← Card de métrica numérica (usado em múltiplas telas)
│   └── componente_alerta.py      ← Card de alerta com botão de confirmação humana
│
├── data/                         ← Arquivos CSV (não versionados — ver .gitignore)
│   ├── guardiao_mar_localidades.csv
│   └── focos_nordeste_consolidado.csv
│
├── requirements.txt
├── .gitignore
└── README.md
```

**Fluxo de dados:**

```
CSV IBAMA → provider_oleo → pipeline_dados → feature_mapa / feature_alertas / feature_boia
CSV INPE  → provider_fogo → pipeline_dados → feature_mapa / feature_alertas / feature_historico / feature_boia
```

---

## Requisitos

- Python 3.10 ou superior
- Bibliotecas listadas em `requirements.txt`

---

## Instalação

**1. Clone o repositório:**

```bash
git clone https://github.com/seunome/guardiao-do-mar.git
cd guardiao-do-mar
```

**2. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**3. Adicione os arquivos CSV na pasta data:**

Baixe os arquivos de dados e coloque na pasta `data/`:
- `guardiao_mar_localidades.csv` — dados IBAMA 2019
- `focos_nordeste_consolidado.csv` — dados INPE 2026

---

## Execução

```bash
streamlit run app.py
```

O dashboard abre automaticamente no navegador em `http://localhost:8501`.

---

## Funcionalidades

- Mapa interativo com manchas de óleo (IBAMA) e focos de fogo (INPE) sobrepostos
- Três filtros interativos: estado, período e nível mínimo de risco de fogo
- Alertas ativos com botão de confirmação humana para autoridades
- Gráficos históricos de focos por dia, por estado e por bioma
- Monitoramento de boia costeira com sensores ESP32 (turbidez, temperatura, distância HC-SR04)
- Cores semânticas: vermelho crítico, laranja alto, amarelo moderado, verde seguro
- Cache de dados para performance otimizada

---

## Integrantes

| Nome |
|------|
| Gabriel Palmeira 
| Mayara Mota 
| Lucas Gambini

---

## Disciplina

Front-end em Sistemas de IA — Global Solution 2026.1 — FIAP

---

## Fontes oficiais

- IBAMA: https://www.gov.br/ibama/pt-br/assuntos/emergencias-ambientais/manchasdeoleo
- INPE Queimadas: https://terrabrasilis.dpi.inpe.br/queimadas/portal
