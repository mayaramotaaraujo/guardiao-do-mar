import streamlit as st

def card_metrica(titulo, valor, unidade="", cor="#042C53", icone=""):
    st.markdown(
        f"""
        <div style='background:{cor}15;border-left:4px solid {cor};
                    border-radius:8px;padding:12px 16px;margin-bottom:8px;'>
            <div style='font-size:12px;color:#666;font-weight:500'>{icone} {titulo}</div>
            <div style='font-size:28px;font-weight:700;color:{cor};line-height:1.2'>
                {valor}
            </div>
            <div style='font-size:11px;color:#888'>{unidade}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
