# -*- coding: utf-8 -*-
"""source_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SXTaM6L4zyBzO4DUddqzm2yaYzRtQAUQ
"""

import numpy as np
import matplotlib.pyplot as plt

clean_dataset = np.loadtxt("wifi_db/clean_dataset.txt")
noisy_dataset = np.loadtxt("wifi_db/noisy_dataset.txt")

# each node in the decision tree will be modelled as an object using OOP
# each instantiated node will either be a decision node, or a leaf node.
# each decision node will store:
#   1. the feature to split on,
#   2. a value
#   3. the depth of the node in the tree
#   4. the left child
#   5. the right child
#   6. A class label, if leaf node only
class Node:
    def __init__(self, feature, split_val, depth, left = None, right = None, label = None):
        self.feature = feature
        self.split_val = split_val
        self.left = left
        self.right = right
        self.depth = depth
        self.label = label



# calculates the entropy of two datasets
# inputs:
#    - left: hashmap from label -> its count in the left split
#    - dataset_map: hashmap from label -> its count in the current_split
#    - count_left: number of elements in the left dataset
#    - total_count: number of elements in the entire dataset for the current split
# returns entropy
def computeEntropy(left, dataset_map, count_left, total_count):

    # hleft will store entropy of left split
    hleft = 0

    # calculate entropy of left split
    for datapoint in left:
        p = (left[datapoint] / count_left)
        hleft -= p * np.log2(p)

    # hright will store entropy of right split
    hright = 0
    count_right = total_count - count_left

    # calculate entropy of left split
    for datapoint in dataset_map:
        right_class_count = dataset_map[datapoint] - left.get(datapoint, 0)
        p = (right_class_count / count_right ) if right_class_count  != 0 else 0
        hright -= p * np.log2(p) if p!=0 else 0

    # return the total entropy
    w = (count_left / total_count)
    return w * hleft + (1 - w) * hright


# recursive decsion tree learning algorithm using information gain
# inputs:
#    - dataset: initially the main dataset, then recurses through subsets
#    - depth: current depth of the tree
# returns a decision tree classifier
def decision_tree_learning(dataset, depth):

    # map from label -> its count in the current_split
    dataset_map = {}

    # total number of elements in the dataset
    total_count = len(dataset)

    # get the class labels from the dataset
    for i in dataset:
        dataset_map[int(i[-1])] = dataset_map.get(int(i[-1]), 0) + 1

    # if there is only one item in the decision tree, then create a leaf/label node
    if len(dataset_map) == 1:
        return Node(None, None,  depth = depth, label = next(iter(dataset_map)))


    # entropy the minimum split gives us
    minEntropy = float("inf")

    # splitting feature
    minEntropy_feature = 0

    # split value
    minEntropySplit = 0

    # index that allows us to split the dataset
    minEntropyidx = 0

    # loop over each feature, and then find a value to to split on that gives us the minimum entropy
    for feature in range(7):

        # sort the dataset with respect to the current feature
        dataset = dataset[np.apply_along_axis(lambda x: x[feature], 1, dataset).argsort()]
        left = {}
        idx = 0
        val = dataset[idx][feature]

        # loop over splits, find the one with the minimum entropy
        # loop over dataset
        while idx < len(dataset):

            # frequency count for left split
            while idx < len(dataset) and dataset[idx][feature] == val:
                left[dataset[idx][-1]] = left.get(dataset[idx][-1], 0) + 1
                idx += 1

            # get entropy of our left split
            entropy = computeEntropy(left, dataset_map, idx, total_count)

            # if entropy of split is less than the current minimum entropy, use this new split instead
            if  entropy < minEntropy:
                minEntropy = entropy
                minEntropy_feature = feature
                minEntropySplit = val
                minEntropyidx = idx
            if idx < len(dataset):
                val = dataset[idx][feature]


    # sort the dataset with respect to the feature that minimises the entropy
    dataset = dataset[np.apply_along_axis(lambda x: x[minEntropy_feature], 1, dataset).argsort()]

    # create a left and right node, based on splitting feature.
    ret = Node(minEntropy_feature, minEntropySplit, depth = depth, left = None, right = None, label=None)

    # recurse through child subsets (left and right) created to continue learning
    leftTree = decision_tree_learning(dataset[:minEntropyidx], depth + 1)
    rightTree = decision_tree_learning(dataset[minEntropyidx:], depth + 1)
    ret.left = leftTree
    ret.right = rightTree

    # return node (holds all subtree data)
    return ret





