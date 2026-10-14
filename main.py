
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read student data
df = pd.read_csv("students.csv")

subjects = ["Python", "Maths", "English", "AI"]

# Calculate total and average marks
df["Total_Marks"] = df[subjects].sum(axis=1)
df["Average_Marks"] = df[subjects].mean(axis=1).round(2)

# Assign grades
def assign_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"

df["Grade"] = df["Average_Marks"].apply(assign_grade)

# Check pass or fail
def check_result(row):
    for subject in subjects:
        if row[subject] < 40:
            return "Fail"
    return "Pass"

df["Result"] = df.apply(check_result, axis=1)

# Display complete student results
print("\nSTUDENT PERFORMANCE ANALYTICS SYSTEM")
print("=" * 50)
print(df.to_string(index=False))

# Class statistics using NumPy
print("\nCLASS SUMMARY")
print("-" * 30)
print("Total students:", len(df))
print("Class average:", round(np.mean(df["Average_Marks"]), 2))
print("Highest average:", df["Average_Marks"].max())
print("Lowest average:", df["Average_Marks"].min())
print("Students passed:", (df["Result"] == "Pass").sum())
print("Students failed:", (df["Result"] == "Fail").sum())

# Subject-wise analysis
print("\nSUBJECT-WISE AVERAGES")
print("-" * 30)
for subject in subjects:
    print(subject, ":", round(df[subject].mean(), 2))


# Department-wise performance analysis
print("\nDEPARTMENT-WISE PERFORMANCE")
print("-" * 35)

department_average = df.groupby("Department")[
    "Average_Marks"
].mean().round(2)

print(department_average.to_string())

# Attendance analysis
print("\nATTENDANCE ANALYSIS")
print("-" * 35)

low_attendance = df[df["Attendance"] < 75]

print("Students with attendance below 75%:",
      len(low_attendance))

if len(low_attendance) > 0:
    print(low_attendance[
        ["Name", "Department", "Attendance"]
    ].to_string(index=False))
else:
    print("No students have attendance below 75%.")

# Identify students who may need academic support
print("\nSTUDENTS NEEDING ACADEMIC SUPPORT")
print("-" * 35)

at_risk = df[
    (df["Average_Marks"] < 50) |
    (df["Attendance"] < 75)
]

if len(at_risk) > 0:
    print(at_risk[
        ["Name", "Average_Marks", "Attendance", "Result"]
    ].to_string(index=False))
else:
    print("No students flagged by these criteria.")


# Top 5 students
print("\nTOP 5 STUDENTS")
print("-" * 30)
top_students = df.nlargest(5, "Average_Marks")
print(top_students[["Name", "Average_Marks", "Grade"]].to_string(index=False))

# Save analyzed results
df.to_csv("student_analysis_results.csv", index=False)

print("\nAnalysis completed successfully!")
print("Results saved in student_analysis_results.csv")

# Chart 1: Department-wise average marks
department_average = df.groupby("Department")[
    "Average_Marks"
].mean()

department_average.plot(kind="bar")
plt.title("Department-wise Student Performance")
plt.xlabel("Department")
plt.ylabel("Average Marks")
plt.ylim(0, 100)
plt.tight_layout()
plt.show()

# Chart 2: Subject-wise average marks
subject_average = df[subjects].mean()

subject_average.plot(kind="bar")
plt.title("Subject-wise Average Marks")
plt.xlabel("Subject")
plt.ylabel("Average Marks")
plt.ylim(0, 100)
plt.tight_layout()
plt.show()

# Chart 3: Pass and fail count
result_counts = df["Result"].value_counts().reindex(
    ["Pass", "Fail"], fill_value=0
)

result_counts.plot(kind="bar")
plt.title("Student Pass and Fail Count")
plt.xlabel("Result")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.show()

