# Agent Network HOCON File Reference

This document describes the neuro-san specifications for a single agent network .hocon file
as used for each [registry](https://github.com/leaf-ai/neuro-san/tree/main/neuro_san/registries)
in the [neuro-san](https://github.com/leaf-ai/neuro-san) and [neuro-san-demos](https://github.com/leaf-ai/neuro-san-demos)
repos.

The neuro-san system uses the HOCON (Human-Optimized Config Object Notation) file format
for its data-driven configuration elements.  Very simply put, you can think of
.hocon files as JSON files that allow comments, but there is more to the hocon
format than that which you can explore on your own.

Specifications in this document each have header changes for the depth of scope of the dictionary
header they pertain to, starting with these sections:

* [top-level](#top-level)
* [single agent specification](#single-agent-specification)

Some key descriptions refer to values that are dictionaries.
Sub-keys to those dictionaries will be described in the next-level down heading scope from their parent.

## Top-Level Agent Network Specifications

All parameters listed here have global scope (to the agent network) and are listed at the top of the file by convention.

### commondefs

A dictionary describing common definitions to be used throughout the particular agent network spec.

#### replacement_strings

A commondefs dictionary where keys are strings to be found within braces within strings
and the values of the dictionary are to replace those keys anywhere throughout the dictionary where string
values are to be found.  Example:

```
{
    "commondefs": {
        "replacement_strings": {
            "operation": "addition",
            ...
        }
    }
    ...

        "instructions": "Perform the {operation} operation."
}
```

This results in a final interpretation where the "instructions" value is "Perform the addition operation."

Multiple passes are made for string replacements, so you can have string replacement values that also have
string replacement keys in them.

#### replacement_values

A commondefs dictionary where keys are strings to be found as full-values (no braces) and the values
of the dictionary are to replace those keys anywhere throughout the dictionary with the value defined
whenever an exact match of the string value is found.
values are to be found.  Example:

```
{
    "commondefs": {
        "replacement_values": {
            "my_dict": {
                "key1": "my_value",
                "key2": 1.0
            }
            ...
        }
    }
    ...

        "function": "my_dict"
}
```

This results in a final interpretation where the "function" value is:

```
"function": {
    "key1": "my_value",
    "key2": 1.0
}
```

Value replacement only happens once, but you can have replacement_strings references within
your string values within your replacement_values and things will work out as you might expect.

### llm_config

An optional dictionary describing the default settings for agent LLMs when specifics
are not available for an given agent.  The default setting when this is not present
is to use an OpenAI gpt-4o model as the model_name for all agents.

#### model_name

The string model name to use for an agent in the network.
When this is not present, the default model is "gpt-4o" which is a decent all-purpose tool-using agent
which gets job done but doesn't cost a ton.

You can use any model listed in the [default_llm_info.hocon](https://github.com/leaf-ai/neuro-san/blob/main/neuro_san/internals/run_context/langchain/default_llm_info.hocon)
file included with the neuro-san distribution without any further modification.

While you can use any model you like for any agent within a neuro-san agent network,
you will need to use a model that has been specifically trained for "tool use" for any agent that
branches off work to any other agent/tool.  You can browse the "capabilities" section of the
default_llm_info.hocon to be sure the llm you choose can use tools.

Note that you will need your own access key set as an environment variable in order
to use LLMs from various providers.

| LLM Provider  | API Key environment variable  |
|:--------------|:------------------------------|
| Anthropic     | ANTHROPIC_API_KEY             |
| Azure OpenAI  | OPENAI_API_KEY                |
| NVidia        | NVIDIA_API_KEY                |
| Ollma         | &lt;None required&gt;         |
| OpenAI        | OPENAI_API_KEY                |

Note: _We strongly recommend to **not** set secrets as values within any source file._
These files tend to creep into source control repos, and it is __very__ bad practice
to expose secrets by checking them in.

If your favorite model, or new hotness is not listed in default_llm_info.hocon,
you can extend this list with your own hocon file by pointing the AGENT_LLM_INFO_FILE
environment variable to your extension hocon file.  For more information on adding your
own llms, see the [llm_info_hocon_reference](./llm_info_hocon_reference.md).

#### fallbacks

Fallbacks is a list of [llm_config](#llm_config) dictionaries to use in priority order.
When the an llm_config in the list fails for any reason, the next in the list is tried.

An simple example usage is given in [esp_decision_assistant.hocon](https://github.com/leaf-ai/neuro-san/blob/main/neuro_san/registries/esp_decision_assistant.hocon).

You cannot have fallbacks listed within fallbacks.

#### max_iterations

An integer controlling the max_iterations of the langchain
[AgentExecutor](https://api.python.langchain.com/en/latest/agents/langchain.agents.agent.AgentExecutor.html)
used for the agent.  Default is 20.

We don't recommend deviating too far from the default of 20.
Some folks find it useful to _temporarily_ boost this waaaaay up when there is "network weather"
effecting your favorite LLM provider and you start to see "Agent stopped due to max iterations" errors.

#### max_execution_seconds

An integer controlling the maximum amount of wall clock time (in seconds) to spend in the langchain
[AgentExecutor](https://api.python.langchain.com/en/latest/agents/langchain.agents.agent.AgentExecutor.html)
used for the agent.  Default is set for 2 minutes.

#### temperature

Pretty much any of the LLMs will take a floating-point temperature parameter as an argument.
Roughly speaking, temperature is a number between 0.0 and 1.0 that indicates a relative amount of randomness
in answers provided by the LLM.  By default this value is 0.7.

#### Other LLM-specific Parameters

LLMs all come with various parameters like temperature that can be set on them.
As long as a parameter is a scalar listed in the args section for your LLM's class in the
[llm_info hocon file](https://github.com/leaf-ai/neuro-san/blob/main/neuro_san/internals/run_context/langchain/default_llm_info.hocon)
file, you can set that parameter in any llm_config within its own technical limits however you like.

Note: _We strongly recommend to **not** set secrets as values within any source file, including hocon files._
These files tend to creep into source control repos, and it is __very__ bad practice
to expose secrets by checking them in.

#### verbose

Controls server-side logging of agent chatter.

By default this is false, indicating no server-side logging is desired.
When true, basic langchain AgentExecutor verbosity is turned on for the agent.
There is an "extra" level of logging which enables a lanchain LoggingCallbackHandler for the agent.

Whenever any logging is turned on, it can be quite chatty, so this is not really a setting appropriate
for a production environment.  It's worth noting that most of the same information obtained by turning
on verbose can also be obtained by AGENT ChatMessages returned when the client's chat_filter is set to
MAXIMAL.

#### error_formatter

String value which describes which error formatter to use by default for any agent in the network.

The default value is "string" which indicates that when errors occur, they are reported upstream
in their original string format.

An alternative value here is "json", which formats the error output into a predictable json dictionary
which contains the following keys:

| Error Dictionary Key | Description |
|:---------------------|:------------|
| error     | The error message itself, usually from a Python exception |
| tool      | The name of the tool within the agent network that generated the error |
| details   | Optional string descibing details of the error. Could include a Traceback, for instance|

#### error_fragments

A list of strings where if any one of the strings appears in agent output,
it is considered an error and reported as such per the [error_formatter](#error-formatter).

### tools

A list/array of [single agent specifications](#single-agent-specification) that make up the agent network.

The first of these in the list is called the "Front Man".
He does handles all the dealings with any client of the agent network.

Other agents listed can be in any order and can reference each other, forming trees or graphs.

Typically any agent that is not the front-man is considered an implementation detail private
to the agent network definition. It is not possible to call these internal agents except from within
the agent network that defines them.  If you find your agent networks have some shared functionality
between them, consider elevating sub-networks to [external agent](#external-agents) status.

## Single Agent Specification

Settings for individual agents are specified by their own dictionary within the list of [tools](#tools) for the network.

There are a few settings that only apply to the front man.

### name

Every agent *must* have a name.

Names can contain alphanumeric characters with - or _ as word separators.
No spaces or other punctuation is allowed.
This allows for snake_case, camelCase, kebab-case, PascalCase, or SCREAMING_SNAKE_CASE
human-readable names, however you like them.

Any agent can refer to any other agent definition within the same agent network hocon file
by using its name in its [tools](#tools-agents) list.

### function

A dictionary which describes what at agent can do and how it wishes to be invoked for the
benefit of its upstream caller's planning.

Neuro-san largely follows the
[OpenAI function spec](https://platform.openai.com/docs/guides/function-calling?api-mode=responses#defining-functions),
however we do not require redefining the "name" (that is already given [above](#name))
and we also do not require redefining the "type" as this is always the same for every agent.

What is defined in this dictionary is what is returned for the agent's Function() neuro-san web API call.

#### description

Every agent *must* have its function description filled out.
This is a single string value which informs anything upstream as to what *this* agent can do for it.

For a user-facing front-man, what is contained in this description often suffices as a prompt for the user.

#### parameters

Parameters contains an optional [JSON Schema](https://json-schema.org) dictionary describing what
specific information the agent needs as input arguments when it is called.

A front-man typically does not need parameters defined, unless the agent network being described
is anticipated as being called from other agent networks.

##### type

The type of the parameters dictionary is always "object".
This lets the parsing system know that the [properties](#properties) will be described as a dictionary.

##### properties

A dictionary whose keys each describe the name of a single argument to be used as input to an agent.
Each key's value is a dictionary describing the single argument value itself.
This dictionary has the following keys:

| Property Key | Description |
|:-------------|:------------|
| description  | A string which describes the particular argument |
| type         | A string describing the type of the property. (See below) |
| default      | An optional default value for the property |

Scalar types here can be "int", "float", "string", "bool".
It is possible that a properties' type can be "array"s for lists or "object"s for nested dictionaries.

Any sample agent hocon with more than one agent will have some example of a simple properties dictionary.
For a concrete, more complex properties definition, with nested objects and arrays,
See the definition of [cao_item in the esp_descision_assistant.hocon](https://github.com/leaf-ai/neuro-san/blob/main/neuro_san/registries/esp_decision_assistant.hocon).

##### required

This is an optional list of string keys in the [properties](#properties) dictionary that are considered
to be required whenever an upstream agent calls the one being described.
Note that it's possible to specify a default value for any property that is not listed as required.

### instructions

When included, the single (often very long) string value here tells an LLM-enabled agent
what it needs to do.

This is optional because not every tool listed in the agent network uses an LLM (there exist CodedTools).
But if you expect an agent to use an LLM, this instructions field is a must.

### command

An optional string to set an LLM-enabled agent in motion.

### tools (agents)

An optional list of strings with the names of other agents available for the agent being described to call.

Typically the names listed here are other agents within the same agent network definition,
often forming a tree structure, but overall agent networks are allowed to contain cycles.

It is important to note that just because an agent is listed in the tools does not mean that it will always
be called by an LLM.  The tools listing is merely a full description of what is _available_ to the agent.
It is the agent itself that actually decides which tools (if any) to invoke depending on its instructions
and the context of its query.

#### External Agents

This is not a hocon file key, but more a description of a concept that relates to listings of tools.

It is possible for any agent to reference another agent on the same server by adding a forward-slash
in front of the served agent's name.  This is typically the stem of an agent network hocon file in
a deployment's registries directory.

Example: "/website_search" or "/math_guy"

This allows common agent network definitions to be used as functions for other local networks.

Furthermore, it is also possible to reference agents on other neuro-san _servers_ by using a URL as a tool reference.

Example: "http://localhost:8080/math_guy"

This enables entire ecosystems of agent webs.

### llm_config

It is possible for any LLM-enabled agent description to also have its own [llm_config](#llm-config)
dictionary.  This allows for agents to use the right agent for the job.
Some considerations might include:

* Use of lower-cost LLMs for lighter (perhaps non-tool-using) jobs
* Use of specially trained LLMs when subject matter expertise is required.
* Use of securely sequestered LLMs when sensitive information is appropos to a single agent's chat stream.

### class

Optional string specifying a Python class which implements the
[CodedTool](https://github.com/leaf-ai/neuro-san/blob/main/neuro_san/interfaces/coded_tool.py)
interface.

Implementations must be found in the directory where the class can be resolved by looking
under the AGENT_TOOL_PATH environment variable setting as part of the PYTHONPATH.
By default neuro-san deployments assume that PYTHONPATH is set to contain the
top-level of your project's repo and that AGENT_TOOL_PATH is set to "<top-level>/coded_tools".
In that directory each agent has its own folder and the value of the class is resolved
from there.

For example:
If the agent is called "math_guy" and the class is valued as "calculator.Calculator",
The python file math_guy/calculator.py under AGENT_TOOL_PATH is expected to have
a class called Calculator which implements the CodedTool interface.


Implementations of the CodedTool interface must have implementations which:

* have a no-args constructor
* implement either the preferred async_invoke() or the discouraged synchronous invoke() method.

Agents representing CodedTools have the arguments described their [function parameters](#parameters)
populated by calling LLMs and passed in via the args dictionary of their async/invoke() method
when they are invoked.  They are also passed the sly_data dictionary which contains
private information not accessable to the chat stream.

Note that the CodedTool also has a synchronous invoke() method, but we discourage its use,
as neuro-san is expected to run in an asynchronous multi-threaded environment.
Using synchronous I/O calls within CodedTool implementations will result in loss of per-request
agent parallelism and performance problems at scale.

### args

Args is an optional dictionary for agents representing CodedTools to pass other
key/value pairs when the agent is invoked.  This allows for greater code sharing
for a single CodedTool implementation when it is referenced by multiple agents
and called in multiple contexts.

### allow

An optional dictionary which controls security policy pertaining to agent information flow.

#### connectivity

Boolean value which allows any agent within the network specification to control whether or
not to report any downstream tools during a Connectivity() API call, which allow for
pre-rendering of agent networks for demo/light-show purposes.

The default value of true says "sure, report all my downstream tools".
A false value does not allow such reporting.

Turning this value to false at the front-man prevents any connectivity reporting from happening.
Mid-level agents can have this be false to hide certain implementation details.

#### to_downstream

Dictionary which specifies security policy for information go *to* downstream [external agents](#external-agents).
This has no effect on any information flowing between agents internal to the network.

##### sly_data

By default no sly_data goes out to any external agent.
To transmit sly_data to an external agent, you _must_ specificaly enable it.

A dictionary value whose keys represent keys in the sly_data dictionary.
Boolean values for each key tell whether or not that data is allowed to go through to external agents.
A string value in the dictionary represents a translation to a new key.

Example:

```
    "allow": {
        "to_downstream": {
            "sly_data": {
                "user_id": true,
                "user_ssn": false,
                "my_session": "session_id"
            }
        }
    }
```

In simple sly_data situations you can simply specify which keys you want to allow
as a list:

```
    "allow": {
        "to_downstream": {
            "sly_data": [ "user_id", "session_id" ]
        }
    }
```

#### from_downstream

Dictionary which specifies security policy for information coming *from* downstream [external agents](#external-agents).
This has no effect on any information flowing between agents internal to the network.

##### sly_data

By default no sly_data is accepted from any external agent.
To accept sly_data from an external agent, you _must_ specificaly enable it.

A dictionary value whose keys represent keys in the sly_data dictionary.
Boolean values for each key tell whether or not that data from any external agent
is allowed to be accepted and merged into this agent's sly_data.
A string value in the dictionary represents a translation to a new key.

The same dictionary/list specification described in [to_downstream](#sly_data) also applies here.

#### to_upstream

_Front Man only_
Dictionary which specifies security policy for information going back to any calling client.

This has no effect on any information flowing between agents internal to the network.

##### sly_data

By default no sly_data goes back to the upstream caller from the agent network
To transmit sly_data to its upstream caller, you _must_ specificaly enable it.

A dictionary value whose keys represent keys in the sly_data dictionary.
Boolean values for each key tell whether or not that data internal to the agent network
is allowed to go back to the client in the final message.
A string value in the dictionary represents a translation to a new key.

The same dictionary/list specification described in [to_downstream](#sly_data) also applies here.

### max_message_history

_Front Man only_

An integer which tells the server how many of the most recent chat history messages
to send back in its chat_context field which allows for continuing a conversation
on the next client invocation.  By default this value is None, indicating there is no limit.

This is useful when end-user conversations with agents are expected to be lengthy and/or change
topics frequently.

### error_formatter

Same as top-level [error_formatter above](#error-formatter), except at single-agent scope.

### error_fragments

Same as top-level [error_fragments above](#error-fragments), except at single-agent scope.
