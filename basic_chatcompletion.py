from email import message_from_string
from groq import Groq
import os 
import json


messages = [
    {
        "role": "system",
        "content": "Your role is as a documentation agent. Every time we produce code in this repository, your role will be to look at the Git working tree, and any files that are new, your job is to write a lesson that explains everything in the new code file that we've written. And then put the code file in a folder and name the folder with a unit and sequence it."
    }
]
    
client = Groq()

def prompt(messages):

    completion = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=messages,
        tools=[{
                "type":"function",
                "function": {
                    "name":"list_dir",
                    "description":"List all the files and folders in a directory",
                    "parameters":
                        {
                            "type":"object",
                            "properties":
                                {
                                    "dir_path":
                                        {
                                            "type":"string",
                                            "description":"The directory path"
                                        }
                                    }
                            }
                        }
                }]
    )
    return completion


def list_dir(directory_path: str) -> str:
    """list_dir

    Args:
        directory_path (str): List all the files and folders in a directory

    Returns:
        str: the files and folders
    """
    files_and_folders = os.listdir(directory_path)
    return "\n".join(files_and_folders)


## get the first tool call
completion = prompt(messages)
print(completion.choices[0].message)

## do the tool call
message = completion.choices[0].message
tool_call = completion.choices[0].message.tool_calls[0]
tool_args = json.loads(tool_call.function.arguments)
print(tool_call)

## remember what we did
messages.append(completion.choices[0].message)

## save the results
tool_result = {
    "role": "tool",
    "tool_call_id": tool_call.id,
    "name": tool_call.function.name,
    "content": str(list_dir(tool_args.get("dir_path")))
}

messages.append(tool_result)

next_call = prompt(messages)

print(next_call)