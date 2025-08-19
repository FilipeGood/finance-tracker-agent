# LangChain Agent Methods – Exploration Notebook

This notebook explores and tests four different agent creation methods from LangChain. Each method demonstrates a different approach to building agents using LLMs with various capabilities and structure.

## Methods Overview

### 1. `create_tool_calling_agent`
Creates an agent capable of calling external tools (functions or APIs) as needed, based on the user's input and reasoning.

- **Use Cases**:  
  Ideal for scenarios where an agent must interact with multiple tools or APIs (e.g. calculator, search, database). Useful in dynamic environments where tool usage is conditional on user input.

---

### 2. `create_react_agent`
Implements the ReAct (Reasoning + Acting) pattern. The agent reasons about what actions to take and observes outcomes iteratively before providing a final answer.

- **Use Cases**:  
  Great for tasks that benefit from intermediate reasoning steps, such as multi-hop question answering, research tasks, or complex decision-making workflows.

---

### 3. `create_structured_chat_agent`
Builds an agent using a structured chat format, allowing it to manage tools and state in a cleaner, more interpretable way.

- **Use Cases**:  
  Useful for production-grade assistants requiring clear tool invocation and consistent conversation structure. Offers better observability and traceability of agent behavior.

---

### 4. `create_openai_functions_agent`
Uses OpenAI's native function calling (via OpenAI Chat Models) to allow the model to directly call predefined functions based on intent recognition.

- **Use Cases**:  
  Ideal when using OpenAI APIs with built-in function calling. Recommended for rapid prototyping and controlled execution of functions based on user queries.

---
