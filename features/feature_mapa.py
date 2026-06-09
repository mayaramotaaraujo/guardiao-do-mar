import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from ui.componente_metrica import card_metrica

def tela_mapa(df_oleo, df_fogo, contadores_dados):
    st.markdown("### Mapa do Litoral Brasileiro")
    st.caption("Cada ponto no mapa representa um local com risco detectado. Passe o mouse para ver detalhes.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card_metrica("Manchas de oleo", contadores_dados["manchas_oleo"], "localidades", "#E24B4A", "")
    with col2:
        card_metrica("Focos de fogo", contadores_dados["focos_fogo"], "registros", "#EF9F27", "")
    with col3:
        card_metrica("Alertas criticos", contadores_dados["alertas_criticos"], "ocorrencias", "#E24B4A", "")
    with col4:
        card_metrica("Estados afetados", contadores_dados["estados_afetados"], "estados", "#042C53", "")

    st.markdown("---")
    col_esq, col_dir = st.columns([2, 1])

    with col_esq:
        fig = go.Figure()

        if len(df_oleo) > 0:
            fig.add_trace(go.Scattermapbox(
                lat=df_oleo["DDLat"],
                lon=df_oleo["DDLon"],
                mode="markers",
                marker=dict(
                    size=df_oleo["Cobertura (%)"].apply(lambda x: max(8, min(28, x * 0.6 + 8))),
                    color=df_oleo["Cor Interface"],
                    opacity=0.85,
                ),
                text=df_oleo["Nome da Localidade"],
                customdata=df_oleo[["Status Original", "Nivel Alerta", "Cobertura (%)"]],
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Situacao: %{customdata[0]}<br>"
                    "Nivel: %{customdata[1]}<br>"
                    "Cobertura: %{customdata[2]:.1f}%<br>"
                    "<extra>Oleo no mar</extra>"
                ),
                name="Mancha de oleo",
            ))

        if len(df_fogo) > 0:
            amostra_fogo = df_fogo.sample(min(200, len(df_fogo)), random_state=42)
            fig.add_trace(go.Scattermapbox(
                lat=amostra_fogo["lat"],
                lon=amostra_fogo["lon"],
                mode="markers",
                marker=dict(
                    size=amostra_fogo["frp"].apply(lambda x: max(5, min(18, x * 0.08 + 5))),
                    color=amostra_fogo["cor_interface"],
                    opacity=0.75,
                ),
                text=amostra_fogo["municipio"],
                customdata=amostra_fogo[["estado", "nivel_alerta", "risco_fogo", "bioma"]],
                hovertemplate=(
                    "<b>%{text} - %{customdata[0]}</b><br>"
                    "Nivel de risco: %{customdata[1]}<br>"
                    "Indice de risco: %{customdata[2]:.2f}<br>"
                    "Vegetacao: %{customdata[3]}<br>"
                    "<extra>Foco de fogo</extra>"
                ),
                name="Foco de fogo",
            ))

        fig.update_layout(
            mapbox=dict(style="carto-darkmatter", center=dict(lat=-8, lon=-38), zoom=4.5),
            margin=dict(l=0, r=0, t=0, b=0),
            height=520,
            legend=dict(
                bgcolor="rgba(0,0,0,0.5)", font=dict(color="white"),
                x=0.01, y=0.99, bordercolor="white", borderwidth=1
            ),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_dir:
        st.markdown("#### Legenda de cores")
        legendas = [
            ("Critico",          "#E24B4A"),
            ("Alerta / Alto",    "#EF9F27"),
            ("Moderado / Medio", "#FAC775"),
            ("Baixo risco",      "#9FE1CB"),
            ("Seguro",           "#1D9E75"),
        ]
        for texto, cor in legendas:
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:6px'>"
                f"<div style='width:16px;height:16px;border-radius:50%;background:{cor}'></div>"
                f"<span style='font-size:13px'>{texto}</span></div>",
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("#### O que cada ponto significa?")
        st.markdown("""
        <div style='padding:4px 0'>
            <div style='display:flex;align-items:flex-start;gap:12px;padding:8px 0;border-bottom:0.5px solid #eee'>
                <div style='width:14px;height:14px;border-radius:50%;background:#042C53;flex-shrink:0;margin-top:2px'></div>
                <div>
                    <div style='font-size:13px;font-weight:600;color:#222;margin-bottom:1px'>Círculo grande</div>
                    <div style='font-size:11px;color:#888'>Área mais afetada</div>
                </div>
            </div>
            <div style='display:flex;align-items:flex-start;gap:12px;padding:8px 0;border-bottom:0.5px solid #eee'>
                <div style='width:14px;height:14px;border-radius:50%;background:#B4B2A9;flex-shrink:0;margin-top:2px'></div>
                <div>
                    <div style='font-size:13px;font-weight:600;color:#222;margin-bottom:1px'>Círculo pequeno</div>
                    <div style='font-size:11px;color:#888'>Área com risco menor</div>
                </div>
            </div>
            <div style='display:flex;align-items:flex-start;gap:12px;padding:8px 0;border-bottom:0.5px solid #eee'>
                <div style='width:14px;height:14px;border-radius:50%;background:#E24B4A;flex-shrink:0;margin-top:2px'></div>
                <div>
                    <div style='font-size:13px;font-weight:600;color:#222;margin-bottom:1px'>Cor vermelha</div>
                    <div style='font-size:11px;color:#888'>Situação crítica</div>
                </div>
            </div>
            <div style='display:flex;align-items:flex-start;gap:12px;padding:8px 0'>
                <div style='width:14px;height:14px;border-radius:50%;background:#1D9E75;flex-shrink:0;margin-top:2px'></div>
                <div>
                    <div style='font-size:13px;font-weight:600;color:#222;margin-bottom:1px'>Cor verde</div>
                    <div style='font-size:11px;color:#888'>Situação sob controle</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
