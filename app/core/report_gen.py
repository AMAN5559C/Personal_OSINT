from fpdf import FPDF
import os
import time
import tempfile

class OSINTReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Kallen Sentinel - Professional Report', new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def create_pdf_report(target_image_path, matches_data):
    # Initialize PDF with modern fpdf2 syntax support
    pdf = OSINTReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # -- 1. SUMMARY SECTION --
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Scan Date: {time.strftime('%Y-%m-%d %H:%M:%S')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Total Positive Matches: {len(matches_data)}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # -- 2. TARGET IMAGE --
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Target Subject:", new_x="LMARGIN", new_y="NEXT")
    try:
        # Fixed width 40mm, height auto-calculated
        pdf.image(target_image_path, x=pdf.get_x(), y=pdf.get_y()+5, w=40)
        pdf.ln(55) # Move cursor down past the image area
    except:
        pdf.cell(0, 10, "[Image Error]", new_x="LMARGIN", new_y="NEXT")

    # -- 3. FINDINGS --
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Intelligence Findings:", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    if not matches_data:
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "No matches found on targeted URLs.", new_x="LMARGIN", new_y="NEXT")
    else:
        for i, match in enumerate(matches_data, 1):
            # Header for this match
            pdf.set_font("Arial", 'B', 11)
            pdf.set_fill_color(240, 240, 240) # Light gray
            pdf.cell(0, 8, f" Match #{i} [Confidence: {match['confidence']}%]", new_x="LMARGIN", new_y="NEXT", fill=True)
            
            # Details using simple multi_cell with forced width to avoid "not enough space" error
            pdf.set_font("Courier", size=8) # Courier handles long unbroken URLs better visually
            
            pdf.write(5, f"Source: {match['source_site']}")
            pdf.ln(6)
            pdf.write(5, f"Image:  {match['image_url']}")
            pdf.ln(6)
            pdf.write(5, f"Time:   {match['timestamp']}")
            pdf.ln(10) # Extra space between entries

    # -- 4. SAVE REPORT --
    report_path = os.path.join(tempfile.gettempdir(), f"Kallen_Report_{int(time.time())}.pdf")
    pdf.output(report_path)
    return report_path