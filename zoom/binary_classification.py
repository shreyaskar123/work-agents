import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Load the dataset
df = pd.read_csv('training_set.csv')
descriptions = df['description'].values
labels = df['label'].values

# Split the dataset
descriptions_train, descriptions_test, labels_train, labels_test = train_test_split(
    descriptions, labels, test_size=0.2, random_state=42
)

# Create and train the model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(descriptions_train, labels_train)

# Now you can use the model to predict a new description
def predict_category(description):
    prediction = model.predict([description])[0]
    return 'coding' if prediction == 1 else 'communication'

# Input from the user
user_description = input("Enter a task description to classify: ")

# Output the prediction
predicted_category = predict_category(user_description)
print(f"The task is predicted to be: {predicted_category} ({1 if predicted_category == 'coding' else 0})")
