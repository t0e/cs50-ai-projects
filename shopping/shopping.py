import csv
import sys
import datetime
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        evidence_list = []
        label_list = []
        for row in reader:
            evidence = []
            label = None
            for (i, cell) in enumerate(row):
                if i in [0, 2, 4, 11, 12, 13, 14]:
                    evidence.append(int(cell))
                elif i == 10:
                    if cell == "June":
                        cell = "Jun"
                    month = datetime.datetime.strptime(cell, "%b").month
                    evidence.append(month - 1)
                elif i == 15:
                    if cell == 'Returning_Visitor':
                        evidence.append(1)
                    else:
                        evidence.append(0)
                elif i == 16:
                    if cell == "FALSE":
                        evidence.append(1)
                    else:
                        evidence.append(0)
                elif i == 17:
                    if cell == "TRUE":
                        label = 1
                    else:
                        label = 0
                else:
                    evidence.append(float(cell))
            evidence_list.append(evidence)
            label_list.append(label)
    return (evidence_list, label_list)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive = 0
    negative = 0
    true_positive = 0
    true_negative = 0
    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            positive += 1
            if actual == predicted:
                true_positive += 1
        elif actual == 0:
            negative += 1
            if actual == predicted:
                true_negative += 1
    return ((true_positive / positive), (true_negative / negative))


if __name__ == "__main__":
    main()
