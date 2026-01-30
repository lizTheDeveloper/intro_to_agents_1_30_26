from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
import asyncio

current_dir = Path(__file__).parent
samples_dir = current_dir / "sample_files"
async def main():
    async with MCPServerStdio(
        name="Playwright",
        params={
            "command": "npx",
            "args": ["@playwright/mcp@latest"],
        }
    ) as server:
        agent = Agent(
            name="Assistant",
            instructions="Use Playwright to use google chrome.",
            mcp_servers=[server],
        )
        result = await Runner.run(agent, "Playtest the game on localhost:3000 and write a report of what might not be working.")
        print(result.final_output)
        
        
asyncio.run(main())