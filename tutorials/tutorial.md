# Neuro AI Multi-Agent Accelerator – Getting Started

Welcome to the **Neuro AI Multi-Agent Accelerator** tutorial. In this guide, we will walk you through the process of setting up a **Data-Driven Multi-Agent Network** using the `neuro-san` library, managing it via a Flask-based web UI, and customizing how Large Language Model (LLM) based Agents coordinate with each other to solve tasks. We will also explore switching LLM providers (like Ollama and Anthropic), adding custom-coded Tools, and running everything from a single command.

---

## Table of Contents

1. [Introduction](#introduction)  
2. [Project Structure](#project-structure)  
3. [The Wheel Files](#the-wheel-files)  
4. [Setting Up a Working Python Environment](#setting-up-a-working-python-environment)  
5. [What is an LLM-based Agent?](#what-is-an-llm-based-agent)  
   - [Agents for Autonomous Decision Making](#agents-for-autonomous-decision-making)  
   - [Function Calling with Agents](#function-calling-with-agents)  
   - [Data-Driven Agent Network](#data-driven-agent-network)  
6. [Creating an Agent Network from Scratch](#creating-an-agent-network-from-scratch)  
   - [Single Agent Network Example](#single-agent-network-example)  
   - [Multi-Agent Network Example](#multi-agent-network-example)  
   - [LLM Config](#llm-config)
7. [How to Switch LLMs Using the HOCON File](#how-to-switch-llms-using-the-hocon-file)  
   - [Setting Up Ollama Locally](#setting-up-ollama-locally)  
   - [Adding Endpoint URL for Any Cloud-Hosted LLM](#adding-endpoint-url-for-any-cloud-hosted-llm)  
8. [Coded Tools](#coded-tools)  
   - [What Are Coded Tools?](#what-are-coded-tools)  
   - [Adding a Coded Tool](#adding-a-coded-tool)  
   - [Simple Calculator Tool](#simple-calculator-tool)  
   - [Complex Calculator Tool](#complex-calculator-tool)  
9. [How to Access the Logs](#how-to-access-the-logs)  
10. [How to Stop the Server](#how-to-stop-the-server)  
11. [Key Positive Aspects of Neuro AI Multi-Agent Accelerator](#key-positive-aspects-of-neuro-ai-multi-agent-accelerator)  
12. [End Notes](#end-notes)  

---

## 1. Introduction

**Neuro-San** is a multi-agent orchestration library that enables you to build **data-driven agent networks**. These networks of agents can use **LLMs** (Large Language Models) and **coded tools** to coordinate and solve complex tasks autonomously. 

The library comes with a **Flask Web Client** (`neuro_san_web_client`) so that users can interact with these multi-agent networks through a web-based UI. This entire setup is easily configurable using **HOCON** (`.hocon`) files.

**Note**: This tutorial is written with the help of the agent network example [advanced_calculator.hocon](https://github.com/leaf-ai/neuro-san-demos/blob/registries/advanced_calculator.hocon).

---

## 2. Project Structure

Below is a simplified view of the reference project structure. You can adapt it to your needs.

```bash
.
├── README.md
├── coded_tools
│   └── advanced_calculator
│       └── calculator_tool.py
├── logs
│   ├── client.log
│   └── server.log
├── registries
│   ├── advanced_calculator.hocon
│   └── manifest.hocon
├── requirements.txt
├── run.py
└── wheels_private
    ├── leaf_common-1.2.18-py3-none-any.whl
    ├── leaf_server_common-0.1.15-py3-none-any.whl
    ├── neuro_san-0.4.6-py3-none-any.whl
    └── neuro_san_web_client-0.1.3-py3-none-any.whl
```

### Key directories and files:

- `coded_tools/`: Contains custom-coded tool classes (e.g., `calculator_tool.py`).
- `registries/`: Holds `.hocon` files that define multi-agent networks and their configurations.
- `logs/`: Where client and server logs are written.
- `wheels_private/`: Contains wheel files for installing the required packages. 
    - Note that the wheel file versions might have changed since the time of writing this tutorial.
- `run.py`: A starter script to run the server and the web client.

Please find the detailed instructions to run an agent network along with a web client here:
- https://github.com/leaf-ai/neuro-san-demos/blob/main/README.md

---

## 3. The Wheel Files
To get your environment up and running, you will need to install several wheel files:

1. `neuro_san`:
- This is the core library for multi-agent orchestration.
2. `neuro_san_web_client-0.1.3-py3-none-any.whl`:
- This package provides a Flask web application UI that interacts with the `neuro-san` backend.
- Internally, it uses the pyvis library (specifically `vis-9.1.2`) for rendering network graphs on the web page.
3. `leaf_common` and `leaf_server_common`:
- These packages manage server-side setups for `neuro-san`. Users typically do not need to worry about them for normal usage.
You can find these wheel files in the `wheels_private/` directory.

---

## 4. Setting Up a Working Python Environment
Follow these steps to set up and activate your Python virtual environment:

```bash
# 1) Clone your project repository (if applicable)
git clone https://github.com/leaf-ai/neuro-san-airline
cd neuro-san-airline

# 2) Create a dedicated Python virtual environment
python -m venv venv

# 3) Activate it
# For Windows
.\venv\Scripts\activate && set PYTHONPATH=%cd%
# For Mac/Linux
source venv/bin/activate && export PYTHONPATH=`pwd`

# 4) Install the required Python packages
pip install -r requirements.txt

# 5) Now install the wheel files from wheels_private/
# Make sure the version numbers match your environment
pip install wheels_private/neuro_san-0.4.5-py3-none-any.whl
pip install wheels_private/neuro_san_web_client-0.1.3-py3-none-any.whl
pip install wheels_private/leaf_common-1.2.18-py3-none-any.whl
pip install wheels_private/leaf_server_common-0.1.15-py3-none-any.whl
```

Please find the detailed instructions to run an agent network along with a web client here:
- https://github.com/leaf-ai/neuro-san-demos/blob/main/README.md

Note: You may need to adapt the filenames if versions differ.


---

## 5. What is an LLM-based Agent?
An **LLM-based Agent** is a component in your agent network that uses a **Large Language Model** to process instructions and make decisions. By embedding the agent’s logic in a data-driven configuration (the `.hocon` file), you can define:

- **Agent roles and responsibilities**
- **Tools** (or other agents) it can call
- **Function schema** that the agent can handle

### Agents for Autonomous Decision Making
These agents can coordinate tasks among themselves. A top-level (or front-man) agent can receive a user’s query, figure out which sub-agents (or tools) are best suited to answer it, and orchestrate the communication necessary to generate a response.

### Function Calling with Agents
In Neuro AI Multi-Agent Accelerator, Agents may declare a function with defined parameters. Other agents can call this function by providing the required parameters. This allows complex tasks to be broken into sub-tasks, each handled by specialized agents or tools.

**Note**: Refer to this [OpenAI blog](https://community.openai.com/t/function-calling-parameter-types/268564/7) and [OpenAI Cookbook](https://cookbook.openai.com/examples/function_calling_with_an_openapi_spec) for more information.

### Data-Driven Agent Network
A Data-Driven Agent Network is composed of multiple agents defined in a `.hocon` file. This file describes:

- **LLM configuration**: which model to use, how to connect to it, whether it’s verbose, etc.
- **Agent definitions**: including instructions, roles, domain knowledge, and which tools/agents they can call.
- **Tools**: references to Coded Tools that contain Python functions or classes.

---

## 6. Creating an Agent Network from Scratch

### Single Agent Network Example
Let’s start simple. We’ll build a minimal `.hocon` file containing only one agent – the Math Geek. This will show how to run a single-agent network that can handle basic math operations (though it won’t actually do the math by itself unless you also link to or embed the coded tool).

#### Step 1: Create a file `registries/single_agent_example.hocon`:

```hocon
{
    "llm_config": {
        "model_name": "llama3.1",
        "verbose": true
    },
    "commondefs": {
        "replacement_strings": {
            "instructions_prefix": """
                You are responsible for a segment of a problem.
                Only answer inquiries that are directly within your domain.
            """,
            "aaosa_instructions": """
                When you receive an inquiry:
                0. If you are clearly not the right agent...
                1. Always call your tools...
                2. ...
            """
        },
        "replacement_values": {}
    },
    "tools": [
        {
            "name": "Math Geek",
            "function": {
                "description": "I can help you to do quick calculations."
            },
            "instructions": """
                {instructions_prefix}
                Your name is `Math Geek`.
                You are the top-level agent for mathematics.
                {aaosa_instructions}
                - Only handle calculation related inquiries.
            """,
            "tools": []
        }
    ]
}
```

#### Step 2: Run the server with this `.hocon` file. You can do so by:

```bash
# Make sure your venv is active
export AGENT_MANIFEST_FILE="./registries/manifest.hocon"
export AGENT_TOOL_PATH="./coded_tools"
python -m run
```

Since this agent has no further sub-agents or coded tools, it will simply respond to queries but won’t be able to do actual calculations. It is functionally incomplete, but demonstrates a minimal single-agent network.

### Multi-Agent Network Example
Let’s take a look at a more robust multi-agent network file: `advanced_calculator.hocon`. Below is a simplified variant with two agents: Math Geek and problem_formulator, plus a coded tool named `CalculatorTool`.

```hocon
{
    "llm_config": {
        "model_name": "llama3.1",
        "verbose": true
    },
    "commondefs": {
        "replacement_strings": {
            "instructions_prefix": """
                You are responsible for a segment of a problem...
            """,
            "aaosa_instructions": """
                When you receive an inquiry:
                0. If you are clearly not the right agent...
                1. Always call your tools...
                ...
            """
        },
        "replacement_values": {}
    },
    "tools": [
        {
            "name": "Math Geek",
            "function": {
                "description": "I can help you to do quick calculations."
            },
            "instructions": """
                {instructions_prefix}
                Your name is `Math Geek`.
                You are the top-level agent for the mathematics system.
                {aaosa_instructions}
            """,
            "tools": ["problem_formulator"]
        },
        {
            "name": "problem_formulator",
            "function": {
                "description": "Convert a math problem into a sequence of known operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "inquiry": { "type": "string" }
                    },
                    "required": ["inquiry"]
                }
            },
            "instructions": """
                Your name is `Problem Formulator`.
                You will be handed a math problem and parse it into a known sequence of operations...
            """,
            "command": """
                - Identify operations and operands
                - Call the CalculatorTool
            """,
            "tools": ["CalculatorTool"]
        },
        {
            "name": "CalculatorTool",
            "function": {
                "description": "Solve the math operations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": { "type": "string" },
                        "operands": {
                            "type": "array",
                            "items": { "type": "float" }
                        }
                    },
                    "required": ["operation", "operands"]
                }
            },
            "class": "calculator_tool.CalculatorCodedTool",
            "command": "Perform the calculation."
        }
    ]
}
```

A few points to note about multi-agent networks: 
- The snippet above is intentionally simplified. The actual `advanced_calculator.hocon` is more verbose and includes more detail (you can see the full example provided in this tutorial’s introduction).
- The relationship between different agents can be defined in the hocon file itself. The down-chain agents can be defined in the `tools` section of each agent definition in a parent-child style. For example the `Math Geek` agent has access to the `problem_formulator` agent and the `problem_formulator` agent has access to the calculator agent via '`"tools": ["CalculatorTool"]`
- It is possible to have the same down-chain agent available for several other agents at the same time.
- Defining an agent network is highly flexible. We can define all sort of networks: Single Agent Network, Hierarchical Agent Network, DAG oriented Network, Single Agent with Coded Tools, Multiple Agents with Multiple Coded Tools.


### LLM Config

LLM configurations is a way to tell the agents whcih LLM (Large Language Model) to use in order to process a query sent to it.

- LLM config is defined on top of the hocon file which implies that the same config is accessible to all the agents in the network by default.
- It is possible to keep the default config and have separate config for each agent in the network. This means an agent that does not have a defined config always uses the default llm_config defined on top of the hocon file.
- It is possible to have different LLMs for each of our agents for example, we can use `gpt-4o` for the front-man agent `Math Geek` and `llama3.1` for the `problem_formulator`. Here is the hocon example to show that:
```hocon
{
    "llm_config": {
        "model_name": "gpt4-o",
        "verbose": true
    },
    "commondefs": {
        "replacement_strings": {
            "instructions_prefix": """
                You are responsible for a segment of a problem...
            """,
            "aaosa_instructions": """
                When you receive an inquiry:
                0. If you are clearly not the right agent...
                1. Always call your tools...
                ...
            """
        },
        "replacement_values": {}
    },
    "tools": [
        {
            "name": "Math Geek",
            "function": {
                "description": "I can help you to do quick calculations."
            },
            "instructions": """
                {instructions_prefix}
                Your name is `Math Geek`.
                You are the top-level agent for the mathematics system.
                {aaosa_instructions}
            """,
            "tools": ["problem_formulator"]
        },
        {
            "name": "problem_formulator",
            "llm_config": {
                "model_name": "llama3.1",
                "verbose": true
            },
            "function": {
                "description": "Convert a math problem into a sequence of known operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "inquiry": { "type": "string" }
                    },
                    "required": ["inquiry"]
                }
            },
            "instructions": """
                Your name is `Problem Formulator`.
                You will be handed a math problem and parse it into a known sequence of operations...
            """,
            "command": """
                - Identify operations and operands
                - Call the CalculatorTool
            """
        },
    ]
}
```

#### Notes on `llm_config`:
- The llm_config uses `model_name` as a parameter. We can use these models with openai, azure, ollama, anthropic and nvidia as a provider.
- Here is a list of supported LLMs that can be used as `model_name` as of 26-Feb-2025:
    - OpenAI: ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4-turbo-preview', 'gpt-4-1106-preview', 'gpt-4-vision-preview', 'gpt-4', 'gpt-4-32k']
    - AzureChatOpenAI: ['azure-gpt-3.5-turbo', 'azure-gpt-4']
    - Anthropic: ['claude-3-haiku', 'claude-3-sonnet', 'claude-3-opus', 'claude-2.1', 'claude-2.0', 'claude-instant-1.2']
    - Ollama: ['llama2', 'llama3', 'llama3.1', 'llama3:70b', 'llava', 'mistral', 'mistral-nemo', 'mixtral', 'qwen2.5:14b', 'deepseek-r1:14b']
    - ChatNvidia: ['nvidia-llama-3.1-405b-instruct', 'nvidia-llama-3.3-70b-instruct', 'nvidia-deepseek-r1']
- Note that not all of these LLMs support function-calling, it is advisable to read the documentation before using any of the LLMs.
- Each of these LLMs have several config params. Some of the common config parameters are: `model_name`, `temperature`, `verbose`, `max_tokens`.
- For the available configuration parameters of the above chat models, please refer to [Langchain Chat Models](https://python.langchain.com/docs/concepts/chat_models/) and their [respective documentation](https://python.langchain.com/docs/integrations/chat/)



#### Running the multi-agent network:

```bash
export AGENT_MANIFEST_FILE="./registries/manifest.hocon"
export AGENT_TOOL_PATH="./coded_tools"
python -m run
```

Now, the top-level **Math Geek** agent will parse user queries, pass them to **problem_formulator**, which in turn calls the **CalculatorTool**. The final answer is then relayed back to the user.

--- 

## 7. How to Switch LLMs Using the HOCON File
Because **Neuro AI Multi-Agent Accelerator** uses `neuro-san`, it is LLM-agnostic, you can switch to different model providers by changing the `llm_config` in your `.hocon` file.

```hocon
"llm_config": {
    "model_name": "llama3.1",
    "verbose": true
    # Additional fields like endpoint_url for local or remote inference servers
}
```

### Setting Up Ollama Locally
Ollama is a local LLM runner for Mac (and also works on Windows via Docker or other means).

1. Download and Install Ollama (follow official instructions from [ollama.com](https://ollama.com/)).
2. Start an Ollama instance listening to a local port (e.g., 11434).

On macOS, that might look like:

```bash
ollama serve --port 11434
```
On Windows, you might use Docker:

```bash
docker run -p 11434:11434 ghcr.io/jmorganca/ollama:latest
```

### Adding Endpoint URL for Any Cloud-Hosted LLM
To direct the calls to your local Ollama, or a cloud-hosted model endpoint, add:

```hocon
"llm_config": {
    "model_name": "llama3.1",
    "verbose": true,
    "base_url": "http://localhost:11434/api/chat" # replace the url in base_url with your actual url
}
```

If you use other providers (e.g., Anthropic, OpenAI, Azure, etc.), simply adjust these values to match the respective endpoints and model names. Be sure to set any necessary environment variables (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `ANTHROPIC_API_URL`, `AZURE_OPENAI_ENDPOINT`, etc.).

**Note**: Please check [langchain api reference](https://python.langchain.com/api_reference/reference.html) for supported parameters.

---

## 8. Coded Tools

### What Are Coded Tools?
Coded Tools are Python classes that implement the neuro_san.interfaces.coded_tool.CodedTool interface. Agents invoke these tools to perform specialized tasks (like calculations, database lookups, API calls, etc.) without relying on the LLM to do everything.

### Adding a Coded Tool
By convention, you create a subdirectory under coded_tools/ matching the HOCON filename. For example, for advanced_calculator.hocon, you can place custom tools in:

```bash
coded_tools/advanced_calculator/
```
Then, reference them in the HOCON file via the `"class"` field, e.g.:

```hocon
"class": "calculator_tool.CalculatorCodedTool"
```
Here, `calculator_tool.py` is placed in the `./coded_tools/advanced_calculator/` directory.

### Simple Calculator Tool
Below is a simplified version of `calculator_tool.py`, supporting only `add`, `subtract`, `multiply`, and `divide`. (We omit error checks for brevity.)

```python
from neuro_san.interfaces.coded_tool import CodedTool

class CalculatorCodedTool(CodedTool):
    def __init__(self):
        self.MATH_FUNCTIONS = {
            "add": lambda a, b: a + b,
            "subtract": lambda a, b: a - b,
            "multiply": lambda a, b: a * b,
            "divide": lambda a, b: a / b if b != 0 else "Error: Division by zero"
        }

    def invoke(self, args, sly_data):
        operation = args.get("operation")
        operands = args.get("operands", [])
        func = self.MATH_FUNCTIONS.get(operation)
        if not func:
            return {"error": f"Unsupported operation: {operation}"}
        if len(operands) < 2:
            return {"error": "Not enough operands"}
        result = func(operands[0], operands[1])
        return {"operation": operation, "result": result}
```

### Complex Calculator Tool
A more complete version of the calculator (like the one in this tutorial’s introduction) uses a large dictionary of math functions, each associated with a Python function. It can handle multiple steps and advanced operations like `factorial`, `sin`, `log`, etc. Refer to the final code snippet in `calculator_tool.py` above.

---

## 9. How to Access the Logs
By default, when you run:

```bash
python -m run
```

- The server logs go to logs/server.log.
- The client (web UI) logs go to logs/client.log.

Additionally, you will see logs on your terminal. Checking these files is useful for:
- Debugging agent interactions
- Viewing any errors or exceptions
- Auditing how the queries are being orchestrated

---

### 10. How to Stop the Server
When you are running the server in the foreground (via `python -m run`), simply press:

- `CTRL + C` on Windows/Mac/Linux terminals
- This will terminate both the Flask web client and the `neuro_san` server gracefully.

If you launched them separately, you would stop each process individually (again by `CTRL + C` or sending a kill signal).

---

## 11. Key Aspects of Neuro AI Multi-Agent Accelerator
- **Flexibility of Use**: Define any agent network structure using `.hocon` files, easily adjustable for different use cases and tasks.
- **LLM Agnostic**: Swap between OpenAI, Anthropic, Ollama, Azure, or your own custom model endpoints with minimal configuration changes.
- **Cloud Agnostic**: Host your solutions on any cloud or on-prem python environment.
- **Tool/Function Calling**: Agents can systematically call coded tools or other sub-agents, enabling powerful, modular, and autonomous decision workflows.
- **Hierarchical Agent Networks**: You can create nested agent networks to handle complex tasks in a structured manner.

---

## 12. End Notes
You’ve now seen how to:

- Set up a Python environment and install the necessary wheels.
- Create single-agent and multi-agent networks in `.hocon` files.
- Switch LLM providers (e.g., Ollama, Anthropic, OpenAI).
- Add coded tools to expand agent capabilities.
- Run the server and Flask client.
- Check logs and stop the server.

Feel free to be creative, explore adding more complex agents, linking them in various ways, or building advanced coded tools. We hope you find Neuro AI Multi-Agent Accelerator intuitive, powerful, and adaptable to your needs.

---
