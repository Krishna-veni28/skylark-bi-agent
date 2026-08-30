# Decision Log — Skylark Business Intelligence Agent

## 1. Objective

The goal was to build a conversational Business Intelligence agent that allows founders and executives to ask business questions about sales deals, pipeline performance, work-order execution, billing, collections, and receivables.

The agent integrates dynamically with Monday.com and does not hardcode the supplied CSV data.

## 2. Key Technical Decisions

### Monday.com API

I chose the Monday.com API rather than hardcoding the provided CSV data.

**Reason:**

* The assignment requires dynamic querying of Monday.com.
* Business data can change after the initial CSV import.
* The API allows the agent to work with the current board data.

The application reads from two boards:

* Deals
* Work Orders

The integration was implemented as read-only because the assignment explicitly requires Monday.com to be used in read-only mode.

### Python + Pandas

Python was selected for the backend because it provides strong support for data processing and Business Intelligence workloads.

Pandas is used for:

* Data transformation
* Numeric calculations
* Grouping and aggregation
* Sector analysis
* Deal-stage analysis
* Work-order metrics

### Streamlit

Streamlit was selected for the conversational interface because it allowed a working web prototype to be developed quickly within the six-hour assignment timeline.

It provides:

* A simple browser-based interface
* Easy deployment
* Fast iteration
* A user-friendly way to test founder-level queries

## 3. Data Resilience Decisions

The supplied business data contains missing values, inconsistent formats, and different Monday.com column types.

The data-cleaning layer was therefore designed to:

* Handle null and missing values safely
* Convert numeric values when possible
* Normalize text fields
* Process inconsistent date formats
* Handle empty Monday.com column values
* Avoid application failure because of individual missing fields

Where information is unavailable, the agent should avoid inventing values and instead provide a meaningful response based on available data.

## 4. Query Understanding

A lightweight rule-based query engine was used for the core prototype.

The engine identifies business intent from keywords and routes questions to the appropriate BI calculation.

Supported areas include:

* Pipeline
* Deal value
* Sector performance
* Deal stages
* Work-order completion
* Billing
* Collections
* Receivables
* Leadership summaries

### Trade-off

A fully general natural-language BI system would require more development and testing.

For the six-hour constraint, a focused query engine was chosen because it:

* Is predictable
* Is easy to test
* Produces deterministic calculations
* Reduces the risk of incorrect business metrics

With more time, the query layer could be extended with a more sophisticated intent/classification system and clarification questions.

## 5. Business Intelligence Interpretation

The agent calculates business metrics from the live Monday.com data rather than returning raw records.

Examples include:

* Total deal count
* Total deal value
* Active pipeline
* Deal value by sector
* Deal value by stage
* Work-order completion rate
* Total billed value
* Total collected value
* Total receivable value

For pipeline analysis, active pipeline is interpreted using active sales/project stages while excluding clearly inactive stages such as lost, on-hold, and irrelevant opportunities.

This assumption was made to provide a more useful founder-level view of the pipeline.

## 6. Leadership Updates

I interpreted "leadership updates" as a concise executive snapshot containing the most important commercial and operational indicators.

The leadership summary combines:

* Number of deals
* Total recorded deal value
* Number of work orders
* Work-order completion rate
* Total billed amount
* Total collected amount
* Total receivable amount

The intention is to reduce the need for executives to manually inspect multiple Monday.com boards.

## 7. Error Handling

The system was tested against Monday.com connectivity and data retrieval.

The application is designed to handle:

* Authentication failures
* Missing data
* Empty fields
* Unsupported column types
* Invalid or unavailable values

The system avoids exposing API credentials in the source code.

## 8. Security

The Monday.com API token is stored in environment variables rather than source code.

For local development:

```text
backend/.env
```

For hosted deployment, the token is stored using deployment secrets.

The `.gitignore` file excludes:

```text
.env
venv/
__pycache__/
*.pyc
```

Therefore, sensitive credentials are not committed to the Git repository.

## 9. Deployment Decision

The application was deployed using Streamlit Community Cloud.

This was selected because:

* The application already uses Streamlit.
* It provides a publicly accessible prototype.
* GitHub integration simplifies deployment.
* Secrets can be configured separately from source code.

This satisfies the requirement that the evaluator should be able to test the prototype without performing a local setup.

## 10. What I Would Improve With More Time

With additional development time, I would add:

1. More advanced natural-language query understanding.
2. Automatic clarification questions for ambiguous requests.
3. Date and quarter filtering.
4. Historical pipeline and operational trends.
5. Interactive charts and dashboards.
6. More cross-board analysis.
7. More detailed data-quality reporting.
8. Automated leadership-report generation.
9. Additional validation and unit tests.
10. Better handling of synonyms and variations in business questions.

## 11. Overall Trade-off

The implementation prioritizes correctness, dynamic Monday.com integration, data resilience, and a working hosted prototype within the six-hour constraint.

Rather than attempting to build a highly complex AI system with limited testing time, the solution focuses on reliable founder-level business questions and transparent calculations.
