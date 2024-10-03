import openai
import streamlit as st
import json
from random import randint


with open("probing_data.json", 'r') as fp:
    probing_data = json.load(fp)


openai.api_key = "sk-proj-8Hj0AxHhdPFQ75QbA7avT3BlbkFJalSAvYvn4CAIV7VQeim8y"

def so_probe1(q_and_a, probing_data, temperature=0.7):
    so_styles = probing_data["styles"]
    style = so_styles[randint(1, 4) - 1]
    user_prompt = """Please write a probe for the following: """ + q_and_a + """ style: """ + style

    user_dict = {"role": "user", "content": user_prompt}
    messages = [{"role": "system", "content": probing_data["system_prompt"]}]
    messages.append(user_dict)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
        )
        probe = response.choices[0].message["content"]
    except Exception as e:
        probe = f"Error: {e}"

    return probe


st.title("LLM Probing Demo")

language = st.sidebar.selectbox("Select Language", ["English", "German"])

if language == "English":
    lang_key = "en"
elif language == "German":
    lang_key = "de"

question = st.text_input("Enter the survey question:")
answer = st.text_input("Enter the respondent's answer:")

if st.button("Generate Probe"):
    if question and answer:
        q_and_a = f"question: \"{question}\" answer: \"{answer}\""
        probe = so_probe1(q_and_a, probing_data[lang_key])
        st.subheader("Generated Probe:")
        st.write(probe)
    else:
        st.error("Please enter both a question and an answer.")
