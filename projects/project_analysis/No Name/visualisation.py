import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set(style="white")
sns.set_context("paper")


# Initialize the figure 
f, ax = plt.subplots(figsize=(7, 6))

# Load
data = pd.read_csv("data/analysis_data.csv")[["WAGP", "SEX", "Degree"]]
grouped = data.groupby("Degree")
order = pd.DataFrame({col:vals["WAGP"] for col,vals in grouped}).median().sort_values(ascending=False)


m_data = data[data["SEX"] == 1]
f_data = data[data["SEX"] == 2]

top_f_data = f_data[((f_data["Degree"] == "Engineering") \
                    | (f_data["Degree"] == "Computer science") \
                    | (f_data["Degree"] == "Transportation") \
                    | (f_data["Degree"] == "Construction") \
                    | (f_data["Degree"] == "Engineering Technologies"))
                    & (f_data["WAGP"] < 400000)]
top_m_data = m_data[((m_data["Degree"] == "Engineering") \
                    | (m_data["Degree"] == "Computer science") \
                    | (m_data["Degree"] == "Transportation") \
                    | (m_data["Degree"] == "Construction") \
                    | (m_data["Degree"] == "Engineering Technologies"))
                    & (m_data["WAGP"] < 400000)]

# Plot the orbital period with horizontal boxes
sns.set_color_codes("bright")
sns.violinplot(x="WAGP", y="Degree", data=top_f_data, fliersize=0.3, boxprops=dict(alpha=.3), color="r")

sns.violinplot(x="WAGP", y="Degree", data=top_m_data, fliersize=0.3, boxprops=dict(alpha=.3), color="b")



# Tweak the visual presentation
ax.xaxis.grid(True)
ax.set(ylabel="")
ax.set(xlabel="Wage")
sns.despine(trim=True, left=True)
plt.subplots_adjust(left=.2)
plt.setp(ax.collections, alpha=.6)
plt.show()

print("hi")