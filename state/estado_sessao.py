import streamlit as st

def inicializar():
    defaults = {
        "estados_selecionados": [],
        "datas_selecionadas":   [],
        "biomas_selecionados":  [],
        "nivel_risco_min":      0.0,
        "aba_ativa":            "Mapa",
        "alerta_confirmado":    False,
        "alerta_pendente":      None,
        "historico_alertas":    [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def resetar():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    inicializar()
