import streamlit as st
import openai
import pandas as pd
import json
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
# OpenAI API Setup using secrets.toml
# --------------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --------------------------
# AI call function (updated for OpenAI >=1.0)
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
# Helper functions for JSON persistence
# --------------------------
def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# --------------------------
# Load persistent data
# --------------------------
tasks_data = load_data("tasks.json")
meals_data = load_data("meals.json")
work_data = load_data("work.json")
health_data = load_data("health.json")
finance_data = load_data("finance.json")
family_data = load_data("family.json")
journal_data = load_data("journal.json")

# --------------------------
# Sidebar Inputs
# --------------------------
st.sidebar.title("Life Manager Inputs")

# Add new task
task = st.sidebar.text_input("Add a task for today:")
if st.sidebar.button("Add Task") and task:
    tasks_data[str(datetime.now())] = task
    save_data("tasks.json", tasks_data)
    st.sidebar.success("Task added!")

# Add meal
meal = st.sidebar.text_input("Add meal/recipe suggestion:")
if st.sidebar.button("Add Meal") and meal:
    meals_data[str(datetime.now())] = meal
    save_data("meals.json", meals_data)
    st.sidebar.success("Meal added!")

# Add family task
family_task = st.sidebar.text_input("Add family task / event:")
if st.sidebar.button("Add Family Task") and family_task:
    family_data[str(datetime.now())] = family_task
    save_data("family.json", family_data)
    st.sidebar.success("Family task added!")

# Add journal entry
journal_entry = st.sidebar.text_area("Write your journal entry:")
if st.sidebar.button("Add Journal Entry") and journal_entry:
    journal_data[str(datetime.now())] = journal_entry
    save_data("journal.json", journal_data)
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
        plan_prompt = f"Create a structured daily schedule including tasks: {list(tasks_data.values())}, family tasks: {list(family_data.values())}, meals: {list(meals_data.values())}, and work/focus sessions."
        today_plan = call_ai(plan_prompt)
        st.text(today_plan)

# 2. Cooking & Meals
with tabs[1]:
    st.header("Meal Suggestions & Grocery List")
    if st.button("Generate Meal Plan"):
        meal_prompt = f"Generate a weekly meal plan based on meals I saved: {list(meals_data.values())}. Include grocery list and meal times."
        meal_plan = call_ai(meal_prompt)
        st.text(meal_plan)

# 3. Work Sessions
with tabs[2]:
    st.header("Work & Focus Sessions")
    if st.button("Generate Work Schedule"):
        work_prompt = f"Create optimized work/focus sessions for today based on tasks: {list(tasks_data.values())}."
        work_schedule = call_ai(work_prompt)
        st.text(work_schedule)

# 4. Health & Fitness
with tabs[3]:
    st.header("Health & Fitness")
    if st.button("Generate Health Plan"):
        health_prompt = f"Generate a daily fitness routine, sleep advice and hydration plan for an adult, considering tasks: {list(tasks_data.values())}."
        health_plan = call_ai(health_prompt)
        st.text(health_plan)

# 5. Finance & Budget
with tabs[4]:
    st.header("Finance & Budget")
    if st.button("Generate Finance Advice"):
        finance_prompt = f"Provide budget and expense advice based on transactions: {finance_data}."
        finance_plan = call_ai(finance_prompt)
        st.text(finance_plan)

# 6. Family & Household
with tabs[5]:
    st.header("Family & Household Tasks")
    if st.button("Organize Family Tasks"):
        family_prompt = f"Organize family tasks and home responsibilities: {list(family_data.values())}."
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
