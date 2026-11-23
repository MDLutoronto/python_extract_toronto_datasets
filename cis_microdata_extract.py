import pandas as pd
import zipfile as zf


# CONFIGURE 
FORM = "CIS"
DATA_PATH = f".\\data_sources\\{FORM.lower()}\\"
FILENAME = "18100273"
FILTER = "GEO=Toronto, Ontario" # Locate Toronto data
FILETAG = "Toronto"         # What tag to include in the filename
FOLDER = ".\\datasets\\"    # Folder where output files go
COMP_ONLY = True            # Comp

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

def divide_by_year(df):
    year_col = []
    for entry in df.itertuples():
        text = str(entry.REF_DATE)
        year,month = text.split('-')
        year_col.append(year)
    df['YEAR'] = year_col
    return df

def get_year_data(df,year):
    df_result = pd.DataFrame()    
    test = df['YEAR'] == year
    df_result = df[test]
    return df_result


df_main = pd.read_csv(f'{DATA_PATH}{FILENAME}.csv')
df_final = get_matches(df_main,FILTER)

print(df_final)
df_years = divide_by_year(df_final)
year_list = set(df_years['YEAR'])

df_final.to_csv(f'{FOLDER}{FORM}_{FILETAG}_Combined_{min(year_list)}-{max(year_list)}.csv')

print(year_list)
for year in year_list:
    print(f'{year} file printing')
    df_year = get_year_data(df_final,year)
    df_year.to_csv(f'{FOLDER}{FORM}_{FILETAG}_{year}.csv')


