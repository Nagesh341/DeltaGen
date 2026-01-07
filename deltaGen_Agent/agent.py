from google.adk.agents.llm_agent import Agent
import os
import json
from .redbend_tool import redbend_tool
from .xdelta_tool import xdelta_tool

def read_input_data() -> str:
    """Read input data from Input_data.json file in current working directory.
    
    Returns:
        JSON string with input data or error message
    """
    cwd = os.getcwd()
    input_file = os.path.join(cwd, "Input_data.json")
    
    print(f"[TRACE] Looking for input file: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"[TRACE] Input_data.json not found")
        return "Error: Input_data.json file not found in current directory"
    
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        print(f"[TRACE] Successfully read Input_data.json: {data}")
        
        # Normalize keys by converting to lowercase and removing underscores/hyphens
        normalized_data = {}
        for key, value in data.items():
            normalized_key = key.lower().replace('_', '').replace('-', '')
            normalized_data[normalized_key] = value
        
        # Extract data using normalized keys
        source_path = normalized_data.get('sourcepath', 'Not specified')
        target_path = normalized_data.get('targetpath', 'Not specified')
        ecu_type = normalized_data.get('ecutype', 'Not specified')
        delta_tool = normalized_data.get('deltatool', 'Not specified')
        
        result = f"""Input data read successfully:
- Source path: {source_path}
- Target path: {target_path}
- ECU type: {ecu_type}
- Delta tool: {delta_tool}

Please review the input data above and confirm if it's correct."""
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"[TRACE] Error parsing JSON: {e}")
        return f"Error: Invalid JSON format in Input_data.json - {str(e)}"
    except Exception as e:
        print(f"[TRACE] Error reading file: {e}")
        return f"Error: Failed to read Input_data.json - {str(e)}"

def update_input_data(source_path: str, target_path: str, ecu_type: str, delta_tool: str) -> str:
    """Update Input_data.json file with new values.
    
    Args:
        source_path: Absolute path of source zip file
        target_path: Absolute path of target zip file
        ecu_type: ECU type/name
        delta_tool: Delta tool type (redbend or delta)
    
    Returns:
        Status message with updated data
    """
    cwd = os.getcwd()
    input_file = os.path.join(cwd, "Input_data.json")
    
    # Use camelCase keys to match the existing format
    data = {
        "sourcePath": source_path,
        "targetPath": target_path,
        "ecuType": ecu_type,
        "deltaTool": delta_tool
    }
    
    try:
        with open(input_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"[TRACE] Successfully updated Input_data.json: {data}")
        
        # Return formatted message with updated data
        result = f"""Input_data.json updated successfully!

Updated Input Data:
- Source path: {source_path}
- Target path: {target_path}
- ECU type: {ecu_type}
- Delta tool: {delta_tool}

Please confirm to proceed with partition file validation and delta generation."""
        
        return result
        
    except Exception as e:
        print(f"[TRACE] Error writing file: {e}")
        return f"Error: Failed to update Input_data.json - {str(e)}"

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

IMPORTANT: At the start of the conversation, display this banner:
Welcome to Unified Smart Delta Generation Agent

Follow this workflow step by step:

STEP 1 - Read Input Data:
- Use the read_input_data tool to read Input_data.json file from current directory
- Display the extracted information to the user:
  * Source path
  * Target path
  * ECU type
  * Delta tool

STEP 2 - User Confirmation:
- Ask the user to review the input data and confirm if it's correct
- If the user wants to make changes, ask them to provide the updated values
- Use the update_input_data tool to save any changes back to Input_data.json
- Confirm the save was successful

STEP 3 - Validate Partition File:
- Use the check_partition_file tool with the ECU type to verify the partition file exists
- If the tool returns an error message, stop and inform the user

STEP 4 - Delegate to Appropriate Tool:
- Based on the delta_tool from Input_data.json, delegate to the appropriate sub-agent:
  * If delta_tool is "redbend" → delegate to redbend_tool
  * If delta_tool is "delta" or "xdelta" → delegate to xdelta_tool
- When delegating, provide the source path, target path, and ECU type in your message

Available tools:
- read_input_data: Reads input data from Input_data.json file
- update_input_data: Updates Input_data.json with new values
- check_partition_file: Verifies if the partition file exists in PWD

Available sub-agents:
- redbend_tool: Agent for Redbend delta generation (vRapidMobileCMD-Linux.exe)
- xdelta_tool: Agent for XDelta delta generation (xdelta3)

Start by displaying the banner and reading the input data from Input_data.json.''',
    tools=[check_partition_file, read_input_data, update_input_data],
    sub_agents=[redbend_tool, xdelta_tool],
)

