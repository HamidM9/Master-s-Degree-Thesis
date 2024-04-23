# Master-s-Degree-Thesis


This repository is made to share codes for a master's degree thesis in sub-network discovery at the University of Padua.\
Codes are commented on properly, and here are relevant explanations.\


The project started with three datasets, snvs.tsv, Compendium_Cancer_Gene.txt ,and samples_labels.txt. Here is a brief description of them:\
-snvs.tsv: It contains data on single nucleotide variants (SNVs), the most common genetic variation among people. These variants occur when a single nucleotide in the genome sequence is altered. A file with a .tsv extension indicates that it is a tab-separated values file, typically used to store table data. This dataset contains 3110 samples and 19424 different mutations.\
-Compendium_Cancer_Gene.txt:\ This dataset is a list of genes (568) potentially associated with various cancers.
-samples_labels.txt:\ The file  is structured in a tabular format where each row represents a sample associated with a specific type of cancer. In total, there are 3110 samples with 11 different cancer types (BRCA, KIRC, OV, HNSC, GBM, UCEC, LAML, COADREAD, LUAD, LUSC, BLCA).


By using these three files, a dataset is created named make_the_dataset.py:/ 
This dataset uses the samples as the indexes( first column in samples_labels.txt) and the genes in Compendium_Cancer_Gene.txt as features. Then, check each feature with the corresponding sample in snvs.tsv file, if existing, puts 1. If not, put zero. Finally, the last feature is the cancer type which is from matching the samples with samples_labels.txt/


After making the dataset in the previous step, it is now possible to make some predictions with classic ML methods. In the primary_classic_methods.py, there is a procedure as follows:/
-Cancer types are encoded into numeric values.
-"Logistic Regression", "Decision Tree", "SVM" with 'linear', 'poly', 'rbf', and sigmoid kernels with four different numbers of Cs(0.1,1,10,100), "Random Forest" with seven different numbers of estimators(1,10,40,50,100,150,200), and an ensemble method are implemented.





Updating...
