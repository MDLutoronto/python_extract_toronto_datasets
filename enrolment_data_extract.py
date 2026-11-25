import pandas as pd

# CONFIGURE 
DATA_PATH = ".\\data_sources\\enrolment_stats\\"
COLLEGE_FILE = "college_enrolment_headcount_2024-25.xlsx"
UNIVERSITY_FILE = "university_enrolment_headcount_2024-25.xlsx"
COLLEGES = ['Centennial College','Collège Boréal','George Brown College','Humber College','Seneca College']
UNIVERSITIES = ['Metropolitan','OCADU','Toronto','UOF','York']

FILETAG = "Toronto"         # What tag to include in the filename
FOLDER = ".\\datasets\\"          # Folder where output files go

def get_matches(df,condition=''):
    df_result = pd.DataFrame()
    key = ''
    value = ''
    test = ''
    if len(condition)>0 and condition.find('=') > -1:
        key,value = condition.split('=')        
        test = df[key]==str(value)
        df_result = df[test]
    return df_result
    

def get_year_data(df,year):
    df_result = pd.DataFrame()
    test = df['REF_DATE'] == year
    df_result = df[test]
    return df_result


df_uni = pd.read_excel(f'{DATA_PATH}{UNIVERSITY_FILE}','Status')
df_college = pd.read_excel(f'{DATA_PATH}{COLLEGE_FILE}','Status')
df_result = pd.DataFrame()

for uni in UNIVERSITIES:
    filter = df_uni['Institution'] == uni
    df_new = df_uni[filter]
    df_result = pd.concat([df_result,df_new])

df_result.to_csv(f'{DATA_PATH}Toronto_{UNIVERSITY_FILE[:-4]}.csv')
df_result.to_excel(f'{DATA_PATH}Toronto_{UNIVERSITY_FILE}')

df_col_result = pd.DataFrame()
for col in COLLEGES:
    filter = df_college['College Name'] == col
    df_new = df_college[filter]
    df_col_result = pd.concat([df_col_result,df_new])
df_col_result.rename(columns={'College Name':'Institution'},inplace=True)
df_col_result.to_csv(f'{DATA_PATH}Toronto_{COLLEGE_FILE[:-4]}.csv')
df_col_result.to_excel(f'{DATA_PATH}Toronto_{COLLEGE_FILE}')

df_combined = pd.concat([df_result,df_col_result])
df_combined.to_csv(f'{DATA_PATH}Toronto_PostSecondary_Enrolment.csv')
