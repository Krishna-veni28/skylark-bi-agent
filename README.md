# Skylark Business Intelligence Agent

An AI-powered Business Intelligence agent that connects to Monday.com and provides founder-level insights from Deals and Work Orders data.

## Overview

The Skylark BI Agent allows business users to ask conversational questions about:

* Sales pipeline
* Deal value
* Sector performance
* Deal stages
* Work-order execution
* Billing
* Collections
* Receivables
* Leadership-level business summaries

The agent dynamically retrieves data from Monday.com rather than hardcoding the supplied CSV data.

## Architecture

```text
User
  ↓
Streamlit Web Interface
  ↓
Query / Agent Layer
  ↓
Business Intelligence Engine
  ↓
Data Cleaning & Normalization
  ↓
Monday.com API
  ↓
Deals Board + Work Orders Board
```

### Main Components

* `backend/app.py` — Streamlit conversational interface
* `backend/agent.py` — Agent/query handling
* `backend/query_engine.py` — Interprets business questions and selects the appropriate analysis
* `backend/bi_engine.py` — Business intelligence calculations
* `backend/data_cleaner.py` — Cleans and normalizes Monday.com data
* `backend/monday_client.py` — Monday.com API integration
* `backend/inspect_data.py` — Inspects board structure and data
* `backend/test_monday.py` — Tests Monday.com connectivity
* `backend/test_bi.py` — Tests BI calculations
* `backend/check_values.py` — Validates important numeric fields
* `backend/debug_monday.py` — Debugging utility
* `backend/requirements.txt` — Python dependencies

## Monday.com Configuration

The application uses two Monday.com boards:

1. Deals
2. Work Orders

The application reads the data dynamically through the Monday.com API.

### Environment Variables

Create a `.env` file inside the `backend` directory:

```env
MONDAY_API_TOKEN=your_monday_api_token
DEALS_BOARD_ID=your_deals_board_id
WORK_ORDERS_BOARD_ID=your_work_orders_board_id
```

Do not commit the `.env` file to GitHub.

The `.gitignore` file excludes:

```text
.env
venv/
__pycache__/
*.pyc
```

## Local Setup

Clone the repository:

```bash
git clone https://github.com/Krishna-veni28/skylark-bi-agent.git
cd skylark-bi-agent
```

Create and activate a virtual environment:

### Windows

```powershell
python -m venv backend\venv
backend\venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r backend\requirements.txt
```

Configure the `.env` file inside `backend`.

Test the Monday.com connection:

```powershell
cd backend
python test_monday.py
```

Run the BI tests:

```powershell
python test_bi.py
```

Start the Streamlit application:

```powershell
streamlit run app.py
```

The application will then be available locally through the Streamlit URL shown in the terminal.

## Hosted Prototype

The application is deployed using Streamlit Community Cloud.

The deployment uses the GitHub repository and reads the Monday.com API credentials from deployment secrets rather than storing credentials in the source code.

## Data Resilience

The agent is designed to handle real-world messy business data.

The data-cleaning layer:

* Handles missing and null values
* Converts numeric fields safely
* Normalizes text values
* Handles inconsistent date representations
* Converts Monday.com column values into analysis-friendly fields
* Avoids application failure when individual fields are missing

The application also separates unavailable data from valid zero values where possible.

## Query Understanding

The agent supports conversational business questions such as:

* "How is our pipeline looking?"
* "Which sector has the highest deal value?"
* "Which deal stage has the highest value?"
* "How many work orders are completed?"
* "How much have we collected?"
* "How much is receivable?"
* "Give me a leadership summary"

For unsupported questions, the agent provides a clear response describing the currently supported business analysis areas.

## Business Intelligence

The agent provides calculated insights rather than simply returning raw Monday.com records.

Examples include:

* Total deal records
* Total recorded deal value
* Active pipeline value
* Deal value by sector
* Deal value by stage
* Work-order completion rate
* Total billed value
* Total collected value
* Total receivable amount

## Leadership Updates

The leadership-summary capability provides a concise snapshot of key commercial and operational metrics.

It combines:

* Sales activity
* Pipeline value
* Work-order volume
* Execution completion
* Billing
* Collections
* Receivables

This is intended to help founders and executives quickly understand the current business position without manually reviewing multiple Monday.com boards.

## Security

The Monday.com API token is stored outside the source code.

For local development, credentials are stored in `.env`.

For hosted deployment, credentials are stored using the deployment platform's secrets management.

The `.env` file, virtual environment, Python cache files, and compiled Python files are excluded through `.gitignore`.

## Limitations

The current implementation focuses on the core assignment requirements and predefined business intelligence areas.

With additional development time, the system could be extended with:

* More natural-language query interpretation
* Automatic clarification questions for ambiguous queries
* Quarter/month/date-range filtering
* Trend analysis
* Visual dashboards and charts
* More cross-board analysis
* Automated leadership-report generation
* More advanced data-quality reporting
* Additional Monday.com boards and metrics

## Technology Stack

* Python
* Pandas
* Streamlit
* Monday.com API
* python-dotenv
* OpenAI API / agent layer

## Project Structure

```text
skylark-bi-agent/
│
├── README.md
│
└── backend/
    ├── app.py
    ├── agent.py
    ├── bi_engine.py
    ├── data_cleaner.py
    ├── monday_client.py
    ├── query_engine.py
    ├── inspect_data.py
    ├── test_monday.py
    ├── test_bi.py
    ├── check_values.py
    ├── debug_monday.py
    ├── requirements.txt
    └── .gitignore
```

## Assignment Deliverables

This repository contains the source code for the Skylark Business Intelligence Agent, including the Monday.com integration, data-cleaning layer, business intelligence calculations, conversational interface, testing utilities, and deployment configuration.
