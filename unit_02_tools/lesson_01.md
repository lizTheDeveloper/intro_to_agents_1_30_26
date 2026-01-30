# Unit 2: Multi-tool Agent System

## Overview

This unit expands the basic agent with a robust file system interaction capability through four core tools:

1. `list_dir()` - File/folder inventory
2. `read_file()` - Content retrieval
3. `write_file()` - Content creation
4. `mkdir()` - Directory management

## Architecture Enhancements

### Tools Management
- Tools registered in `tools[]` list
- Map to functions in `tools_by_name` dictionary
- Dynamic execution through `the_function_to_call(**tool_args)`

### Execution Loop
```python
while not_done:
    print("-------------------- next loop -----------------")
    completion = prompt(messages)
    # Process results and execute tool calls
```

### Key Improvements
- Tool call persistence across iterations
- JSON parsing for structured arguments
- Error handling for invalid function references

This system demonstrates a complete agent capable of maintaining state, handling multiple tool types, and executing complex workflows.