import pandas as pd
import numpy as np
import random
import os

# Define all necessary variations for the placeholders
features = ["RESTful API endpoints", "dynamic data visualization", "user authentication workflow", "payment processing module"]
technologies = ["React", "Django", "Node.js", "Flutter"]
specifications = ["security protocols", "responsive design", "cross-browser compatibility", "accessibility standards"]
modules = ["database schema", "login system", "search functionality", "checkout flow"]
aspects = ["query performance", "user experience", "security", "code maintainability"]
coverage = ["80%", "90%", "95%", "100%"]
actions = ["log in through social media", "submit a form with validation", "navigate through different sections of the app", "complete a purchase"]

meeting_types = ["brainstorming session", "retrospective meeting", "sprint planning", "technical review"]
topics = ["project milestones", "code optimization techniques", "agile methodologies", "team collaboration tools"]
materials = ["a presentation", "discussion questions", "a project timeline", "feedback forms"]
departments = ["marketing", "product design", "customer support", "quality assurance"]
documents = ["the project roadmap", "the feature specification", "the release schedule", "the budget report"]
key_points = ["the achieved metrics", "upcoming challenges", "team achievements", "resource needs"]
reports = ["quarterly performance review", "project status update", "market analysis findings", "user feedback compilation"]

# Ensure each template has corresponding values for all placeholders
coding_templates = [
    "Implement {feature} using {technology}. Ensure to include {specification}.",
    "Refactor the {module} to improve {aspect}. Consider using {technology} for better performance.",
    "Develop a {feature} that allows users to {action}. Use {technology} for the frontend.",
    "Write unit tests for the {module} covering {aspect}. Aim for {coverage} coverage."
]

communication_templates = [
    "Organize a {meeting_type} to discuss {topic}. Prepare {material} beforehand.",
    "Lead a workshop on {topic} focusing on {aspect}. Include practical exercises.",
    "Coordinate with the {department} to finalize {document}. Ensure all details are accurate.",
    "Present the {report} on {topic} during the next team meeting. Highlight {key_points}."
]

# Generate the dataset with 1000 entries
data = []
for _ in range(500):
    template = random.choice(coding_templates)
    description = template.format(
        feature=random.choice(features),
        technology=random.choice(technologies),
        specification=random.choice(specifications),
        module=random.choice(modules),
        aspect=random.choice(aspects),
        coverage=random.choice(coverage),
        action=random.choice(actions)
    )
    data.append((description, 1))

for _ in range(500):
    template = random.choice(communication_templates)
    description = template.format(
        meeting_type=random.choice(meeting_types),
        topic=random.choice(topics),
        material=random.choice(materials),
        department=random.choice(departments),
        document=random.choice(documents),
        key_points=random.choice(key_points),
        report=random.choice(reports),
        aspect=random.choice(aspects)  # Assuming 'aspect' could also fit in communication context for clarity
    )
    data.append((description, 0))

df_varied = pd.DataFrame(data, columns=['description', 'label'])
df_varied = df_varied.sample(frac=1).reset_index(drop=True)

# Introduce mislabeled noise to prevent 100% accuracy
noise_ratio = 0.05  # 5% of the data will be mislabeled
indices = np.random.choice(df_varied.index, size=int(len(df_varied) * noise_ratio), replace=False)
df_varied.loc[indices, 'label'] = 1 - df_varied.loc[indices, 'label']

# Saving the dataset
csv_path = 'zoom/varied_training_set_with_noise.csv'  # Update path as needed
if not os.path.exists(os.path.dirname(csv_path)):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
df_varied.to_csv(csv_path, index=False)

print(f"Dataset saved to {csv_path}. It contains varied and noisy data.")
