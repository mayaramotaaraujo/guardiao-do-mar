import pandas as pd
import pandas as pd
import os

BASE = r"C:\Users\Mayara\Downloads\guardiao_do_mar_vscode\guardiao_do_mar"
CAMINHO = os.path.join(BASE, "data", "guardiao_mar_localidades.csv")

def carregar_oleo():
    df = pd.read_csv(CAMINHO, header=1)
    df.columns = df.columns.str.strip()
    df.columns = [c.encode("ascii", "ignore").decode("ascii").strip() for c in df.columns]
    col_alerta = [c for c in df.columns if "lerta" in c.lower()]
    if col_alerta:
        df = df.rename(columns={col_alerta[0]: "Nivel Alerta"})
    col_mun = [c for c in df.columns if "unic" in c.lower()]
    if col_mun:
        df = df.rename(columns={col_mun[0]: "Municipio"})
    col_cor = [c for c in df.columns if "or" in c.lower() and "nter" in c.lower()]
    if col_cor:
        df = df.rename(columns={col_cor[0]: "Cor Interface"})
    col_exp = [c for c in df.columns if "xpos" in c.lower()]
    if col_exp:
        df = df.rename(columns={col_exp[0]: "Dias Exposicao"})
    df["DDLat"] = pd.to_numeric(df["DDLat"], errors="coerce")
    df["DDLon"] = pd.to_numeric(df["DDLon"], errors="coerce")
    df["Cobertura (%)"] = pd.to_numeric(df["Cobertura (%)"], errors="coerce").fillna(0)
    df = df.dropna(subset=["DDLat", "DDLon"])
    return df