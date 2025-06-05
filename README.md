# Content Creation Workflow with Simplified AI Agents Powered by Claude

This project simulates a collaborative content creation process for a B2B content agency. It uses Claude models to roleplay key team members: Account Manager, Writer, Editor, and Fact Checker. 

AI team members can make decisions at various points in the process and the fact checker can access Google Search through the SerpAPI. But they operate sequentially as part of a predetermined workflow; they are not always on and do not operate concurrently.

The code was created by ChatGPT and tested in my local environment. It's a work in progress--there is major room for improvement--and results will vary A LOT depending on how you tweak the prompts and which Claude models you choose. 

## Project structure

```plaintext

├── agent_runner.py        # Sends prompts to Claude and returns structured JSON
├── workflow.py            # Orchestrates the agent interactions in sequence
├── prompts.py             # Stores role-specific system prompts
├── fact_checker.py        # Scrapes the web for source material using claims
├── utils.py               # Handles markdown file creation and sanitization
├── save_results.py        # Saves each step of the workflow to Markdown
├── run.py                 # Entry point to run the entire pipeline
├── brief.md               # Saved copy of the brief the writer is expected to follow
├── .env                   # Stores your Claude API key (not tracked by Git)

└── README.md              # This file

```

## Agents

Each agent has a specialized role and voice, with strict response formats in JSON:

**Account Manager**
Reviews the client brief, asks for clarification, and summarizes for the writer.

**Writer**
Writes a 1,500+ word blog post in markdown, following brand tone and structure.

**Editor**
Checks for tone, structure, and alignment with the brief. Can iterate up to 3 times.

**Fact Checker**
Flags unsupported claims and suggests corrections backed by external sources.

## Workflow overview

Start with a creative brief (creative_brief)

Account Manager reviews and may request clarifications.

Writer produces a first draft.

Editor reviews and may request revisions (up to 3 rounds).

Fact Checker identifies unverified claims and suggests corrections.

Writer revises the draft based on fact-checker feedback.

All output and intermediate feedback are saved as Markdown for easy review.

## Set up

You will need API keys from Anthropic and SerpAPI. These should be stored in a .env file. *Never put API keys directly in your code!*

Your .env file should look like this: 
ANTHROPIC_API_KEY=YOUR KEY HERE
SERP_API_KEY=YOUR KEY HERE

You will need to install Python and these libraries: anthropic, python-dotenv, requests, and serpapi

Ask your favorite LLM how to access the command line and install Python on your machine. Once that's done, libraries can be installed as follows:

pip install anthropic python-dotenv requests serpapi 

If you want to **customize the prompts** and tweak the agents' instructions and personalities, edit **prompt.py** 

If you want to update the assignment, edit **brief.md** Otherwise the workflow will run for the default project--an atyicle on how to edit AI-generated text. 😄

## Start the workflow

You can run the workflow from the command line like this:
python run.py

Let me know how it goes!
