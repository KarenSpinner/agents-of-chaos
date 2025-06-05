# Experimental Content Creation Workflow with AI Agents Powered by Claude

This project simulates a collaborative content creation process for a B2B content agency. It uses Claude models to roleplay key team members: Account Manager, Writer, Editor, and Fact Checker. 

AI team members can make decisions at various points in the workflow and the fact checker can access Google Search through the SerpAPI. But they operate sequentially as part of a predetermined workflow. 

The code was created by ChatGPT and tested in my local environment. It's a work in progress--results will vary A LOT depending on how you tweak the prompts and which Claude models you choose. 

## Project Structure

```plaintext
.
├── agent_runner.py        # Sends prompts to Claude and returns structured JSON
├── workflow.py            # Orchestrates the agent interactions in sequence
├── prompts.py             # Stores role-specific system prompts
├── fact_checker.py        # Scrapes the web for source material using claims
├── utils.py               # Handles markdown file creation and sanitization
├── save_results.py        # Saves each step of the workflow to Markdown
├── run.py                 # Entry point to run the entire pipeline
├── .env                   # Stores your Claude API key (not tracked by Git)
└── README.md              # This file

**## Agents**

Each agent has a specialized role and voice, with strict response formats in JSON:

Account Manager
Reviews the client brief, asks for clarification, and summarizes for the writer.

Writer
Writes a 1,500+ word blog post in markdown, following brand tone and structure.

Editor
Checks for tone, structure, and alignment with the brief. Can iterate up to 3 times.

Fact Checker
Flags unsupported claims and suggests corrections backed by external sources.

**## Workflow Overview**

Start with a creative brief (creative_brief)

Account Manager reviews and may request clarifications

Writer produces a first draft

Editor reviews and may request revisions (up to 3 rounds)

Fact Checker identifies unverified claims and suggests corrections

Writer revises the draft based on fact-checker feedback

The final version is saved as a .md file

All output and intermediate feedback are saved as Markdown for easy review.

