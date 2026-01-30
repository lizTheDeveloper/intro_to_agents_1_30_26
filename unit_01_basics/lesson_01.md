# Unit 1: Basic Chat Completion Agent

## Overview

This unit introduces a Python implementation of a basic chat completion agent using the Groq API integration. The code demonstrates core concepts of AI agent architecture including message handling, tool function registration, and API interaction.

## Code Structure

### Key Components
- `messages` list: Tracks conversation history with role-based messaging
- `client`: Groq API client instance
- `prompt()` function: Main interface to the AI model
- `list_dir()` function: First tool function implementation

### Message Flow
1. Initial system prompt sets documentation agent role
2. The AI is instructed to process Git working tree changes
3. The Groq client uses a 32B parameter Qwen3 model

### Example Execution
```python
completion = prompt(messages)
print(completion.choices[0].message)
```

This implementation forms the foundation for more complex agent architectures.