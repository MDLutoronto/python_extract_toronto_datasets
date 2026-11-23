import pandas as pd 
import os

path = "../../_Search_SLA/SLA_odesi_applicants/"

files = os.listdir(path)
output = []

for file in files:
    name = file[5:]
    name = name[:-4]
    pos = name.rfind('-')+1
    surname = name[0:pos-1]
    firstname = name[pos:]
    result = {"surname":surname, "firstname":firstname, "filename":file}
    output.append(result)

df_result = pd.DataFrame(output)
df_result.to_excel(path+"2026_sla_applications.xlsx")

    

