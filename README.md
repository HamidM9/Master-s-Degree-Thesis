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

To enrich the dataset, network-base, **extrinsic** and **intrinsic (topological)** features are engineered:
### 🧬 Subnetwork-Based Feature Engineering

To enhance the biological interpretability and focus of feature engineering, this project incorporates **subnetworks discovered using the DAMOKLE algorithm**.

#### ⚙️ DAMOKLE Execution

We run the script `DAMOKLE-Python3-damokle-withoutloop.py` with multiple parameter configurations to generate diverse sets of **mutated subnetworks** from the gene-gene interaction network.

Each run produces subnetworks that are potentially enriched in cancer-relevant mutations.

#### 🧵 Subnetwork Processing Pipeline

Two utility scripts are used to post-process the DAMOKLE output:

- `extract_subnetworks_from_damokle_output.py`  
  Extracts all subnetworks from DAMOKLE result files.

- `extract_unique_genes_from_damokle_output.py`  
  Aggregates and deduplicates gene lists across all extracted subnetworks to produce a final set of **unique genes**.

#### 🧪 Gene Set Variants for Feature Selection

Three distinct gene sets are used as feature bases:

1. **DAMOKLE-only** — genes found exclusively in the discovered subnetworks.
2. **Compendium-only** — curated cancer genes from `Compendium_Cancer_Gene.txt`.
3. **Union set** — the combined set of DAMOKLE and Compendium genes.

Each set serves as a different feature subset, allowing for comparative analysis of their impact on classification performance.

These DAMOKLE-informed features introduce network-driven biological context into the dataset, offering a functional and mutation-aware dimension to the learning pipeline.

To add new features and fill them with zeros, we use the add_3_new_columns.py file, which can be easily modified to add more columns in different locations of the dataset.

#### 🔹 Extrinsic Features

These features are derived directly from mutation data and biological annotations:

- **Binary mutation presence** (1/0) for each gene
- **Mutation frequency per gene**
- **Cancer type labels** for supervised learning
- **Gene-level biological roles**, including:
  - **Oncogene**
  - **TSG** (Tumor Suppressor Gene)
  - **Fusion gene**
  - **Fate**
  - **Survival**
  - **Maintenance**

To count the number of mutated genes per category (e.g., oncogene, TSG, fusion) in each sample, the script `count_oncogene_TSG_fusion.py` is used.

This script:
- Loads mutation data from a CSV file.
- Loads gene classification mappings from `filtered_gene_classifications.txt`.
- Iterates through all mutated genes in each sample.
- Increments counts for each gene that belongs to a known class.
- Writes the updated dataset with added columns for counts of **oncogene**, **TSG**, and **fusion** genes.

The classification structure is modular — the script can be easily extended to include other gene categories such as **fate**, **survival**, and **maintenance**, simply by modifying the classification list and data mapping.

These extrinsic features reflect both the **statistical mutation patterns** and **biological functions** of genes relevant to cancer development.
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

Implemented in `accuracy.py`:

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

Feature combinations (binary, topological, extrinsic) were evaluated on classification tasks. Using engineered features significantly improved prediction accuracy across multiple models, especially when topological features were included.

---
---

## 🔬 Statistical Validation

To confirm the effectiveness of feature engineering and model enhancements, a ** One-sided Wilcoxon signed-rank test"** is used to statistically evaluate performance improvements.

The script `wilcoxon_test.py` performs a one-sided Wilcoxon signed-rank test to compare accuracy before and after applying specific features.

### 📄 How It Works

- Reads metric values (one per line) from two text files:  
  - `before.txt` (baseline performance)  
  - `after.txt` (post-enhancement performance)

- Executes a one-sided Wilcoxon test using `scipy.stats.wilcoxon`.

- Saves the output to:  
  `wilcoxon_results_one_sided/senza_counts/`

### 🧪 Example Usage

```python
perform_wilcoxon_test("results/before.txt", "results/after.txt", alternative="greater")

### UPDATING...
