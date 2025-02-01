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

**IMPORTANT**: By default the service relies on OpenAI's `gpt-4o` model. 
Set the OpenAI API key, and add it to your shell configuration so it's available in future sessions:  
**NOTE**: Replace `XXX` with your actual OpenAI API key.  
**NOTE**: This is OS dependent. This command is for MacOS and Linux.
```bash
export OPENAI_API_KEY="XXX" && echo 'export OPENAI_API_KEY="XXX"' >> ~/.zshrc
```
Other models are supported too but will require proper setup.

## Run

Start the server and the client in one single command:
```bash
python -m run
```
The client and server logs will show on the screen,
and will also be saved to `logs/server.log` and `logs/client.log` respectively.

As a default, on a web browser you can now navigate to http://127.0.0.1:5003/ to start using the application.

To see the various config options for this app, on terminal
```bash
python -m run -h
```
or
```bash
python -m run --help
```

## (Optional) How to run in demo-mode

This is really meant to experience some of the default multi-agent networks that are available in the neuro-san library.
To use it, start the server and the client in one single command:
```bash
python -m run --demo-mode
```

## (Optional) Details for manual run


Export the following environment variables:
```bash
# Point the server to the manifest file containing the agent network configurations
export AGENT_MANIFEST_FILE="./registries/manifest.hocon"
# Point the server to the directory containing the agent Python tools
export AGENT_TOOL_PATH="./coded_tools"
```

Configure the Absence Manager API.
Note: if you do not have access to the Absence Manager API, you can skip this step.
The coded tools will return a mock response instead of calling the API.
```bash
# Absence Manager configuration
export ABSENCE_MANAGER_CLIENT_ID="XXX"
export ABSENCE_MANAGER_CLIENT_SECRET="XXX"
export ASSOCIATE_ID="XXX"
```

### Start the server

```bash
python -m neuro_san.service.agent_main_loop --port 30011
```

### Start the client

#### Option 1: Web client

```bash
python -m neuro_san_web_client.app
```

#### Option 2: Command line interface

```bash
python -m neuro_san.client.agent_cli --connection service --agent onec_assistant
```

### Query the client
Once the client is started, you can ask it questions. For example:
```
I am travelling to a new planet and wish to send greetings to the orb.
```
And it should return something like:

    Hello, world.

... but you are dealing with LLMs. Your results will vary!