# use our decision tree, classify a datapoint
# input:
#   - datapoint: sample to classify
#   - tree: our model used to classify the datapoint
# returns predicted label of the datapoint
def compute_class(datapoint, tree):

    # if its a label, return the value of the label, otherwise, we recurse
    if tree.label != None:
        return tree.label
    else:
        if datapoint[tree.feature] <= tree.split_val:
            return compute_class(datapoint, tree.left)
        else:
            return compute_class(datapoint, tree.right)





# helper function to print the decision tree
def printTree(trained_tree):
        if trained_tree.label == None:
                print(" " * trained_tree.depth + "Node with depth " + str(trained_tree.depth) + ".")
                print(" " * trained_tree.depth + "This node splits on feature " + str(trained_tree.feature) + " on the input data.")
                print(" " * trained_tree.depth + "Values less than or equal to " + str(trained_tree.split_val) + " are transferred to the left dataset, the rest to the right dataset.")
                printTree(trained_tree.left)
                printTree(trained_tree.right)
        else:
                print(" " * trained_tree.depth + "We are now at a label node. We classify all datapoints that reach this point in the tree as label " + str(trained_tree.label))





# helper function to evaluate the accuracy of a given decision tree on a given dataset
# returns the accuracy
def evaluate_accuracy(tree, dataset):
    accuracy = 0
    for datapoint in dataset:
        accuracy += int(compute_class(datapoint, tree) == datapoint[-1])
    return accuracy / len(dataset)

# clean_tree = decision_tree_learning(clean_dataset, 0)
# noisy_tree = decision_tree_learning(noisy_dataset, 0)

# printTree(noisy_tree)

# helper function to visualise decision tree in portrait, top down
def plot_tree_top_down(node, depth=0, position=0, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(200, 100))

    # if current node is an internal node, plot split node, recurse children
    if node.label is None:

        # plot blue split node
        ax.scatter(position, -depth, s=5000, c='blue', edgecolors='black', zorder=2)
        ax.text(position, -depth, f"F{node.feature}\n<={node.split_val}", va='center', ha='center', color='white', fontsize=7, zorder=3)

        # recurse for left and right children
        left_position = position - 1/(2**(depth+2))
        right_position = position + 1/(2**(depth+2))

        # connect children
        ax.plot([position, left_position], [-depth, -depth-1], 'k-', zorder=1)
        ax.plot([position, right_position], [-depth, -depth-1], 'k-', zorder=1)

        plot_tree_top_down(node.left, depth+1, left_position, ax)
        plot_tree_top_down(node.right, depth+1, right_position, ax)

    # if leaf (label) node, plot this in green
    else:
        # add green class/label leaf node
        ax.scatter(position, -depth, s=5000, c='green', edgecolors='black', zorder=2)
        ax.text(position, -depth, f"Label {node.label}", va='center', ha='center', color='black', fontsize=7, zorder=3)

    ax.axis('off')
    return ax

# Plotting the sample tree top-down
# plot_tree_top_down(clean_tree)
# plt.show()

# # sanity checks
# print(evaluate_accuracy(clean_tree, clean_dataset))
# print(evaluate_accuracy(noisy_tree, noisy_dataset))

