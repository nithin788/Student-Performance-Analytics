
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Performance Analytics System")
st.write("Analyze student marks, grades, attendance, and performance.")

# Load student data
@st.cache_data
def load_data():
    return pd.read_csv("students.csv")

try:
    df = load_data()

    subjects = ["Python", "Maths", "English", "AI"]

    # Calculate student results
    df["Total_Marks"] = df[subjects].sum(axis=1)
    df["Average_Marks"] = df[subjects].mean(axis=1).round(2)

    def get_grade(avg):
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
        return "F"

    df["Grade"] = df["Average_Marks"].apply(get_grade)
    df["Result"] = df[subjects].ge(40).all(axis=1).map(
        {True: "Pass", False: "Fail"}
    )

    # Dashboard summary
    total_students = len(df)
    class_average = df["Average_Marks"].mean()
    passed = (df["Result"] == "Pass").sum()
    failed = (df["Result"] == "Fail").sum()
    pass_rate = (passed / total_students * 100) if total_students else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", total_students)
    col2.metric("Class Average", f"{class_average:.2f}")
    col3.metric("Students Passed", int(passed))
    col4.metric("Pass Rate", f"{pass_rate:.1f}%")

    st.divider()

    # Department filter
    st.subheader("🔎 Filter Students")
    departments = ["All"] + sorted(df["Department"].unique().tolist())
    selected_department = st.selectbox(
        "Choose Department", departments
    )

    filtered_df = df.copy()
    if selected_department != "All":
        filtered_df = filtered_df[
            filtered_df["Department"] == selected_department
        ]

    # Search by student name
    search_name = st.text_input("Search student by name")
    if search_name:
        filtered_df = filtered_df[
            filtered_df["Name"].str.contains(
                search_name, case=False, na=False
            )
        ]

    # Student table
    st.subheader("👨‍🎓 Student Performance Table")
    display_columns = [
        "Student_ID", "Name", "Department",
        *subjects, "Attendance", "Total_Marks",
        "Average_Marks", "Grade", "Result"
    ]
    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    # Department chart
    st.subheader("📊 Department-wise Average")
    department_average = df.groupby("Department")[
        "Average_Marks"
    ].mean()
    st.bar_chart(department_average)

    # Subject chart
    st.subheader("📚 Subject-wise Average")
    subject = ["Python", "Math", "English", "AI"]
    subject_average = df[subjects].mean()
    st.bar_chart(subject_average)

    # Pass and fail chart
    
    st.subheader("✅ Pass and Fail Analysis")

    result_counts = (
    df["Result"]
    .value_counts()
    .reindex(["Pass", "Fail"], fill_value=0)
      )

    st.bar_chart(result_counts)
    st.write("Pass:", int(result_counts["Pass"]))
    st.write("Fail:", int(result_counts["Fail"]))

    
    
    st.bar_chart(result_counts)

    # Students needing support
    st.subheader("⚠️ Students Needing Academic Support")
    at_risk = df[
        (df["Average_Marks"] < 50) |
        (df["Attendance"] < 75)
    ]
    if at_risk.empty:
        st.success("No students flagged by the selected rules.")
    else:
        st.dataframe(
            at_risk[
                ["Name", "Department", "Average_Marks", "Attendance", "Result"]
            ],
            use_container_width=True,
            hide_index=True
        )

    # Download results
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Analyzed Results",
        data=csv_data,
        file_name="student_analysis_results.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error(
        "students.csv was not found. Keep app.py and students.csv "
        "in the same project folder."
    )
except Exception as error:
    st.error(f"Something went wrong: {error}")

# Individual Student Performance Analysis

st.divider()
st.header("🎓 Individual Student Performance Analysis")

student_names = sorted(df["Name"].unique())

selected_student = st.selectbox(
    "Choose a student",
    student_names,
    key="individual_student"
)

student = df[df["Name"] == selected_student].iloc[0]

st.subheader(f"Performance Report: {selected_student}")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Marks",
    f"{student['Average_Marks']:.2f}"
)

col2.metric(
    "Attendance",
    f"{student['Attendance']}%"
)

col3.metric(
    "Grade",
    student["Grade"]
)

st.subheader("📊 Subject-wise Marks")

subject_columns = ["Python", "Maths", "English", "AI"]

student_marks = student[subject_columns]

st.bar_chart(student_marks)

st.subheader("📋 Student Result")

st.write("Student ID:", student["Student_ID"])
st.write("Department:", student["Department"])
st.write("Total Marks:", student["Total_Marks"])
st.write("Final Result:", student["Result"])

