import pandas as pd
import os

# This Is The Function That Generates the Excel File Sheet
def generate_excel(data_dict_mapping, excel_file_name='demo'):
    df = pd.DataFrame(data_dict_mapping)
    # print df.head()
    df.to_excel(excel_file_name+".xlsx", sheet_name="sheet1")
    os.startfile(excel_file_name+".xlsx")


"""
address = list()
contact = list()
id = list()
name = list()

result =  list(sup.execute('SELECT * FROM suppliers'))
# category = list(cat.execute('SELECT * FROM categories'))

# This Is How I have to format my input dict
for v in result:
    address.append(v.get('address'))
    contact.append(int(v.get('contact')))
    id.append(int(v.get('id')))
    name.append(v.get('name'))
data_dict = {
    '1_ID': id,
    '2_Name': name,
    '3_Address': address,
    '4_Contact': contact
}

# exit()

generate_excel(data_dict, excel_file_name="supplier_report4")
os.startfile("supplier_report4.xlsx")

print "Done"

"""


