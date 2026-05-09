from mcp.server.fastmcp import FastMCP
import mcp

mcp = FastMCP("Tools")

@mcp.tool()
def func1(a: int, b: int) -> int:
    pass

@mcp.tool()
def func2(a: int, b: int) -> int:
    pass

if __name__ == "__main__":
    mcp.run(transport="sse", mount_path="/mcp")