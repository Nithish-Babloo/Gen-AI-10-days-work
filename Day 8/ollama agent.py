
from agno.agent import Agent
from agno.models.ollama import Ollama

# 1. Initialize Ollama model
model = Ollama(id="llama3.2:1b")

# 2. Create Java Interview Agent
agent = Agent(
    name="JavaInterviewAgent",
    model=model,
    instructions="""
    You are a Personal Java Interview Preparation Agent.

    Rules:
    1. Help the user prepare for Java interviews.
    2. Answer only Java interview-related questions.
    3. Explain Java concepts in simple language.
    4. Provide Java code examples whenever useful.
    5. Help with OOP, collections, multithreading,
       exception handling, and Java basics.
    6. If the question is not related to Java interviews,
       respond exactly:
       "It's not a Java interview question."
    """
)

# 3. Run the agent continuously
while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() == "exit":
        print("Bye! Happy Java Interview Preparation!")
        break

    response = agent.run(user_input)

    print("\nAgent:", response.content)

