import pandas as pd
import ast

# Load the dataset
dataset = pd.read_csv('10splits_k6_minfreq0p01threshold0p1permutation100/mutated_dataset_solo_compendium3C.csv')

# Load gene classifications from the filtered_gene_classifications.txt file
gene_classifications = {}
with open('filtered_gene_classifications.txt', 'r') as file:
    for line in file:
        gene_dict = ast.literal_eval(line.strip())
        gene_classifications.update(gene_dict)

# Identify the gene columns and classification columns in the dataset
gene_columns = dataset.columns[1:-6]  # Assume genes are in columns [1:-6]
classification_columns = {'oncogene': dataset.columns[-6], 'TSG': dataset.columns[-5], 'fusion': dataset.columns[-4]}

# Iterate through each sample in the dataset
for sample_index, row in dataset.iterrows():
    # Initialize counters for this sample
    classification_counts = {'oncogene': 0, 'TSG': 0, 'fusion': 0}

    # Check each gene in the gene columns
    for gene in gene_columns:
        if row[gene] == 1:  # If the gene value is 1 for this sample
            if gene in gene_classifications:
                classifications = gene_classifications[gene]

                # Increment counts for each classification found
                for classification in classifications:
                    if classification in classification_counts:
                        classification_counts[classification] += 1

    # Update the sample's classification columns in the dataset
    for classification, count in classification_counts.items():
        dataset.at[sample_index, classification_columns[classification]] = count

# Save the modified dataset
output_path = '10splits_k6_minfreq0p01threshold0p1permutation100/mutated_dataset_solo_compendium3CC.csv'
dataset.to_csv(output_path, index=False)
print(f"Updated dataset saved to {output_path}")
