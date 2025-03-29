
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Academic Success Predictor (ASP)", layout="wide")

st.title("🎓 Academic Success Predictor (ASP)")
st.markdown("Upload your student data or enter values manually to calculate the ASP Score (0–100) and risk category.")

# Scoring function
def calculate_asp_score(row):
    gpa_score = (row['GPA'] / 4) * 100 * 0.20
    attendance_score = row['Attendance Rate'] * 0.15
    engagement_score = row['Engagement Score'] * 0.10
    credit_score = row['Credit Completion'] * 0.10

    financial_score = 0 if row['Financial Risk'] else 100
    first_gen_score = 60 if row['First-Gen'] else 100
    housing_score = 0 if row['Housing Risk'] else 100
    ell_score = 70 if row['ELL'] else 100
    meals_score = 0 if row['Missed Meals'] else 100
    internet_score = 0 if row['No Internet'] else 100
    support_score = 0 if row['No Academic Support'] else 100

    risk_score = (
        financial_score * 0.05 +
        first_gen_score * 0.05 +
        housing_score * 0.03 +
        ell_score * 0.02 +
        meals_score * 0.03 +
        internet_score * 0.02 +
        support_score * 0.03
    )

    belonging_score = row['Peer Belonging'] * 0.10
    bullying_score = (20 - row['Bullying Reports']) / 20 * 100 * 0.05
    ally_score = row['Adult Ally'] * 0.05
    activity_score = row['Activity Participation'] * 0.05
    discipline_score = (50 - row['Disciplinary Referrals']) / 50 * 100 * 0.05

    sel_score = belonging_score + bullying_score + ally_score + activity_score + discipline_score
    total_score = gpa_score + attendance_score + engagement_score + credit_score + risk_score + sel_score
    return round(total_score, 2)

def rag_status(score):
    if score >= 85:
        return "🟢 Green (Low Risk)"
    elif score >= 70:
        return "🟠 Amber (Moderate Risk)"
    else:
        return "🔴 Red (High Risk)"

# File upload
uploaded_file = st.file_uploader("📤 Upload Excel file with student data", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df["ASP Score"] = df.apply(calculate_asp_score, axis=1)
    df["RAG Category"] = df["ASP Score"].apply(rag_status)
    st.success("✅ ASP Scores calculated!")
    st.dataframe(df)

# Manual entry
st.markdown("Or enter a single student's info below:")
with st.form("asp_form"):
    col1, col2 = st.columns(2)
    with col1:
        gpa = st.number_input("GPA (0–4)", 0.0, 4.0, 3.0)
        attendance = st.slider("Attendance Rate (%)", 0, 100, 90)
        engagement = st.slider("Engagement Score (%)", 0, 100, 85)
        credit = st.slider("Credit Completion (%)", 0, 100, 90)
        financial = st.checkbox("Financial Risk")
        first_gen = st.checkbox("First-Gen")
        housing = st.checkbox("Housing Risk")
        ell = st.checkbox("ELL")
    with col2:
        meals = st.checkbox("Missed Meals")
        internet = st.checkbox("No Internet Access")
        support = st.checkbox("No Academic Support")
        belonging = st.slider("Peer Belonging (0–100)", 0, 100, 80)
        bullying = st.slider("Bullying Reports (#)", 0, 20, 2)
        ally = st.slider("Adult Ally (0–100)", 0, 100, 100)
        activity = st.slider("Activity Participation (0–100)", 0, 100, 100)
        discipline = st.slider("Disciplinary Referrals (#)", 0, 50, 3)

    submitted = st.form_submit_button("Calculate Score")
    if submitted:
        row = {
            'GPA': gpa, 'Attendance Rate': attendance, 'Engagement Score': engagement,
            'Credit Completion': credit, 'Financial Risk': financial, 'First-Gen': first_gen,
            'Housing Risk': housing, 'ELL': ell, 'Missed Meals': meals, 'No Internet': internet,
            'No Academic Support': support, 'Peer Belonging': belonging, 'Bullying Reports': bullying,
            'Adult Ally': ally, 'Activity Participation': activity, 'Disciplinary Referrals': discipline
        }
        score = calculate_asp_score(row)
        rag = rag_status(score)
        st.metric("📊 ASP Score", f"{score}/100", help="Whole-child success prediction")
        st.metric("🧠 Risk Category", rag)
