from agent_runner import ask_agent
from fact_checker import search_web
from utils import save_raw_draft


def run_content_pipeline(creative_brief):
    print("\n🔷 Account Manager Reviewing Brief...")
    am_output = ask_agent("account_manager", creative_brief)
    print(am_output)

    # Human clarifies if needed
    if am_output.get("decision") == "revise":
        print("\n🧑‍💼 Account Manager Needs More Info:")
        print(am_output.get("comments", "[No comments provided]"))
        user_response = input("\n✍️ Enter your response to the Account Manager:\n")
        writer_input = (
            "Here is the original creative brief:\n\n"
            f"{creative_brief.strip()}\n\n"
            "And here are the client's clarifications based on your questions:\n\n"
            f"{user_response.strip()}"
        )
    else:
        writer_input = am_output.get("comments", creative_brief)

    print("\n🟢 Writer Drafting First Version...")
    writer_draft = ask_agent("writer", writer_input)["content"]
    print(writer_draft)

    save_raw_draft(writer_draft, filename="first_draft.md")

    # Editor review loop with reference to original brief
    current_draft = writer_draft
    final_editor_notes = None
    for round_num in range(1, 4):
        print(f"\n🟡 Editor Review Round {round_num}...")

        editor_prompt = (
            f"Here is the original creative brief to check against:\n\n{creative_brief.strip()}\n\n"
            f"And here is the current draft:\n\n{current_draft}"
        )
        editor_feedback = ask_agent("editor", editor_prompt)
        print(editor_feedback)

        if editor_feedback.get("decision") == "approve":
            print("✅ Editor approved the draft.")
            break

        print("📝 Writer revising based on feedback...")
        revision_prompt = (
            f"Editor Feedback:\n{editor_feedback['comments']}\n\n"
            f"Original Draft:\n{current_draft}"
        )
        current_draft = ask_agent("writer", revision_prompt)["content"]
        print(current_draft)

        save_raw_draft(current_draft, filename=f"editor_round_{round_num}_revision.md")
        final_editor_notes = editor_feedback

    revised_draft = current_draft

    print("\n🔍 Fact Checker Reviewing Revised Draft...")
    fact_check_result = ask_agent("fact_checker", revised_draft)
    print(fact_check_result)

    if fact_check_result.get("decision") == "revise":
        print("\n🕵️ Fact Checker flagged issues. Searching the web...")

        sources_by_claim = {}
        for claim in fact_check_result.get("claims", []):
            print(f"\n🔎 {claim}")
            sources_by_claim[claim] = search_web(claim)

        fact_feedback_md = "# 🕵️ Fact Checker Feedback\n\n"
        fact_feedback_md += f"**Reason:** {fact_check_result.get('reason')}\n\n"
        fact_feedback_md += f"**Comments:** {fact_check_result.get('comments')}\n\n"
        fact_feedback_md += "## Sources per Claim\n"

        for claim, sources in sources_by_claim.items():
            fact_feedback_md += f"\n### {claim}\n{sources}\n"

        save_raw_draft(fact_feedback_md, filename="fact_checker_feedback.md")

        writer_fact_prompt = (
            f"The fact checker flagged several issues in your draft. "
            f"Please revise the piece using the comments and supporting sources below.\n\n"
            f"{fact_feedback_md}\n\n"
            f"---\n\nHere is the current draft:\n\n{revised_draft}"
        )

        final_draft = ask_agent("writer", writer_fact_prompt)["content"]
        print("\n📝 Writer Submitted Fact-Checked Revision")
    else:
        print("\n✅ Fact Checker approved the draft.")
        final_draft = revised_draft

    save_raw_draft(final_draft, filename="final_draft.md")

    return {
        "brief": writer_input,
        "first_draft": writer_draft,
        "editor_feedback": editor_feedback,
        "revised_draft": revised_draft,
        "fact_check_result": fact_check_result,
        "final_editor_notes": final_editor_notes,
        "final_draft": final_draft
    }

