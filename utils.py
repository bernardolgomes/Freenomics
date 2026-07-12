"""
utils.py — Freenomics
Funções partilhadas entre todas as páginas.
"""
import streamlit as st
import os
import base64

def show_logo():
    """Mostra o logo + nome Freenomics no topo da página."""
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
            <img src="data:image/png;base64,{logo_b64}"
                 style="width:42px;height:42px;border-radius:8px;"/>
            <span style="font-size:1.1rem;font-weight:700;
                         color:#4FB8C4;letter-spacing:0.5px;">Freenomics</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### 📊 Freenomics")
