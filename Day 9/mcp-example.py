
from fastmcp import FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Text

# Create MCP server
mcp = FastMCP("Study Planner")


@mcp.tool(app=True)
def study_planner():
    """Display a daily study timetable."""

    with Column(gap=3) as view:
        Heading("My Daily Study Planner")

        Text("Morning Session")
        Text("8:00 AM - Python Programming")

        Text("Afternoon Session")
        Text("2:00 PM - Data Structures and Algorithms")

        Text("Evening Session")
        Text("6:00 PM - SQL Practice")

        Text("Night Session")
        Text("8:00 PM - AI and MCP Projects")

        Text("Daily Goal: Study for 5 hours")

    return PrefabApp(view=view)


if __name__ == "__main__":
    mcp.run()
