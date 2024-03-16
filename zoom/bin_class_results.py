from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, roc_curve, precision_recall_curve, average_precision_score
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('zoom/varied_training_set_with_noise.csv')
X = df['description'].values
y = df['label'].values

# Split the dataset for final evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define a scoring function for cross-validation
scoring = {'accuracy': 'accuracy', 'f1_score': 'f1', 'auc': 'roc_auc'}

# Experiment with different alpha values
alphas = [0.01, 0.1, 1, 5, 10]
results = []

for alpha in alphas:
    # Create and train the model with cross-validation
    model = make_pipeline(TfidfVectorizer(), MultinomialNB(alpha=alpha))
    
    # Perform cross-validation and store results
    cv_results = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
    avg_auc = np.mean(cv_results)
    print(f"Alpha: {alpha} -> Average AUC: {avg_auc:.4f}")
    results.append((alpha, avg_auc))

# Select the best alpha value
best_alpha, best_score = max(results, key=lambda x: x[1])
print(f"Best Alpha: {best_alpha} with AUC: {best_score:.4f}")

# Train a final model using the best alpha value on the full training set
final_model = make_pipeline(TfidfVectorizer(), MultinomialNB(alpha=best_alpha))
final_model.fit(X_train, y_train)

# Predictions for the test set
y_pred = final_model.predict(X_test)
y_prob = final_model.predict_proba(X_test)[:, 1]  # Probabilities for the positive class

# Compute statistics on the test set
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)
print(f"Test Set Accuracy: {accuracy:.4f}")
print(f"Test Set F1 Score: {f1:.4f}")
print(f"Test Set AUC: {auc:.4f}")

# Plot ROC curve
fpr, tpr, _ = roc_curve(y_test, y_prob)
plt.figure()
plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.savefig('roc_curve.png')
plt.show()

# Plot Precision-Recall curve
precision, recall, _ = precision_recall_curve(y_test, y_prob)
average_precision = average_precision_score(y_test, y_prob)
plt.figure()
plt.plot(recall, precision, label='Precision-Recall curve (area = %0.2f)' % average_precision)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower left")
plt.savefig('precision_recall_curve.png')
plt.show()
