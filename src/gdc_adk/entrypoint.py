import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from loguru import logger

from .config.settings import settings
from .agents import EchoAgent

app = FastAPI(title="gdc-adk", docs_url="/docs")
router = APIRouter(prefix=settings.API_PREFIX)

agents = {}

@router.post("/agents/{agent_name}/run")
async def run_agent(agent_name: str, payload: dict):
    agent = agents.get(agent_name)
    if not agent:
        return JSONResponse(status_code=404, content={"error": "agent not found"})
    result = await agent.run(payload)
    return result

@router.post("/agents/{agent_name}/create")
async def create_agent(agent_name: str, config: dict = None):
    if agent_name in agents:
        return JSONResponse(status_code=400, content={"error": "agent already exists"})
    config = config or {}
    agent = EchoAgent(name=agent_name, config=config)
    agents[agent_name] = agent
    logger.info("Created agent: {}", agent_name)
    return {"status": "created", "agent": agent_name}

app.include_router(router)


def main():
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level=settings.LOG_LEVEL)
    uvicorn.run("gdc_adk.entrypoint:app", host=settings.HOST, port=settings.PORT, log_level=settings.LOG_LEVEL.lower())


if __name__ == "__main__":
    main()
