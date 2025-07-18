import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

#imporing necessary packages packages from langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
key=os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(openai_api_key=key,model_name="gpt-3.5-turbo", temperature=0.7)

TEMPLATE="""
You are an expert educator with deep knowledge in {topic} at a {level} level.
You also understand human psychology and engagement design, enabling you to create fun, thought-provoking quizzes.

Your task is to generate exactly {number_of_questions} quiz questions based on the following source material:
"{text}". Make sure to cover key concepts from the text and the questions should vary in structure (e.g., multiple choice, true/false, fill-in-the-blank), if appropriate.
The questions should not be repeatable and should be designed to test understanding of the material.

### Requirements:
1. Match the tone: **{tone}**
2. Match the difficulty: **{level}** level
3. Ensure coverage of key concepts from the text.
4. Include a clear explanation for each correct answer.
5. Questions should vary in structure (e.g., multiple choice, true/false, fill-in-the-blank), if appropriate.

### Format:
Return the quiz in this exact JSON format:
{response_json}

Make sure the JSON is syntactically valid and structured precisely.
Do not add any extra commentary outside the JSON.
"""

quiz_generator_prompt = PromptTemplate(
    input_variables=["text","number_of_questions","topic","level","tone","response_json"],
    template = TEMPLATE
)


quiz_chain = LLMChain(
    llm=llm,
    prompt=quiz_generator_prompt,
    output_key="quiz",
    verbose=True
)


TEMPLATE2="""
You are an expert English grammarian, cognitive learning specialist, and educational content editor.

Your task is to review the following multiple-choice quiz designed for {topic} students.

### Instructions:
1. **Evaluate the overall language, tone, and complexity** of the quiz.
2. **Assess if the questions align** with the cognitive and analytical level appropriate for {topic} students.
3. **Keep the complexity analysis within 50 words.**
4. If any questions are too hard, too easy, poorly worded, or misaligned:
   - **Revise only those specific questions.**
   - Adjust the tone and phrasing to better suit the target student's ability.
   - Preserve the original structure (e.g., multiple-choice format).

### Input Quiz:
{quiz}

### Output Format:
- **Complexity Analysis (<= 50 words)**:
  ...
- **Updated Questions (if any)**:
  ...
"""



quiz_eval_prompt = PromptTemplate(
    input_variables=["quiz", "topic"],
    template=TEMPLATE2
    )
review_chain = LLMChain(
    llm=llm,
    prompt=quiz_eval_prompt,
    output_key="review",
    verbose=True
)

# This is an Overall Chain where we run the two chains in Sequence
generate_eval_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number_of_questions", "topic", "level", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)