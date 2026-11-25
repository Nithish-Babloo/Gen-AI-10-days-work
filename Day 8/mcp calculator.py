from mcp.server import MCPServer
mcp = MCPServer("Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run()


pyproject.toml :

[project]
name = "simple-mcp"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastmcp[apps]>=4.2.6",
    "google-genai>=3.6.1",
    "mcp[cli]",
]
