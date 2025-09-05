from agents import function_tool
from agents.run_context import RunContextWrapper

from app.services.llm.dataclasses.project_info import ProjectInfo



@function_tool
def read_file(wrapper: RunContextWrapper[ProjectInfo], filename: str):
    with open(f"sandbox/projects/{wrapper.context.id}/{filename}", "r") as f:
        content = f.read()

    return f"File {filename} has been read, content: {content}"


@function_tool
def write_file(wrapper: RunContextWrapper[ProjectInfo], filename: str, content: str):
    with open(f"sandbox/projects/{wrapper.context.id}/{filename}", "w") as f:
        f.write(content)

    return f"File {filename} has been written"
