# Decision Tree with Pruning and Comprehensive Evaluation Suite

### Introduction
This script is designed to build, evaluate, and prune decision trees for classification tasks.
It includes functionality to compute various performance metrics, such as accuracy, precision, recall, and F1 score, as well as to visualize decision trees and confusion matrices.

### Prerequisites and Dependencies
To run this script, you need to have Python installed on your system along with the following libraries:
    - `numpy`: For numerical computations.
    - `matplotlib`: For plotting decision trees and confusion matrices.
You can install these dependencies using pip

### Usage Instructions:

To use the script with your datasets, follow these steps:
- Prepare your dataset: Ensure your dataset files are formatted correctly, as described in the Dataset Format section. Place them in a directory named `wifi_db`.
- Run the script: Execute the script in a Python environment with the required libraries installed. You can use the command:

`python source_code.py`

IMPORTANT IF YOU RUN WITH OWN DATASETS 
- Clean Dataset and Noisy defined at top of the `.py` file
- Adjust this path for your own datasets if you wish

To evaluate your dataset WITHOUT pruning:
- run the `tenfold(dataset)` function with the name of your dataset defined at the top of the file
- this function returns the average confusion matrix and the average accuracy over 10-fold cross validation

To evaluate your dataset WITH pruning:
- run the: `prune(dataset)` function with the name of your dataset defined at the top of the file
- ths function returns the average confusion matrix and the average accuracy over a nested 10-fold cross validation

To visualise your tree WITHOUT pruning:
- run `plot_tree(dataset)` function

To display your results visually (tables and confusion matrix):
- if you wish to display ALL PRE-PRUNING RESULTS: metrics, and confusion matrix for a given dataset, run `display_metrics_for_dataset(dataset)` function
- if you wish to display ALL POST-PRUNING RESULTS: statistical table, metrics, and confusion matrix for a given dataset, run `display_results_for_prune_data(dataset)` function
- if you wish to display:
  - only confusion matrix: run `display_confusion_matrix(confusion_matrix)` if you have the confusion matrix already, or `display_dataset_confusion_matrix(dataset)`
  - only metrics table: run `display_metrics_table` if you have the metrics already (from the tenfold)
  - only stats table (PRUNING ONLY): run `display_info_table` with the shown arguments

Examples are given in comments in the file. Note that displaying all results for BOTH are active when you run. 

Extra Function Information:
- The function decision_tree_learning creates a decision tree and takes in a dataset and a integer that is used for the depth
- The function evaluate_accuracy evaluates the accuaracy of the a given tree given a tree as the first parameter, and the dataset as the second parameter.
- The function plot_tree plots the tree. It takes in a dataset to train the tree on, and then plots that corresonding tree.
- The function display_dataset_confusion_matrix takes in a dataset, trains a tree on that dataset, and then returns a confusion matrix for that tree.
- The function display_metrics_for_dataset takes in a dataset and then returns the corresponding confusion matrix, the accuracy, the recall and precision, and the F1 measures using ten-fold on that dataset to create trees and test them.
- The function prune(dataset), takes in a dataset and then prunes on that tree using inner 10 fold cross validation.
