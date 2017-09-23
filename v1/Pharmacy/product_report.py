import subprocess
from datetime import date
from category import *
from fpdf import FPDF, HTMLMixin
import glob
import os

def create_table(sorted_list ,data_dict, category_dic):

    header = """
    
    <br />
    <br />
    
    """

    i = 1

    td = ""
    for key in sorted_list:
        if i % 2 == 1:
            td += """
                <tr>
                    <td align="center" bgcolor="#b3e5fc">%i</td>
                    <td align="center" bgcolor="#b3e5fc">%s</td>
                    <td align="center" bgcolor="#b3e5fc">%s</td>
                    <td align="center" bgcolor="#b3e5fc">%s</td>
                    <td align="center" bgcolor="#b3e5fc">%s</td>
                    <td align="center" bgcolor="#b3e5fc">%s</td>
                    <td align="center" bgcolor="#b3e5fc">%s</td>
                    <td align="center" bgcolor="#b3e5fc">%s</td>
                </tr>
                """ % (i, data_dict.get(key)['brandname'], data_dict.get(key)['genericname'], data_dict.get(key)['quantityperunit'],
                       data_dict.get(key)['unitprice'], category_dic.get(str(data_dict.get(key)['category_id']))['name'] , data_dict.get(key)['expiry_date'],
                       data_dict.get(key)['status'])
        else:
            td += """
                <tr>
                    <td align="center" bgcolor="#81d4fa">%d</td>
                    <td align="center" bgcolor="#81d4fa">%s</td>
                    <td align="center" bgcolor="#81d4fa">%s</td>
                    <td align="center" bgcolor="#81d4fa">%s</td>
                    <td align="center" bgcolor="#81d4fa">%s</td>
                    <td align="center" bgcolor="#81d4fa">%s</td>
                    <td align="center" bgcolor="#81d4fa">%s</td>
                    <td align="center" bgcolor="#81d4fa">%s</td>
                </tr>
                """ % (i, data_dict.get(key)['brandname'], data_dict.get(key)['genericname'], data_dict.get(key)['quantityperunit'],
                       data_dict.get(key)['unitprice'], category_dic.get(str(data_dict.get(key)['category_id']))['name'], data_dict.get(key)['expiry_date'],
                       data_dict.get(key)['status'])
        i += 1

    table = """
    <table border="1"  width="100%">
    
        <thead>
            <tr>
                <th width="5%" bgcolor="#00b0ff">ID</th>
                <th width="16%" bgcolor="#00b0ff">Brand Name</th>
                <th width="16%" bgcolor="#00b0ff">Generic Name</th>
                <th width="10%" bgcolor="#00b0ff">Qty/Unit</th>
                <th width="15%" bgcolor="#00b0ff">Unit Price</th>
                <th width="15%" bgcolor="#00b0ff">Category</th>
                <th width="15%" bgcolor="#00b0ff">Expiry Date</th>
                <th width="8%" bgcolor="#00b0ff">Status</th>
                
            </tr>
        </thead>
        
        <tbody>
            {}
        </tbody>
    
    </table>
    """.format(td)
    return header+table

def open_pdf(pdf):
    # C:\Program Files (x86)\Foxit Software\Foxit Reader\FoxitReader.exe
    cmd = 'C:\Program Files (x86)\Foxit Software\Foxit Reader\FoxitReader.exe'
    cmd = """ "{}" "{}" """.format(cmd, pdf)
    subprocess.call(cmd, shell=True)
    # os.system(cmd)

class MyFPDF(FPDF, HTMLMixin):
    # Page footer
    def footer(self):
        self.set_y(-20)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Add Text
        self.cell(10, 10, 'Pharmacy Management System')
        # move to the right
        self.cell(150)
        # Add Text
        self.cell(10, 10, 'Copyright I3M')
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def generate_pdf(sorted_list,table_dict, category_dic):
    pdf = MyFPDF()
    # {nb} variable
    pdf.alias_nb_pages()
    # First page
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    # Logo
    pdf.image('img/boy-512.png', 10, 8, 33)
    # Arial bold 15
    pdf.set_font('Arial', 'B', 15)
    # Move to the right
    pdf.cell(80)
    # Title
    pdf.set_text_color(114, 176, 239)
    pdf.cell(30, 10, 'I3m Pharmacy Management System', 0, 0, 'C')
    # Move to the right
    pdf.cell(50)
    # side text
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 10, '%s'%(date.today()), 0, 0)
    # next line
    pdf.ln()
    # Move to the right
    pdf.cell(80)
    pdf.set_font('Arial', 'B', 15)
    pdf.set_text_color(63, 150, 238)
    pdf.cell(30, 10, 'General Report', 0, 0, 'C')
    # next line
    pdf.ln()
    # Move to the right
    pdf.cell(80)
    pdf.set_font('Arial', 'B', 25)
    pdf.set_text_color(27, 128, 232)
    pdf.cell(30, 10, 'Products Report', 0, 0, 'C')

    # Line break
    pdf.ln(20)

    pdf.write_html(create_table(sorted_list, table_dict, category_dic))

    save_dir = 'reports\\product\\'
    f = glob.glob(save_dir+'*.pdf')
    pdf_file = save_dir+'%s_No%d.pdf'%(date.today(), len(f)+1)

    pdf.output(pdf_file, 'F')

    open_pdf(os.path.abspath(pdf_file))
