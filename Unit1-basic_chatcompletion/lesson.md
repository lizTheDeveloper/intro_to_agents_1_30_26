# Course Design for `basic_chatcompletion.py`

**Unit1 Objectives:**
1. Understand basic chat-completion patterns using LLMs
2. Handle API connections and message formatting
3. Process structured JSON responses from model outputs
4. Maintain strict message flow integrity

## Code Explanation

1. **Imports**:
- `Groq()` connects to a language model (assumed Qwen 32b version)
- `message_from_string` is included but not used
- `json` handles structured data parsing

2. **Model Setup**:
```python
client = Groq()
```
Establishes connection to AI service

3. **Prompt Function**:
```python
def prompt(messages):
    completion = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=messages,
        tools=
... 
    )
```
Configures model call with JSON tool definitions preserved

4. **Tool Handling**:
```json
{
  "function": {"description": "List dir contents"},
  "type": "function"
}
```
Toolkit includes `list_dir()` for local filesystem interaction

5. **Message Flow**:
- Initial system message defines documentation agent role
- Completion response includes both:
  - Natural language output
  - Structured tool calls
- Code processes both types of responses

6. **Code Flow**:
```python
#1: Initial prompt sends instructions
#2: First response includes directory listing tool call
#3: Code executes tool call and appends result
#4: Final prompt receives next instructions
```

## Code Sample
```python
# Full code demonstrates:
# - Message threading
# - Function injection
# - API tool execution
# - State maintenance across turns
# - JSON data handling
#
# Maintains explicit message sequence:
# [system message] -> [model response + tool call] -> [tool result] -> [model final response]
```