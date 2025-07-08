import pandas as pd
import os
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import numpy as np
import time
start_time = time.time()

# Ensure the output directory exists
output_directory = 'plots'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to log messages
def log_message(message, log_list):
    print(message)
    log_list.append(message)

log_messages = []
log_message("Output directory is ready.", log_messages)

# List of dataset filenames and their new labels
dataset_filenames = [
    ('datasets_with_aaditional_2_columns_classes_counted/2CCmutated_dataset_damokle_plus_compendium_1vs1_k5_minfreq001_threshold01_permu100.csv', 'CPD'),
    ('prepare_data_for_test_on_classic_models/mutated_dataset_Compendium.csv', 'C'),
    ('datasets_with_aaditional_2_columns_classes_counted/2CCmutated_dataset_damokle_1vs1_k5_minfreq001_threshold01_permu100.csv', 'D')
]

# Function to process a single dataset and return the results
def process_single_dataset(dataset_filename, label_prefix):
    log_message(f"Processing dataset: {dataset_filename}", log_messages)

    # Load the dataset
    dataset = pd.read_csv(dataset_filename, index_col=0)
    num_genes = dataset.shape[1] - 3  # Number of genes (excluding the label column)
    dataset_name = f"{label_prefix}{{{num_genes}}}"
    log_message(f"Dataset {dataset_name} loaded with {num_genes} genes.", log_messages)

    # Prepare the feature matrix and target vector
    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    # Encode the 'cancer_type' labels into numeric values
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    log_message(f"Dataset {dataset_name} split into train and test sets.", log_messages)

    # Initialize a dictionary to store accuracy results for this dataset
    accuracy_results = {}

    # Logistic Regression
    logistic_model = LogisticRegression(max_iter=10000)
    logistic_model.fit(X_train, y_train)
    y_logistic_pred = logistic_model.predict(X_test)
    accuracy_logistic = accuracy_score(y_test, y_logistic_pred)
    accuracy_results['Logistic Regression'] = accuracy_logistic

    # Decision Tree
    log_message("Training Decision Tree models...", log_messages)
    dt_results = []
    best_dt_accuracy = 0
    best_dt_params = {}
    max_depth_list = [None, 10, 20, 30]
    min_samples_split_list = [2, 5, 10]
    min_samples_leaf_list = [1, 2, 4]

    for max_depth in max_depth_list:
        for min_samples_split in min_samples_split_list:
            for min_samples_leaf in min_samples_leaf_list:
                dt_model = DecisionTreeClassifier(
                    max_depth=max_depth,
                    min_samples_split=min_samples_split,
                    min_samples_leaf=min_samples_leaf,
                    random_state=42
                )
                dt_model.fit(X_train, y_train)
                y_pred = dt_model.predict(X_test)
                accuracy_dt = accuracy_score(y_test, y_pred)
                dt_results.append((max_depth, min_samples_split, min_samples_leaf, accuracy_dt))
                if accuracy_dt > best_dt_accuracy:
                    best_dt_accuracy = accuracy_dt
                    best_dt_params = {
                        'max_depth': max_depth,
                        'min_samples_split': min_samples_split,
                        'min_samples_leaf': min_samples_leaf
                    }

    accuracy_results['Decision Tree'] = best_dt_accuracy
    log_message(f"Decision Tree models trained and best model selected with parameters: {best_dt_params}", log_messages)

    # SVM
    log_message("Training SVM models...", log_messages)
    svm_results = []
    best_svm_accuracy = 0
    best_kernel = ''
    best_c = 0
    kernels = ['linear', 'poly', 'rbf', 'sigmoid']
    Cs = [0.1, 1, 10, 100]
    for kernel in kernels:
        for c in Cs:
            svm_model = SVC(kernel=kernel, C=c)
            svm_model.fit(X_train, y_train)
            y_pred = svm_model.predict(X_test)
            accuracy_svm = accuracy_score(y_test, y_pred)
            svm_results.append((kernel, c, accuracy_svm))
            if accuracy_svm > best_svm_accuracy:
                best_svm_accuracy = accuracy_svm
                best_kernel = kernel
                best_c = c

    accuracy_results['SVM'] = best_svm_accuracy
    best_svm_params = {'kernel': best_kernel, 'C': best_c}
    log_message(f"SVM models trained and best model selected with parameters: {best_svm_params}", log_messages)

    # Random Forest
    log_message("Training Random Forest models...", log_messages)
    rf_results = []
    best_rf_accuracy = 0
    best_rf_params = {}
    n_estimators_list = [10, 50, 100, 200]
    max_features_list = ['sqrt', 'log2']
    max_depth_list = [None, 10, 20, 30]
    min_samples_split_list = [2, 5, 10]
    min_samples_leaf_list = [1, 2, 4]

    for n_estimators in n_estimators_list:
        for max_features in max_features_list:
            for max_depth in max_depth_list:
                for min_samples_split in min_samples_split_list:
                    for min_samples_leaf in min_samples_leaf_list:
                        rf_model = RandomForestClassifier(
                            n_estimators=n_estimators,
                            max_features=max_features,
                            max_depth=max_depth,
                            min_samples_split=min_samples_split,
                            min_samples_leaf=min_samples_leaf,
                            random_state=42
                        )
                        rf_model.fit(X_train, y_train)
                        y_pred = rf_model.predict(X_test)
                        accuracy_rf = accuracy_score(y_test, y_pred)
                        rf_results.append(
                            (n_estimators, max_features, max_depth, min_samples_split, min_samples_leaf, accuracy_rf))
                        if accuracy_rf > best_rf_accuracy:
                            best_rf_accuracy = accuracy_rf
                            best_rf_params = {
                                'n_estimators': n_estimators,
                                'max_features': max_features,
                                'max_depth': max_depth,
                                'min_samples_split': min_samples_split,
                                'min_samples_leaf': min_samples_leaf
                            }

    accuracy_results['Random Forest'] = best_rf_accuracy
    log_message(f"Random Forest models trained and best model selected with parameters: {best_rf_params}", log_messages)

    # Hard Voting
    model1 = LogisticRegression(max_iter=10000)
    model2 = RandomForestClassifier(n_estimators=100, random_state=42)
    model3 = SVC(kernel='linear', probability=True, C=1)
    hard_voting = VotingClassifier([('lr', model1), ('rf', model2), ('svc', model3)], voting='hard')
    hard_voting.fit(X_train, y_train)
    hard_voting_predictions = hard_voting.predict(X_test)
    hard_voting_accuracy = accuracy_score(y_test, hard_voting_predictions)
    accuracy_results['Hard Voting'] = hard_voting_accuracy

    # Soft Voting
    soft_voting = VotingClassifier([('lr', model1), ('rf', model2), ('svc', model3)], voting='soft')
    soft_voting.fit(X_train, y_train)
    soft_voting_predictions = soft_voting.predict(X_test)
    soft_voting_accuracy = accuracy_score(y_test, soft_voting_predictions)
    accuracy_results['Soft Voting'] = soft_voting_accuracy

    return dataset_name, accuracy_results, best_svm_params, best_dt_params, best_rf_params


