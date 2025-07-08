import os
from scipy.stats import wilcoxon


# Function to read values from a text file
def read_values_from_file(file_path):
    with open(file_path, 'r') as file:
        return [float(line.strip()) for line in file.readlines()]


# Function to perform a one-sided Wilcoxon signed-rank test
def perform_wilcoxon_test(before_path, after_path, alternative):
    before = read_values_from_file(before_path)
    after = read_values_from_file(after_path)

    stat, p_value = wilcoxon(before, after, alternative=alternative)

    output_folder = "wilcoxon_results_one_sided/senza_counts"
    os.makedirs(output_folder, exist_ok=True)

    folder_name = os.path.basename(os.path.dirname(after_path))
    file_name = os.path.basename(after_path)
    output_file_name = f"{folder_name}-{file_name}"
    output_file_path = os.path.join(output_folder, output_file_name)

    with open(output_file_path, 'w') as file:
        file.write("Wilcoxon Signed-Rank Test\n")
        file.write("=" * 35 + "\n")
        file.write(f"Before file: {before_path}\n")
        file.write(f"After file: {after_path}\n")
        file.write(f"Before values: {before}\n")
        file.write(f"After values: {after}\n")
        file.write(f"Wilcoxon signed-rank test statistic: {stat}\n")
        file.write(f"P-value: {p_value},\n")

    print(f"Wilcoxon test results saved to: {output_file_path}")
