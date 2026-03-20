import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("../data/cleaned_students.csv")

# Average scores
avg = data.mean(numeric_only=True)

print("Average Marks")
print(avg)

# Bar chart
avg.plot(kind="line")
plt.title("Average Score per Subject")
plt.savefig("../visuals/average_scores.png")
plt.show()

# Distribution plot
sns.histplot(data["Math"], bins=5)
plt.title("Math Score Distribution")
plt.savefig("../visuals/math_distribution.png")
plt.show()

# Correlation heatmap
sns.heatmap(data.corr(numeric_only=True), annot=True)
plt.title("Correlation Between Subjects")
plt.savefig("../visuals/correlation.png")
plt.show()