import pandas as pd

NIVEL_COR_OLEO = {
    "MONITORAMENTO": "#1D9E75",
    "MODERADO":      "#FAC775",
    "ALERTA":        "#EF9F27",
    "CRITICO":       "#E24B4A",
}

NIVEL_COR_FOGO = {
    "MINIMO":  "#1D9E75",
    "BAIXO":   "#9FE1CB",
    "MEDIO":   "#FAC775",
    "ALTO":    "#EF9F27",
    "CRITICO": "#E24B4A",
}

def filtrar_oleo(df, estados=None, niveis=None):
    if estados:
        df = df[df["Estado"].isin(estados)]
    if niveis:
        df = df[df["Nivel Alerta"].isin(niveis)]
    return df

def filtrar_fogo(df, estados=None, datas=None, biomas=None, nivel_min=0.0):
    if estados:
        df = df[df["estado"].isin(estados)]
    if datas:
        df = df[df["data_arquivo"].isin(datas)]
    if biomas:
        df = df[df["bioma"].isin(biomas)]
    df = df[df["risco_fogo"] >= nivel_min]
    return df

def resumo_por_estado_fogo(df):
    return (
        df.groupby("estado")
          .agg(total_focos=("id","count"), risco_medio=("risco_fogo","mean"))
          .reset_index()
          .sort_values("total_focos", ascending=False)
    )

def serie_temporal_fogo(df):
    return (
        df.groupby("data_arquivo")
          .agg(total_focos=("id","count"), risco_medio=("risco_fogo","mean"))
          .reset_index()
          .sort_values("data_arquivo")
    )

def contadores(df_oleo, df_fogo):
    return {
        "manchas_oleo":     len(df_oleo),
        "focos_fogo":       len(df_fogo),
        "alertas_criticos": int(
            (df_oleo["Nivel Alerta"] == "CRITICO").sum() +
            (df_fogo["nivel_alerta"] == "CRITICO").sum()
        ),
        "estados_afetados": df_fogo["estado"].nunique(),
    }
