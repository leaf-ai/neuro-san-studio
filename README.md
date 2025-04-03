# Demos for the neuro-san library
This repository contains a collection of demos for the neuro-san library.
They should help developers to get started with the library and to understand how to create their own agents.

- [Demos for the neuro-san library](#demos-for-the-neuro-san-library)
  - [Installation](#installation)
  - [Run](#run)
    - [Option 1: Command Line Interface](#option-1-command-line-interface)
    - [Option 2: Using a basic Web Client interface](#option-2-using-a-basic-web-client-interface)
    - [Option 3: Using `nsflow` as a developer-oriented web client](#option-3-using-nsflow-as-a-developer-oriented-web-client)
  - [Tutorial](#tutorial)
  - [Quick-Start](#quick-start)
    - [Hello World](#hello-world)
    - [Hello World - custom LLMs](#hello-world---custom-llms)
    - [Hocon files](#hocon-files)
      - [Manifest](#manifest)
      - [Agent network](#agent-network)
        - [Agent specifications](#agent-specifications)
        - [Tool specifications](#tool-specifications)
        - [LLM specifications](#llm-specifications)
    - [Multi-agent networks](#multi-agent-networks)
    - [Coded tools](#coded-tools)
      - [Simple tool](#simple-tool)
      - [API calling tool](#api-calling-tool)
      - [Sly data](#sly-data)
    - [Toolbox](#toolbox)
    - [Logging and debugging](#logging-and-debugging)
    - [Advanced](#advanced)
      - [Sub networks](#sub-networks)
      - [AAOSA](#aaosa)
      - [Connect with other agent frameworks](#connect-with-other-agent-frameworks)

---

## Installation

Clone the repo:
```bash
git clone https://github.com/leaf-ai/neuro-san-demos
```

Go to dir:
```bash
cd neuro-san-demos
```
Ensure you have a supported version of python (3.12 at this time)
```bash
python --version
```

Create a dedicated Python virtual environment:
```bash
python -m venv venv
```
Source it:
```bash
source venv/bin/activate && export PYTHONPATH=`pwd`
```

Install the requirements:
```bash
pip install -r requirements.txt
```

**IMPORTANT**: By default the server relies on OpenAI's `gpt-4o` model. 
Set the OpenAI API key, and add it to your shell configuration so it's available in future sessions:  
**NOTE**: Replace `XXX` with your actual OpenAI API key.  
**NOTE**: This is OS dependent. This command is for MacOS and Linux.
```bash
export OPENAI_API_KEY="XXX" && echo 'export OPENAI_API_KEY="XXX"' >> ~/.zshrc
```
Other models are supported too but will require proper setup.

---

## Run

There are multiple ways in which we can now use the neuro-san server with a client

### Option 1: Command Line Interface

- Export the following environment variables:
```bash
# Point the server to the manifest file containing the agent network configurations
export AGENT_MANIFEST_FILE="./registries/manifest.hocon"
# Point the server to the directory containing the agent Python tools
export AGENT_TOOL_PATH="./coded_tools"
```

- Start the server:
```bash
python -m neuro_san.service.agent_main_loop --port 30011
```

- Start the client:
From another terminal window, navigate to the repo's folder and activate the virtual environment:
```bash
source venv/bin/activate && export PYTHONPATH=`pwd`
```

Then start the client:
```bash
python -m neuro_san.client.agent_cli --connection service --agent hello_world
```

- Query the client
When prompted, ask a question to the `hello_world` agent network. For example:
```
I am travelling to a new planet and wish to send greetings to the orb.
```
And it should return something like:

    Hello, world.

... but you are dealing with LLMs. Your results will vary!

Type `quit` to exit the client.

---

### Option 2: Using a basic Web Client interface

- Start the server and the client in one single command:
```bash
python -m run
```

The client and server logs will show on the screen,
and will also be saved to `logs/server.log` and `logs/client.log` respectively.
As a default, on a web browser you can now navigate to http://127.0.0.1:5003/ to start using the application.

- To see the various config options for this app, on terminal
```bash
python -m run -h
```
or
```bash
python -m run --help
```

- (Optional) How to run in demo-mode

This is really meant to experience some of the default multi-agent networks that are available in the neuro-san library.
To use it, start the server and the client in one single command:
```bash
python -m run --demo-mode
```

---

### Option 3: Using `nsflow` as a developer-oriented web client
If you want to use neuro-san with a FastAPI-based developer-oriented client, follow these steps:

- Start the Backend & Frontend, from project root
```bash
python -m nsflow.run
```

By default:
- Frontend will be available at: `http://127.0.0.1:4173`
- OpenAPI specs will be available at: `http://127.0.0.1:4173/docs`

To see the various config options for this app, on terminal
```bash
python -m nsflow.run -h
```
or
```bash
python -m nsflow.run --help
```

---

## Tutorial
For a detailed tutorial, refer to a detailed [tutorial.md](tutorials/tutorial.md)

---

## Quick-Start

### Hello World

The `hello_world` agent network is a simple agent network that returns a greeting when prompted.

The steps to start the server and the client are described above.
When starting, the first thing the server will do is load the agent network configurations
from the "manifest" file. The manifest file is specified by the `AGENT_MANIFEST_FILE` environment variable:
```
AGENT_MANIFEST_FILE="./registries/manifest.hocon"
```
Open [./registries/manifest.hocon](./registries/manifest.hocon) and look at its contents. It should look something like this:
```hocon
{
    # Currently we list each hocon file we want to serve as a key with a boolean value.
    # Eventually we might have a dictionary value with server specifications for each.
    "hello_world.hocon": true,
    # ...
}
```
This tells the server to load the `hello_world.hocon` file from the same `/registries` folder.

Open [./registries/hello_world.hocon](./registries/hello_world.hocon) and have a look at it.
For now just note that it contains a "Front Man",
called "announcer", which is the entry point to the agent network.
The "announcer" tool, also known as an "agent", has 1 tool at its disposal (another agent), called "synonymizer".
Read the instructions of these 2 agents to see what they do.
Feel free to modify the instructions to see how the agent network behaves.

We'll come back to the structure of .hocon files later.

### Hello World - custom LLMs

TODO

### Hocon files

#### Manifest

A manifest file is a list of agent network configurations that the server will load.

It's simple dictionary where the keys are the names of the agent network configuration files
and the values are booleans. For instance:
```hocon
{
    "agent_network_A.hocon": true,
    "agetn_network_B.hocon": false,
    "agent_network_C.hocon": true,
}
```
In this example the server will load agent networks A and C but not B.

When you start the server, you can see which agent networks have been loaded by looking at the logs:
```
> python -m neuro_san.service.agent_main_loop --port 30011

tool_registries found: ['agent_network_A', 'agent_network_C']
```

#### Agent network

##### Agent specifications

| **Field**    | **Description**                                                                                                                              |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| agent_name   | text handle for other agent specs and hosting system to refer to                                                                             |
| function     | Open AI function spec (standard) that formally describes the various inputs that the agent expects                                           |
| instructions | text that sets up the agent in detail for its task                                                                                           |
| command      | text that sets the agent in motion after it receives all its inputs                                                                          |
| tools        | optional list of references to other agents that this agent is allowed to call in the course of working through their input and instructions |
| llm_config   | optional agent-specification for different LLMs for different purposes such as specialization, costs, etc.                                   |

##### Tool specifications

| **Field**     | **Description**                                                                                   |
|---------------|---------------------------------------------------------------------------------------------------|
| agent_name    | text handle for other agent specs to refer to                                                     |
| function      | Open AI function spec (standard) that formally describes the various inputs that the tool expects |
| method        | Code reference to the function that is to be invoked when the tool is called.                     |

##### LLM specifications

| **Field**   | **Description**                                                                                                                       |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------|
| model_name  | name of the model to use (i.e. “gpt-4o”, “claude-3-haiku”)                                                                            |
| *_api_key   | api key value or environment variable to reference to allow access to the LLM provider if different from hosting environment default. |
| temperature | optional level of randomness 0.0-1.0 to use for LLM results                                                                           |

### Multi-agent networks

TODO

### Coded tools

#### Simple tool

#### API calling tool

#### Sly data

Specific data can be passed to CodeTools via the `sly_data` dictionary.
The `sly_data` dictionary can be passed along with the chat_request from the client side.
The LLMs won’t see the `sly_data`, but the coded tools can access it.
Useful to hold onto a user id and tokens for instance.

### Toolbox

RAG
DB connectors

### Logging and debugging

### Advanced

#### Sub networks

#### AAOSA

AAOSA stands for Adaptive Agent Oriented Software Architecture.

In this architecture, agents decide if they can answer inquiries or if they need to call other agents to help them.

Reference:
[Iterative Statistical Language Model Generation for Use with an
Agent-Oriented Natural Language Interface ](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=3004005f1e736815b367be83f2f90cc0fa9e0411)

<!-- (https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=011fb718658d611294613286c0f4b143aed40f43) -->

Look at [./registries/smart_home.onf.hocon](./registries/smart_home_onf.hocon) and in particular:
- aaosa_instructions
- aaosa_call
- aaosa_command

#### Connect with other agent frameworks

e.g. crewAI, AutoGen, LangGraph, etc.
AgentForce, ServiceNow, 
