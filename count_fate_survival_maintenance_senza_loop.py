import os
import pandas as pd
import ast

# Define the input file path and output folder
input_file_path = 'output_for_fate_survival_maintenance/mutated_dataset_solo_compendium_3Cfate.csv'  # Replace with the actual file path
output_folder = 'output_for_fate_survival_maintenance'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load gene classifications from the genes_with_fate_survival_maintenance_dictionary.txt file
gene_classifications = {}
with open('genes_with_fate_survival_maintenance_dictionary.txt', 'r') as file:
    for line in file:
        gene_dict = ast.literal_eval(line.strip())
        gene_classifications.update(gene_dict)

# Load the dataset
dataset = pd.read_csv(input_file_path)

# Identify the gene columns and classification columns in the dataset
gene_columns = dataset.columns[1:-6]  # Assume genes are in columns [1:-6]
classification_columns = {
    'fate': dataset.columns[-6],
    'cell_survival': dataset.columns[-5],
    'genome_maintenance': dataset.columns[-4],
}

# Iterate through each sample in the dataset
for sample_index, row in dataset.iterrows():
    # Initialize counters for this sample
    classification_counts = {'fate': 0, 'cell_survival': 0, 'genome_maintenance': 0}

    # Check each gene in the gene columns
    for gene in gene_columns:
        if row[gene] == 1:  # If the gene value is 1 for this sample
            if gene in gene_classifications:
                print(f"Gene found: {gene}")  # Print the gene name

                classifications = gene_classifications[gene]

                # Increment counts for each classification found
                for classification in classifications:
                    if classification in classification_counts:
                        classification_counts[classification] += 1

    # Update the sample's classification columns in the dataset
    for classification, count in classification_counts.items():
        dataset.at[sample_index, classification_columns[classification]] = count

# Define the output file path
output_file_name = f"{os.path.splitext(os.path.basename(input_file_path))[0]}_3CCfate.csv"
output_file_path = os.path.join(output_folder, output_file_name)

# Save the modified dataset
dataset.to_csv(output_file_path, index=False)

print(f"Updated dataset saved to {output_file_path}")