# compute the confusion matrix of a given decision tree on a given dataset
# input:
#   - dataset
#   - decision tree
# returns confusion matrix
def calculate_confusion_matrix(dataset, trained_tree):

    # initialise matrix
    confusion_matrix = [[0, 0, 0, 0] for i in range(4)]

    # calculate each value for the matrix
    for datapoint in dataset:
        prediction = compute_class(datapoint, trained_tree)
        confusion_matrix[int(datapoint[-1]) - 1][prediction - 1] += 1
    return np.array(confusion_matrix)

# get the confusion matrix of the full clean dataset
# confusion_matrix = calculate_confusion_matrix(clean_dataset, clean_tree)

# helper function to take a confusion matrix as a 2-d array and display it nicely
def displayCF(confusion_matrix):

    # print the input matrix
    print(confusion_matrix)
    plt.imshow(confusion_matrix, cmap='Blues')

    # title, axes and colour bar on the side
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.colorbar()

    # labels
    plt.xticks(np.arange(4), [1, 2, 3, 4])
    plt.yticks(np.arange(4), [1, 2, 3, 4])
    threshold = 0.7 * np.max(confusion_matrix)

    # styling
    for i in range(4):
        for j in range(4):
            color = 'white' if confusion_matrix[i, j] > threshold else 'black'
            formatted_value = f"{confusion_matrix[i, j]:.1f}"
            plt.text(j, i, formatted_value, ha='center', va='center', color=color)
    plt.show()

# displayCF(confusion_matrix)

# computes all metrics that are needed for the report
# inputs:
#   - test_db: dataset
#   - trained_tree: decision tree to test
# returns accuracy, precision, recall, f1
def compute_metrics(test_db, trained_tree):
    confusion_matrix = calculate_confusion_matrix(test_db, trained_tree)
    true_values = sum(confusion_matrix[i][i] for i in range(4))
    accuracy = true_values / confusion_matrix.sum()
    precisions = np.array([confusion_matrix[i][i] for i in range(4)]) / confusion_matrix.sum(axis = 0)
    recalls = np.array([confusion_matrix[i][i] for i in range(4)]) / confusion_matrix.sum(axis = 1)
    f1_mesaures = 2 * precisions * recalls / (precisions + recalls)
    return [accuracy, precisions, recalls, f1_mesaures]





# also computes all metrics that are needed for the report
# different to above function - this one takes a cf matrix rather than computing one
# inputs:
#   - confusion_matrix: confusion matrix of decision tree to evaluate
# returns accuracy, precision, recall, f1
def compute_metrics_cf(confusion_matrix):
    true_values = sum(confusion_matrix[i][i] for i in range(4))
    accuracy = true_values / confusion_matrix.sum()
    precisions = np.array([confusion_matrix[i][i] for i in range(4)]) / confusion_matrix.sum(axis = 0)
    recalls = np.array([confusion_matrix[i][i] for i in range(4)]) / confusion_matrix.sum(axis = 1)
    f1_mesaures = 2 * precisions * recalls / (precisions + recalls)
    return [accuracy, precisions, recalls, f1_mesaures]




# tabulate the metrics for an evaluated decision tree for the report
# inputs:
#   - accuracy
#   - precisions: precision value for each class
#   - recalls: recall value for each class
#   - f1_measures: f1 measure for each class
# returns nothing but displays table when called
def display_metrics_table(name, accuracy, precisions, recalls, f1_measures):
    print("Accuracy: ", accuracy)
    print("Precisions: ", precisions)
    print("Recalls: ", recalls)
    print("F1 Measures: ", f1_measures)
    accuracy = round(accuracy, 3)
    precisions = [round(p, 3) for p in precisions]
    recalls = [round(r, 3) for r in recalls]
    f1_measures = [round(f, 3) for f in f1_measures]
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    table = ax.table(cellText=[["Accuracy", accuracy],
                               ["Precision 1", precisions[0]],
                               ["Precision 2", precisions[1]],
                               ["Precision 3", precisions[2]],
                               ["Precision 4", precisions[3]],
                               ["Recall 1", recalls[0]],
                               ["Recall 2", recalls[1]],
                               ["Recall 3", recalls[2]],
                               ["Recall 4", recalls[3]],
                               ["F1 Measure 1", f1_measures[0]],
                               ["F1 Measure 2", f1_measures[1]],
                               ["F1 Measure 3", f1_measures[2]],
                               ["F1 Measure 4", f1_measures[3]]],
                colLabels=["Metric", "Value"],
                cellLoc='center',
                loc='center')

    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_text_props(fontweight='bold')
            cell.set_facecolor('#FF8000')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    plt.title(name)
    plt.show()

