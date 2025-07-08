### UPDATING...

# Master's Degree Thesis

This repository contains the code developed for a master's degree thesis on **subnetwork discovery and cancer type prediction** in gene-gene interaction networks, carried out at the **University of Padua**.

The code is well-commented and supplemented with relevant explanations.

This thesis is composed of two main parts: **Subnetwork Discovery** and **Feature Engineering**.
## Part I: Subnetwork Discovery
to be updated
## Part II: Feature Engineering

The second part of this thesis focuses on engineering a structured dataset from mutation data and gene-gene interaction networks to enable cancer type classification using machine learning.

### 📦 Input Files

- **`snvs.tsv`**  
  Contains 3,110 samples and 19,424 SNVs (single-nucleotide variants).

- **`Compendium_Cancer_Gene.txt`**  
  A curated list of 568 genes known to be related to cancer.

- **`samples_labels.txt`**  
  Maps each sample to one of 11 cancer types:  
  BRCA, KIRC, OV, HNSC, GBM, UCEC, LAML, COADREAD, LUAD, LUSC, BLCA

---

### 🛠 Dataset Construction

The dataset is built using `make_the_dataset.py` by combining all three files:

- Rows are samples, and columns are gene mutation indicators (1 if mutated, 0 otherwise).
- Each gene from `Compendium_Cancer_Gene.txt` becomes a binary feature.
- Cancer type is added as the final label column.

---

### ✨ Feature Types

To enrich the dataset, both **extrinsic** and **intrinsic (topological)** features are engineered:

#### 🔹 Extrinsic Features

These are derived directly from mutation data:

#### 🔹 Extrinsic Features

These are derived directly from mutation data and biological annotations:

- **Binary mutation presence** (1/0) for each gene
- **Mutation frequency per gene**
- **Cancer type labels** for supervised learning
- **Gene-level biological roles**, such as:
  - **TSG** (Tumor Suppressor Gene)
  - **Oncogene**
  - **Fusion gene**
  - **Fate**
  - **Survival**
  - **Maintenance**

These features reflect both the statistical mutation patterns and known biological functions of genes relevant to cancer development.


These features reflect mutation patterns and sample-level characteristics.

#### 🔸 Intrinsic (Topological) Features

Extracted from the gene-gene interaction network using graph-based analysis:

- **Degree Centrality** — number of direct connections
- **Betweenness Centrality** — importance based on shortest paths
- **Closeness Centrality** — inverse of total distance to all other nodes
- **Clustering Coefficient** — local neighborhood density
- **PageRank** — importance via link structure
- **Eigenvector Centrality** — influence of a node in terms of the importance of neighbors

Each gene is enriched with these graph-based scores, making the feature space biologically meaningful.

---

### 🤖 Classification Methods

Implemented in `primary_classic_methods.py`:

- **Label encoding** for cancer types
- Models used:
  - Logistic Regression
  - Decision Tree
  - Support Vector Machine (SVM)  
    - Kernels: `linear`, `poly`, `rbf`, `sigmoid`  
    - C values: `0.1`, `1`, `10`, `100`
  - Random Forest  
    - Estimators: `1`, `10`, `40`, `50`, `100`, `150`, `200`

---

### 🔗 Ensemble Learning

An ensemble model uses both **soft voting** and **hard voting**, combining:

- `model1`: Logistic Regression  
- `model2`: Random Forest (`n_estimators=100`)  
- `model3`: SVM (`C=1`)

---

### 📊 Numerical Results

Feature combinations (binary, topological, extrinsic) were evaluated on classification tasks. Using engineered features significantly improved prediction accuracy across multiple models — especially when topological features were included.

---

### UPDATING...
