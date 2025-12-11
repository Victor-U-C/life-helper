import streamlit as st
import openai
from datetime import datetime

st.markdown(
    """
    <style>
    /* -------------------------- */
    /* App background and text */
    /* -------------------------- */
    .stApp {
        background: linear-gradient(to bottom right, #8B4513, #A0522D);
        background-size: cover;
        color: #FFFFFF; /* white text for contrast */
    }

    /* -------------------------- */
    /* Headers style */
    /* -------------------------- */
    h1, h2, h3, h4, h5, h6 {
        color: #FFF8DC;
        font-family: 'Georgia', serif;
    }

    /* -------------------------- */
    /* Sidebar style */
    /* -------------------------- */
    .css-1d391kg {
        background-color: #5C4033;
        color: #FFFFFF;
    }

    /* -------------------------- */
    /* Main and sidebar buttons */
    /* -------------------------- */
    div.stButton > button {
        background-color: #D2691E !important; /* solid brown */
        color: white !important;               /* text color */
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border: 2px solid #8B4513;            /* optional border */
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }

    div.stButton > button:hover {
        background-color: #CD853F !important;  /* lighter brown on hover */
        color: #FFF8DC !important;             /* text color on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# OpenAI API Setup
# --------------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --------------------------
# AI call function
# --------------------------
def call_ai(prompt, max_tokens=500):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful personal life assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

# --------------------------
# Initialize session state (temporary storage)
# --------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "meals" not in st.session_state:
    st.session_state.meals = []

if "family" not in st.session_state:
    st.session_state.family = []

if "journal" not in st.session_state:
    st.session_state.journal = []

# --------------------------
# Sidebar Inputs
# --------------------------
st.sidebar.title("Life Manager Inputs")

task = st.sidebar.text_input("Add a task for today:")
if st.sidebar.button("Add Task") and task:
    st.session_state.tasks.append(task)
    st.sidebar.success("Task added!")

meal = st.sidebar.text_input("Add meal/recipe suggestion:")
if st.sidebar.button("Add Meal") and meal:
    st.session_state.meals.append(meal)
    st.sidebar.success("Meal added!")

family_task = st.sidebar.text_input("Add family task / event:")
if st.sidebar.button("Add Family Task") and family_task:
    st.session_state.family.append(family_task)
    st.sidebar.success("Family task added!")

journal_entry = st.sidebar.text_area("Write your journal entry:")
if st.sidebar.button("Add Journal Entry") and journal_entry:
    st.session_state.journal.append(journal_entry)
    st.sidebar.success("Journal entry saved!")

# --------------------------
# Main Tabs
# --------------------------
tabs = st.tabs(["Today Plan","Cooking & Meals","Work Sessions","Health & Fitness",
                "Finance & Budget","Family & Household","Journal & Reflection","AI Assistant"])

# 1. Today Plan
with tabs[0]:
    st.header("Today’s Plan")
    if st.button("Generate Today Plan"):
        plan_prompt = f"Create a structured daily schedule including tasks: {st.session_state.tasks}, family tasks: {st.session_state.family}, meals: {st.session_state.meals}, and work/focus sessions."
        today_plan = call_ai(plan_prompt)
        st.text(today_plan)

# 2. Cooking & Meals
with tabs[1]:
    st.header("Meal Suggestions & Grocery List")
    if st.button("Generate Meal Plan"):
        meal_prompt = f"Generate a weekly meal plan based on meals I saved: {st.session_state.meals}. Include grocery list and meal times."
        meal_plan = call_ai(meal_prompt)
        st.text(meal_plan)

# 3. Work Sessions
with tabs[2]:
    st.header("Work & Focus Sessions")
    if st.button("Generate Work Schedule"):
        work_prompt = f"Create optimized work/focus sessions for today based on tasks: {st.session_state.tasks}."
        work_schedule = call_ai(work_prompt)
        st.text(work_schedule)

# 4. Health & Fitness
with tabs[3]:
    st.header("Health & Fitness")
    if st.button("Generate Health Plan"):
        health_prompt = f"Generate a daily fitness routine, sleep advice and hydration plan for an adult, considering tasks: {st.session_state.tasks}."
        health_plan = call_ai(health_prompt)
        st.text(health_plan)

# 5. Finance & Budget
with tabs[4]:
    st.header("Finance & Budget")
    if st.button("Generate Finance Advice"):
        finance_prompt = "Provide budget and expense advice based on example financial data."
        finance_plan = call_ai(finance_prompt)
        st.text(finance_plan)

# 6. Family & Household
with tabs[5]:
    st.header("Family & Household Tasks")
    if st.button("Organize Family Tasks"):
        family_prompt = f"Organize family tasks and home responsibilities: {st.session_state.family}."
        family_plan = call_ai(family_prompt)
        st.text(family_plan)

# 7. Journal & Reflection
with tabs[6]:
    st.header("Daily Journal & Reflection")
    journal_input = st.text_area("Write your reflection:")
    if st.button("Analyze Journal"):
        reflection = call_ai(f"Analyze this journal input and provide insights: {journal_input}")
        st.text(reflection)

# 8. AI Assistant
with tabs[7]:
    st.header("Ask AI for Life Advice")
    user_question = st.text_input("Ask AI something about your life or planning:")
    if st.button("Get AI Advice") and user_question:
        advice = call_ai(user_question)
        st.text(advice)
