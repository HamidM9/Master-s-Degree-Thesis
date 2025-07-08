import os

# Define the directory containing the .txt files
directory = 'damokle_output_1vs1_k5_minfreq001_threshold01_permu100'  # Replace with the actual path to your files
output_file = 'networks_1vs1_k5_minfreq001_threshold01_permu100.txt'

# Open the output file for writing
with open(output_file, 'w') as out_file:
    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        # Process only .txt files
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as f:
                # Read the fourth line of the file
                lines = f.readlines()
                if len(lines) >= 4:
                    # Extract the fourth line and get the list part
                    list_line = lines[3].strip()  # Fourth line (index 3)
                    list_part = list_line.split(': ')[-1]  # Extracts the part after "Best solution: "

                    # Extract filename without extension and create the new format
                    fname = filename.split('.')[0]
                    parts = fname.split('_')
                    formatted_name = f"{parts[0].replace('is', '')}_{parts[1].replace('is', '')}"

                    # Write the filename in modified format and extracted list to the output file
                    out_file.write(f"{formatted_name}: {list_part}\n")
