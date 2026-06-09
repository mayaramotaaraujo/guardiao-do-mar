import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from ui.componente_alerta import card_alerta

def tela_alertas(df_oleo, df_fogo):
    st.markdown("### Alertas Ativos")
    st.caption("Situacoes que precisam de atencao agora. Voce pode confirmar o envio de avisos para as autoridades.")

    col_oleo, col_fogo = st.columns(2)

    with col_oleo:
        st.markdown("#### Manchas de oleo no mar")
        criticos_oleo = df_oleo[df_oleo["Nivel Alerta"].isin(["CRITICO", "ALERTA"])]
        if len(criticos_oleo) == 0:
            st.success("Nenhuma mancha critica no momento.")
        else:
            for i, row in criticos_oleo.iterrows():
                card_alerta(
                    tipo="OLEO NO MAR",
                    local=f"{row['Nome da Localidade']} — {row['Municipio']} ({row['Estado']})",
                    detalhe=f"Situacao: {row['Status Original']} | Cobertura: {row['Cobertura (%)']:.1f}%",
                    nivel=row["Nivel Alerta"],
                    chave=f"oleo_{i}"
                )

    with col_fogo:
        st.markdown("#### Focos de fogo na vegetacao")
        criticos_fogo = df_fogo[df_fogo["nivel_alerta"].isin(["CRITICO", "ALTO"])].head(10)
        if len(criticos_fogo) == 0:
            st.success("Nenhum foco critico no momento.")
        else:
            for i, row in criticos_fogo.iterrows():
                card_alerta(
                    tipo="FOGO NA VEGETACAO",
                    local=f"{row['municipio']} — {row['estado']}",
                    detalhe=f"Risco: {row['risco_fogo']:.2f} | Vegetacao: {row['bioma']} | Dias sem chuva: {int(row['numero_dias_sem_chuva'])}",
                    nivel=row["nivel_alerta"],
                    chave=f"fogo_{i}"
                )

    if st.session_state.get("historico_alertas"):
        st.markdown("---")
        st.markdown("#### Avisos ja enviados nesta sessao")
        for alerta in reversed(st.session_state["historico_alertas"]):
            st.markdown(f"**{alerta['hora']}** — {alerta['tipo']} em {alerta['local']} ({alerta['nivel']})")
