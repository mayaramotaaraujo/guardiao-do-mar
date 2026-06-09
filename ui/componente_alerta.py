import streamlit as st
from datetime import datetime

CORES = {
    "CRITICO":       ("#E24B4A", "#FCEBEB"),
    "ALERTA":        ("#EF9F27", "#FAEEDA"),
    "MODERADO":      ("#FAC775", "#FFF8E7"),
    "MONITORAMENTO": ("#1D9E75", "#E1F5EE"),
    "ALTO":          ("#EF9F27", "#FAEEDA"),
    "MEDIO":         ("#FAC775", "#FFF8E7"),
    "BAIXO":         ("#9FE1CB", "#E1F5EE"),
    "MINIMO":        ("#1D9E75", "#E1F5EE"),
    "ATENCAO":       ("#EF9F27", "#FAEEDA"),
    "NORMAL":        ("#1D9E75", "#E1F5EE"),
}

def card_alerta(tipo, local, detalhe, nivel, chave=None):
    cor_borda, cor_fundo = CORES.get(nivel.upper(), ("#888", "#f5f5f5"))
    st.markdown(
        f"""
        <div style='background:{cor_fundo};border-left:5px solid {cor_borda};
                    border-radius:8px;padding:12px 14px;margin-bottom:10px;'>
            <div style='font-size:11px;font-weight:600;color:{cor_borda};
                        text-transform:uppercase;margin-bottom:4px'>{tipo}</div>
            <div style='font-size:14px;font-weight:600;color:#222'>{local}</div>
            <div style='font-size:12px;color:#555;margin-top:3px'>{detalhe}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if chave and nivel.upper() in ["CRITICO", "ALERTA", "ALTO", "ATENCAO"]:
        if st.button("Confirmar aviso para autoridades", key=chave, type="primary"):
            if "historico_alertas" not in st.session_state:
                st.session_state["historico_alertas"] = []
            st.session_state["historico_alertas"].append({
                "tipo": tipo, "local": local, "nivel": nivel,
                "hora": datetime.now().strftime("%d/%m %H:%M")
            })
            st.success("Aviso enviado para as autoridades responsaveis!")
            st.balloons()
