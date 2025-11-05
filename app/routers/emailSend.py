from flask import request, jsonify, Blueprint
import os
import resend
import re
from dotenv import load_dotenv
import markdown

load_dotenv()
from xhtml2pdf import pisa
from datetime import datetime, timedelta, timezone
import base64
from io import BytesIO

emailSend = Blueprint("emailSend", __name__)


@emailSend.route("/a", methods=["GET"])
def hello_module1():
    return "Hello from Module emailSend"


@emailSend.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.json
        student_email = data.get("student_email")
        student_name = data.get("student_name")
        bcc_emails = data.get("bccEmail", [])
        cc_emails = data.get("ccEmail", [])
        report_history = data.get("report_history")
        contributionAnalysis = data.get("contributionAnalysis")
        hiddenReport = data.get("hiddenReport", None)
        report_info = data.get("report_info", None)
        student_number = data.get("student_number", None)
        section_number = data.get("section_number", None)

        # Validate essential fields
        if not student_email:
            return (
                jsonify({"success": False, "error": "Student email is required"}),
                400,
            )

        # Ensure cc/bcc are lists
        if isinstance(bcc_emails, str):
            bcc_emails = [bcc_emails]
        if isinstance(cc_emails, str):
            cc_emails = [cc_emails]

        # Combine CC and BCC list into one group (no distinction)
        admin_emails = list(
            set(cc_emails + bcc_emails)
        )  # remove duplicates just in case

        # Validate email format
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        all_emails = [student_email] + admin_emails
        for email in all_emails:
            if not re.match(email_pattern, email):
                return (
                    jsonify(
                        {"success": False, "error": f"Invalid email format: {email}"}
                    ),
                    400,
                )

        # Get API key
        Resend_API_KEY = os.getenv("RESEND_API_KEY")
        if not Resend_API_KEY:
            return (
                jsonify({"success": False, "error": "Resend API key not configured"}),
                500,
            )

        resend.api_key = Resend_API_KEY

        # ============================
        # 1️⃣ Send email to Student (without hiddenReport)
        # ============================
        html_content_student = report_history_to_html(
            report_history,
            contributionAnalysis,
            hiddenReport=None,
            student_name=student_name,
            student_email=student_email,
            report_info=report_info,
            student_number=student_number,
            section_number=section_number,
        )

        markdown_content_student = report_to_markdown(
            report_history,
            contributionAnalysis,
            hiddenReport=None,
            student_name=student_name,
            student_email=student_email,
            report_info=report_info,
            student_number=student_number,
            section_number=section_number,
        )

        params_student: resend.Emails.SendParams = {
            "from": "no-reply@hkbuchatbot.smartutor.me",
            "to": [student_email],
            "subject": "HKBU Chatbot Report",
            "html": create_email(html_content_student),
            "attachments": [
                {
                    "filename": "report.pdf",
                    "content": html_to_pdf(html_content_student),
                },
                {
                    "filename": "report.md",
                    "content": base64.b64encode(
                        markdown_content_student.encode("utf-8")
                    ).decode("utf-8"),
                },
            ],
        }

        resend.Emails.send(params_student)

        # ============================
        # 2️⃣ Send email to Admin/Observers (with hiddenReport)
        # ============================
        if admin_emails:
            html_content_full = report_history_to_html(
                report_history,
                contributionAnalysis,
                hiddenReport,  # include hidden content
                student_name,
                student_email,
                report_info=report_info,
                student_number=student_number,
                section_number=section_number,
            )

            markdown_content_full = report_to_markdown(
                report_history,
                contributionAnalysis,
                hiddenReport,
                student_name,
                student_email,
                report_info=report_info,
                student_number=student_number,
                section_number=section_number,
            )

            params_admin: resend.Emails.SendParams = {
                "from": "no-reply@hkbuchatbot.smartutor.me",
                "to": admin_emails,  # unified list for cc+bcc
                "subject": "HKBU Chatbot Report (Full Version)",
                "html": create_email(html_content_full),
                "attachments": [
                    {
                        "filename": "report_full.pdf",
                        "content": html_to_pdf(html_content_full),
                    },
                    {
                        "filename": "report_full.md",
                        "content": base64.b64encode(
                            markdown_content_full.encode("utf-8")
                        ).decode("utf-8"),
                    },
                ],
            }

            resend.Emails.send(params_admin)

        return jsonify({"success": True, "message": "Emails sent successfully!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


from datetime import datetime


def report_to_markdown(
    report_history,
    contributionAnalysis,
    hiddenReport,
    student_name,
    student_email,
    report_info,
    student_number,
    section_number,
):
    """Generate a well-formatted Markdown report from conversation and analysis data."""
    now = datetime.now()

    # --- Header Section ---
    md = f"""# HKBU LANG 0036 Learning Session Report

**Generated:** {now.strftime('%Y-%m-%d %H:%M:%S')}  
"""

    if student_name:
        md += f"**Student Name:** {student_name}  \n"

    md += f"""**Student Email:** {student_email}  
**Student Number:** {student_number}  
**Section:** {section_number}  

---

## Course Information and Student Background
"""
    md += report_info

    md += f"""

---

## Contribution Analysis

{contributionAnalysis}

"""

    # --- Hidden Report Section ---
    if hiddenReport:
        md += f"""---

## 🟤 Grading Result *(Hidden from Students)*

{hiddenReport}

"""

    # --- Conversation Log ---
    md += """---

## Complete Conversation
"""

    for msg in report_history:
        role = "You" if msg.get("role") == "user" else "Assistant"
        content = msg.get("content", "").strip()
        time = msg.get("timestamp", "")
        md += f"**{role}:** {content}\n\n*Time:* {time}\n\n"

    # --- Footer ---
    md += "---\n*Created by Dr. Simon Wang, Language Centre, HKBU*\n"

    return md


def create_email(html_content):
    email_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>HKBU Chatbot Report</title>
    <style>
        /* Reset default styles for email client consistency */
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            color: #333333;
            background-color: #f4f4f9;
            line-height: 1.6;
        }}
        * {{
            box-sizing: border-box;
        }}
        /* Container */
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            border-radius: 8px;
        }}
        /* Header */
        .header {{
            background-color: #003087;
            padding: 20px;
            text-align: center;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }}
        .header img {{
            max-width: 120px;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        .header h1 {{
            color: #ffffff;
            font-size: 24px;
            margin: 10px 0 0;
            font-weight: 600;
        }}
        /* Content */
        .content {{
            padding: 25px;
        }}
        .content p {{
            margin: 0 0 15px;
            font-size: 16px;
            color: #333333;
        }}
        .content h2 {{
            font-size: 20px;
            color: #003087;
            margin: 20px 0 10px;
        }}
        .content h3 {{
            font-size: 18px;
            color: #003087;
            margin: 15px 0 8px;
        }}
        .content ul, .content ol {{
            margin: 0 0 15px 20px;
            padding: 0;
        }}
        .content li {{
            margin-bottom: 8px;
            font-size: 16px;
        }}
        /* Button */
        .button {{
            display: inline-block;
            padding: 12px 24px;
            background-color: #003087;
            color: #ffffff !important;
            text-decoration: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 500;
            text-align: center;
            transition: background-color 0.3s;
        }}
        .button:hover {{
            background-color: #00205b;
        }}
        /* Footer */
        .footer {{
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666666;
            background-color: #f4f4f9;
            border-top: 1px solid #dcdcdc;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
        }}
        .footer a {{
            color: #003087;
            text-decoration: underline;
        }}
        /* Responsive Design */
        @media only screen and (max-width: 600px) {{
            .container {{
                width: 100% !important;
                border: none;
            }}
            .content {{
                padding: 15px;
            }}
            .header h1 {{
                font-size: 20px;
            }}
            .button {{
                width: 100%;
                box-sizing: border-box;
            }}
        }}
    </style>
</head>
<body>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f4f4f9;">
        <tr>
            <td align="center">
                <table role="presentation" class="container" width="100%" style="max-width: 600px;" cellspacing="0" cellpadding="0">
                    <tr>
                        <td class="header">
                            <h1>Chatbot Report</h1>
                        </td>
                    </tr>
                    <tr>
                        <td class="content">
                            <p>Dear Student,</p>
                            <p>Your learning session report is ready. Please find the attached files or view the details below.</p>
                            <hr>
                            {html_content}
                            <hr>
                            <p>Thank you for using the HKBU Chatbot. For any questions, please contact us at <a href="mailto:simonwang@hkbu.edu.hk">simonwang@hkbu.edu.hk</a>.</p>
                        </td>
                    </tr>
                    <tr>
                        <td class="footer">
                            <p>
                                Created by: Dr. Simon Wang, Innovation Officer<br>
                                Language Centre, Hong Kong Baptist University<br>
                                &copy; 2025 HKBU Chatbot
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """
    return email_template


def report_history_to_html(
    report_history,
    contributionAnalysis,
    hiddenReport,
    student_name,
    student_email,
    report_info,
    student_number,
    section_number,
):
    """Convert report history (with Markdown support) to HTML."""
    try:
        if not report_history or len(report_history) == 0:
            raise Exception("No conversation to export")

        # Calculate metadata
        now = datetime.now()

        # Create HTML header
        html_content = f"""
        <h1 style="text-align: center; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
            HKBU LANG 0036 Learning Session Report
        </h1>

        <div style="margin: 20px 0;">
            <p><strong>Generated:</strong> {now.strftime('%Y-%m-%d %H:%M:%S')}</p>"""

        if student_name:
            html_content += f"""<p><strong>Student Name:</strong> {student_name}</p>"""

        html_content += f"""
            <p><strong>Student Email:</strong> {student_email}</p>
            <p><strong>Student Number:</strong> {student_number}</p>
            <p><strong>Section:</strong> {section_number}</p>
        </div>
        """

        # --- Course Information ---
        html_content += """
        <h2 style="color: #34495e; margin-top: 30px;">Course Information and Student Background</h2>
        <div style="background: #eef5fb; padding: 15px; border-radius: 8px; margin: 10px 0;">
        """
        if isinstance(report_info, dict):
            html_content += "<ul style='list-style-type: none; padding-left: 0;'>"
            for key, value in report_info.items():
                html_content += (
                    f"<li><strong>{key}:</strong> {markdown.markdown(str(value))}</li>"
                )
            html_content += "</ul>"
        else:
            html_content += f"<p>{markdown.markdown(str(report_info))}</p>"
        html_content += "</div>"

        # --- Contribution Analysis ---
        html_content += """
        <h2 style="color: #34495e; margin-top: 30px;">Contribution Analysis</h2>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <p>{}</p>
        </div>
        """.format(
            markdown.markdown(contributionAnalysis)
        )

        # Include hidden grading report if applicable
        if hiddenReport:
            html_content += f"""
            <h2 style="color: #34495e; margin-top: 30px;">Grading Result (Hidden from students)</h2>
            <div style="background: #fff4f4; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <p>{markdown.markdown(hiddenReport)}</p>
            </div>
            """

        # Conversation section (timestamps removed)
        html_content += """
        <h2 style="color: #34495e; margin-top: 30px;">Complete Conversation</h2>
        """

        for msg in report_history:
            role = "You:" if msg.get("role") == "user" else "Assistant:"
            raw_content = msg.get("content", "")
            content_html = markdown.markdown(
                raw_content, extensions=["fenced_code", "tables", "nl2br"]
            )

            html_content += f"""
            <div style="margin: 15px 0; padding: 10px; border-left: 3px solid #3498db;">
                <p style="margin: 0 0 5px 0;"><strong>{role}</strong></p>
                <div style="margin: 0; line-height: 1.6;">{content_html}</div>
            </div>
            """

        # Add footer
        html_content += """
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; font-size: 12px; color: #666;">
            <p>Created by: Dr. Simon Wang, Innovation Officer</p>
            <p>Language Centre, Hong Kong Baptist University</p>
            <p>simonwang@hkbu.edu.hk</p>
        </div>
        """

        return html_content

    except Exception as e:
        raise Exception(f"Error generating HTML report: {str(e)}")


def report_md_to_md(report_md):
    """Convert markdown report to base64 encoded content for email attachment"""
    try:
        if not report_md:
            raise Exception("No markdown content provided")

        # Encode the markdown content as base64
        md_bytes = report_md.encode("utf-8")
        base64_content = base64.b64encode(md_bytes).decode("utf-8")
        return base64_content

    except Exception as e:
        raise Exception(f"Error processing markdown report: {str(e)}")


def html_to_pdf(html_content):
    """Convert HTML to PDF and return base64 encoded content"""
    try:
        # Create a complete HTML document with proper structure
        complete_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    margin: 20px;
                    padding: 0;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }}
                h1 {{
                    font-size: 24px;
                    text-align: center;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    font-size: 20px;
                    color: #34495e;
                }}
                h3 {{
                    font-size: 16px;
                    color: #7f8c8d;
                }}
                p {{
                    margin-bottom: 10px;
                }}
                div {{
                    margin-bottom: 10px;
                }}
                strong {{
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #666;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Create a BytesIO buffer for the PDF
        result = BytesIO()

        # Convert HTML to PDF using xhtml2pdf
        pdf = pisa.pisaDocument(BytesIO(complete_html.encode("utf-8")), result)

        if not pdf.err:
            # Get PDF content and encode as base64
            pdf_content = result.getvalue()
            result.close()
            base64_content = base64.b64encode(pdf_content).decode("utf-8")
            return base64_content
        else:
            result.close()
            raise Exception("Error generating PDF")

    except Exception as e:
        raise Exception(f"Error converting HTML to PDF: {str(e)}")
