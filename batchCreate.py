from fpdf import FPDF
import pandas as pd

LINE_SPACE = 10
pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=False, margin=0)

df = pd.read_csv("topics.csv")

for _, row in df.iterrows():
    # Add header
    pdf.add_page()
    pdf.set_font(family="Times", style="B", size=24)
    pdf.set_text_color(100,100,100)
    pdf.cell(w=0, h=12, txt=row["Topic"], align="L", ln=1)
    pdf.line(10,22,200,22)

    # Add line for pages
    y = 22
    for i in range(26):
        y += LINE_SPACE
        pdf.line(10,y,200,y)
    # Add footer
    pdf.ln(265)
    pdf.set_font(family="Times", style="I", size=8)
    pdf.set_text_color(100,100,100)
    pdf.cell(w=0, h=10, txt=row["Topic"], align="R")

    for _ in range(int(row["Pages"] - 1)):
        pdf.add_page()
        # Add line for pages
        y = 22
        for i in range(26):
            y += LINE_SPACE
            pdf.line(10,y,200,y)
        # Addd footer
        pdf.ln(272)
        pdf.set_text_color(100,100,100)
        pdf.cell(w=0, h=10, txt=row["Topic"], align="R")



pdf.output("output.pdf")

