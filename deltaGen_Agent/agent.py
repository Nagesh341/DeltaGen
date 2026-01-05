from google.adk.agents.llm_agent import Agent
import os
from .redbend_tool import redbend_tool
from .xdelta_tool import xdelta_tool

def check_partition_file(ecu_type: str) -> str:
    """Check if partition file exists in current working directory.
    
    Args:
        ecu_type: ECU type/name
    
    Returns:
        Status message indicating if file exists or not
    """
    partition_filename_base = f"{ecu_type}_Partition_file"
    cwd = os.getcwd()
    
    print(f"[TRACE] Checking for partition file: {partition_filename_base}")
    print(f"[TRACE] Current working directory: {cwd}")
    
    # Check for .xlsx extension
    xlsx_file = f"{partition_filename_base}.xlsx"
    xlsx_path = os.path.join(cwd, xlsx_file)
    if os.path.exists(xlsx_path):
        print(f"[TRACE] Partition file found: {xlsx_path}")
        return f"Partition file exists: {xlsx_file}"
    
    # Check for .csv extension
    csv_file = f"{partition_filename_base}.csv"
    csv_path = os.path.join(cwd, csv_file)
    if os.path.exists(csv_path):
        print(f"[TRACE] Partition file found: {csv_path}")
        return f"Partition file exists: {csv_file}"
    
    # File not found with either extension
    print(f"[TRACE] Partition file NOT found: {partition_filename_base}.xlsx or .csv")
    return f"Error: Partition file not found - {partition_filename_base}.xlsx or .csv does not exist in {cwd}"

# Root orchestrator agent
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Orchestrator agent that routes delta generation requests to appropriate tool agents.',
    instruction='''You are the root orchestrator agent for delta generation.

Parse user input in the following format:
Source path: <absolute path of source zip file>
Target path: <absolute path of target zip file>
ECU type: <ECU type/name>
Delta tool: <redbend or delta>

MANDATORY FIELDS (Required):
- Target path
- ECU type
- Delta tool

Your task:
1. Extract the source path, target path, ECU type, and delta tool type from the user input
2. Validate mandatory fields:
   - If Target path is missing: Return "Error: Data not valid - Target path is required"
   - If ECU type is missing: Return "Error: Data not valid - ECU type is required"
   - If Delta tool is missing: Return "Error: Data not valid - Delta tool is required"
3. Validate partition file exists:
   - Use the check_partition_file tool with the ECU type to verify the partition file exists
   - If the tool returns an error message, stop and return that error
4. If all validations pass, proceed based on the Delta tool specified:
   - If "redbend": Delegate to redbend_tool agent providing the source path, target path, and ECU type as part of your message
   - If "delta": Delegate to xdelta_tool agent providing the source path, target path, and ECU type as part of your message
5. Return the result from the delta generation agent

Available tools:
- check_partition_file: Verifies if the partition file exists in PWD

Available sub-agents:
- redbend_tool: Separate agent for Redbend delta generation (vRapidMobileCMD-Linux.exe)
- xdelta_tool: Separate agent for XDelta delta generation

After validation, provide the information to the appropriate sub-agent by including it in your response message.''',
    tools=[check_partition_file],
    sub_agents=[redbend_tool, xdelta_tool],
)

