import pandas as pd
import os

BASE = r"C:\Users\Mayara\Downloads\guardiao_do_mar_vscode\guardiao_do_mar"
CAMINHO = os.path.join(BASE, "data", "focos_nordeste_consolidado.csv")

def carregar_fogo():
    df = pd.read_csv(CAMINHO)
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["risco_fogo"] = pd.to_numeric(df["risco_fogo"], errors="coerce").fillna(0)
    df["frp"] = pd.to_numeric(df["frp"], errors="coerce").fillna(0)
    df["numero_dias_sem_chuva"] = pd.to_numeric(df["numero_dias_sem_chuva"], 
errors="coerce").fillna(0)
    df = df.dropna(subset=["lat", "lon"])
    return df