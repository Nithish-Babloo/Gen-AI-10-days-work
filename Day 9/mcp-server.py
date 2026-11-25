
from fastmcp import FastMCP
from google import genai
import os

# Create MCP server
mcp = FastMCP("Student Assistant")

# Gemini API client
client = genai.Client(
    api_key=os.environ["GOOGLE_API_KEY"]
)


# Tool 1: Ask Gemini study questions
@mcp.tool
def ask_gemini(question: str) -> str:
    """Answer study and educational questions using Gemini."""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=question
    )

    return response.text or "No response generated."


# Tool 2: Calculate student percentage
@mcp.tool
def calculate_percentage(
    total_marks: float,
    obtained_marks: float
) -> float:
    """Calculate percentage from total and obtained marks."""

    if total_marks <= 0:
        raise ValueError("Total marks must be greater than zero.")

    if obtained_marks < 0 or obtained_marks > total_marks:
        raise ValueError("Obtained marks must be between 0 and total marks.")

    percentage = (obtained_marks / total_marks) * 100

    return round(percentage, 2)


# Tool 3: Check student grade
@mcp.tool
def check_grade(percentage: float) -> str:
    """Return a grade based on the student's percentage."""

    if percentage < 0 or percentage > 100:
        return "Invalid percentage"

    if percentage >= 90:
        return "Grade A"

    elif percentage >= 75:
        return "Grade B"

    elif percentage >= 60:
        return "Grade C"

    elif percentage >= 40:
        return "Grade D"

    else:
        return "Fail"


# Start MCP server
if __name__ == "__main__":
    mcp.run()
