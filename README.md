# Master's Degree Thesis

This repository contains the code developed for a master's degree thesis on **subnetwork discovery and cancer type prediction** in gene-gene interaction networks, carried out at the **University of Padua**.

The code is well-commented and supplemented with relevant explanations.

## 📁 Datasets

The project is based on three key datasets:

- **`snvs.tsv`**  
  Contains data on single-nucleotide variants (SNVs), the most common form of genetic variation. SNVs occur when a single nucleotide in the genome sequence is altered. This dataset includes **3,110 samples** and **19,424 different mutations**.

- **`Compendium_Cancer_Gene.txt`**  
  A list of **568 genes** potentially associated with various cancers.

- **`samples_labels.txt`**  
  A tabular file where each row represents a sample and its corresponding cancer type. It includes **3,110 samples** across **11 cancer types**:
  - BRCA, KIRC, OV, HNSC, GBM, UCEC, LAML, COADREAD, LUAD, LUSC, BLCA

## 🛠 Dataset Creation

The script `make_the_dataset.py` processes the above files to construct a machine learning-ready dataset:

- Samples (from `samples_labels.txt`) are set as indices.
- Features correspond to genes listed in `Compendium_Cancer_Gene.txt`.
- For each sample-gene pair:
  - If the mutation exists in `snvs.tsv`, a **1** is assigned.
  - Otherwise, a **0** is assigned.
- The cancer type is added as the final column based on `samples_labels.txt`.

## 🤖 Classification and Prediction

The script `primary_classic_methods.py` applies classic machine learning models for cancer type prediction:

- **Cancer types are label-encoded**
- Models used:
  - Logistic Regression
  - Decision Tree
  - Support Vector Machine (SVM) with:
    - Kernels: linear, polynomial, RBF, sigmoid
    - C values: 0.1, 1, 10, 100
  - Random Forest with:
    - Estimators: 1, 10, 40, 50, 100, 150, 200

### 🔗 Ensemble Model

An ensemble approach using **soft voting** and **hard voting** is also implemented:

- `model1`: Logistic Regression  
- `model2`: Random Forest (`n_estimators = 100`)  
- `model3`: SVM (`C = 1`)

---

Feel free to explore, fork, or contribute!
