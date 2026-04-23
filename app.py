import streamlit as st
import matplotlib.pyplot as plt

# =========================
# RECOMMENDATION FUNCTION
# =========================
def recommend_tool(input_data):
    
    scores = {
        "Excel": 0,
        "Tableau": 0,
        "Power BI": 0,
        "Matplotlib": 0,
        "Seaborn": 0
    }
    
    rows = input_data["rows"]
    columns = input_data["columns"]
    purpose = input_data["purpose"]
    user = input_data["user"]
    interactive = input_data["interactive"]
    data_type = input_data["data_type"]
    
    if rows < 5000:
        scores["Excel"] += 4
    elif rows < 100000:
        scores["Tableau"] += 3
        scores["Power BI"] += 2
    else:
        scores["Power BI"] += 5
        scores["Tableau"] += 3
    
    if columns <= 2:
        scores["Excel"] += 3
    elif columns <= 10:
        scores["Power BI"] += 3
        scores["Tableau"] += 2
    
    if purpose == "Trend":
        scores["Tableau"] += 4
    elif purpose == "Distribution":
        scores["Seaborn"] += 4
    elif purpose == "Relationship":
        scores["Seaborn"] += 5
    elif purpose == "Comparison":
        scores["Excel"] += 3
    elif purpose == "Composition":
        scores["Power BI"] += 4
    
    if user == "Student":
        scores["Excel"] += 3
    elif user == "Analyst":
        scores["Seaborn"] += 3
    else:
        scores["Power BI"] += 5
    
    if interactive == "Yes":
        scores["Power BI"] += 5
        scores["Tableau"] += 4
    
    if data_type == "Time-series":
        scores["Tableau"] += 3
    elif data_type == "Mixed":
        scores["Power BI"] += 3
    elif data_type == "Numerical":
        scores["Matplotlib"] += 3
    
    sorted_tools = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_tools[:3]

# =========================
# DYNAMIC REASON FUNCTION 🔥
# =========================
def generate_reason(input_data, tool):
    
    reasons = []

    rows = input_data["rows"]
    columns = input_data["columns"]
    purpose = input_data["purpose"]
    user = input_data["user"]
    interactive = input_data["interactive"]
    data_type = input_data["data_type"]

    if tool == "Excel":
        if rows < 5000:
            reasons.append("Best for small datasets")
        if columns <= 5:
            reasons.append("Works well with fewer columns")
        if user == "Student":
            reasons.append("Easy for beginners")

    elif tool == "Power BI":
        if interactive == "Yes":
            reasons.append("Supports interactive dashboards")
        if rows > 50000:
            reasons.append("Handles medium to large datasets")
        if purpose == "Composition":
            reasons.append("Ideal for business reports")

    elif tool == "Tableau":
        if rows > 100000:
            reasons.append("Excellent for large datasets")
        if purpose == "Trend":
            reasons.append("Strong for trend analysis")
        if interactive == "Yes":
            reasons.append("Advanced interactive visuals")

    elif tool == "Matplotlib":
        if data_type == "Numerical":
            reasons.append("Best for numerical data")
        reasons.append("Good for static plots")

    elif tool == "Seaborn":
        if purpose in ["Distribution","Relationship"]:
            reasons.append("Great for statistical visualization")
        reasons.append("Advanced visualization library")

    return ", ".join(reasons)

# =========================
# UI
# =========================
st.set_page_config(page_title="Visualization Tool Recommender")

st.title("📊 Visualization Tool Recommendation System")
st.write("Enter your dataset details:")

rows = st.number_input("Number of Rows", 100, 1000000, 1000)
columns = st.slider("Number of Columns", 1, 15)

purpose = st.selectbox("Purpose", ["Trend","Comparison","Distribution","Relationship","Composition"])
user = st.selectbox("User Type", ["Student","Analyst","Manager"])
interactive = st.selectbox("Interactive Required", ["Yes","No"])
data_type = st.selectbox("Data Type", ["Numerical","Categorical","Time-series","Mixed"])

# =========================
# BUTTON ACTION
# =========================
if st.button("Recommend Tool"):
    
    input_data = {
        "rows": rows,
        "columns": columns,
        "purpose": purpose,
        "user": user,
        "interactive": interactive,
        "data_type": data_type
    }
    
    result = recommend_tool(input_data)
    
    # Recommendations
    st.subheader("🏆 Top Recommendations")
    for i, (tool, score) in enumerate(result, 1):
        st.write(f"{i}. {tool} (Score: {score})")
    
    # Dynamic Reasons 🔥
    st.subheader("🧠 Reasons")
    for tool, score in result:
        reason = generate_reason(input_data, tool)
        st.write(f"👉 {tool}: {reason}")
    
    # Pie Chart
    tools = [t[0] for t in result]
    scores = [t[1] for t in result]
    
    fig, ax = plt.subplots()
    ax.pie(scores, labels=tools, autopct='%1.1f%%', startangle=140)
    ax.set_title("Tool Recommendation Distribution")
    
    st.pyplot(fig)