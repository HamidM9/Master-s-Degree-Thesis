import os
import random

# Define base directories
base_directory = "data/splits"
network_file = "network_file.txt"
muts_black_list_file = "muts_black_list_file.txt"
min_freq = 0.01
threshold = 0.1
max_size = 6
num_permutations = 100

def get_sample2muts(mut_matrix_file):
    sample2muts = {}
    with open(mut_matrix_file, 'r') as file:
        for line in file:
            v = line.strip().split()
            if len(v) < 2:
                continue  # Skip empty or invalid lines
            sampleID = v[0]
            if sampleID in sample2muts:
                print(f"Duplicated sample: {sampleID}")
            sample2muts[sampleID] = set(v[1:])
    return sample2muts

def get_sample2class(class_file):
    sample2class = {}
    with open(class_file, 'r') as file:
        next(file)  # Skip header
        for line in file:
            v = line.strip().split()
            if len(v) < 2:
                continue
            sampleID, class_sample = v[0], v[1]
            if sampleID in sample2class:
                print(f"Duplicated sample: {sampleID}")
            sample2class[sampleID] = class_sample
    return sample2class

def get_muts2sample(sample2muts, sample2class):
    muts2sample = {}
    total_samples_class0 = total_samples_class1 = 0
    for sample in samples_with_muts_AND_class:
        muts = sample2muts[sample]
        for mut in muts:
            muts2sample.setdefault(mut, []).append(sample)
        if sample2class[sample] == "0":
            total_samples_class0 += 1
        elif sample2class[sample] == "1":
            total_samples_class1 += 1
    return muts2sample, total_samples_class0, total_samples_class1

def get_adj_matrix_network(network_file):
    mut2neighbors = {}
    with open(network_file, 'r') as file:
        for line in file:
            v = line.strip().split()
            if len(v) < 2:
                continue
            mut1, mut2 = v[0].upper(), v[1].upper()
            mut2neighbors.setdefault(mut1, []).append(mut2)
            mut2neighbors.setdefault(mut2, []).append(mut1)
    return mut2neighbors

def compute_weight(mut2samples, sample2class, list1, list2, tot_class0, tot_class1):
    all_muts = sorted(set(list1).union(set(list2)))
    count_class0 = sum(1 for s in {s for m in all_muts for s in mut2samples.get(m, [])} if sample2class[s] == "0")
    count_class1 = sum(1 for s in {s for m in all_muts for s in mut2samples.get(m, [])} if sample2class[s] == "1")
    return abs(count_class0 / tot_class0 - count_class1 / tot_class1)

def get_mut_white_list(mut2samples, muts_black_list_file):
    with open(muts_black_list_file, 'r') as file:
        mut_black_list = set(line.strip() for line in file)
    return {mut for mut, samples in mut2samples.items()
            if sum(1 for s in samples if sample2class[s] == "0") > min_freq
            or sum(1 for s in samples if sample2class[s] == "1") > min_freq} - mut_black_list

def get_edges_above_threshold(mut2samples, sample2class, tot_class0, tot_class1, mut2neighbors, mut_white_list):
    edges = []
    for mut in mut_white_list:
        if mut in mut2neighbors:
            for neigh_mut in mut2neighbors[mut]:
                if neigh_mut > mut and neigh_mut in mut_white_list:
                    edge_weight = compute_weight(mut2samples, sample2class, [mut], [neigh_mut], tot_class0, tot_class1)
                    if edge_weight >= threshold:
                        edges.append([mut, neigh_mut])
    return edges

def extend_solution(mut2samples, sample2class, tot_class0, tot_class1, mut2neighbors, mut_white_list, curr_sol):
    neighbors = {neigh for mut in curr_sol for neigh in mut2neighbors.get(mut, [])} - set(curr_sol)
    best_weight, best_neighbor = compute_weight(mut2samples, sample2class, curr_sol, [], tot_class0, tot_class1), None
    for neighbor in neighbors:
        if neighbor in mut_white_list:
            new_weight = compute_weight(mut2samples, sample2class, curr_sol, [neighbor], tot_class0, tot_class1)
            if new_weight > best_weight:
                best_weight, best_neighbor = new_weight, neighbor
    return (curr_sol + [best_neighbor], best_weight) if best_neighbor else (curr_sol, best_weight)

def best_solution_from_edge(mut2samples, sample2class, tot_class0, tot_class1, mut2neighbors, mut_white_list, edge):
    curr_sol, curr_val = edge, 0.0
    while len(curr_sol) < max_size:
        new_sol, new_val = extend_solution(mut2samples, sample2class, tot_class0, tot_class1, mut2neighbors, mut_white_list, curr_sol)
        if len(new_sol) == len(curr_sol):
            break
        curr_sol, curr_val = new_sol, new_val
    return curr_sol, curr_val

# Iterate through each split folder
for i in range(1, 11):
    split_folder = os.path.join(base_directory, f'split_{i}')
    mut_matrix_file = os.path.join(split_folder, 'snvs_train.tsv')
    class_folder = os.path.join(split_folder, 'classes')
    output_folder = os.path.join(split_folder, 'damokle_output')
    print(f"Split{i}")
    os.makedirs(output_folder, exist_ok=True)

    sample2muts = get_sample2muts(mut_matrix_file)

    for class_filename in os.listdir(class_folder):
        if not class_filename.endswith(".txt"):
            continue
        class_file = os.path.join(class_folder, class_filename)
        output_file = os.path.join(output_folder, f"{class_filename}_output.txt")
        print(f"class{class_filename}")
        sample2class = get_sample2class(class_file)
        samples_with_muts_AND_class = set(sample2muts.keys()).intersection(set(sample2class.keys()))

        mut2samples, total_samples_class0, total_samples_class1 = get_muts2sample(sample2muts, sample2class)
        mut2neighbors = get_adj_matrix_network(network_file)
        mut_white_list = get_mut_white_list(mut2samples, muts_black_list_file)
        edges = get_edges_above_threshold(mut2samples, sample2class, total_samples_class0, total_samples_class1, mut2neighbors, mut_white_list)

        best_sol, best_val = [], 0.0
        for edge in edges:
            sol, val = best_solution_from_edge(mut2samples, sample2class, total_samples_class0, total_samples_class1, mut2neighbors, mut_white_list, edge)
            if val > best_val:
                best_sol, best_val = sol, val

        with open(output_file, 'w') as outfile:
            outfile.write(f"Number of samples with both mutations and class: {len(samples_with_muts_AND_class)}\n")
            outfile.write(f"Number of samples in class 0: {total_samples_class0}\n")
            outfile.write(f"Number of samples in class 1: {total_samples_class1}\n")
            outfile.write(f"Best solution: {best_sol}\n")
            outfile.write(f"Best weight: {best_val}\n")

print("Processing completed for all splits and files saved in their respective 'damokle_output' folders.")