# performs 10-fold cross validation for our decision tree learning algorithm
# input:
#   - dataset
# returns the averaged confusion matrix and average accuracy
def tenfold(dataset):

    # shuffle the dataset e.g. because noisy dataset is sorted by class value
    np.random.shuffle(dataset)

    # store accuracy and cf for each folds tree
    accuracies = []
    confusion_matrices = []

    # for each of the 10 folds, create a model and test it
    for i in range(10):

        # split the data into train and test folds
        train = np.append(dataset[:i * 200], dataset[(i+1) * 200:], axis=0)

        # train tree based on training folds
        trained_tree = decision_tree_learning(train, 0)

        # test the tree on test fold
        test_db = dataset[i * 200: (i+1) * 200]
        correct =  0
        for test_point in test_db:
            if compute_class(test_point, trained_tree) == test_point[-1]:
                correct += 1
        accuracies.append(correct / 200)

        cf = calculate_confusion_matrix(test_db, trained_tree)
        confusion_matrices.append(cf)

    # get the average confusion matrix by element-wise operations
    summed_matrix = np.zeros((4, 4))
    for matrix in confusion_matrices:
        summed_matrix += matrix
    average_cf = summed_matrix / len(confusion_matrices)

    average_accruacy = np.mean(accuracies)

    return average_cf, average_accruacy



# helper function to take the accuracy only from 10-fold
def evaluate(test_db, trained_tree):
    _, accuracy = tenfold(test_db)
    return accuracy


# displaying results using above methods for both the clean data and noisy data
# clean_cf, _ = tenfold(clean_dataset)
# displayCF(clean_cf)
# accuracy, precisions, recalls, f1_measures = compute_metrics_cf(clean_cf)
# display_metrics_table("Clean Tenfold", accuracy, precisions, recalls, f1_measures)


# noisy_cf, _ = tenfold(noisy_dataset)
# displayCF(noisy_cf)
# accuracy, precisions, recalls, f1_measures = compute_metrics_cf(noisy_cf)
# display_metrics_table("Noisy Tenfold", accuracy, precisions, recalls, f1_measures)

# # sanity check: clean tree metrics for pure model
# compute_metrics(clean_dataset, clean_tree)
# display_metrics_table("Clean", *compute_metrics(clean_dataset, clean_tree))

# use our decision tree, classify a datapoint for the pruned sets
# input:
#   - datapoint: sample to classify
#   - tree: our model used to classify the datapoint
#   - leaf_map_count: map of leaf node -> number of training examples in that leaf node label
# returns predicted label of the datapoint
def compute_class_prune(datapoint, tree, leaf_map_count):
    if tree.label != None:
        if not tree in leaf_map_count: leaf_map_count[tree] = 0
        leaf_map_count[tree] += 1
    else:
        if datapoint[tree.feature] <= tree.split_val:
            return compute_class_prune(datapoint, tree.left, leaf_map_count)
        else:
            return compute_class_prune(datapoint, tree.right, leaf_map_count)

# helper function to compute and return depth of tree recursively
def depth(tree):
    if tree.label != None: return 0
    return 1 + max(depth(tree.left), depth(tree.right))

# depth(clean_tree)

