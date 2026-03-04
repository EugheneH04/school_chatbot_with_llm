'''Purpose:
    Excel loading
    CSV loading
    Pandas agent
    DataFrame querying'''

"""
Excel & CSV Service
Handles DataFrame-based question answering.
"""

from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_ollama import ChatOllama
import pandas as pd


def create_dataframe_agent(df: pd.DataFrame):
    """
    Create pandas agent for Excel/CSV querying.
    """
    llm = ChatOllama(model="qwen2.5:7b")

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True
    )

    return agent


def ask_dataframe_question(agent, question: str):
    """
    Ask question to dataframe agent.
    """
    return agent.run(question)
