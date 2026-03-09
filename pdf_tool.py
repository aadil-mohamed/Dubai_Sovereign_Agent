import os
from fpdf import FPDF
import json

class PropIQDossier(FPDF):
    def header(self):
        # Professional Header
        self.set_fill_color(10, 14, 26) # Deep Navy
        self.rect(0, 0, 210, 30, 'F')
        self.set_y(12)
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(201, 168, 76) # Dubai Gold
        self.cell(0, 0, 'PropIQ UAE - Sovereign Intelligence Brief', 0, 1, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_investment_dossier(state_data: dict, filename="Investment_Dossier.pdf"):
    """
    Takes the LangGraph state dictionary and formats it into a professional PDF.
    """
    print("📄 PDF Engine: Compiling Investment Dossier...")
    
    pdf = PropIQDossier()
    pdf.add_page()
    
    # 1. Target Property Details
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(10, 14, 26)
    pdf.cell(0, 10, 'Target Property Profile', 0, 1)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 6, f"Location: {state_data.get('area', 'N/A')}", 0, 1)
    pdf.cell(0, 6, f"Configuration: {state_data.get('bedrooms', 'N/A')} Bedroom(s)", 0, 1)
    pdf.cell(0, 6, f"Client Budget: AED {state_data.get('budget_aed', 0):,.2f}", 0, 1)
    pdf.ln(5)
    
    # 2. Executive Summary (From Supervisor)
    try:
        final_verdict = json.loads(state_data.get('final_verdict', '{}'))
    except:
        final_verdict = {}
        
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, f"Investment Grade: {final_verdict.get('investment_grade', 'N/A')}", 0, 1)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, final_verdict.get('executive_summary', 'No summary generated.'))
    pdf.ln(5)
    
    # 3. Financial & Visual Analysis
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Quantitative & Visual Analysis', 0, 1)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 6, f"Computed ML Valuation: AED {state_data.get('ml_price', 0):,.2f}", 0, 1)
    pdf.cell(0, 6, f"CV Luxury Premium Applied: {state_data.get('cv_multiplier', 1.0)}x", 0, 1)
    pdf.ln(5)
    
    # 4. Market Comparables (Scraped)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Live Market Comparables', 0, 1)
    
    pdf.set_font('Helvetica', '', 10)
    for idx, listing in enumerate(state_data.get('listings', [])[:3], 1):
        pdf.multi_cell(0, 6, f"{idx}. {listing.get('title', 'Property')} \nLink: {listing.get('url', 'N/A')}")
        pdf.ln(2)
        
    # Generate the physical file
    pdf.output(filename)
    print(f"✅ PDF Engine: Dossier saved successfully as {filename}")
    return filename

# --- Quick Diagnostic Test ---
if __name__ == "__main__":
    # Mock data to test the PDF generation
    mock_state = {
        "area": "Downtown Dubai",
        "bedrooms": 3,
        "budget_aed": 4500000,
        "ml_price": 8578720.62,
        "cv_multiplier": 1.25,
        "final_verdict": '{"investment_grade": "B", "executive_summary": "Property is overvalued compared to budget but possesses strong fundamentals."}',
        "listings": [{"title": "Luxury 3 Bed in Burj Khalifa", "url": "https://bayut.com/fake-link"}]
    }
    generate_investment_dossier(mock_state, "Test_Dossier.pdf")