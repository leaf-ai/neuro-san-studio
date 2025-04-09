from typing import Any
from typing import Dict
from typing import Union

import logging
import aiofiles  # Import for asynchronous file operations

from neuro_san.interfaces.coded_tool import CodedTool

WRITE_TO_FILE = True
OUTPUT_PATH = "registries/"
AGENT_NETWORK_NAME = "AutomaticallyDesignedAgentNetwork"
HOCON_HEADER_START = ("{\n"
"    \"llm_config\": {\n"
"        \"model_name\": \"gpt-4o\",\n"
"        \"verbose\": true\n"
"    },\n"
"    \"commondefs\": {\n"
"        \"replacement_strings\": {\n"
"            \"instructions_prefix\": \"\"\"\n"
"You are part of a ")
HOCON_HEADER_REMAINDER = (" of assistants.\n"
"Only answer inquiries that are directly within your area of expertise.\n"
"Do not try to help for other matters.\n"
"Do not mention what you can NOT do. Only mention what you can do.\n"
"            \"\"\",\n"
"            \"aaosa_instructions\": \"\"\"\n"
"When you receive an inquiry, you will:\n"
"1. If you are clearly not the right agent for this type of inquiry, reply you're not relevant.\n"
"2. If there is a chance you're relevant, call your down-chain agents to determine if they can answer all or part of the inquiry.\n"
"   Do not assume what your down-chain agents can do. Always call them. You'll be surprised.\n"
"3. Determine which down-chain agents have the strongest claims to the inquiry.\n"
"   3.1 If the inquiry is ambiguous, for example if more than one agent can fulfill the inquiry, then always ask for clarification.\n"
"   3.2 Otherwise, call the relevant down-chain agents and:\n"
"       - ask them for follow-up information if needed,\n"
"       - or ask them to fulfill their part of the inquiry.\n"
"4. Once all relevant down-chain agents have responded, either follow up with them to provide requirements or,\n"
"   if all requirements have been fulfilled, compile their responses and return the final response.\n"
"You may, in turn, be called by other agents in the system and have to act as a down-chain agent to them.\n"
"            \"\"\"\n"
"        },\n"
"        \"replacement_values\": {\n"
"            \"aaosa_call\": {\n"
"                \"description\": \"Depending on the mode, returns a natural language string in response.\",\n"
"                \"parameters\": {\n"
"                    \"type\": \"object\",\n"
"                    \"properties\": {\n"
"                        \"inquiry\": {\n"
"                            \"type\": \"string\",\n"
"                            \"description\": \"The inquiry\"\n"
"                        },\n"
"                        \"mode\": {\n"
"                            \"type\": \"string\",\n"
"                            \"description\": \"\"\"\n"
"'Determine' to ask the agent if the inquiry belongs to it, in its entirety or in part.\n"
"'Fulfill' to ask the agent to fulfill the inquiry, if it can.\n"
"'Follow up' to ask the agent to respond to a follow up.\n"
"                            \"\"\"\n"
"                        },\n"
"                    },\n"
"                    \"required\": [\n"
"                        \"inquiry\",\n"
"                        \"mode\"\n"
"                    ]\n"
"                }\n"
"            },\n"
"            \"aaosa_command\": \"\"\"\n"
"If mode is 'Determine', return a json block with the following fields:\n"
"{\n"
"    \"Name\": <your name>,\n"
"    \"Inquiry\": <the inquiry>,\n"
"    \"Mode\": <Determine | Fulfill>,\n"
"    \"Relevant\": <Yes | No>,\n"
"    \"Strength\": <number between 1 and 10 representing how certain you are in your claim>,\n"
"    \"Claim:\" <All | Partial>,\n"
"    \"Requirements\" <None | list of requirements>\n"
"}\n"
"If mode is 'Fulfill' or \"Follow up\", respond to the inquiry and return a json block with the following fields:\n"
"{\n"
"    \"Name\": <your name>,\n"
"    \"Inquiry\": <the inquiry>,\n"
"    \"Mode\": Fulfill,\n"
"    \"Response\" <your response>\n"
"}\n"
"            \"\"\"\n"
"        },\n"
"    }\n"
"\"tools\": [\n")
TOP_AGENT_TEMPLATE = ("        {\n"
"            \"name\": \"%s\",\n"
"            \"function\": {\n"
"                \"description\": \"\"\"\n"
"An assistant that answer inquiries from the user.\n"
"                \"\"\"\n"
"            },\n"
"            \"instructions\": \"\"\"\n"
"{instructions_prefix}\n"
"%s\n"
"{aaosa_instructions}\n"
"            \"\"\",\n"
"            \"tools\": [%s]\n"
"        },\n")
REGULAR_AGENT_TEMPLATE = ("        {\n"
"            \"name\": \"%s\",\n"
"            \"function\": \"aaosa_call\",\n"
"            \"instructions\": \"\"\"\n"
"{instructions_prefix}\n"
"%s\n"
"{aaosa_instructions}\n"
"            \"\"\",\n"
"            \"command\": \"aaosa_command\",\n"
"            \"tools\": [%s]\n"
"        },\n")
LEAF_NODE_AGENT_TEMPLATE = ("        {\n"
"            \"name\": \"%s\",\n"
"            \"function\": \"aaosa_call\",\n"
"            \"instructions\": \"\"\"\n"
"{instructions_prefix}\n"
"%s\n"
"            \"\"\",\n"
"            \"command\": \"aaosa_command\",\n"
"        },\n")


