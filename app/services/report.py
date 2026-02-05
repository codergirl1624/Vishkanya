from fpdf import FPDF
import os


def clean_text(text):
    """Remove unsupported Unicode characters"""
    return text.encode("ascii", "ignore").decode()


def generate_pdf_report(evidence: dict):
    """Generate FIR style PDF report"""

    # Create logs folder
    os.makedirs("logs", exist_ok=True)

    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, "VISH-KANYA Scam Evidence Report", ln=True)
    pdf.ln(10)

    # Transcript (safe)
    transcript = evidence["transcript"].replace("₹", "Rs.")
    pdf.multi_cell(0, 10, "Transcript:")
    pdf.multi_cell(0, 10, clean_text(transcript))
    pdf.ln(5)

    # Risk Level
    pdf.cell(200, 10, f"Risk Level: {evidence['risk_level']}", ln=True)

    # Extracted UPI IDs
    pdf.cell(
        200,
        10,
        f"UPI IDs Found: {evidence['extracted_entities']['upi_ids']}",
        ln=True
    )

    # Evidence Hash
    pdf.multi_cell(0, 10, f"Evidence Hash: {evidence['evidence_hash']}")

    # Save PDF
    filename = "logs/FIR_Report.pdf"
    pdf.output(filename)

    return filename

