import pandas as pd
import zipfile as zf


# CONFIGURE 
YEAR_START = 2015
YEAR_END = 2026
FILTER = "PROV=35"            # CMA=4 is Toronto, PROV=35 is Ontario
FILETAG = "Ontario"         # What tag to include in the filename
FOLDER = "Ontario"          # Folder where output files go

def get_month_data(year,month='',condition='',output='filtered'):    
    result_list = []
    filelist = ''
    key = ''
    value = ''
    test = ''
    if len(condition)>0 and condition.find('=') > -1:
        key,value = condition.split('=')        
    fname = f'{str(year)}-CSV.zip'    
    with zf.ZipFile(fname,'r') as zip_file:
        filelist = zip_file.namelist()
        for file in filelist:
            if file.startswith('pub') and file.endswith('.csv'):
                if month=='' or file[3:4] == month:
                    df_final = pd.DataFrame()
                    df_result = pd.DataFrame()
                    print(f'filename = {file}')
                    with zip_file.open(file) as f:
                        df_result = pd.read_csv(f)
                    
                    if len(condition) > 0:        
                        if key in df_result.columns:            
                            test = df_result[key] ==  int(value)
                            df_final = df_result[test]                                                      
                            df_final.to_csv(f'./Toronto/Monthly/LFS_Toronto_20{file[5:7]}-{file[3:5]}.csv',index=False)
                        else:
                            df_final = df_result
                            print(f'{key} not found in dataframe')
                    result_list.append(df_final)
    
    

def get_year_data(year,condition=''):
    df_result = pd.DataFrame()
    bStarted = False
    filelist = ''
    key = ''
    value = ''
    test = ''
    if len(condition)>0 and condition.find('=') > -1:
        key,value = condition.split('=')        
    fname = f'{str(year)}-CSV.zip'    
    with zf.ZipFile(fname,'r') as zip_file:
        filelist = zip_file.namelist()
        for file in filelist:
            if file.startswith('pub') and file.endswith('.csv'):
                try:
                    print(f'filename = {file}')
                    with zip_file.open(file) as f:
                        df = pd.read_csv(f)
                        if not bStarted:
                            df_result = df
                            bStarted = True
                        else:
                            df_result = pd.concat([df_result,df],ignore_index=True)                        
                except:
                    print(f'ERROR: {file} failed')
    
    df_final = df_result    
    
    if len(condition) > 0:        
        if key in df_final.columns:            
            test = df_final[key] ==  int(value)
            df_final = df_final[test]
        else:
            print(f'{key} not found in dataframe')
    
    return df_final


# Set YEAR_START, YEAR_END, FILTER, and FILETAG at the top of this file
def get_provincial_data(startYear,endYear,folder="output",filter=""):
    df_complete = pd.DataFrame()
    bFirst = True
    for year in range(startYear,endYear+1):
        print(f'Current year: {year}')
        df_data = get_year_data(year,filter)

        if bFirst:
            df_complete = df_data
            bFirst = False
        else:
            df_complete = pd.concat([df_complete,df_data],ignore_index=True)
        df_data.to_csv(f'./{folder}/LFS_{folder}_{year}.csv')
    return df_complete
    #df_complete.to_csv('LFS_{folder}_2015-2026.csv')

#get_provincial_data(2015,2026,folder="Ontario",filter="PROV=35")


def get_occupation_data(startYear,endYear,folder,filter,bUseFile=False):
    if bUseFile:
        df_test =pd.read_csv('./WorkRule/LFS_WorkRule_2026.csv')
    else:
        df_test = get_provincial_data(startYear,endYear,folder,filter)

def count_occupation(occ_list):
    counts = {}
    for entry in occ_list:
        if str(entry) in counts.keys():
            counts[str(entry)] += 1
        else:
            counts[str(entry)] = 1

    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[0], reverse=False))
    print(sorted_counts)
    print(f'Total Entries = {len(occ_list)}')
    #unique_occupations = occ_list.unique()
    #print(unique_occupations)

#df_test = get_occupation_data(2025,2026,"WorkRuleEffect","")    
#occupations = df_test['NOC_43'].fillna(0)

#df_toronto = get_provincial_data(2026,2026,"Toronto","CMA=4")
for year in range(2015,2026):
    big_df_list = get_month_data(year,'','CMA=4','Toronto')




