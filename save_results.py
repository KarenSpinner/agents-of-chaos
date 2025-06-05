import json

def save_to_markdown(results_dict, output_file="blog_draft_report.md"):
    with open(output_file, "w") as f:
        for section, content in results_dict.items():
            f.write(f"# {section.replace('_', ' ').title()}\n\n")
            
            if isinstance(content, dict):
                # Pretty-print JSON content
                f.write("```json\n")
                f.write(json.dumps(content, indent=2))
                f.write("\n```\n\n")
            else:
                # Write regular string content
                f.write(content.strip() + "\n\n")
            
            f.write("---\n\n")