# nested 10-fold cross validation using pruning with decision trees
# produces 90 trees overall
# input:
#   - dataset
# returns the average confusion matrix, depth information and accuracy pre and post pruning
def prune(dataset):
    
    np.random.shuffle(dataset)

    # variables to track, process and return
    depth_before = 0
    depth_after = 0
    accuracies_before = []
    accuracies_after = []
    confusion_matrices = []

    # split the dataset into a train_and_validation set, and a test_dataset 10 times
    # train each of these 9 times using train set and validation set to test / tune
    for i in range(10):
        train_and_validation = np.append(dataset[:i * 200], dataset[(i+1) * 200:], axis=0)
        test_dataset = dataset[i * 200: (i+1) * 200]

        # perform pruning over 8 train folds and evaluate / tune using validation fold
        for val_index in range(9):

            # split the train_and_validation set into the train dataset and a validation set
            train = np.append(train_and_validation[:val_index * 200], train_and_validation[(val_index+1) * 200:], axis=0)
            validation_set = train_and_validation[val_index * 200: (val_index+1) * 200]

            # create decision tree
            trained_tree = decision_tree_learning(train, 0)
            depth_before += depth(trained_tree)
            leaf_map_count = {}

            # for each leaf, compute the number of example training points that enter that leaf
            for training_point in train:
                compute_class_prune(training_point, trained_tree, leaf_map_count)

            # accuracy before pruning
            accuracy = evaluate_accuracy(trained_tree, validation_set) # compute the accuracy before any pruning
            accuracy_before = accuracy

            # perform pruning
            pruned_tree, accuracy = prune_node(trained_tree, validation_set, trained_tree, leaf_map_count, accuracy) #prune the tree

            # update depth after pruning
            depth_after += depth(pruned_tree)

            # update accuracies array
            accuracy_after = evaluate_accuracy(pruned_tree, test_dataset)
            accuracies_before.append(accuracy_before)
            accuracies_after.append(accuracy_after)

            # compute confusion matrix for pruned tree
            cf = calculate_confusion_matrix(test_dataset, pruned_tree)
            confusion_matrices.append(cf)


    # compute average confusion matrix
    summed_matrix = np.zeros((4,4))
    for matrix in confusion_matrices:
        for i in range(4):
            summed_matrix[i] = [sum(x) for x in zip(summed_matrix[i], matrix[i])]

    # compute average of metrics to return
    average_cf = summed_matrix / len(confusion_matrices)
    avg_depth_before_prune = depth_before / 90
    avg_depth_after_prune = depth_after / 90
    avg_accuracy_before = sum(accuracies_before) / len(accuracies_before)
    avg_accuracy_after = sum(accuracies_after) / len(accuracies_after)

    return average_cf, avg_depth_before_prune, avg_depth_after_prune, avg_accuracy_before, avg_accuracy_after




# used by the prune function to actually prune a node and replace parent with label
# input:
#   - tree_node: initially root node, recursively becomes subtrees and leaf nodes
#   - validation_set: to determine whether to prune or not
#   - root_node: keep track of root note
#   - leaf_map_count: label -> count
#   - accuracy
# returns pruned tree and its accuracy
def prune_node(tree_node, validation_set, root_node, leaf_map_count, accuracy):

    #if its a leaf node, return the leaf and the
    if tree_node.label != None:
        return tree_node, accuracy

    # prune both the left and right nodes
    tree_node.left, accuracy = prune_node(tree_node.left, validation_set, root_node, leaf_map_count, accuracy)
    tree_node.right, accuracy = prune_node(tree_node.right, validation_set, root_node, leaf_map_count, accuracy)

    #if both the children are leafs, then prune
    # store the current leaf values, in case we do not prune
    if tree_node.left.label != None and tree_node.right.label != None:
        left, right, feature, split_val = tree_node.left, tree_node.right, tree_node.feature, tree_node.split_val

        #set the label of the parent to the majority class
        if leaf_map_count[tree_node.left] >= leaf_map_count[tree_node.right]:
            tree_node.label = tree_node.left.label
        else:
            tree_node.label = tree_node.right.label

        # replacing node with empty one
        leaf_map_count[tree_node] = leaf_map_count[tree_node.left] + leaf_map_count[tree_node.right]
        tree_node.left = None
        tree_node.right = None
        tree_node.feature = None
        tree_node.split_val = None
        new_accuracy = evaluate_accuracy(root_node, validation_set)

        #if after pruning, the accuracy was worse, resort back to original setting
        if new_accuracy < accuracy:
            tree_node.left = left
            tree_node.right = right
            tree_node.feature = feature
            tree_node.split_val = split_val
            tree_node.label = None
            return tree_node, accuracy
        return tree_node, min(accuracy, new_accuracy)

    else:
        return tree_node, accuracy

