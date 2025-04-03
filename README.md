<h1 align="center">🧬 Pathway & PPI Analysis App</h1>
<p align="center">
  <strong>Analyze gene lists for pathway enrichment and protein-protein interactions (PPI) with a powerful Streamlit-based bioinformatics tool.</strong>
</p>

<h2 align="center">🖼️ Screenshots</h2>

<p align="center">
  <img src="https://drive.google.com/uc?id=1yQrL2Bb8K4EUiBOG5G39_CXdaZWZSlRR" width="90%" alt="Screenshot 1"/>
  <br/><br/>
  <img src="https://drive.google.com/uc?id=ID_FOR_2.png" width="90%" alt="Screenshot 2"/>
  <br/><br/>
  <img src="https://drive.google.com/uc?id=ID_FOR_3.png" width="90%" alt="Screenshot 3"/>
  <br/><br/>
  <img src="https://drive.google.com/uc?id=ID_FOR_4.png" width="90%" alt="Screenshot 4"/>
  <br/><br/>
  <img src="https://drive.google.com/uc?id=ID_FOR_5.png" width="90%" alt="Screenshot 5"/>
</p>


<p align="center">
  <img src="https://drive.google.com/uc?id=19K32Xioz0Jq7ducXDyMhMuQfsd2qX2tI" width="80%"/>
</p>

---

## 🚀 Overview

This interactive app allows researchers and bioinformaticians to:

- Upload gene lists (`.csv` or `.xlsx`)
- Run **Pathway Enrichment** via STRING-DB API (Reactome, KEGG, WikiPathways, etc.)
- Perform **Protein-Protein Interaction (PPI)** network analysis with degree sorting
- Visualize top networks interactively using **pyvis**
- Download combined results in Excel format

---

## 🧪 Features

- 🎯 **Single or Combined Analysis**: Choose from Pathway, PPI, or Combined.
- 📊 **Real-time Visualization**: Preview enriched terms and hub genes.
- 🔍 **Interactive Graphs**: Explore top 20 nodes using force-directed layouts.
- 💾 **One-click Downloads**: Export to Excel with separate sheets for each analysis.

---

## 🖼️ Screenshots

<h4 align="center">1. Landing Page</h4>
<img src="https://drive.google.com/uc?id=19K32Xioz0Jq7ducXDyMhMuQfsd2qX2tI" width="100%"/>

<h4 align="center">2. Upload Gene File</h4>
<img src="https://drive.google.com/uc?id=1CDdpKY3n_0kUmyOaHj3r-dz_LYNGMLn6" width="100%"/>

<h4 align="center">3. Pathway Enrichment Preview</h4>
<img src="https://drive.google.com/uc?id=1m9P9VOvd7-7rb8da5zL7X7gY10EeIzkk" width="100%"/>

<h4 align="center">4. PPI Node Degree Output</h4>
<img src="https://drive.google.com/uc?id=1gCSSEUphzPpeHhMrMqaZKPzHRxR4-zOi" width="100%"/>

<h4 align="center">5. Interactive Network Graph</h4>
<img src="https://drive.google.com/uc?id=1whPSNvTPd4quRmQL5vRt7Jv_p1mF0-sE" width="100%"/>

<h4 align="center">6. Download Buttons</h4>
<img src="https://drive.google.com/uc?id=1Ok0x0Nez1A2FkHQEKuEpgk_MIbT9icLO" width="100%"/>

<h4 align="center">7. Stylish UI Elements</h4>
<img src="https://drive.google.com/uc?id=1__VBBRRKPlYeAq8B-rE-WgPIlfgb_Vnc" width="100%"/>

---

## 🧰 Tech Stack

- Python
- Streamlit
- pandas, requests, networkx, pyvis
- STRING API

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/pathway-ppi-app.git
cd pathway-ppi-app
pip install -r requirements.txt
streamlit run app.py
