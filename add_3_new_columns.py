import pandas as pd

# Load the dataset
dataset = pd.read_csv('prepare_data_for_test_on_classic_models/mutated_dataset_compendium.csv')

# Remove any existing 'oncogene', 'TSG', and 'fusion' columns to avoid duplication
dataset = dataset.drop(columns=['oncogene', 'TSG', 'fusion'], errors='ignore')

# Add the columns with default values of 0
dataset['oncogene'] = 0
dataset['TSG'] = 0
dataset['fusion'] = 0

# Define the exact column order
cols = list(dataset.columns[:-6]) + ['oncogene', 'TSG', 'fusion', 'mutated_count', 'genes_count', 'cancer_type']

# Reorder the dataset columns based on the specified order
dataset = dataset[cols]

# Save the modified dataset
output_path = '10splits_k6_minfreq0p01threshold0p1permutation100/mutated_dataset_solo_compendium3C.csv'
dataset.to_csv(output_path, index=False)
print(f"Updated dataset saved to {output_path}")