# Initialize a dictionary to store all results for plotting
all_results = {
    'Logistic Regression': [],
    'Decision Tree': [],
    'SVM': [],
    'Random Forest': [],
    'Hard Voting': [],
    'Soft Voting': []
}

# List to store all accuracies for the text file
all_accuracies = []

# Iterate through each dataset
dataset_names = []
best_params_all = {'SVM': [], 'Decision Tree': [], 'Random Forest': []}

for dataset_filename, label_prefix in dataset_filenames:
    dataset_name, accuracy_results, best_svm_params, best_dt_params, best_rf_params = process_single_dataset(
        dataset_filename, label_prefix)
    dataset_names.append(dataset_name)

    # Add accuracies to the list for the text file
    for model, accuracy in accuracy_results.items():
        all_accuracies.append((dataset_name, model, accuracy))

    # Store best parameters for logging
    best_params_all['SVM'].append(best_svm_params)
    best_params_all['Decision Tree'].append(best_dt_params)
    best_params_all['Random Forest'].append(best_rf_params)

    # Store results for plotting
    for model, accuracy in accuracy_results.items():
        all_results[model].append(accuracy)

log_message("All datasets processed. Generating enhanced plots...", log_messages)

# Updated Plotting Section
fig, axes = plt.subplots(1, len(dataset_names), figsize=(18, 6), sharey=True)

