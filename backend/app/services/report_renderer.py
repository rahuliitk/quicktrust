"""PDF and CSV report rendering for QuickTrust GRC reports.

Supports report types: compliance_summary, risk_report, evidence_audit,
training_completion.
"""

from __future__ import annotations

import csv
import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)


# ---------------------------------------------------------------------------
# PDF rendering
# ---------------------------------------------------------------------------

def render_pdf(report_data: dict, report_type: str) -> bytes:
    """Generate a PDF document from *report_data* and return raw bytes."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=20,
        spaceAfter=20,
        textColor=colors.HexColor("#1a237e"),
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=16,
        spaceAfter=8,
        textColor=colors.HexColor("#283593"),
    )
    body_style = styles["BodyText"]

    elements: list = []

    # Title
    title_map = {
        "compliance_summary": "Compliance Summary Report",
        "risk_report": "Risk Assessment Report",
        "evidence_audit": "Evidence Audit Report",
        "training_completion": "Training Completion Report",
    }
    title = title_map.get(report_type, "Report")
    elements.append(Paragraph(title, title_style))

    # Metadata
    generated_at = report_data.get("generated_at", datetime.utcnow().isoformat())
    elements.append(Paragraph(f"Generated: {generated_at}", body_style))
    elements.append(Spacer(1, 12))

    # Build sections based on report type
    if report_type == "compliance_summary":
        elements.extend(_build_compliance_summary_pdf(report_data, heading_style, body_style))
    elif report_type == "risk_report":
        elements.extend(_build_risk_report_pdf(report_data, heading_style, body_style))
    elif report_type == "evidence_audit":
        elements.extend(_build_evidence_audit_pdf(report_data, heading_style, body_style))
    elif report_type == "training_completion":
        elements.extend(_build_training_completion_pdf(report_data, heading_style, body_style))

    doc.build(elements)
    return buf.getvalue()


def _make_table(headers: list[str], rows: list[list], col_widths: list[float] | None = None) -> Table:
    """Create a styled table with header row."""
    data = [headers] + rows
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a237e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f5f5f5")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdbdbd")),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return table


def _build_compliance_summary_pdf(data: dict, heading: ParagraphStyle, body: ParagraphStyle) -> list:
    elements: list = []

    # Control stats
    ctrl = data.get("control_stats", {})
    if ctrl:
        elements.append(Paragraph("Control Status", heading))
        rows = [
            ["Total Controls", str(ctrl.get("total", 0))],
            ["Implemented", str(ctrl.get("implemented", 0))],
            ["Draft", str(ctrl.get("draft", 0))],
        ]
        elements.append(_make_table(["Metric", "Count"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    # Risk stats
    risk = data.get("risk_stats", {})
    if risk:
        elements.append(Paragraph("Risk Overview", heading))
        rows = [[str(k), str(v)] for k, v in risk.items()]
        elements.append(_make_table(["Metric", "Value"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    # Policy stats
    pol = data.get("policy_stats", {})
    if pol:
        elements.append(Paragraph("Policy Status", heading))
        rows = [
            ["Total Policies", str(pol.get("total", 0))],
            ["Published", str(pol.get("published", 0))],
        ]
        elements.append(_make_table(["Metric", "Count"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    # Evidence stats
    ev = data.get("evidence_stats", {})
    if ev:
        elements.append(Paragraph("Evidence Collection", heading))
        rows = [["Total Evidence Items", str(ev.get("total", 0))]]
        elements.append(_make_table(["Metric", "Count"], rows, [3.5 * inch, 2 * inch]))

    return elements


def _build_risk_report_pdf(data: dict, heading: ParagraphStyle, body: ParagraphStyle) -> list:
    elements: list = []

    risk = data.get("risk_stats", {})
    if risk:
        elements.append(Paragraph("Risk Statistics", heading))
        rows = [[str(k), str(v)] for k, v in risk.items()]
        elements.append(_make_table(["Metric", "Value"], rows, [3.5 * inch, 2 * inch]))

    return elements


def _build_evidence_audit_pdf(data: dict, heading: ParagraphStyle, body: ParagraphStyle) -> list:
    elements: list = []

    ctrl = data.get("control_stats", {})
    if ctrl:
        elements.append(Paragraph("Controls Covered", heading))
        rows = [
            ["Total Controls", str(ctrl.get("total", 0))],
            ["Implemented", str(ctrl.get("implemented", 0))],
            ["Draft", str(ctrl.get("draft", 0))],
        ]
        elements.append(_make_table(["Metric", "Count"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    ev = data.get("evidence_stats", {})
    if ev:
        elements.append(Paragraph("Evidence Summary", heading))
        rows = [["Total Evidence Items", str(ev.get("total", 0))]]
        elements.append(_make_table(["Metric", "Count"], rows, [3.5 * inch, 2 * inch]))

    return elements


def _build_training_completion_pdf(data: dict, heading: ParagraphStyle, body: ParagraphStyle) -> list:
    elements: list = []

    ts = data.get("training_stats", {})
    if ts:
        elements.append(Paragraph("Training Completion", heading))
        rows = [
            ["Total Assignments", str(ts.get("total_assignments", 0))],
            ["Completed", str(ts.get("completed", 0))],
            ["Completion Rate", f"{ts.get('completion_rate', 0)}%"],
        ]
        elements.append(_make_table(["Metric", "Value"], rows, [3.5 * inch, 2 * inch]))

    return elements


# ---------------------------------------------------------------------------
# CSV rendering
# ---------------------------------------------------------------------------

def render_csv(report_data: dict, report_type: str) -> bytes:
    """Generate a CSV file from *report_data* and return raw bytes (UTF-8)."""
    buf = io.StringIO()
    writer = csv.writer(buf)

    if report_type == "compliance_summary":
        _write_compliance_summary_csv(writer, report_data)
    elif report_type == "risk_report":
        _write_risk_report_csv(writer, report_data)
    elif report_type == "evidence_audit":
        _write_evidence_audit_csv(writer, report_data)
    elif report_type == "training_completion":
        _write_training_completion_csv(writer, report_data)
    else:
        # Fallback: dump all top-level keys as rows
        writer.writerow(["Key", "Value"])
        for key, value in report_data.items():
            writer.writerow([key, str(value)])

    return buf.getvalue().encode("utf-8")


def _write_compliance_summary_csv(writer: csv.writer, data: dict) -> None:
    writer.writerow(["Section", "Metric", "Value"])

    generated_at = data.get("generated_at", "")
    writer.writerow(["Metadata", "Generated At", generated_at])

    ctrl = data.get("control_stats", {})
    if ctrl:
        writer.writerow(["Controls", "Total", ctrl.get("total", 0)])
        writer.writerow(["Controls", "Implemented", ctrl.get("implemented", 0)])
        writer.writerow(["Controls", "Draft", ctrl.get("draft", 0)])

    risk = data.get("risk_stats", {})
    if risk:
        for k, v in risk.items():
            writer.writerow(["Risk", k, v])

    pol = data.get("policy_stats", {})
    if pol:
        writer.writerow(["Policies", "Total", pol.get("total", 0)])
        writer.writerow(["Policies", "Published", pol.get("published", 0)])

    ev = data.get("evidence_stats", {})
    if ev:
        writer.writerow(["Evidence", "Total", ev.get("total", 0)])


def _write_risk_report_csv(writer: csv.writer, data: dict) -> None:
    writer.writerow(["Metric", "Value"])

    generated_at = data.get("generated_at", "")
    writer.writerow(["Generated At", generated_at])

    risk = data.get("risk_stats", {})
    if risk:
        for k, v in risk.items():
            writer.writerow([k, v])


def _write_evidence_audit_csv(writer: csv.writer, data: dict) -> None:
    writer.writerow(["Section", "Metric", "Value"])

    generated_at = data.get("generated_at", "")
    writer.writerow(["Metadata", "Generated At", generated_at])

    ctrl = data.get("control_stats", {})
    if ctrl:
        writer.writerow(["Controls", "Total", ctrl.get("total", 0)])
        writer.writerow(["Controls", "Implemented", ctrl.get("implemented", 0)])
        writer.writerow(["Controls", "Draft", ctrl.get("draft", 0)])

    ev = data.get("evidence_stats", {})
    if ev:
        writer.writerow(["Evidence", "Total", ev.get("total", 0)])


def _write_training_completion_csv(writer: csv.writer, data: dict) -> None:
    writer.writerow(["Metric", "Value"])

    generated_at = data.get("generated_at", "")
    writer.writerow(["Generated At", generated_at])

    ts = data.get("training_stats", {})
    if ts:
        writer.writerow(["Total Assignments", ts.get("total_assignments", 0)])
        writer.writerow(["Completed", ts.get("completed", 0)])
        writer.writerow(["Completion Rate (%)", ts.get("completion_rate", 0)])
