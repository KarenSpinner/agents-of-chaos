# run.py
from workflow import run_content_pipeline
from save_results import save_to_markdown

# Load the creative brief from a Markdown file
with open("brief.md", "r") as f:
    creative_brief = f.read()

# Run the pipeline
results = run_content_pipeline(creative_brief)

# Save output to markdown
save_to_markdown(results, output_file="blog_draft_report.md")