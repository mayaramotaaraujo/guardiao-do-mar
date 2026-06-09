import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from streamlit_option_menu import option_menu
from providers.provider_oleo    import carregar_oleo
from providers.provider_fogo    import carregar_fogo
from pipelines.pipeline_dados   import filtrar_oleo, filtrar_fogo, contadores
from features.feature_mapa      import tela_mapa
from features.feature_alertas   import tela_alertas
from features.feature_historico import tela_historico
from features.feature_boia      import tela_boia
from state.estado_sessao        import inicializar

st.set_page_config(
    page_title="Guardiao do Mar",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .stButton > button { border-radius: 8px; font-weight: 600; }
    [data-testid="stSidebar"] { background-color: #042C53; }
    [data-testid="stSidebar"] * { color: white !important; }
    h1, h2, h3 { color: #042C53; }
    .nav-link { font-size: 15px !important; font-weight: 500 !important; }
    .nav-link-selected { font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

inicializar()

# ─── CABEÇALHO ───────────────────────────────────────────────────────────────
col_logo, col_titulo = st.columns([1, 6])
with col_logo:
    st.markdown("""
    <div style='text-align:center;padding-top:8px'>
        <svg width="130" height="130" viewBox="0 0 136 140" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="68" cy="70" r="62" fill="#042C53"/>
            <path d="M18 68 Q31 54 44 68 Q57 82 68 68 Q79 54 92 68 Q105 82 118 68"
                  stroke="#9FE1CB" stroke-width="3.5" fill="none" stroke-linecap="round"/>
            <path d="M18 81 Q31 67 44 81 Q57 95 68 81 Q79 67 92 81 Q105 95 118 81"
                  stroke="#185FA5" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>
            <circle cx="68" cy="39" r="11" fill="#9FE1CB"/>
            <circle cx="68" cy="39" r="6" fill="#042C53"/>
            <line x1="57" y1="34" x2="50" y2="25" stroke="#9FE1CB" stroke-width="2" stroke-linecap="round"/>
            <line x1="79" y1="34" x2="86" y2="25" stroke="#9FE1CB" stroke-width="2" stroke-linecap="round"/>
            <line x1="68" y1="28" x2="68" y2="18" stroke="#9FE1CB" stroke-width="2" stroke-linecap="round"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)
with col_titulo:
    st.markdown(
        "<h1 style='color:#042C53;margin-bottom:0;font-size:48px;font-weight:800;"
        "letter-spacing:-1.5px;line-height:1.1'>Guardião do Mar</h1>"
        "<p style='color:#042C53;font-size:17px;margin-top:8px;font-weight:400'>"
        "Monitoramento do litoral brasileiro em tempo real — manchas de óleo e focos de fogo"
        "</p>",
        unsafe_allow_html=True
    )

# ─── BARRA DE FONTES ─────────────────────────────────────────────────────────
st.markdown(
    "<div style='border-top:3px solid #042C53;background:#f8fafc;padding:10px 18px;"
    "display:flex;align-items:center;gap:24px;border-radius:0 0 6px 6px;margin-bottom:16px'>"
    "<span style='background:#042C53;color:white;font-size:11px;font-weight:600;"
    "padding:3px 10px;border-radius:99px;flex-shrink:0'>INPE</span>"
    "<span style='font-size:13px;color:#444'>Focos de fogo — dados atualizados em tempo real</span>"
    "<span style='color:#ccc;margin:0 4px'>|</span>"
    "<span style='background:#E24B4A;color:white;font-size:11px;font-weight:600;"
    "padding:3px 10px;border-radius:99px;flex-shrink:0'>IBAMA</span>"
    "<span style='font-size:13px;color:#444'>Manchas de óleo — registros históricos 2019</span>"
    "</div>",
    unsafe_allow_html=True
)

# ─── CARREGAMENTO COM CACHE ───────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def carregar_todos_dados():
    df_o = carregar_oleo()
    df_f = carregar_fogo()
    return df_o, df_f

with st.spinner("Carregando dados do satelite... aguarde um momento"):
    df_oleo_raw, df_fogo_raw = carregar_todos_dados()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='color:#9FE1CB;font-size:18px;margin-bottom:16px'>🔍 Filtros de Busca</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:12px;color:#aaa;margin-bottom:16px'>"
        "Use os filtros para ver uma regiao ou nivel de risco especifico.</p>",
        unsafe_allow_html=True
    )

    estados_disponiveis = sorted(df_fogo_raw["estado"].unique().tolist())
    estados_sel = st.multiselect(
        "Estado do nordeste",
        options=estados_disponiveis,
        default=[],
        placeholder="Todos os estados",
    )
    st.session_state["estados_selecionados"] = estados_sel

    datas_disponiveis = sorted(df_fogo_raw["data_arquivo"].unique().tolist())
    datas_sel = st.multiselect(
        "Periodo",
        options=datas_disponiveis,
        default=[],
        placeholder="Todo o periodo",
    )
    st.session_state["datas_selecionadas"] = datas_sel

    nivel_min = st.slider(
        "Risco de fogo minimo:",
        min_value=0.0, max_value=1.0,
        value=0.0, step=0.05,
    )
    st.session_state["nivel_risco_min"] = nivel_min

    st.markdown("---")
    if st.button("Limpar filtros", use_container_width=True):
        from state.estado_sessao import resetar
        resetar()
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<p style='font-size:11px;color:#aaa;text-align:center'>"
        "Guardião do Mar<br>"
        "Fontes: IBAMA · INPE</p>",
        unsafe_allow_html=True
    )

# ─── FILTRAR DADOS ────────────────────────────────────────────────────────────
df_fogo_filtrado = filtrar_fogo(
    df_fogo_raw,
    estados=estados_sel if estados_sel else None,
    datas=datas_sel if datas_sel else None,
    nivel_min=nivel_min,
)
df_oleo_filtrado = filtrar_oleo(df_oleo_raw)
contadores_dados = contadores(df_oleo_filtrado, df_fogo_filtrado)

if len(df_fogo_filtrado) == 0:
    st.warning("Nenhum foco encontrado com os filtros selecionados. Tente ampliar o periodo ou remover filtros.")

# ─── NAVEGAÇÃO COM ÍCONES VETORIAIS ───────────────────────────────────────────
aba_selecionada = option_menu(
    menu_title=None,
    options=["Mapa do Litoral", "Alertas Ativos", "Historico e Graficos", "Boia Costeira"],
    icons=["map", "exclamation-triangle", "bar-chart-line", "broadcast-pin"],
    menu_icon=None,
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "6px",
            "background-color": "#042C53",
            "border-radius": "10px",
            "margin-bottom": "20px",
        },
        "icon": {
            "color": "rgba(255,255,255,0.7)",
            "font-size": "18px",
        },
        "nav-link": {
            "font-size": "15px",
            "font-weight": "500",
            "color": "rgba(255,255,255,0.65)",
            "border-radius": "7px",
            "padding": "11px 22px",
            "--hover-color": "rgba(255,255,255,0.1)",
        },
        "nav-link-selected": {
            "background-color": "white",
            "color": "#042C53",
            "font-weight": "600",
        },
    }
)

# ─── CONTEÚDO DAS ABAS ────────────────────────────────────────────────────────
if aba_selecionada == "Mapa do Litoral":
    tela_mapa(df_oleo_filtrado, df_fogo_filtrado, contadores_dados)

elif aba_selecionada == "Alertas Ativos":
    tela_alertas(df_oleo_filtrado, df_fogo_filtrado)

elif aba_selecionada == "Historico e Graficos":
    tela_historico(df_fogo_filtrado if len(df_fogo_filtrado) > 0 else df_fogo_raw)

elif aba_selecionada == "Boia Costeira":
    tela_boia(df_oleo_filtrado)

# ─── RODAPÉ ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-size:11px;color:#aaa;padding:8px'>"
    "Guardião do Mar &nbsp;|&nbsp; "
    "Dados: IBAMA (manchas de oleo 2019) e INPE (focos de fogo 2026) &nbsp;|&nbsp; "
    "Em caso de emergência consulte sempre as autoridades competentes."
    "</div>", unsafe_allow_html=True
)
