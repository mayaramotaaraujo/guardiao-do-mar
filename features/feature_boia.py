import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import math

def render_boia_costeira(df_oleo=None):
    st.markdown("""
    <style>
    .boia-titulo {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0D2137;
        margin-bottom: 0.2rem;
    }
    .boia-subtitulo {
        font-size: 0.95rem;
        color: #5A7A99;
        margin-bottom: 1.5rem;
    }
    .alerta-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #E74C3C;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 20px rgba(231,76,60,0.3);
    }
    .alerta-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.8rem;
    }
    .alerta-titulo-texto {
        font-size: 1rem;
        font-weight: 700;
        color: #E74C3C;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .alerta-msg {
        color: #BDC3C7;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        font-style: italic;
    }
    .sensor-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.6rem;
    }
    .sensor-item {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .sensor-emoji { font-size: 1.1rem; }
    .sensor-label { color: #8898AA; font-size: 0.75rem; }
    .sensor-valor { color: #ECF0F1; font-size: 0.9rem; font-weight: 600; }
    .sensor-critico { color: #E74C3C !important; }
    .alerta-timestamp {
        margin-top: 0.8rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        color: #7F8C8D;
        font-size: 0.78rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .metrica-card {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #2980B9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 0.5rem;
    }
    .metrica-label { font-size: 0.75rem; color: #8898AA; text-transform: uppercase; letter-spacing: 0.5px; }
    .metrica-valor { font-size: 1.8rem; font-weight: 700; color: #0D2137; line-height: 1.1; }
    .metrica-unidade { font-size: 0.8rem; color: #8898AA; }
    .metrica-critico { border-left-color: #E74C3C !important; }
    .metrica-critico .metrica-valor { color: #E74C3C !important; }
    .metrica-alerta { border-left-color: #F39C12 !important; }
    .secao-titulo {
        font-size: 1rem;
        font-weight: 700;
        color: #0D2137;
        margin: 1.2rem 0 0.6rem 0;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #E8EEF4;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="boia-titulo"> Boia Costeira — Monitoramento Local</div>', unsafe_allow_html=True)
    st.markdown('<div class="boia-subtitulo">Sensores em tempo real ancorados no oceano. Alertas automáticos enviados ao Telegram quando valores críticos são detectados.</div>', unsafe_allow_html=True)

    # ─── VISUALIZAÇÃO ANIMADA DO OCEANO ──────────────────────────────────────
    components.html("""
    <style>
      #ocean-canvas { width: 100%; display: block; border-radius: 14px; }
      body { margin: 0; padding: 0; background: transparent; }
    </style>
    <canvas id="ocean-canvas" height="260"></canvas>
    <script>
    const canvas = document.getElementById('ocean-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth || 900;
    let W = canvas.width, H = canvas.height;
    let t = 0;

    // Manchas de óleo no oceano
    const manchas = [
      { x: 0.18, y: 0.38, r: 38, cor: '#C0392B', alfa: 0.82, label: 'Óleo crítico' },
      { x: 0.42, y: 0.28, r: 22, cor: '#E67E22', alfa: 0.75, label: 'Óleo moderado' },
      { x: 0.68, y: 0.22, r: 16, cor: '#E67E22', alfa: 0.65, label: 'Óleo moderado' },
      { x: 0.55, y: 0.52, r: 12, cor: '#27AE60', alfa: 0.5, label: 'Foco de fogo' },
      { x: 0.80, y: 0.48, r: 10, cor: '#F1C40F', alfa: 0.6, label: 'Risco de fogo' },
      { x: 0.30, y: 0.55, r: 8,  cor: '#27AE60', alfa: 0.5, label: 'Vegetação sadia' },
      { x: 0.90, y: 0.35, r: 7,  cor: '#27AE60', alfa: 0.45, label: 'Vegetação sadia' },
    ];

    // Boia
    let boiaX = 0.72, boiaY_base = 0.35;

    function waveY(x, time) {
      return Math.sin(x * 0.012 + time * 0.04) * 12
           + Math.sin(x * 0.025 - time * 0.025) * 7
           + Math.sin(x * 0.007 + time * 0.015) * 5;
    }

    function drawScene() {
      ctx.clearRect(0, 0, W, H);

      // Céu / fundo
      const sky = ctx.createLinearGradient(0, 0, 0, H * 0.55);
      sky.addColorStop(0, '#D6EAF8');
      sky.addColorStop(1, '#AED6F1');
      ctx.fillStyle = sky;
      ctx.fillRect(0, 0, W, H * 0.55);

      // Costa / terra
      const terra = ctx.createLinearGradient(0, H * 0.52, 0, H);
      terra.addColorStop(0, '#5D8A3C');
      terra.addColorStop(0.3, '#4A7A2E');
      terra.addColorStop(1, '#3A6B20');
      ctx.fillStyle = terra;
      ctx.fillRect(0, H * 0.52, W, H * 0.48);

      // Linha de costa ondulada
      ctx.beginPath();
      ctx.moveTo(0, H * 0.52 + waveY(0, t) * 0.3);
      for (let x = 1; x <= W; x++) {
        ctx.lineTo(x, H * 0.52 + waveY(x, t) * 0.3);
      }
      ctx.lineTo(W, H); ctx.lineTo(0, H);
      ctx.closePath();
      ctx.fillStyle = '#5D8A3C';
      ctx.fill();

      // Oceano
      const mar = ctx.createLinearGradient(0, 0, 0, H * 0.54);
      mar.addColorStop(0, '#1A5276');
      mar.addColorStop(0.5, '#1F618D');
      mar.addColorStop(1, '#2471A3');
      ctx.fillStyle = mar;
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(W, 0);
      ctx.lineTo(W, H * 0.50);
      for (let x = W; x >= 0; x--) {
        const wy = H * 0.50 + waveY(x, t);
        ctx.lineTo(x, wy);
      }
      ctx.closePath();
      ctx.fill();

      // Reflexo de luz no mar
      ctx.save();
      ctx.globalAlpha = 0.08;
      ctx.fillStyle = '#FFFFFF';
      for (let i = 0; i < 5; i++) {
        const rx = W * (0.1 + i * 0.18 + Math.sin(t * 0.02 + i) * 0.03);
        const ry = H * 0.18 + Math.sin(t * 0.03 + i * 0.7) * 8;
        ctx.beginPath();
        ctx.ellipse(rx, ry, 60, 6, Math.PI / 6, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();

      // Manchas de óleo e fogo
      manchas.forEach(m => {
        const mx = m.x * W;
        const my = m.y * H + Math.sin(t * 0.02 + m.x * 10) * 3;
        ctx.save();
        ctx.globalAlpha = m.alfa * (0.88 + Math.sin(t * 0.04 + m.x * 5) * 0.12);
        const g = ctx.createRadialGradient(mx, my, 0, mx, my, m.r);
        g.addColorStop(0, m.cor);
        g.addColorStop(1, m.cor + '00');
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(mx, my, m.r, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      });

      // Boia animada
      const bx = boiaX * W;
      const by = boiaY_base * H + waveY(bx, t);
      const incl = Math.sin(t * 0.04) * 0.15;

      // Âncora (linha pontilhada)
      ctx.save();
      ctx.setLineDash([3, 4]);
      ctx.strokeStyle = 'rgba(255,255,255,0.3)';
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(bx, by + 20);
      ctx.lineTo(bx, by + 60);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.restore();

      // Radar pulsante
      const pulso = (Math.sin(t * 0.06) + 1) / 2;
      ctx.save();
      ctx.globalAlpha = 0.15 + pulso * 0.25;
      ctx.strokeStyle = '#E74C3C';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(bx, by, 28 + pulso * 22, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();

      // Corpo da boia
      ctx.save();
      ctx.translate(bx, by);
      ctx.rotate(incl);
      // sombra
      ctx.shadowColor = 'rgba(0,0,0,0.35)';
      ctx.shadowBlur = 8;
      // cilindro
      const grad = ctx.createLinearGradient(-14, -10, 14, 10);
      grad.addColorStop(0, '#ECF0F1');
      grad.addColorStop(0.4, '#BDC3C7');
      grad.addColorStop(1, '#95A5A6');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.roundRect(-13, -10, 26, 20, 6);
      ctx.fill();
      // faixa vermelha
      ctx.fillStyle = '#E74C3C';
      ctx.fillRect(-13, -3, 26, 6);
      // luz piscante
      ctx.shadowBlur = 12;
      ctx.shadowColor = '#E74C3C';
      ctx.fillStyle = pulso > 0.5 ? '#E74C3C' : '#922B21';
      ctx.beginPath();
      ctx.arc(0, -14, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;
      ctx.restore();

      // Rótulo da boia
      ctx.save();
      ctx.font = 'bold 11px Arial';
      ctx.fillStyle = '#FFFFFF';
      ctx.textAlign = 'center';
      ctx.shadowColor = 'rgba(0,0,0,0.8)';
      ctx.shadowBlur = 4;
      ctx.fillText('B-02 • ATIVA', bx, by + 38);
      ctx.restore();

      // Legenda
      const legendItems = [
        { cor: '#C0392B', label: 'Óleo crítico (>60%)' },
        { cor: '#E67E22', label: 'Óleo moderado (20–60%)' },
        { cor: '#E74C3C', label: 'Fogo na vegetação' },
        { cor: '#F1C40F', label: 'Risco de fogo' },
        { cor: '#27AE60', label: 'Vegetação sadia' },
      ];
      ctx.save();
      let lx = 14, ly = H - 16;
      legendItems.forEach(item => {
        ctx.fillStyle = item.cor;
        ctx.beginPath();
        ctx.arc(lx + 6, ly, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#FFFFFF';
        ctx.font = '11px Arial';
        ctx.shadowColor = 'rgba(0,0,0,0.7)';
        ctx.shadowBlur = 3;
        ctx.fillText(item.label, lx + 16, ly + 4);
        lx += ctx.measureText(item.label).width + 36;
      });
      ctx.restore();

      t++;
      requestAnimationFrame(drawScene);
    }

    window.addEventListener('resize', () => {
      W = canvas.width = canvas.offsetWidth;
      H = canvas.height;
    });

    drawScene();
    </script>
    """, height=270)

    # ─── ALERTA SMART BUOY (dados reais do Telegram) ──────────────────────────
    st.markdown("""
    <div class="alerta-box">
      <div class="alerta-header">
        <span style="font-size:1.3rem">🚨</span>
        <span class="alerta-titulo-texto">Alerta Smart Buoy</span>
      </div>
      <div class="alerta-msg">⚠️ Possível alteração na qualidade da água detectada.</div>
      <div class="sensor-grid">
        <div class="sensor-item">
          <span class="sensor-emoji">🟦</span>
          <div>
            <div class="sensor-label">Turbidez</div>
            <div class="sensor-valor sensor-critico">4095 NTU</div>
          </div>
        </div>
        <div class="sensor-item">
          <span class="sensor-emoji">🌡️</span>
          <div>
            <div class="sensor-label">Temperatura</div>
            <div class="sensor-valor">24 °C</div>
          </div>
        </div>
        <div class="sensor-item">
          <span class="sensor-emoji">💧</span>
          <div>
            <div class="sensor-label">Umidade</div>
            <div class="sensor-valor">40%</div>
          </div>
        </div>
        <div class="sensor-item">
          <span class="sensor-emoji">📏</span>
          <div>
            <div class="sensor-label">Nível da água</div>
            <div class="sensor-valor">399,89 cm</div>
          </div>
        </div>
      </div>
      <div class="alerta-timestamp">
        🕐 09/06/2026 às 01:35:09 &nbsp;|&nbsp; Monitoramento automático da boia inteligente &nbsp;|&nbsp; Enviado via Telegram
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── MÉTRICAS RESUMIDAS ───────────────────────────────────────────────────
    st.markdown('<div class="secao-titulo">Leituras atuais da boia B-02 — Boia Pipa</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="metrica-card metrica-critico">
          <div class="metrica-label">Turbidez</div>
          <div class="metrica-valor">4095</div>
          <div class="metrica-unidade">NTU — CRÍTICO (limite: 80 NTU)</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metrica-card">
          <div class="metrica-label">Temperatura</div>
          <div class="metrica-valor">24</div>
          <div class="metrica-unidade">°C — normal</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metrica-card metrica-alerta">
          <div class="metrica-label">Nível da água</div>
          <div class="metrica-valor">399,89</div>
          <div class="metrica-unidade">cm — monitorando</div>
        </div>
        """, unsafe_allow_html=True)

    # ─── MAPA DAS 5 BOIAS ────────────────────────────────────────────────────
    st.markdown('<div class="secao-titulo"> Status das boias no litoral</div>', unsafe_allow_html=True)

    import plotly.graph_objects as go

    boias = [
        {"id": "B-01", "nome": "Boia Natal",        "lat": -5.79,  "lon": -35.20, "turbidez": 22,   "status": "Normal",   "cor": "#27AE60"},
        {"id": "B-02", "nome": "Boia Pipa",          "lat": -6.23,  "lon": -35.04, "turbidez": 4095, "status": "Crítico",  "cor": "#E74C3C"},
        {"id": "B-03", "nome": "Boia Areia Preta",   "lat": -5.76,  "lon": -35.19, "turbidez": 22,   "status": "Normal",   "cor": "#27AE60"},
        {"id": "B-04", "nome": "Boia Galinhos",      "lat": -4.97,  "lon": -36.26, "turbidez": 58,   "status": "Alerta",   "cor": "#F39C12"},
        {"id": "B-05", "nome": "Boia Canguaretama",  "lat": -6.37,  "lon": -35.13, "turbidez": 12,   "status": "Normal",   "cor": "#27AE60"},
    ]

    fig_boias = go.Figure()

    fig_boias.add_trace(go.Scattermapbox(
        lat=[b["lat"] for b in boias],
        lon=[b["lon"] for b in boias],
        mode="markers+text",
        marker=dict(
            size=[28 if b["status"] == "Crítico" else 20 if b["status"] == "Alerta" else 16 for b in boias],
            color=[b["cor"] for b in boias],
            opacity=0.9,
        ),
        text=[b["id"] for b in boias],
        textposition="top right",
        textfont=dict(size=11, color="white"),
        customdata=[[b["nome"], b["turbidez"], b["status"]] for b in boias],
        hovertemplate="<b>%{customdata[0]}</b><br>Turbidez: %{customdata[1]} NTU<br>Status: %{customdata[2]}<extra></extra>",
    ))

    fig_boias.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=-5.8, lon=-35.4),
            zoom=7,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig_boias, use_container_width=True)

    # Legenda de status
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("🟢 **Normal** — turbidez abaixo de 60 NTU")
    with c2:
        st.markdown("🟡 **Alerta** — turbidez entre 60 e 80 NTU")
    with c3:
        st.markdown("🔴 **Crítico** — turbidez acima de 80 NTU")

    # ─── HISTÓRICO DE ALERTAS ─────────────────────────────────────────────────
    st.markdown('<div class="secao-titulo"> Histórico de alertas enviados ao Telegram</div>', unsafe_allow_html=True)

    historico = [
        {"data": "09/06/2026", "hora": "01:35:09", "boia": "B-02 — Boia Pipa",       "turbidez": 4095, "temperatura": 24.0, "nivel": 399.89, "status": "🔴 Crítico"},
        {"data": "08/06/2026", "hora": "23:12:44", "boia": "B-02 — Boia Pipa",       "turbidez": 3820, "temperatura": 24.3, "nivel": 398.10, "status": "🔴 Crítico"},
        {"data": "08/06/2026", "hora": "18:47:22", "boia": "B-04 — Boia Galinhos",   "turbidez": 68,   "temperatura": 26.1, "nivel": 210.50, "status": "🟡 Alerta"},
        {"data": "08/06/2026", "hora": "14:05:11", "boia": "B-02 — Boia Pipa",       "turbidez": 3540, "temperatura": 25.0, "nivel": 401.20, "status": "🔴 Crítico"},
        {"data": "07/06/2026", "hora": "09:30:58", "boia": "B-04 — Boia Galinhos",   "turbidez": 72,   "temperatura": 27.2, "nivel": 198.30, "status": "🟡 Alerta"},
        {"data": "06/06/2026", "hora": "22:15:33", "boia": "B-02 — Boia Pipa",       "turbidez": 2980, "temperatura": 23.8, "nivel": 395.60, "status": "🔴 Crítico"},
    ]

    import pandas as pd
    df_hist = pd.DataFrame(historico)
    df_hist.columns = ["Data", "Hora", "Boia", "Turbidez (NTU)", "Temperatura (°C)", "Nível (cm)", "Status"]

    st.dataframe(
        df_hist,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Turbidez (NTU)": st.column_config.NumberColumn(format="%d NTU"),
            "Temperatura (°C)": st.column_config.NumberColumn(format="%.1f °C"),
            "Nível (cm)": st.column_config.NumberColumn(format="%.2f cm"),
        }
    )

    # ─── COMO FUNCIONA A BOIA ─────────────────────────────────────────────────
    with st.expander(" Como funciona a boia e seus sensores?"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("**💧 Turbidez da água**\n\nMedida pelo potenciômetro. Água turva pode indicar presença de óleo. Valores acima de 80 NTU são críticos.")
        with c2:
            st.info("**🌡️ Temperatura**\n\nMedida pelo DHT22. Mudanças bruscas indicam correntes oceânicas trazendo contaminação para a costa.")
        with c3:
            st.info("**📏 Nível da água (HC-SR04)**\n\nSensor ultrassônico que detecta objetos flutuantes próximos à boia, como acúmulo de óleo denso.")

    st.markdown("""
    <div style="margin-top:1rem; padding: 0.7rem 1rem; background:#F4F6F9; border-radius:8px; font-size:0.78rem; color:#7F8C8D;">
     Hardware: ESP32 + Potenciômetro (turbidez) + DHT22 (temperatura/umidade) + HC-SR04 (nível/distância) &nbsp;|&nbsp;
     Comunicação: MQTT via HiveMQ → Node-RED → InfluxDB &nbsp;|&nbsp;
     Alertas: Telegram Bot API &nbsp;|&nbsp;
     Dados de óleo: IBAMA 2019
    </div>
    """, unsafe_allow_html=True)
tela_boia = render_boia_costeira
