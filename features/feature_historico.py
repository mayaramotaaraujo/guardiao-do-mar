import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pipelines.pipeline_dados import serie_temporal_fogo, resumo_por_estado_fogo

def tela_historico(df_fogo):
    st.markdown("### Historico de Focos de Fogo")
    st.caption("Veja como os focos de fogo mudaram ao longo das semanas no nordeste brasileiro.")

    serie  = serie_temporal_fogo(df_fogo)
    resumo = resumo_por_estado_fogo(df_fogo)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Quantidade de focos por dia")
        fig_linha = px.line(
            serie, x="data_arquivo", y="total_focos",
            markers=True,
            labels={"data_arquivo": "Data", "total_focos": "Total de focos"},
            color_discrete_sequence=["#EF9F27"],
        )
        fig_linha.update_traces(
            line_width=3, marker_size=8,
            hovertemplate="<b>%{x}</b><br>Focos: %{y}<extra></extra>"
        )
        fig_linha.update_layout(
            plot_bgcolor="#f8f9fa", paper_bgcolor="white",
            height=320, margin=dict(t=10, b=40),
        )
        st.plotly_chart(fig_linha, use_container_width=True)

    with col2:
        st.markdown("#### Total de focos por estado")
        fig_barra = px.bar(
            resumo, x="total_focos", y="estado",
            orientation="h",
            labels={"total_focos": "Total de focos", "estado": "Estado"},
            color="total_focos",
            color_continuous_scale=["#1D9E75", "#FAC775", "#EF9F27", "#E24B4A"],
        )
        fig_barra.update_layout(
            plot_bgcolor="#f8f9fa", paper_bgcolor="white",
            height=320, margin=dict(t=10, b=40),
            showlegend=False, coloraxis_showscale=False,
        )
        st.plotly_chart(fig_barra, use_container_width=True)

    st.markdown("#### Distribuicao por bioma")
    fig_mat, ax = plt.subplots(figsize=(8, 3.5))
    bioma_counts = df_fogo["bioma"].value_counts()
    cores_bioma  = ["#1D9E75", "#EF9F27", "#185FA5", "#E24B4A"]
    bars = ax.barh(bioma_counts.index, bioma_counts.values,
                   color=cores_bioma[:len(bioma_counts)])
    ax.set_xlabel("Quantidade de focos", fontsize=10)
    ax.set_title("Focos por tipo de vegetacao", fontsize=11, fontweight="bold")
    for bar, val in zip(bars, bioma_counts.values):
        ax.text(val + 10, bar.get_y() + bar.get_height()/2,
                str(val), va="center", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig_mat.patch.set_facecolor("#f8f9fa")
    ax.set_facecolor("#f8f9fa")
    plt.tight_layout()
    st.pyplot(fig_mat)
    plt.close()

    st.markdown("#### Resumo por estado")
    st.dataframe(
        resumo.rename(columns={
            "estado": "Estado",
            "total_focos": "Total de Focos",
            "risco_medio": "Risco Medio"
        }).style.format({"Risco Medio": "{:.2f}"}),
        use_container_width=True, hide_index=True
    )
