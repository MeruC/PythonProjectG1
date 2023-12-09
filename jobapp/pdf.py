from fpdf import FPDF

name = "MEL VINCENT T. CARMELO"
rawdesc = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
desc = "\t\t\t\t\t\t\t\t\t\t" + rawdesc

class Work_Experience():
    def __init__(self, title, company, position, startDate, endDate) -> None:
        self.title = title
        self.company = company
        self.position = position
        self.startDate = startDate
        self.endDate = endDate
        
exp = Work_Experience("Title", "Company", "Position", "2020-01-01", "2022-01-01")
exp.title = "Work Title"
exp.company = "Company"
exp.position = "Position"
exp.startDate = "2020-01-01"
exp.endDate = "2022-01-01"

class PDF(FPDF):
    def header(self):
        self.set_fill_color(56, 102, 65)
        self.rect(0,0,210,40,style="F")
        self.image("jobapp/mel.png", 170, 8, 25)
        self.set_font("helvetica", "", 24)
        self.set_text_color(230,230,230)
        self.cell(0, 14, "", border=False, ln=1, align='L')
        self.cell(0, 4, name, border=False, ln=1, align='L')
        self.ln(20)

pdf = PDF('P', 'mm', 'A4')
#pdf.set_margins(0,0,0)

pdf.set_auto_page_break(auto=True, margin = 15)

#Add Page
pdf.add_page()

##About
pdf.set_font('helvetica', 'B', 20)
pdf.set_text_color(97,178,113)
pdf.cell(0, 5, "About", ln=True)

#Line Break
pdf.cell(0, 4, "", ln=True)
pdf.set_fill_color(0, 0, 0)
pdf.cell(190, 0.5, "", ln=True, fill=True)
pdf.cell(0, 4, "", ln=True)

#About Content
pdf.set_font('helvetica', '', 12)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 5, desc, align="J")

##Work Experience
pdf.cell(0, 8, "", ln=True)
pdf.set_font('helvetica', 'B', 20)
pdf.set_text_color(97,178,113)
pdf.cell(0, 5, "Work Experience", ln=True)

#Line Break
pdf.cell(0, 4, "", ln=True)
pdf.set_fill_color(0, 0, 0)
pdf.cell(190, 0.5, "", ln=True, fill=True)
pdf.cell(0, 4, "", ln=True)

#Works
for i in range(2):
    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, exp.title, ln=True)
    pdf.cell(10, 8, "")
    pdf.set_font('helvetica', '', 14)
    pdf.set_text_color(97,178,113)
    pdf.cell(40, 8, exp.company, ln=True)
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    date = exp.startDate + " to " + exp.endDate
    pdf.cell(10, 8, "")
    pdf.cell(40, 8, date, ln=True)
    pdf.set_text_color(50, 50, 50)
    if(i != 1):
        pdf.cell(0, 8, "--------------------------------------------------------------------------------------------------------------------------------------", ln=True, align="J")
#pdf.cell(40, 8, exp.position, ln=True)
#for works in exp:
    
##Education
pdf.cell(0, 8, "", ln=True)
pdf.set_font('helvetica', 'B', 20)
pdf.set_text_color(97,178,113)
pdf.cell(0, 5, "Education", ln=True)

#Line Break
pdf.cell(0, 4, "", ln=True)
pdf.set_fill_color(0, 0, 0)
pdf.cell(190, 0.5, "", ln=True, fill=True)
pdf.cell(0, 4, "", ln=True)

pdf.output("pdf_1.pdf")