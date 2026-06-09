import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from ui.componente_metrica import card_metrica
from ui.componente_alerta  import card_alerta

BOIAS = [
    {"id": "B-01", "nome": "Boia Pirangi",    "lat": -5.97, "lon": -35.13, "municipio": "Parnamirim - RN"},
    {"id": "B-02", "nome": "Boia Pipa",        "lat": -6.23, "lon": -35.04, "municipio": "Tibau do Sul - RN"},
    {"id": "B-03", "nome": "Boia Areia Preta", "lat": -5.79, "lon": -35.19, "municipio": "Natal - RN"},
    {"id": "B-04", "nome": "Boia Zumbi",       "lat": -5.32, "lon": -35.36, "municipio": "Rio do Fogo - RN"},
    {"id": "B-05", "nome": "Boia Sagi",        "lat": -6.47, "lon": -34.97, "municipio": "Baia Formosa - RN"},
]

def gerar_leituras_boia(boia_id, n=20):
    seed = abs(hash(boia_id)) % 100
    rng  = np.random.default_rng(seed)
    base_turb = {"B-01": 45, "B-02": 72, "B-03": 28, "B-04": 85, "B-05": 15}
    base_dist = {"B-01": 32, "B-02": 18, "B-03": 45, "B-04": 12, "B-05": 58}
    turbidez  = np.clip(rng.normal(base_turb.get(boia_id, 40), 12, n), 0, 100)
    temp      = np.clip(rng.normal(27.5, 1.5, n), 22, 35)
    distancia = np.clip(rng.normal(base_dist.get(boia_id, 35), 6, n), 2, 80)
    return pd.DataFrame({
        "minuto":    np.arange(n) * 5,
        "turbidez":  np.round(turbidez, 1),
        "temp":      np.round(temp, 1),
        "distancia": np.round(distancia, 1),
    })

def nivel_turbidez(valor):
    if valor >= 80:   return "CRITICO",  "#E24B4A"
    elif valor >= 60: return "ALERTA",   "#EF9F27"
    elif valor >= 40: return "MODERADO", "#FAC775"
    else:             return "SEGURO",   "#1D9E75"

def nivel_distancia(valor):
    if valor <= 10:   return "CRITICO", "#E24B4A"
    elif valor <= 20: return "ATENCAO", "#EF9F27"
    else:             return "NORMAL",  "#1D9E75"

