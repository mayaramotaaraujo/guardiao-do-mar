import streamlit as st

def tela_assistente(df_oleo=None):

    st.markdown("""
    <style>
    .assist-titulo {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0D2137;
        margin-bottom: 0.2rem;
    }
    .assist-subtitulo {
        font-size: 0.95rem;
        color: #5A7A99;
        margin-bottom: 1.5rem;
    }
    .badge-rag {
        display: inline-block;
        background: #1A5276;
        color: white;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        letter-spacing: 0.5px;
        margin-right: 0.4rem;
    }
    .badge-gpt {
        display: inline-block;
        background: #27AE60;
        color: white;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        letter-spacing: 0.5px;
        margin-right: 0.4rem;
    }
    .badge-faiss {
        display: inline-block;
        background: #8E44AD;
        color: white;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }
    .arq-box {
        background: #F4F6F9;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        font-family: monospace;
        font-size: 0.82rem;
        color: #2C3E50;
        margin-bottom: 1.5rem;
        border-left: 4px solid #1A5276;
    }
    .pergunta-box {
        background: #EBF5FB;
        border-left: 4px solid #2980B9;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        margin-bottom: 0.4rem;
        font-weight: 600;
        color: #1A5276;
        font-size: 0.95rem;
    }
    .fontes-box {
        font-size: 0.75rem;
        color: #8898AA;
        margin-bottom: 0.4rem;
        padding-left: 0.2rem;
    }
    .resposta-box {
        background: white;
        border: 1px solid #E8EEF4;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.5rem;
        color: #2C3E50;
        font-size: 0.92rem;
        line-height: 1.6;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .robo-icon {
        font-size: 1.1rem;
        margin-right: 0.4rem;
    }
    .secao-titulo {
        font-size: 1rem;
        font-weight: 700;
        color: #0D2137;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #E8EEF4;
    }
    </style>
    """, unsafe_allow_html=True)

    # Cabeçalho
    st.markdown('<div class="assist-titulo">🤖 Assistente IA — Guardião do Mar</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="assist-subtitulo">
        Assistente com arquitetura RAG que responde perguntas sobre os dados do IBAMA usando linguagem natural.<br>
        <span class="badge-rag">RAG</span>
        <span class="badge-gpt">GPT-4o-mini</span>
        <span class="badge-faiss">FAISS</span>
    </div>
    """, unsafe_allow_html=True)

    # Arquitetura
    st.markdown('<div class="secao-titulo"> Como o assistente funciona</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="arq-box">
    Datasets CSV (IBAMA)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    Conversão em Documentos de Texto (7 documentos)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    Embeddings — text-embedding-3-small (OpenAI)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    Vector Store — FAISS (busca por similaridade, top-4 chunks)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    RAG Chain — LangChain + GPT-4o-mini (temperature: 0.1)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    Resposta em português com citação da fonte
    </div>
    """, unsafe_allow_html=True)

    # Consultas geradas
    st.markdown('<div class="secao-titulo"> Consultas realizadas ao assistente</div>', unsafe_allow_html=True)

    consultas = [
        {
            "pergunta": "Quantas localidades foram afetadas pelo derramamento de óleo?",
            "fontes": ["impacto_social", "resumo_ibama", "localidades_ibama", "fauna_ibama"],
            "resposta": "O derramamento de óleo afetou 195 localidades. (Fonte: IBAMA)"
        },
        {
            "pergunta": "Quais estados foram mais afetados pelas manchas de óleo?",
            "fontes": ["impacto_social", "resumo_ibama", "estados_ibama", "localidades_ibama"],
            "resposta": (
                "Os estados mais afetados pelas manchas de óleo em 2019 foram:\n\n"
                "1. Bahia (BA): 82 pontos — 42,1% do total\n"
                "2. Alagoas (AL): 34 pontos — 17,4% do total\n"
                "3. Sergipe (SE): 25 pontos — 12,8% do total\n"
                "4. Rio Grande do Norte (RN): 23 pontos — 11,8% do total\n"
                "5. Pernambuco (PE): 22 pontos — 11,3% do total\n\n"
                "Dados provenientes do IBAMA."
            )
        },
        {
            "pergunta": "Como o sistema detecta manchas de óleo via satélite?",
            "fontes": ["tecnologia_sistema", "contexto_geral", "impacto_social", "resumo_ibama"],
            "resposta": (
                "O sistema Guardião do Mar detecta manchas de óleo via satélite utilizando imagens do Sentinel-1, "
                "que opera com tecnologia SAR (Synthetic Aperture Radar). Esse satélite penetra nuvens e funciona à noite, "
                "permitindo a detecção de anomalias no oceano. O processo inclui:\n\n"
                "(1) Download de imagens SAR a cada 6 dias\n"
                "(2) Pré-processamento radiométrico\n"
                "(3) Extração de features espectrais\n"
                "(4) Classificação por machine learning (incluindo QSVC quântico)\n"
                "(5) Geração de alertas\n"
                "(6) Notificação ao IBAMA e à Marinha\n\n"
                "Essa abordagem permite emitir alertas em tempo real para autoridades e comunidades costeiras."
            )
        },
        {
            "pergunta": "Qual foi o impacto na fauna marinha?",
            "fontes": ["impacto_social", "resumo_ibama", "estados_ibama", "fauna_ibama"],
            "resposta": (
                "O derramamento de 2019 resultou em 45 animais marinhos afetados, conforme registrado pelo IBAMA. "
                "No Rio Grande do Norte foram contabilizados:\n\n"
                "• 12 tartarugas marinhas vivas\n"
                "• 19 tartarugas marinhas mortas\n"
                "• 2 tartarugas marinhas em captura preventiva\n"
                "• 4 aves vivas\n"
                "• 6 aves mortas\n"
                "• 2 peixes mortos\n\n"
                "A detecção precoce via satélite poderia ter reduzido o número de animais afetados, "
                "permitindo ações preventivas antes da chegada do óleo à costa."
            )
        },
        {
            "pergunta": "O que significa o nível de alerta CRÍTICO?",
            "fontes": ["tecnologia_sistema", "localidades_ibama"],
            "resposta": (
                "O nível de alerta CRÍTICO significa que a cobertura de manchas de óleo é superior a 50%. "
                "Esse nível aciona automaticamente o Plano Nacional de Contingência. "
                "Os níveis completos do sistema são:\n\n"
                "• MONITORAMENTO: vestígios com menos de 1% de cobertura\n"
                "• MODERADO: cobertura entre 1% e 10%\n"
                "• ALTO: cobertura entre 10% e 50%\n"
                "• CRÍTICO: cobertura acima de 50% — aciona o Plano Nacional de Contingência"
            )
        },
    ]

    for i, c in enumerate(consultas):
        st.markdown(f"""
        <div class="pergunta-box">
            ❓ Pergunta {i+1}: {c['pergunta']}
        </div>
        <div class="fontes-box">
             Fontes consultadas: {' · '.join(c['fontes'])}
        </div>
        """, unsafe_allow_html=True)

        resposta_formatada = c['resposta'].replace('\n', '<br>')
        st.markdown(f"""
        <div class="resposta-box">
            <span class="robo-icon">🤖</span>{resposta_formatada}
        </div>
        """, unsafe_allow_html=True)

    # Rodapé técnico
    st.markdown("""
    <div style="margin-top:1rem; padding: 0.7rem 1rem; background:#F4F6F9; border-radius:8px; font-size:0.78rem; color:#7F8C8D;">
     Modelo: GPT-4o-mini (OpenAI) &nbsp;|&nbsp;
     Embeddings: text-embedding-3-small &nbsp;|&nbsp;
     Busca vetorial: FAISS top-4 chunks &nbsp;|&nbsp;
     Framework: LangChain &nbsp;|&nbsp;
     Corpus: 5 CSVs do IBAMA (derramamento de 2019)
    </div>
    """, unsafe_allow_html=True)

