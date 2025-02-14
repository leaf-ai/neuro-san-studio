# Demos for the neuro-san library
This repository contains a collection of demos for the neuro-san library.
They should help developers to get started with the library and to understand how to create their own agents.

## Installation

Clone the repo:
```bash
git clone https://github.com/leaf-ai/neuro-san-demos
```

Go to dir:
```bash
cd neuro-san-demos
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

## Run

### Start the server

Export the following environment variables:
```bash
# Point the server to the manifest file containing the agent network configurations
export AGENT_MANIFEST_FILE="./registries/manifest.hocon"
# Point the server to the directory containing the agent Python tools
export AGENT_TOOL_PATH="./coded_tools"
```

and start the server:

```bash
python -m neuro_san.service.agent_main_loop --port 30011
```

### Start the client

#### Option 1: Command line interface

From another terminal, navigate to the repo's folder and activate the virtual environment:
```bash
source venv/bin/activate && export PYTHONPATH=`pwd`
```

Then start the client:

```bash
python -m neuro_san.client.agent_cli --connection service --agent hello_world
```

### Query the client
When prompted, ask a question to the agent network. For example:
```
I am travelling to a new planet and wish to send greetings to the orb.
```
And it should return something like:

    Hello, world.

... but you are dealing with LLMs. Your results will vary!

Type `quit` to exit the client.

#### Option 2: Web client

You can also start a web client instead to interact with the agent network:

```bash
python -m neuro_san_web_client.app
```

Then navigate to http://127.0.0.1:5001 in your browser.

You can now type your message in the chat box and press 'Send' to interact with the agent network.

## Tutorial

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
