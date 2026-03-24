# RAG Chatbot — Twitch Data Analysis

<p align="left"> <a href="LICENSE"> <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"> </a> <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version"> <img src="https://img.shields.io/badge/Framework-Ollama-red.svg" alt="Framework"> <img src="https://img.shields.io/badge/Models-Llama3.2%20%7C%20Gemma7B-green.svg" alt="Models Used"> <img src="https://img.shields.io/badge/Approach-RAG-purple.svg" alt="Approach"> </p>

An intelligent Retrieval-Augmented Generation (RAG) chatbot that allows users to query a Twitch dataset using natural language.
The system converts queries into pandas code, executes them, and generates insightful summaries using multiple locally hosted LLMs.

## Project Overview

This project builds an AI-powered data assistant that bridges natural language queries with structured data analysis.

It includes:

- Natural language → pandas query generation
- Execution on a real dataset (Twitch streamers)
- Multi-model comparison (Llama vs Gemma)
- Insight generation and summarisation
- Error handling and validation for robust outputs

## Pipeline
<img width="2391" height="3155" alt="User Query Processing-2026-03-23-234243" src="https://github.com/user-attachments/assets/7c5ae98c-864d-4473-8bab-de9234b46de2" />

## Features
### Query Generation (LLM-Powered)
- Converts user questions into valid pandas queries
- Strict prompt rules ensure:
- No invalid syntax
- No hallucinated columns
- Safe execution
### Data Processing
- Executes queries on the dataset
- Handles:
DataFrame
Series → converted to DataFrame
- Scalar outputs
- Ensures consistent output format
### Multi-Model Comparison
- Uses:
  - Llama 3.2 → more accurate
  - Gemma 7B → faster
- Generates:
  - Individual summaries
  -Final consensus answer
### Validation & Error Handling
- Detects invalid column usage
- Prevents large outputs (>10 rows)
- Ensures only executable code is returned
### Insight Generation
- Produces short, meaningful summaries
- Focuses on key patterns and trends

## Repository Structure
```bash
RAG_Chatbot_Project/
│
├── rag-chatbot.py              # Main chatbot script
├── twitchdata-update.csv       # Dataset (Top 1000 Twitch streamers)
├── requirements.txt            # Dependencies
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## Installation & Setup
1. Install dependencies
```bash
pip install -r requirements.txt
```
Or manually:
```bash
pip install pandas tabulate
```

2. Install & Run Ollama (Local LLMs)
3. 
Make sure Ollama is installed and running:
```bash
ollama run llama3.2
ollama run gemma:7b
```

3. Run the Chatbot
```bash
python rag-chatbot.py
```

## Example Queries
1. “Streamer with highest average viewers”
2. “Top 5 streamers by followers gained”
3. “Show streamers with most watch time”
4. “Streamer with highest peak viewers”

## How It Works
1. User inputs a natural language query
2. LLM converts it into pandas code
3. Code is executed on dataset
4. Each model generates a summary
5. Final model compares results and outputs a unified answer

## Dataset
Twitch Top 1000 Streamers Dataset
Includes:
- Average viewers
- Followers gained
- Watch time
- Stream time
- Peak viewers...

## Limitations
- Requires exact column name matching
- No fuzzy matching or synonym handling
- Large results are restricted (>10 rows)
- Dependent on LLM accuracy

## Key Learnings
- Prompt engineering is critical for structured outputs
- LLMs can generate inconsistent formats → requires cleaning
- Data normalisation improves reliability
- Multi-model validation increases robustness

- Trade-off between speed vs accuracy in LLMs
  
## Demo Preview
<img width="1757" height="491" alt="Screenshot 2026-03-24 010202" src="https://github.com/user-attachments/assets/012eb76c-efcf-4055-a2fe-c62774d4fba9" />
<img width="1761" height="493" alt="Screenshot 2026-03-24 010502" src="https://github.com/user-attachments/assets/04c93833-d7c4-40c6-9a59-2c1c56846b7b" />
<img width="1576" height="854" alt="Screenshot 2026-03-24 010527" src="https://github.com/user-attachments/assets/45c74b13-427c-4d25-a146-be87048ad499" />
