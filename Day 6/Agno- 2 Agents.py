
import os
from getpass import getpass

from agno.agent import Agent
from agno.team import Team
from agno.team.mode import TeamMode
from agno.models.groq import Groq
from agno.tools.websearch import WebSearchTools

os.environ["GROQ_API_KEY"] = getpass("Enter Groq API Key: ")

# Google Search Agent
google_agent = Agent(
    name="Google Search Agent",
    role="Search Google and collect useful information",
    model=Groq(id="openai/gpt-oss-20b"),
    tools=[
        WebSearchTools(
            backend="google",
            enable_news=False,
            fixed_max_results=5,
            timeout=20
        )
    ],
    instructions=[
        "Search Google for the user's question",
        "Find relevant and reliable information",
        "Explain the results simply",
        "Include source URLs"
    ],
    markdown=True
)

# Qwen Agent
qwen_agent = Agent(
    name="Qwen Agent",
    role="Analyze questions and provide detailed explanations",
    model=Groq(id="qwen/qwen3.8-27b"),
    instructions=[
        "Answer the user's question clearly",
        "Use your knowledge to explain the topic",
        "Provide examples when useful",
        "Check the Google Agent's findings when available",
        "Do not claim to have searched the internet"
    ],
    markdown=True
)

# Multi-Agent Team
agent_team = Team(
    name="AI Research Team",
    model=Groq(id="openai/gpt-oss-120b"),
    members=[
        google_agent,
        qwen_agent
    ],
    mode=TeamMode.broadcast,
    instructions=[
        "Both agents must work on the same question",
        "Google Search Agent must search Google",
        "Qwen Agent must analyze and explain the topic",
        "Read both agents' responses",
        "Combine their findings into one clear answer",
        "Include source links from Google Search Agent",
        "Do not provide two separate answers",
        "Mention if information may be outdated"
    ],
    markdown=True,
    show_members_responses=True
)

agent_team.print_response(
    "Explain binary search in Java with code and time complexity",
    stream=True
)

agent_team.print_response(
    "Find the latest developments in Artificial Intelligence",
    stream=True
)
