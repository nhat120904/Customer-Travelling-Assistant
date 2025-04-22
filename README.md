# Customer Support Bot

A specialized workflow system that combines large language models with agent-based architecture to provide automated customer support for travel-related inquiries.

## Overview

This project implements a customer support system that can handle various travel-related tasks including:
- Flight booking and updates
- Hotel reservations
- Car rental arrangements
- Excursion/activity bookings
- General travel information inquiries

The system uses a graph-based agent workflow that routes customer queries to specialized agents based on intent detection.

## Prerequisites

- Python 3.8+
- Required API keys:
  - OpenAI or Azure OpenAI
  - Tavily API key (for search functionality)
  - LangSmith (optional, for tracing and debugging)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd CustomerSupportBot/specialized_workflow
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables by creating a `.env` file with the following keys:
```
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
# Optional for Azure OpenAI
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_VERSION=your_azure_openai_version
AZURE_OPENAI_DEPLOYMENT=your_azure_openai_deployment
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
# Optional for LangSmith tracing
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=your_langsmith_project_name
```

## Configuration

The project uses YAML configuration files located in the `configs` directory:

- `config.yaml`: Main application configuration
- `llm.yaml`: LLM provider and model settings
- `database.yaml`: Database connection settings
- `vectordb.yaml`: Vector store settings
- `api.yaml`: API configuration
- `logger.ini`: Logger configuration

You can modify these files to customize the behavior of the system.

## Usage

### Running the Interactive Chat

Run the interactive chat interface:

```bash
python -m app
```

### Using the Web Interface

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Then navigate to `http://localhost:8000` in your browser.

You can also use the Streamlit interface:

```bash
streamlit run app.py
```

## Project Structure

- `agents/`: Contains agent implementations
  - `agent.py`: Core agent functionality
  - `graph.py`: Agent workflow graph definition
  - `schema.py`: Data schemas for agent communication
  - `tools.py`: Tool implementations for agents
  - `utils.py`: Utility functions for agents
- `app/`: Web application
  - `main.py`: FastAPI server implementation
- `configs/`: Configuration files
- `llm/`: LLM provider implementations
  - `base.py`: Base LLM interface
  - `openai.py`: OpenAI implementation
- `utils/`: General utilities
- `app.py`: Streamlit interface
- `db.py`: Database utilities

## Features

- **Multi-agent system**: Routes queries to specialized agents based on intent
- **Conversation history**: Maintains context throughout the conversation
- **Tool-using agents**: Agents can use tools to perform tasks
- **Approval workflow**: User approval for sensitive operations
- **Fallback mechanisms**: Graceful handling of errors and edge cases
- **Multiple interfaces**: Command-line, notebook, web, and API interfaces

## Available Tools

- Flight search and booking
- Hotel search and booking
- Car rental search and booking
- Excursion recommendations and booking
- Policy lookups
- General web search (via Tavily)

## Development

To extend the system with new functionality:

1. Add new tools in `agents/tools.py`
2. Define new schemas in `agents/schema.py`
3. Update the agent graph in `agents/graph.py`
4. Add new prompts in `prompts/prompts.py`

## Troubleshooting

Common issues:

1. **API key errors**: Ensure all required API keys are set in your `.env` file
2. **Model availability**: Check that the specified model in `llm.yaml` is available for your API key
3. **Database errors**: Make sure the SQLite database file exists and is properly initialized

## License

[Specify your license information here]
