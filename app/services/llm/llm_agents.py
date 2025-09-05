from agents import Agent, Runner
from agents.items import ItemHelpers

from app.services.llm.dataclasses.project_info import ProjectInfo
from app.services.llm.llm_config import runner_config
from app.services.llm.mcps.mcps import get_mcp_servers_context
from app.services.llm.prompts.builder_prompts import AGENT_PROMPT
from app.services.llm.tools.file_system import read_file, write_file


async def running_agent(messages: list, project: ProjectInfo):
    async with get_mcp_servers_context() as (active_servers, _):
        agent = Agent[ProjectInfo](name="Assistant Agent", instructions=AGENT_PROMPT, tools=[read_file, write_file])

        runner = Runner.run_streamed(agent, input=messages, run_config=runner_config, context=project)

        async for event in runner.stream_events():
            if event.type == "raw_response_event":
                continue
            elif event.type == "agent_updated_stream_event":
                yield {"type": "agent_updated", "agent_name": event.new_agent.name}
                continue
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    raw_item_dict = (
                        event.item.raw_item.model_dump()
                        if hasattr(event.item.raw_item, "model_dump")
                        else vars(event.item.raw_item)
                        if hasattr(event.item.raw_item, "__dict__")
                        else str(event.item.raw_item)
                    )
                    yield {"type": "tool_call", "message": "Tool was called", "raw_item": raw_item_dict}
                elif event.item.type == "tool_call_output_item":
                    raw_item_dict = (
                        event.item.raw_item.model_dump()
                        if hasattr(event.item.raw_item, "model_dump")
                        else vars(event.item.raw_item)
                        if hasattr(event.item.raw_item, "__dict__")
                        else str(event.item.raw_item)
                    )
                    yield {"type": "tool_output", "output": event.item.output, "raw_item": raw_item_dict}
                elif event.item.type == "message_output_item":
                    yield {"type": "message_output", "content": ItemHelpers.text_message_output(event.item)}
                else:
                    pass
