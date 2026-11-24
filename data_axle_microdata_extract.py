# import a library for working with tabular data, pandas
# we are importing it using the shorthand "pd" to more easily call it's functions

import pandas as pd
import chardet
import os
import csv
import zipfile as zf

DATA_FOLDER = './archives/'    # the folder where your Data Axle files (zipped) are stored  (You must have zipped DataAxle files in here for this to work)
UNZIP_FOLDER = './unzipped/'  # folder where the contents of unzipped files are stored (folder will be created if not present)
PROCESS_FOLDER = './processed/' # folder where processed files go after being renamed and encoding conversion (folder will be created if not present)
OUTPUT_FOLDER = './toronto/'  # the folder where you want the final extracted datasets to go (folder will be created if not present)

YEARS = [2009]
DATA_FILES = {}

# ==========================================================
# Extract Data Axle data from the zip file
# ==========================================================
def extract_datafiles(year_range=[]):
    if len(year_range) == 0:
        filelist = os.listdir(DATA_FOLDER)
        print(f'Extracting all files in {DATA_FOLDER}...')
        for file in filelist:
            with zf.ZipFile(file,'r') as zip_file:
                zip_file.extractall(UNZIP_FOLDER)
    else:
        for year in year_range:
            fname = f'{DATA_FOLDER}CanadaDB{year}.zip'
            print(f'Extracting Data Axle data from {fname}...')
            with zf.ZipFile(fname,'r') as zip_file:
                zip_file.extractall(UNZIP_FOLDER)

# ==========================================================
# Rename files to eliminate spaces in names
# ==========================================================
def fix_filenames():
    filelist = os.listdir(UNZIP_FOLDER)
    print(f'Replacing spaces with _ in filenames in {UNZIP_FOLDER}')    
    for file in filelist:                
        newname = file.replace(' ','_')
        if not os.path.isfile(f'{UNZIP_FOLDER}{newname}'):
            os.rename(f'{UNZIP_FOLDER}{file}',f'{UNZIP_FOLDER}{newname}')


# ==========================================================
# Check file to see if text is UTF-8 or ASCII encoded
# ==========================================================
def get_encoding(filename):
    with open(f'{UNZIP_FOLDER}{filename}',"rb") as file:
        raw_data = file.read(10240)         # read a sample, not the whole file
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return encoding
    return ''

# ==========================================================
# Convert an ASCII-encoded CSV file to UTF-8 encoding
# Handles decoding errors gracefully.
# ==========================================================
def convert_csv_ascii_to_utf8(input_file):
    infile = f'{UNZIP_FOLDER}{input_file}'
    outfile = f"{PROCESS_FOLDER}{input_file.replace(' ','_')}"

    if not os.path.isdir(PROCESS_FOLDER):
        os.mkdir(PROCESS_FOLDER)
    try:        
        if not os.path.isfile(infile):
            raise FileNotFoundError(f"Input file '{input_file}' not found.")
        
        # Read the ASCII file
        with open(infile, mode='r', encoding='ascii', errors='replace') as ifile:
            reader = csv.reader(ifile)
            rows = list(reader)  # Load all rows into memory

        # Write to UTF-8 file
        newout = outfile
        with open(newout, mode='w', encoding='utf-8', newline='') as ofile:
            writer = csv.writer(ofile)
            writer.writerows(rows)

    except FileNotFoundError as e:
        print(e)
    except UnicodeDecodeError as e:
        print(f"Decoding error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# ==========================================================
# Fix encoding issues with earlier Data Axle files (ASCII vs UTF-8)
# ==========================================================
def fix_encoding_issue(year_range):   
    import shutil 
    filelist = os.listdir(UNZIP_FOLDER)
    for file in filelist:
        fname,ext = file.split('.')
        year = fname[-4:]
        if int(year) in year_range:
            encoding = get_encoding(file)

            # If ascii, then convert to UTF-8 and save as a new file
            if encoding == 'ascii':
                print(f'Changing text encoding from Ascii to UTF-8 in {file}')
                fname,ext = file.split('.')
                convert_csv_ascii_to_utf8(file)  
                DATA_FILES[year] = file.replace(' ','_')
            else:
                src = os.path.join(UNZIP_FOLDER,file)
                dst = os.path.join(PROCESS_FOLDER,file.replace(' ','_'))
                shutil.copy(src,dst)
                DATA_FILES[year] = file.replace(' ','_')

        
# ==========================================================
# Retrieve Data Axle data for a given year
# ==========================================================
def get_canada_data_axle_by_year(year):
    file = ''
    df_result = pd.DataFrame()
    try:
        file = f'{PROCESS_FOLDER}{DATA_FILES[str(year)]}'
    except:
        file = ''
        print(f'ERROR: No data available for {year} year')

    try:
        df_result = pd.read_csv(file,dtype=str)
    except:
        print(f'ERROR: File {file} could not be read')        
    return df_result


# ==========================================================
# Return the correct city field by year
# ==========================================================
def get_city_field(year):
    result = ''
    test_year = str(year)
    match test_year:
        case '2009'|'2010'|'2011'|'2012'|'2013':
            result = 'CMLCTY'
        case '2014'|'2015'|'2016':
            result = 'EMLCTY'
        case _:
            result = "STCITY"
    return result



# ==========================================================
# Extract Toronto data
# ==========================================================
def get_toronto_data_axle(year_range=[]):
    if len(year_range) == 0:
        years = DATA_FILES.keys
        get_toronto_data_axle(years)
    else:
        if not os.path.isdir(OUTPUT_FOLDER):
            os.mkdir(OUTPUT_FOLDER)
        for year in year_range:
            canada_data = get_canada_data_axle_by_year(year)     
            city_field = get_city_field(year)
            toronto_data = canada_data[canada_data[city_field].str.lower() == "toronto"]
            canada_data.head(5)
            toronto_data.head(5)
            print(f'Outputting data_axle_toronto_{year}.csv to {OUTPUT_FOLDER}')
            toronto_data.to_csv(f"{OUTPUT_FOLDER}data_axle_toronto_{year}.csv")            


# ==========================================================
# MAIN CODE
# ==========================================================

# DATA_FOLDER points to the local folder where your zipped Data Axle files are located

# YEARS is a list of dataset years you wish to extract from
# eg. YEARS = [2009,2010,2014]


extract_datafiles(YEARS)
fix_encoding_issue(YEARS)
get_toronto_data_axle(YEARS)