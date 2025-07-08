# Master's Degree Thesis

This repository contains the code developed for a master's degree thesis on **subnetwork discovery and cancer type prediction** in gene-gene interaction networks, carried out at the **University of Padua**.

The code is well-commented and supplemented with relevant explanations.

This thesis is composed of two main parts: **Subnetwork Discovery** and **Feature Engineering**.

---

## 📁 Datasets

The project is based on three key datasets:

- **`snvs.tsv`**  
  Contains data on single-nucleotide variants (SNVs), the most common form of genetic variation. SNVs occur when a single nucleotide in the genome sequence is altered. This dataset includes **3,110 samples** and **19,424 different mutations**.

- **`Compendium_Cancer_Gene.txt`**  
  A list of **568 genes** potentially associated with various cancers.

- **`samples_labels.txt`**  
  A tabular file where each row represents a sample and its corresponding cancer type. It includes **3,110 samples** across **11 cancer types**:  
  BRCA, KIRC, OV, HNSC, GBM, UCEC, LAML, COADREAD, LUAD, LUSC, BLCA

---

## 🧪 Dataset Creation

The script `make_the_dataset.py` processes the above files to construct a machine learning-ready dataset:

- Samples (from `samples_labels.txt`) are used as indices.
- Features correspond to genes listed in `Compendium_Cancer_Gene.txt`.
- For each sample-gene pair:
  - If the mutation exists in `snvs.tsv`, a **1** is assigned.
  - Otherwise, a **0** is assigned.
- The cancer type is added as the final column based on `samples_labels.txt`.

---

## 🤖 Classification and Prediction

The script `primary_classic_methods.py` applies traditional machine learning models for cancer type classification:

- **Cancer types are label-encoded**
- Models implemented:
  - Logistic Regression
  - Decision Tree
  - Support Vector Machine (SVM) with:
    - Kernels: linear, polynomial, RBF, sigmoid
    - C values: 0.1, 1, 10, 100
  - Random Forest with:
    - Estimators: 1, 10, 40, 50, 100, 150, 200

### 🔗 Ensemble Model

An ensemble approach using both **soft voting** and **hard voting** is implemented with the following components:

- `model1`: Logistic Regression  
- `model2`: Random Forest (`n_estimators = 100`)  
- `model3`: SVM (`C = 1`)

---

## 🧠 Feature Engineering

The second part of this thesis is dedicated to **feature engineering**, aiming to enhance the accuracy of cancer type prediction models. Two main types of features were engineered from the gene-gene interaction network and mutation data:

### 🔹 Topological Features

Topological features capture the structural role of each gene within the gene-gene interaction network. These features were computed using graph-based measures, including:

- **Degree Centrality** — number of direct connections a gene has.
- **Clustering Coefficient** — how densely connected a gene’s neighbors are.
- **Betweenness Centrality** — how often a gene appears on the shortest paths between other genes.
- **Closeness Centrality** — average distance from a gene to all other genes in the network.
- **PageRank** — measures gene importance based on the global link structure.

These features reflect the functional and relational significance of genes in the biological network.

### 🔹 Extrinsic Features

Extrinsic features are derived from the mutation data and the sample labels. These include:

- **Mutation frequency per gene** — how frequently each gene is mutated across samples.
- **Binary mutation presence** — a binary matrix indicating whether a gene is mutated (1) or not (0) in a given sample.
- **Sample-specific mutation vectors** — capturing the unique mutation profile of each sample.
- **Cancer type labels** — used as target classes for supervised learning.

By combining **topological** and **extrinsic** features, the dataset becomes richer and more informative, enabling more effective machine learning models for **multi-class cancer type classification**.

---

Feel free to explore, fork, or contribute!
