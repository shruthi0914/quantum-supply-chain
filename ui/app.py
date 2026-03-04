import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(page_title="Quantum Supply Chain Agent", layout="wide")

st.title("📦 Quantum Supply Chain Agent")
st.markdown("### Senior Decision Intelligence System for Supply Chain Optimization")

query = st.text_input("Ask a business question:", placeholder="Which products are likely to run out of stock next week?")

if st.button("Run Analysis"):
    if query:
        with st.spinner("Agentic workflow in progress..."):
            try:
                # In production, this would point to the FastAPI endpoint
                # For demo purposes, we can call the orchestrator directly or assume API is up
                response = requests.post("http://localhost:8000/ask", json={"query": query})
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analysis Complete")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("Executive Explanation")
                        st.write(data["result"])
                    
                    with col2:
                        st.subheader("Key Metrics")
                        st.metric("Stockout Risk", "35%", "-5%")
                        st.metric("Inventory Turnover", "4.2", "+0.8")
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Could not connect to API: {e}")
    else:
        st.warning("Please enter a query.")

st.sidebar.markdown("---")
st.sidebar.info("Powering autonomous supply chain decisions with Multi-Agent AI.")