# helper function for tabulating data for report
# tabulate the accuracy and depth stats for pruned tree
#   - f1_measures: f1 measure for each class
# returns nothing but displays table when called
def display_info_table(dataset_name, cf_matrix, avg_before, avg_after, avg_acc_before, avg_acc_after):
    true_values = sum(cf_matrix[i][i] for i in range(4))
    accuracy = true_values / cf_matrix.sum()
    accuracy = round(accuracy, 3)
    avg_acc_after = round(avg_acc_after, 3)
    avg_acc_before = round(avg_acc_before, 3)
    avg_before = round(avg_before, 3)
    avg_after = round(avg_after, 3)
    avg_improvement = avg_acc_after - avg_acc_before
    avg_improvement = round(avg_improvement * 100, 2)
    print("Accuracy: ", accuracy)
    print("Average Depth Before: ", avg_before)
    print("Average Depth After: ", avg_after)
    print("Avg Accuracy Before Pruning: ", avg_acc_before)
    print("Avg Accuracy After Pruning: ", avg_acc_after)
    print("Avg Improvement in Accuracy %: ", avg_improvement)
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')

    table = ax.table(cellText=[["Accuracy", accuracy],
                               ["Average Depth Before", avg_before],
                               ["Average Depth After", avg_after],
                               ["Avg Accuracy Before Pruning", avg_acc_before],
                               ["Avg Accuracy After Pruning", avg_acc_after],
                               ["Avg Improvement in Accuracy %", avg_improvement]],
                     colLabels=["Metric", "Value"],
                     cellLoc='center',
                     loc='center')

    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_text_props(fontweight='bold')
            cell.set_facecolor('#FF8000')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    plt.title(dataset_name)
    plt.show()

    return accuracy

## remaining code gets the figures and metrics/stats needed for the report
## can replace with own dataset to set

# cf_matrix_clean, avg_before_clean, avg_after_clean, avg_acc_before_clean, avg_acc_after_clean = prune(clean_dataset)

# clean_prune_accuracy = display_info_table("Clean Dataset", cf_matrix_clean, avg_before_clean, avg_after_clean, avg_acc_before_clean, avg_acc_after_clean)
# displayCF(cf_matrix_clean)
# accuracy_clean, precisions_clean, recalls_clean, f1_measures_clean = compute_metrics_cf(cf_matrix_clean)
# display_metrics_table("Clean Pruned", accuracy_clean, precisions_clean, recalls_clean, f1_measures_clean)

cf_matrix_noisy, avg_before_noisy, avg_after_noisy, avg_acc_before_noisy, avg_acc_after_noisy = prune(noisy_dataset)

noisy_prune_accuracy = display_info_table("Noisy Dataset", cf_matrix_noisy, avg_before_noisy, avg_after_noisy, avg_acc_before_noisy, avg_acc_after_noisy)
displayCF(cf_matrix_noisy)
accuracy_noisy, precisions_noisy, recalls_noisy, f1_measures_noisy = compute_metrics_cf(cf_matrix_noisy)
display_metrics_table("Noisy Pruned", accuracy_noisy, precisions_noisy, recalls_noisy, f1_measures_noisy)