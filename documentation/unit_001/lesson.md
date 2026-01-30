# Unit 001: Documentation Agent with Groq

This lesson explains the `basic_chatcompletion.py` code that sets up a Groq-powered documentation agent using the `list_dir` tool.

## Overview
The code implements an agent system where an AI acts as a documentation agent, processing user prompts, calling a tool to list directory contents, and maintaining message history.

## Code Structure
1. **Imports**
   - `Groq`: Groq API client
   - `json`: For JSON handling

2. **Message History**
   ```json
   messages = [
     {
       "role": "system",
       "content": "Your role is as a documentation agent..."
     }
   ]
   ```
   System message instructs the model to act as a documentation agent following specific tasks.

3. **Groq Client Initialization**
   ```python
   client = Groq()
   ```

4. **Prompt Function**
   ```python
   def prompt(messages):
     completion = client.chat.completions.create(
       model="qwen/qwen3-32b",
       messages=messages,
       tools=[{
         "type": "function",
         "function": {
           "name": "list_dir",
           "description": "List files/folders in a directory",
           "parameters": {"type": "object", "properties": {"dir_path": {"type": "string"}}}
         }
       }]
     )
     return completion
   ``

5. **Tool Functions**
   ```python
   def list_dir(directory_path: str) -> str:
     """List files/folders in a directory"""
     files_and_folders = os.listdir(directory_path)
     return "\n".join(files_and_folders)
   ``

6. **Execution Flow**
   ```python
   ## Initial call
   completion = prompt(messages)

   ## Process tool call
   tool_call = completion.choices[0].message.tool_calls[0]
   tool_args = json.loads(tool_call.function.arguments)

   ## Append to message history
   messages.append(completion.choices[0].message)

   ## Execute tool and append result
   tool_result = {
     "role": "tool",
     "tool_call_id": tool_call.id,
     "name": tool_call.function.name,
     "content": str(list_dir(tool_args.get("dir_path")))
   }
   messages.append(tool_result)

   ## Next call
   next_call = prompt(messages)
   ```

## JSON Structure
Tool definitions follow strict JSON structure:
```json
{
  "type": "function",
  "function": {
    "name": "list_dir",
    "description": "List files/folders",
    "parameters": {
      "type": "object",
      "properties": {
        "dir_path": {"type": "string"}
      }
    }
  }
}
```

## Key Features
- Maintains conversation history in `messages` array
- Uses function calls for directory listing
- Dynamically adds tool results to conversation history
- Follows strict JSON structures for tools

## How It Works
1. The system message defines the agent's role
2. The first prompt triggers a function call to `list_dir`
3. The response includes both
   - The model's reasoning about directory listing
   - The actual directory contents from the tool
4. The combined result is used to make a next call