import os
import glob
import ast

# Path to the directory containing the text files
directory_path = 'damokle_output_1vs1_k6_minfreq001_threshold01_permu100'
directory_path_output = '/Users/hamidkhan/PycharmProjects/lastModification/'

# Glob pattern to match all text files
file_pattern = os.path.join(directory_path, '*.txt')

# Set to hold all unique genes
unique_genes = set()

# Read each text file in the directory
for file_path in glob.glob(file_pattern):
    try:
        with open(file_path, 'r') as file:
            # Skip the first four lines and read the fifth
            for _ in range(3):
                next(file)
            fourth_line = next(file).strip()  # Read the fifth line
            print(fourth_line)

            # Extract gene names from the fifth line
            # Assuming the line format is: "Best Solution: ['gene1', 'gene2', ...]"
            start_idx = fourth_line.find('[')
            end_idx = fourth_line.find(']')
            if start_idx != -1 and end_idx != -1:
                # Safely evaluate the list of gene names
                gene_list = ast.literal_eval(fourth_line[start_idx:end_idx + 1])
                unique_genes.update(gene_list)  # Add genes to the set of unique genes
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except StopIteration:
        print(f"Not enough lines in file: {file_path}")
    except SyntaxError:
        print(f"Error parsing genes in file: {file_path}")

# Save the unique genes to a new text file
output_file_path = os.path.join(directory_path_output, 'unique_damokle_output_damokle_output_1vs1_k6_minfreq001_threshold01_permu100.txt')
with open(output_file_path, 'w') as output_file:
    for gene in sorted(unique_genes):
        output_file.write(gene + '\n')  # Write each gene on a new line

print(f"Unique genes have been saved to {output_file_path}.")
