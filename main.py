
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import json
import io
import networkx as nx
from pyvis.network import Network

# =========================
# Minimal Bioinformatics Analysis App
# =========================

st.set_page_config(page_title="Pathway + PPI Analysis", layout="centered", page_icon="🧬")

# Inject custom CSS styling
st.markdown("""
<style>
h1, h2, h3 {
    color: #ffffff;
    text-align: center;
}
body {
    background-image: url('https://www.genome.gov/sites/default/files/tg/en/illustration/DNA_helix_hero.jpg');
    background-size: cover;
    background-attachment: fixed;
    background-repeat: no-repeat;
}
textarea:hover, .stTextInput>div:hover {
    border: 2px solid #FF5733 !important;
    box-shadow: 0 0 10px rgba(255,87,51,0.6);
}
.stButton>button:hover {
    background-color: #FF5733 !important;
    color: white !important;
    transform: scale(1.05);
}
.response-box {
    background-color: rgba(255, 255, 255, 0.92);
    padding: 20px;
    border-radius: 10px;
    color: #000000;
    font-size: 1rem;
    line-height: 1.5;
    margin-top: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# Title & Description
st.markdown("<h1>🧬 Pathway & PPI Analysis Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e0e0e0;'>Upload your gene list to perform pathway enrichment and interaction analysis.</p>", unsafe_allow_html=True)
st.markdown("---")

# Analysis Selector
analysis_type = st.selectbox("Select Analysis Type", ["Pathway Enrichment", "PPI Analysis", "Combined Analysis"])
uploaded_file = st.file_uploader("Upload your gene file (Excel or CSV)", type=["xlsx", "csv"])

if uploaded_file is not None and st.button("Run Analysis"):
    try:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    if "Gene" not in df.columns and "gene" not in df.columns:
        st.error("Your file must contain a 'Gene' or 'gene' column.")
        st.stop()

    df.rename(columns={"gene": "Gene"}, inplace=True)
    genes = df["Gene"].dropna().tolist()
    pathway_results_df, ppi_results_df = pd.DataFrame(), pd.DataFrame()

    if analysis_type in ["Pathway Enrichment", "Combined Analysis"]:
        st.info("Running Pathway Enrichment...")
        request_url = "https://string-db.org/api/json/enrichment"
        results_list = []
        for gene in genes:
            params = {"identifiers": gene, "species": 9606, "caller_identity": "your_app_name"}
            try:
                response = requests.post(request_url, data=params)
                if response.status_code == 200:
                    data = json.loads(response.text)
                    for row in data:
                        if row.get("category") in ["Process", "KEGG", "Reactome", "WikiPathways", "Pfam", "InterPro", "SMART"] and row.get("fdr", 1) < 0.05:
                            results_list.append({
                                'Gene': gene,
                                'Term': row.get("term", ""),
                                'Preferred Names': ",".join(row.get("preferredNames", [])),
                                'FDR': float(row.get("fdr", 1)),
                                'Description': row.get("description", ""),
                                'Category': row.get("category", "")
                            })
            except Exception as e:
                st.write(f"Failed to process {gene}: {e}")

        pathway_results_df = pd.DataFrame(results_list)
        pathway_merged_df = pd.merge(df, pathway_results_df, how="left", on="Gene") if not pathway_results_df.empty else df.copy()
        st.subheader("Pathway Enrichment Results Preview")
        st.dataframe(pathway_merged_df.head(15))

    if analysis_type in ["PPI Analysis", "Combined Analysis"]:
        st.info("Running PPI Analysis...")
        def query_stringdb_batch(gene_list):
            url = "https://string-db.org/api/json/network?identifiers="
            ppi_data = []
            for i in range(0, len(gene_list), 500):
                genes_query = '%0D'.join(gene_list[i:i+500])
                try:
                    resp = requests.get(url + genes_query + "&species=9606")
                    if resp.status_code == 200:
                        ppi_data.extend(resp.json())
                except: pass
            return ppi_data

        ppi_data = query_stringdb_batch(genes)
        G = nx.Graph()
        for interaction in ppi_data:
            if interaction.get("score", 0) >= 0.15:
                G.add_edge(
                    (interaction["preferredName_A"], interaction["stringId_A"]),
                    (interaction["preferredName_B"], interaction["stringId_B"]),
                    weight=interaction["score"]
                )

        node_data = [[n[0], n[1], deg] for n, deg in G.degree()]
        ppi_results_df = pd.DataFrame(node_data, columns=["Gene", "Identifier", "Node Degree"])
        ppi_results_df_sorted = ppi_results_df.sort_values(by="Node Degree", ascending=False)
        st.subheader("PPI Node Degree Preview")
        st.dataframe(ppi_results_df_sorted.head(15))

        top_20 = ppi_results_df_sorted.head(20)["Gene"].tolist()
        G_top = nx.Graph()
        for edge in ppi_data:
            if edge["preferredName_A"] in top_20 and edge["preferredName_B"] in top_20:
                G_top.add_edge(edge["preferredName_A"], edge["preferredName_B"], weight=edge["score"])
        net = Network(height="800px", width="100%", notebook=True)
        for node in G_top.nodes(): net.add_node(node, label=node)
        for u, v, d in G_top.edges(data=True): net.add_edge(u, v, weight=d["weight"])
        net.force_atlas_2based()
        net_path = "network.html"
        net.save_graph(net_path)
        with open(net_path, "r", encoding="utf-8") as f:
            components.html(f.read(), height=800, scrolling=True)

    if analysis_type == "Combined Analysis":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            (pathway_merged_df if not pathway_results_df.empty else df).to_excel(writer, sheet_name="Pathway Enrichment", index=False)
            (ppi_results_df_sorted if not ppi_results_df.empty else df).to_excel(writer, sheet_name="PPI Analysis", index=False)
        output.seek(0)
        st.download_button("Download Combined Excel", data=output, file_name="combined_results.xlsx")
    elif analysis_type == "Pathway Enrichment" and not pathway_results_df.empty:
        out = io.BytesIO()
        pathway_merged_df.to_excel(out, index=False)
        out.seek(0)
        st.download_button("Download Pathway Enrichment", data=out, file_name="pathway_enrichment.xlsx")
    elif analysis_type == "PPI Analysis" and not ppi_results_df.empty:
        out = io.BytesIO()
        ppi_results_df_sorted.to_excel(out, index=False)
        out.seek(0)
        st.download_button("Download PPI Results", data=out, file_name="ppi_analysis.xlsx")
