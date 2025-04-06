# Agentic AI Documentation Q&A 

This AI-powered question-answering agent processes documentation from help websites and accurately answers user queries about product features, integrations, and functionality.

## Features

- Crawls and processes documentation websites
- Extracts meaningful content while filtering out navigation elements and non-content
- Maintains proper context hierarchy of the documentation
- Processes natural language questions
- Provides accurate answers based on the processed documentation
- Clearly indicates when information is not available
- Includes source references (URLs) for answers

## Installation

### Prerequisites

- Python 3.8 or higher
- Google API key for Gemini LLM

### Setup

1. Clone this repository:
```bash
git clone https://github.com/shashankpandey2411/Agentic-Doc-Crawler-QA-Bot.git
cd Agentic-Doc-Crawler-QA-Bot
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your Google API key:
```
GOOGLE_API_KEY="your_google_api_key_here"
```

## Usage

### Basic Usage

Run the agent with a documentation URL:

```bash
python main.py --url https://docs.python.org/3/ --max-pages 50
```

### Command Line Options

- `--url` (Required): URL of the documentation website to process
- `--max-pages` (Optional, default=100): Maximum number of pages to crawl
- `--persist-dir` (Optional, default="./chroma_db"): Directory to persist vector store
- `--verbose` (Optional): Enable verbose logging

### Example Sessions

```bash
# Quick test with minimal pages
python main.py --url https://docs.python.org/3/ --max-pages 5
```

### Command Line Options

- `--url` (Required): URL of the documentation website to process
- `--max-pages` (Optional, default=100): Maximum number of pages to crawl
- `--persist-dir` (Optional, default="./chroma_db"): Directory to persist vector store
- `--verbose` (Optional): Enable verbose logging

### Example Usage

```bash
(base) user@shashank:~/Downloads/AgentAI/pulsegen/qa_agent$ python main.py  --url https://docs.python.org/3/ --max-pages 5
Initializing Documentation Q&A Agent...
Crawling documentation from https://docs.python.org/3/...
2025-04-06 15:56:06,258 [INFO] Starting crawl from https://docs.python.org/3/
2025-04-06 15:56:08,396 [INFO] Crawl complete. Processed 6 pages.
Extracting content from crawled pages...
Processing and indexing documents...
Creating vector store...
2025-04-06 15:56:08,677 [INFO] Anonymized telemetry enabled. See                     https://docs.trychroma.com/telemetry for more information.
/home/user/Downloads/AgentAI/pulsegen/qa_agent/utils/processor/indexer.py:130: LangChainDeprecationWarning: Since Chroma 0.4.x the manual persistence method is no longer supported as docs are automatically persisted.
  vector_store.persist()
2025-04-06 15:56:11,380 [INFO] Vector store created with 26 chunks
Initialization complete! Ask me questions about the documentation.

> whats new in python 3.13?
Based on the provided documentation, a section titled "What's new in Python 3.13?" exists within the Python 3.13.2 documentation. This section, along with older "What's new" documents since    
Python 2.0, can be found at the following URLs:                                                                                                                                                  

 • https://docs.python.org/3/ (Source 1, Source 3, Source 5)                                                                                                                                     
 • https://docs.python.org/3.13/ (Source 2, Source 4)                                                                                                                                            

Sources:
- https://docs.python.org/3/
- https://docs.python.org/3.13/

> what new in java 21?
I'm sorry, but I cannot provide information about what's new in Java 21. The provided documentation only covers Python versions 3.11 and 3.12. ([Source 1], [Source 2], [Source 3], [Source 4],  
[Source 5])                                                                                                                                                                                      

Sources:
- https://docs.python.org/3.11/
- https://docs.python.org/3.12/
```

## Architecture

The agent is built with a modular architecture:

- **Crawler Module**: Handles fetching and parsing content from documentation websites
- **Content Extractor**: Filters out non-content elements and extracts meaningful content
- **Document Processor**: Processes and indexes documents for efficient querying
- **Query Processor**: Handles natural language questions
- **Gemini LLM Integration**: Generates comprehensive answers based on relevant documentation
- **CLI Interface**: Provides user-friendly terminal interaction

- ## Project Structure

```
qa_agent/
│
├── __init__.py             # Makes the directory a Python package
├── main.py                 # Entry point for the application
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── .env                    # Environment variables (API keys)
│
├── chroma_db/              # Directory for storing vector database
│
└── utils/                  # Utilities and main modules
    ├── __init__.py         # Makes utils a Python package
    ├── error_handling.py   # Error handling utilities
    ├── logger.py           # Logging configuration
    ├── progress.py         # Progress tracking for long operations
    │
    ├── cli/                # Command Line Interface
    │   └── interface.py    # CLI implementation
    │
    ├── crawler/            # Web Crawling functionality
    │   ├── crawler.py      # Website crawler
    │   └── extractor.py    # Content extraction from HTML
    │
    ├── knowledge_base/     # Knowledge storage
    │   ├── document.py     # Document class definitions
    │   └── vector_store.py # Vector database interface
    │
    ├── llm/                # Language Model integration
    │   ├── gemini.py       # Gemini LLM integration
    │   └── prompt_templates.py # Prompt engineering templates
    │
    ├── processor/          # Content processing
    │   ├── indexer.py      # Document indexing logic
    │   └── cleaner.py      # Content cleaning and normalization
    │
    └── qa/                 # Question Answering
        ├── query_processor.py # Query processing
        └── answer_generator.py # Answer generation
```

## Module Descriptions

- **main.py**: Entry point that initializes and runs the application
- **utils/cli/**: Command line interface implementation
- **utils/crawler/**: Web crawling and content extraction functionality
  - **crawler.py**: Handles recursive crawling of documentation sites
  - **extractor.py**: Extracts meaningful content from HTML pages
- **utils/knowledge_base/**: Document storage and retrieval
  - **document.py**: Document structure and hierarchy models
  - **vector_store.py**: Vector database for efficient document retrieval
- **utils/processor/**: Content processing and indexing
  - **indexer.py**: Handles document indexing and chunking
  - **cleaner.py**: Content cleaning and normalization
- **utils/llm/**: Language model integration
  - **gemini.py**: Gemini LLM integration for answer generation
  - **prompt_templates.py**: Prompt engineering for effective Q&A
- **utils/qa/**: Question answering logic
  - **query_processor.py**: Processes user queries
  - **answer_generator.py**: Generates answers from retrieved documents
