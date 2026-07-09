import streamlit as st, numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from translations import T_SIMULADOR, CSS, PLOT_COLORS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")
T = T_SIMULADOR[lang]

st.markdown("### 📊 Freenomics"); st.title(T["titulo"]); st.caption(T["subtitulo"])
st.sidebar.header(T["sidebar"])
inv_inicial = st.sidebar.number_input(T["inv_inicial"], value=1000, step=100, min_value=0)
contrib     = st.sidebar.number_input(T["contrib"], value=200, step=50, min_value=0)
anos        = st.sidebar.slider(T["anos"], 1, 40, 10)
retorno     = st.sidebar.slider(T["retorno"], 1.0, 20.0, 8.0, step=0.5)
inflacao    = st.sidebar.slider(T["inflacao"], 0.0, 6.0, 2.5, step=0.5)
st.sidebar.caption(T["dica"])

meses = anos*12; r_m = retorno/100/12; r_real_m = ((1+retorno/100)/(1+inflacao/100)-1)/12
vn, vr, ti = [], [], []
cn, cr, inv = inv_inicial, inv_inicial, inv_inicial
for _ in range(meses):
    cn = cn*(1+r_m)+contrib; cr = cr*(1+r_real_m)+contrib; inv += contrib
    vn.append(cn); vr.append(cr); ti.append(inv)

vf = vn[-1]; vreal = vr[-1]; tinv = ti[-1]; ganho = vf-tinv; mult = vf/tinv if tinv>0 else 1
col1,col2,col3,col4 = st.columns(4)
col1.metric(T["valor_final"], f"€{vf:,.0f}", f"+€{ganho:,.0f}")
col2.metric(T["valor_real"], f"€{vreal:,.0f}", T["adj_inflacao"])
col3.metric(T["total_inv"], f"€{tinv:,.0f}")
col4.metric(T["multiplicador"], f"{mult:.1f}x", f"{retorno}%/{T['anos_label']}")

st.subheader(T["grafico"])
labels = [m/12 for m in range(1, meses+1)]
fig = go.Figure()
fig.add_trace(go.Scatter(x=labels, y=vn, name=T["capital_nominal"], line=dict(color=PLOT_COLORS[0], width=2.5)))
fig.add_trace(go.Scatter(x=labels, y=ti, name=T["total_investido"], line=dict(color=PLOT_COLORS[1], width=2, dash="dash")))
fig.add_trace(go.Scatter(x=labels, y=vr, name=T["capital_real"], line=dict(color=PLOT_COLORS[2], width=1.5, dash="dot")))
fig.update_layout(plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3", yaxis_title=T["grafico_y"], xaxis_title=T["grafico_x"], hovermode="x unified", height=430, legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True)

st.subheader(T["marcos"])
marcos = [m for m in [5,10,15,20,25,30] if m<=anos]
if marcos:
    cols = st.columns(len(marcos))
    for col, ano in zip(cols, marcos):
        idx = ano*12-1
        col.metric(f"{ano} {T['anos_label']}", f"€{vn[idx]:,.0f}", f"{T['investido_label']}: €{ti[idx]:,.0f}")

import re
def renderizar(texto):
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", texto)

st.markdown(f"<div class='insight-box'>{renderizar(T['insight'](contrib,anos,retorno,tinv,vf,ganho,inflacao,vreal))}</div>", unsafe_allow_html=True)
st.caption(T["aviso"]); st.markdown("---"); st.caption(T["rodape"])
