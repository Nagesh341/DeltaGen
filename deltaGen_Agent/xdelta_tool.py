from google.adk.agents.llm_agent import Agent

xdelta_tool = Agent(
    model='gemini-2.5-flash',
    name='xdelta_tool',
    description='XDelta delta generation agent. Generates delta using XDelta tool with provided source and target paths.',
    instruction='''You are the XDelta delta generation agent.

When called, you will receive information about:
- source_path: Absolute path of source zip file
- target_path: Absolute path of target zip file
- ecu_type: ECU type/name

Your task:
1. Print trace information: "[TRACE] XDelta tool called with:"
2. Print "Source: <source_path>"
3. Print "Target: <target_path>"
4. Print "ECU Type: <ecu_type>"
5. Generate delta using XDelta tool with the provided paths
6. Return status message of delta generation

Return a confirmation message that XDelta delta generation was initiated with the provided paths and ECU type.''',
)