def tela_boia(df_oleo):
    st.markdown("### Boia Costeira — Monitoramento Local")
    st.caption(
        "A boia fica ancorada no oceano e mede a qualidade da agua em tempo real. "
        "Quando detecta algo fora do normal, um aviso e enviado para as autoridades."
    )

    with st.expander("Como funciona a boia e seus sensores?", expanded=False):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(
                "<div style='background:#E6F1FB;border-radius:8px;padding:14px;text-align:center'>"
                "<div style='font-size:30px'>&#128167;</div>"
                "<div style='font-weight:600;color:#0C447C;margin:6px 0'>Turbidez da Agua</div>"
                "<div style='font-size:12px;color:#444'>Medido pelo potenciometro. "
                "Agua turva pode indicar presenca de oleo. "
                "Valores acima de 60 NTU sao preocupantes.</div>"
                "</div>", unsafe_allow_html=True
            )
        with col_b:
            st.markdown(
                "<div style='background:#FAEEDA;border-radius:8px;padding:14px;text-align:center'>"
                "<div style='font-size:30px'>&#127777;</div>"
                "<div style='font-weight:600;color:#633806;margin:6px 0'>Temperatura</div>"
                "<div style='font-size:12px;color:#444'>Medido pelo DHT22. "
                "Mudancas bruscas indicam correntes oceanicas "
                "trazendo contaminacao para a costa.</div>"
                "</div>", unsafe_allow_html=True
            )
        with col_c:
            st.markdown(
                "<div style='background:#E1F5EE;border-radius:8px;padding:14px;text-align:center'>"
                "<div style='font-size:30px'>&#128207;</div>"
                "<div style='font-weight:600;color:#085041;margin:6px 0'>Distancia de Objeto</div>"
                "<div style='font-size:12px;color:#444'>Medido pelo HC-SR04 ultrassonico. "
                "Detecta objetos flutuantes proximos a boia, "
                "como acumulo de oleo denso.</div>"
                "</div>", unsafe_allow_html=True
            )

    st.markdown("---")
    col_sel, col_info = st.columns([1, 2])

    with col_sel:
        nomes_boias = [f"{b['id']} — {b['nome']}" for b in BOIAS]
        escolha  = st.selectbox("Selecione uma boia:", options=nomes_boias)
        idx_boia = nomes_boias.index(escolha)
        boia     = BOIAS[idx_boia]
        st.markdown(
            f"<div style='background:#042C53;color:white;border-radius:8px;padding:12px;margin-top:8px'>"
            f"<div style='font-size:11px;color:#9FE1CB;margin-bottom:4px'>LOCALIZACAO</div>"
            f"<div style='font-weight:600'>{boia['nome']}</div>"
            f"<div style='font-size:12px;color:#aaa;margin-top:3px'>{boia['municipio']}</div>"
            f"<div style='font-size:11px;color:#aaa;margin-top:3px'>"
            f"Lat: {boia['lat']} | Lon: {boia['lon']}</div>"
            f"</div>", unsafe_allow_html=True
        )

    df_leit = gerar_leituras_boia(boia["id"])
    ultima  = df_leit.iloc[-1]
    nivel_t, cor_t = nivel_turbidez(ultima["turbidez"])
    nivel_d, cor_d = nivel_distancia(ultima["distancia"])

    with col_info:
        c1, c2, c3 = st.columns(3)
        with c1:
            card_metrica("Turbidez",    f"{ultima['turbidez']:.0f}", "NTU", cor_t,    "")
        with c2:
            card_metrica("Temperatura", f"{ultima['temp']:.1f}",     "C",   "#185FA5","")
        with c3:
            card_metrica("Distancia",   f"{ultima['distancia']:.0f}","cm",  cor_d,    "")

        if nivel_t in ["CRITICO", "ALERTA"]:
            card_alerta(
                tipo=f"BOIA {boia['id']} — TURBIDEZ {nivel_t}",
                local=f"{boia['nome']} — {boia['municipio']}",
                detalhe=f"Turbidez: {ultima['turbidez']:.0f} NTU | Possivel presenca de oleo na agua.",
                nivel=nivel_t,
                chave=f"boia_turb_{boia['id']}"
            )
        if nivel_d in ["CRITICO", "ATENCAO"]:
            card_alerta(
                tipo=f"BOIA {boia['id']} — OBJETO DETECTADO",
                local=f"{boia['nome']} — {boia['municipio']}",
                detalhe=f"HC-SR04: objeto a {ultima['distancia']:.0f} cm da boia. Possivel acumulo de oleo.",
                nivel=nivel_d,
                chave=f"boia_dist_{boia['id']}"
            )

    st.markdown("---")
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("#### Turbidez da agua")
        st.caption("Acima de 60 NTU: alerta | Acima de 80 NTU: critico")
        fig_turb = go.Figure()
        fig_turb.add_trace(go.Scatter(
            x=df_leit["minuto"], y=df_leit["turbidez"],
            mode="lines+markers",
            line=dict(color=cor_t, width=2.5),
            marker=dict(size=6, color=cor_t),
            fill="tozeroy", fillcolor="rgba(100,100,100,0.1)",
            hovertemplate="Minuto %{x}: %{y:.1f} NTU<extra></extra>",
        ))
        fig_turb.add_hline(y=60, line_dash="dash", line_color="#EF9F27",
                           annotation_text="Limite alerta", annotation_position="top right")
        fig_turb.add_hline(y=80, line_dash="dash", line_color="#E24B4A",
                           annotation_text="Limite critico", annotation_position="top right")
        fig_turb.update_layout(
            xaxis_title="Minutos", yaxis_title="Turbidez (NTU)",
            height=280, margin=dict(t=20, b=40),
            plot_bgcolor="#f8f9fa", paper_bgcolor="white", showlegend=False,
        )
        st.plotly_chart(fig_turb, use_container_width=True)

    with col_g2:
        st.markdown("#### Distancia e temperatura")
        st.caption("HC-SR04: objeto flutuante | DHT22: temperatura")
        fig_dt = go.Figure()
        fig_dt.add_trace(go.Scatter(
            x=df_leit["minuto"], y=df_leit["distancia"],
            mode="lines+markers", name="Distancia (cm)",
            line=dict(color=cor_d, width=2), marker=dict(size=5),
            hovertemplate="Minuto %{x}: %{y:.1f} cm<extra>HC-SR04</extra>",
            yaxis="y1"
        ))
        fig_dt.add_trace(go.Scatter(
            x=df_leit["minuto"], y=df_leit["temp"],
            mode="lines+markers", name="Temperatura (C)",
            line=dict(color="#185FA5", width=2, dash="dot"), marker=dict(size=5),
            hovertemplate="Minuto %{x}: %{y:.1f} C<extra>DHT22</extra>",
            yaxis="y2"
        ))
        fig_dt.update_layout(
            height=280, margin=dict(t=20, b=40),
            plot_bgcolor="#f8f9fa", paper_bgcolor="white",
            legend=dict(x=0.01, y=0.99),
            yaxis=dict(title="Distancia (cm)", title_font=dict(color=cor_d)),
            yaxis2=dict(title="Temperatura (C)", title_font=dict(color="#185FA5"),
                        overlaying="y", side="right"),
        )
        st.plotly_chart(fig_dt, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Posicao das boias no litoral do RN")

    dados_mapa = []
    for b in BOIAS:
        df_tmp = gerar_leituras_boia(b["id"])
        turb   = df_tmp.iloc[-1]["turbidez"]
        dist   = df_tmp.iloc[-1]["distancia"]
        nv, cr = nivel_turbidez(turb)
        dados_mapa.append({
            "id": b["id"], "nome": b["nome"], "municipio": b["municipio"],
            "lat": b["lat"], "lon": b["lon"],
            "turbidez": turb, "distancia": dist, "nivel": nv, "cor": cr,
        })
    df_mapa = pd.DataFrame(dados_mapa)

    fig_mapa = go.Figure()
    if len(df_oleo) > 0:
        fig_mapa.add_trace(go.Scattermapbox(
            lat=df_oleo["DDLat"], lon=df_oleo["DDLon"],
            mode="markers",
            marker=dict(size=10, color=df_oleo["Cor Interface"], opacity=0.45),
            text=df_oleo["Nome da Localidade"],
            hovertemplate="<b>%{text}</b><br>Mancha de oleo<extra></extra>",
            name="Mancha de oleo"
        ))
    fig_mapa.add_trace(go.Scattermapbox(
        lat=df_mapa["lat"], lon=df_mapa["lon"],
        mode="markers+text",
        marker=dict(size=20, color=df_mapa["cor"], opacity=0.95),
        text=df_mapa["id"],
        textposition="top center",
        textfont=dict(size=11, color="white"),
        customdata=df_mapa[["nome", "municipio", "turbidez", "distancia", "nivel"]],
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>%{customdata[1]}<br>"
            "Turbidez: %{customdata[2]:.0f} NTU<br>"
            "Distancia HC-SR04: %{customdata[3]:.0f} cm<br>"
            "Nivel: %{customdata[4]}<extra>Boia Costeira</extra>"
        ),
        name="Boia costeira"
    ))
    fig_mapa.add_trace(go.Scattermapbox(
        lat=[boia["lat"]], lon=[boia["lon"]],
        mode="markers",
        marker=dict(size=32, color="white", opacity=0.3),
        hoverinfo="skip", showlegend=False
    ))
    fig_mapa.update_layout(
        mapbox=dict(style="carto-darkmatter", center=dict(lat=-5.8, lon=-35.2), zoom=7.5),
        margin=dict(l=0, r=0, t=0, b=0), height=420,
        legend=dict(bgcolor="rgba(0,0,0,0.5)", font=dict(color="white"), x=0.01, y=0.99),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_mapa, use_container_width=True)

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;font-size:11px;color:#aaa;padding:8px'>"
        "Hardware: ESP32 + Potenciometro (turbidez) + DHT22 (temperatura) + HC-SR04 (distancia) | "
        "Comunicacao: MQTT via HiveMQ | Alertas: Telegram | Dados oleo: IBAMA 2019"
        "</div>", unsafe_allow_html=True
    )
