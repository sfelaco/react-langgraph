from dotenv import load_dotenv

load_dotenv()

from langgraph.prebuilt import ToolNode


from react.chains.reasoning_chain import react_reasoning_runnable, tools
from react.state import AgentState


def run_agent_reasoning_engine(state: AgentState):
    agent_outcome = react_reasoning_runnable.invoke(state)
    return {"agent_outcome": agent_outcome}



tool_node = ToolNode(
    tools=tools
)



def execute_tools(state: AgentState):
    agent_action = state["agent_outcome"]
    
    # Estrai il nome del tool e l'input
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input
    
    # Trova il tool corretto nella lista tools
    selected_tool = None
    for tool in tools:
        if tool.name == tool_name:
            selected_tool = tool
            break
    
    if selected_tool:
        # Esegui il tool selezionato con l'input fornito
        output = selected_tool.invoke(tool_input)
    else:
        output = f"Error: Tool '{tool_name}' not found"
    
    return {"intermediate_steps": [(agent_action, str(output))]}

