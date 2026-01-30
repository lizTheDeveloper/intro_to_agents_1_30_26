from groq import Groq
import os
import json

def create_tool_agent():
    """Initialize multi-tool agent with file system capabilities"""
    return {
        'client': Groq(),
        'messages': [
            {'role': 'system',
             'content': 'Multi-tool file system agent'}
        ],
        'tools': [
            {'name': 'list_dir',
             'description': 'List directory contents',
             'function': list_dir},
            {'name': 'read_file',
             'description': 'Read file contents',
             'function': read_file},
            {'name': 'write_file',
             'description': 'Write text to file',
             'function': write_file},
            {'name': 'mkdir',
             'description': 'Create new directory',
             'function': mkdir}
        ],
        'tools_by_name': {
            'list_dir': list_dir,
            'read_file': read_file,
            'write_file': write_file,
            'mkdir': mkdir
        }
    }

if __name__ == "__main__":
    agent = create_tool_agent()
    response = agent['client'].chat.completions.create(
        model="qwen/qwen3-32b",
        messages=agent['messages']
    )
    print(f"Initial response: {response.choices[0].message}")
    agent['messages'].append(response.choices[0].message)