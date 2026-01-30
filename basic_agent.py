from email import message_from_string
from groq import Groq
import os 
import json


messages = [
    {
        "role": "system",
        "content": """Your role is as a documentation agent. 
        Every time we produce code in this repository, your role will be to look at the Git working tree, and any files that are new, your job is to write a lesson that explains everything in the new code file that we've written, and then put the code file in a folder and name the folder with a unit and sequence it. 
        When documenting the way the code works, often there is JSON in a particular structure. 
        Do not alter the structure of any JSON, otherwise you may break the code. 
        Maintain the code's structure, the flow, and keep everything simple and well-commented. 
        Name all folders in this convention:
        ./Unit1-basic_chatcompletion/
        ./Unit2-basic_agent/
        Remember to include line breaks in your markdown.
        """
    }
]

tools = [{
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
},
{
"type":"function",
"function": {
    "name":"read_file",
    "description":"read the contents of a file as a string",
    "parameters":
    {
        "type":"object",
        "properties":
            {
                "file_path":
                    {
                        "type":"string",
                        "description":"The file path"
                    }
                }
        }
    }
},
{
"type":"function",
"function": {
    "name":"write_file",
    "description":"write the given text content to a file",
    "parameters":
    {
        "type":"object",
        "properties":
            {
                "file_path":
                    {
                        "type":"string",
                        "description":"The file path"
                    },

                "content":
                    {
                        "type":"string",
                        "description":"The content to write"
                    }
            }
        }
    }
},
{
"type":"function",
"function": {
    "name":"mkdir",
    "description":"create a new directory",
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
    
client = Groq()

def prompt(messages):

    completion = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=messages,
        tools=tools
    )
    return completion


def list_dir(dir_path: str) -> str:
    """list_dir

    Args:
        directory_path (str): List all the files and folders in a directory

    Returns:
        str: the files and folders
    """
    files_and_folders = os.listdir(dir_path)
    return "\n".join(files_and_folders)

def read_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        contents = f.read()
    return contents

def write_file(file_path: str, content: str) -> str:
    with open(file_path, "w") as f:
        f.write(content)
    return file_path

def mkdir(dir_path: str) -> str:
    os.mkdir(dir_path)
    return "successfully created " + dir_path


tools_by_name = {
    "list_dir": list_dir,
    "read_file": read_file,
    "write_file": write_file,
    "mkdir": mkdir
}
not_done = True

while not_done:
    print("-------------------- next loop -----------------")
    ## send the conversation so far to the AI
    completion = prompt(messages)
    print(completion.choices[0].message)
    message = completion.choices[0].message
    ## remember what we said
    messages.append(message)
    
    ## do the tool call
    if message.tool_calls:
        if len(message.tool_calls) > 0:
            ## get the first tool call
            for tool_call in message.tool_calls:
                tool_args = json.loads(tool_call.function.arguments)
                print(tool_call)
                try:
                    the_function_to_call = tools_by_name.get(tool_call.function.name)

                    ## save the results
                    tool_result = {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": str(the_function_to_call(**tool_args))
                    }

                    messages.append(tool_result)
                except Exception as e:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": "Your function call returned an error:" + str(e)
                    })