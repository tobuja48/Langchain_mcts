# LangChain MCTS

🚧 **Under Development** - Monte Carlo Tree Search integration for LangChain

A library that integrates Monte Carlo Tree Search (MCTS) with LangChain for advanced search and reasoning with language models.

## Project Status

⚠️ **This library is under active development**. All functions currently return "in development" messages.

## Installation

```bash
pip install langchain-mcts
```

## Basic Usage

```python
from langchain_mcts import MCTSAgent
from langchain_groq import ChatGroq
import os
from getpass import getpass

# Securely get the Groq API key
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass("Enter your Groq API key: ")

# 1. Initialize the Groq language model
# You can choose different models like "llama3-8b-8192" or "llama3-70b-8192"
llm = ChatGroq(model_name="llama3-8b-8192")

# 2. Create the MCTS agent and provide the model
agent = MCTSAgent(model=llm)

# 3. Perform the MCTS search
# This will now work because the agent has a model
try:
    result = agent.search("What is the best strategy for learning a new language?")
    print(result)
except Exception as e:
    print(f"An error occurred during the MCTS search: {e}")
```

## 🆕 Newly Implemented Features

- **Basic implementation of the MCTS algorithm**: The core of the Monte Carlo Tree Search (MCTS) tree, with selection, expansion, simulation, and backpropagation, is now functional[...]
- **Direct integration with LangChain models**: You can now use your own models (`BaseLanguageModel`) when creating agents or performing MCTS searches.
- **Enhanced convenience functions**:
  - `mcts_search(query, model, iterations, seed_answers, ...)`: Run a custom MCTS search in a single line.
  - `create_mcts_chain(model, ...)`: Generate a configured MCTS agent ready to integrate with LangChain chains.
- **System for evaluating and improving answers**: The agent can request a critique, improve the answer step-by-step, and automatically score its quality.
- **Support for custom seed answers**: You can provide initial answers to guide the search.
- **Test coverage and integration examples**: Integration tests and end-to-end workflow examples using mocks have been added.

## Updated Usage Example

```python
from langchain_mcts import MCTSAgent, mcts_search, create_mcts_chain

# Create agent with a custom model
agent = MCTSAgent(model=my_llm)

# Perform advanced MCTS search
result = agent.search("What is the best strategy?", iterations=5)
print(result)

# Use convenience function
result = mcts_search("My query", model=my_llm, iterations=3, seed_answers=["Answer 1", "Answer 2"])
print(result)

# Direct integration with LangChain
chain = create_mcts_chain(model=my_llm)
```

## Available Functions

### `MCTSAgent`
Main class for the MCTS agent:
- `search(query, iterations=100, seed_answers=None)`: Performs advanced MCTS search.
- Internal methods for expansion, simulation, critique, and answer improvement.

### `mcts_search(query, model, iterations=2, seed_answers=None, ...)`
Convenience function for quick MCTS search.

### `create_mcts_chain(model, ...)`
Creates an MCTS chain for integration with LangChain.

### `MCTSNode`
Represents a node in the MCTS tree with methods for:
- Parent/child node management
- Statistics update
- Leaf node verification

### **New**
- Methods for improving (`improve_answer`) and scoring (`rate_answer`) answers with the help of the LLM model.

## Planned Features (updated)

- ✅ Basic library structure
- ✅ Basic implementation of MCTS and convenience functions
- ✅ Support for custom seed answers
- ✅ Automatic evaluation and improvement of answers with LLM
- 🚧 Advanced integration with LangChain models (chains and tools)
- 🚧 Optimization and tuning of search policies
- 🚧 Support for different types of problems and domains
- 🚧 Search parallelization and performance optimization
- 🚧 Metrics and visualization
- 🚧 Advanced integration examples and tutorials
- 🚧 Interface improvements for non-technical users

## Development

To contribute to development:

```bash
git clone https://github.com/your-username/langchain-mcts
cd langchain-mcts
pip install -e .[dev]
```

To run tests:

```bash
pytest tests/
```

## Dependencies

- `langchain>=0.1.0`
- `numpy>=1.20.0`

## License

MIT

---

🔬 **Ongoing research**: This library is part of a research project on integrating search algorithms with large language models.