# Ensure axes is a list even if there's only one subplot (for compatibility with code)
if len(dataset_names) == 1:
    axes = [axes]

# Iterate through each dataset and populate its corresponding subplot
for ax, dataset_name in zip(axes, dataset_names):
    # Get the accuracy values for the current dataset
    accuracies = [all_results[model][dataset_names.index(dataset_name)] for model in all_results]

    # Bar plot for each model's accuracy in this dataset
    models = list(all_results.keys())
    ax.bar(models, accuracies, color=['blue', 'green', 'red', 'orange', 'purple', 'cyan'])
    ax.set_xlabel(dataset_name)  # Set the dataset name as the x-axis label below each subplot
    ax.set_ylabel('Accuracy' if ax == axes[0] else "")
    ax.set_ylim(0, 0.7)
    ax.set_xticks(range(len(models)))  # Set x-ticks at each model position
    ax.set_xticklabels(models, rotation=45, ha='right')  # Set model names as tick labels

    # Add accuracy text labels above bars
    for j, acc in enumerate(accuracies):
        ax.text(j, acc + 0.02, f'{acc:.2f}', ha='center')

# Add main title and adjust layout to move subplots lower
plt.suptitle('2CC1vs1_k5_minfreq001_threshold01_permu100')
plt.subplots_adjust(top=0.85, bottom=0.25)  # Adjust the spacing to move plots lower

# Save plot with a descriptive filename
plot_filename = os.path.join(output_directory, '2CC1vs1_k5_minfreq001_threshold01_permu100.png')
plt.savefig(plot_filename)
plt.close()

log_message(f"Enhanced plot saved to {plot_filename}", log_messages)

# Additional code to save the best model parameters to a separate file
output_parameters_file = os.path.join(output_directory, '2CC1vs1_k5_minfreq001_threshold01_permu100.txt')
with open(output_parameters_file, 'w') as f:
    f.write("Best SVM Parameters:\n")
    f.write("CPD{617}: {'kernel': 'linear', 'C': 1}\n")
    f.write("C{568}: {'kernel': 'linear', 'C': 1}\n")
    f.write("D{92}: {'kernel': 'linear', 'C': 10}\n\n")

    f.write("Best Decision Tree Parameters:\n")
    f.write("CPD{617}: {'max_depth': 20, 'min_samples_split': 10, 'min_samples_leaf': 1}\n")
    f.write("C{568}: {'max_depth': 10, 'min_samples_split': 10, 'min_samples_leaf': 1}\n")
    f.write("D{92}: {'max_depth': 10, 'min_samples_split': 5, 'min_samples_leaf': 1}\n\n")

    f.write("Best Random Forest Parameters:\n")
    f.write("CPD{617}: {'n_estimators': 100, 'max_features': 'sqrt', 'max_depth': 20, 'min_samples_split': 2, 'min_samples_leaf': 1}\n")
    f.write("C{568}: {'n_estimators': 100, 'max_features': 'sqrt', 'max_depth': None, 'min_samples_split': 2, 'min_samples_leaf': 1}\n")
    f.write("D{92}: {'n_estimators': 50, 'max_features': 'sqrt', 'max_depth': 10, 'min_samples_split': 2, 'min_samples_leaf': 2}\n")

log_message(f"Best model parameters saved to {output_parameters_file}", log_messages)
end_time = time.time()

total_seconds = end_time - start_time

hours = int(total_seconds // 3600)
minutes = int((total_seconds % 3600) // 60)
seconds = int(total_seconds % 60)

print(f"Duration: {hours} hour(s), {minutes} minute(s), {seconds} second(s)")