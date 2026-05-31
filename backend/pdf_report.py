from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

import os


def generate_candidate_report(

    candidate,

    output_path
):

    doc = SimpleDocTemplate(
        output_path
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Recruiter Candidate Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"<b>Candidate:</b> {candidate['filename']}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Final Score:</b> {candidate['match_score']}%",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Semantic Score:</b> {candidate['semantic_score']}%",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Skill Match:</b> {candidate['skill_score']}%",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Recommendation:</b> {candidate['recommendation']}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 15)
    )

    content.append(
        Paragraph(
            "<b>Matched Skills</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            ", ".join(
                candidate["matched_skills"]
            ),
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 10)
    )

    content.append(
        Paragraph(
            "<b>Missing Skills</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            ", ".join(
                candidate["missing_skills"]
            ),
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 15)
    )

    content.append(
        Paragraph(
            "<b>AI Recruiter Analysis</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            candidate["analysis"],
            styles["BodyText"]
        )
    )

    doc.build(content)

    return output_path