async def modify_registry(the_agent_network_hocon_str, the_agent_network_name):
    # Write the agent network file
    file_path = OUTPUT_PATH + the_agent_network_name + ".hocon"
    async with aiofiles.open(file_path, 'w') as file:
        await file.write(the_agent_network_hocon_str)
    # Update the manifest.hocon file
    manifest_path = OUTPUT_PATH + "manifest.hocon"
    manifest_entry = f'    "{the_agent_network_name}.hocon": true,'
    # Read the current manifest content
    async with aiofiles.open(manifest_path, 'r') as file:
        manifest_content = await file.read()
    # Find the position to insert the new entry (before the closing brace)
    insert_position = manifest_content.rfind('}')
    if insert_position != -1:
        # Check if the entry already exists to avoid duplicates
        if f'"{the_agent_network_name}.hocon"' not in manifest_content:
            # Insert the new entry
            updated_content = (manifest_content[:insert_position] + "\n" +
                               manifest_entry + manifest_content[insert_position:])

            # Write the updated content back to the manifest file
            async with aiofiles.open(manifest_path, 'w') as file:
                await file.write(updated_content)


class GetAgentNetworkHocon(CodedTool):
    """
    CodedTool implementation which provides a way to get a full hocon of a designed agent network from the sly data
    """

    def __init__(self):
        self.agents = None

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        :param args: An argument dictionary whose keys are the parameters
                to the coded tool and whose values are the values passed for them
                by the calling agent.  This dictionary is to be treated as read-only.

                The argument dictionary expects the following keys:
                    "app_name" the name of the One Cognizant app for which the URL is needed.

        :param sly_data: A dictionary whose keys are defined by the agent hierarchy,
                but whose values are meant to be kept out of the chat stream.

                This dictionary is largely to be treated as read-only.
                It is possible to add key/value pairs to this dict that do not
                yet exist as a bulletin board, as long as the responsibility
                for which coded_tool publishes new entries is well understood
                by the agent chain implementation and the coded_tool implementation
                adding the data is not invoke()-ed more than once.

                Keys expected for this implementation are:
                    None

        :return:
            In case of successful execution:
                The full agent network hocon as a string.
            otherwise:
                a text string an error message in the format:
                "Error: <error message>"
        """
        self.agents = sly_data.get(AGENT_NETWORK_NAME, None)
        if not self.agents:
            return "Error: No network in sly data!"

        the_agent_network_name: str = args.get("agent_network_name", "")
        if the_agent_network_name == "":
            return "Error: No agent_name provided."

        logger = logging.getLogger(self.__class__.__name__)
        logger.info(">>>>>>>>>>>>>>>>>>>GetAgentNetworkHocon>>>>>>>>>>>>>>>>>>")
        logger.info("Agent Network Name: %s", str(the_agent_network_name))
        the_agent_network_hocon_str = self.get_agent_network_hocon(the_agent_network_name)
        logger.info("The resulting agent network: \n %s", str(the_agent_network_hocon_str))
        if WRITE_TO_FILE:
            await modify_registry(the_agent_network_hocon_str, the_agent_network_name)
        logger.info(">>>>>>>>>>>>>>>>>>>DONE !!!>>>>>>>>>>>>>>>>>>")
        return the_agent_network_hocon_str

    def get_agent_network_hocon(self, agent_network_name):
        """
        Returns a full agent network hocon.
        """
        agent_network_hocon = HOCON_HEADER_START + agent_network_name + HOCON_HEADER_REMAINDER
        for i, (agent_name, agent) in enumerate(self.agents.items()):
            tools = ""
            if agent["down_chains"]:
                for j, down_chain in enumerate(agent["down_chains"]):
                    tools = tools + "\"" + down_chain + "\""
                    if j < len(agent["down_chains"]) - 1:
                        tools = tools + ","
            if i == 0: # top agent
                an_agent = TOP_AGENT_TEMPLATE % (agent_name, agent["instructions"], tools)
            elif agent["down_chains"]:
                an_agent = REGULAR_AGENT_TEMPLATE % (agent_name, agent["instructions"], tools)
            else: # leaf node agent
                an_agent = LEAF_NODE_AGENT_TEMPLATE % (agent_name, agent["instructions"])
            agent_network_hocon = agent_network_hocon + an_agent
        agent_network_hocon = agent_network_hocon + "]\n}\n"
        return agent_network_hocon
