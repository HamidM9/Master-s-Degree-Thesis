import pandas as pd

# appending each row of <Compendium_Cancer_Genes> to <cancer_gene_list>
file_path = 'Compendium_Cancer_Genes.txt'

cancer_gene_list = []

with open(file_path, 'r') as file:
    for line in file:
        cleaned_line = line.strip()
        cancer_gene_list.append(cleaned_line)

file_path = 'samples_labels.txt'

rows_list = []
with open(file_path, 'r') as file:
    for line in file:
        elements = line.strip().split(' ')
        rows_list.append(elements)

file_path = 'snvs.tsv'

case_dict = {}

with open(file_path, 'r') as file:
    for line in file:
        parts = line.strip().split('\t')  # Split by tabs
        if len(parts) >= 2:
            # The first part is the id (key)
            id_key = parts[0].strip()
            values = []
            for value in parts[1:]:
                if value.strip() != '':
                    values.append(value.strip())
            case_dict[id_key] = values

cases = list(case_dict.keys())

dataset = pd.DataFrame(0, columns=cancer_gene_list, index=cases)

for case in cases:
    gene_list = case_dict.get(case, [])

    if case in dataset.index:
        for gene_name in gene_list:
            if gene_name in dataset.columns:
                dataset.loc[case, gene_name] = 1

dataset['cancer_type'] = 'xxx'

# Iterate through rows_list to update the 'cancer_type' column
for row in rows_list:
    case_name = row[0]
    cancer_type = row[1]

    # Check if the case_name exists in the dataset
    if case_name in dataset.index:
        dataset.at[case_name, 'cancer_type'] = cancer_type

mutated_dataset_filename = 'mutated_dataset.csv'
dataset.to_csv(mutated_dataset_filename)

print("Done")
