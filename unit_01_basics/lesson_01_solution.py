from groq import Groq
import os
import json

def generate_agent():
    """Initialize and return a basic chat completion agent"""
    return {'client': Groq(),
            'messages': [{'role': 'system',
                         'content': 'Documentation agent for code repository'}],
            'tools': [{'name': 'list_dir',
                     'description': 'List directory contents',
                     'function': list_dir}],
            'tools_by_name': {'list_dir': list_dir}}

if __name__ == "__main__":
    agent = generate_agent()
    response = agent['client'].chat.completions.create(model="qwen/qwen3-32b",
                                                    messages=agent['messages'])
    print(response.choices[0].message)