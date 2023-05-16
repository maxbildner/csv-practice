import os
import csv

MASTER_FILE = "./test_csv_files/test_master_file.csv"
UPDATE_FILES_FOLDER = "./update_files" # put all update csv files in this folder
UPDATE_FILES = os.listdir(UPDATE_FILES_FOLDER)  # list of all files in "update_files" folder
print(UPDATE_FILES) #=> ['test_update_file_1.csv', 'test_update_file_2.csv']
print("\n")

REMOVE_LEADING_ZEROS = True # if true, remove leading zeros from values in 2nd column when comparing- does NOT remove leading zeros from either csv file
REMOVE_SPACES = True # if true, remove spaces from 4th column when comparing- does NOT remove spcaes from either csv file


def build_set(file_path):
  f = open(file_path, "r") # create object reference to csv file
  f_csvreader = csv.reader(f) # create csvreader object
  f_header = next(f_csvreader) # next() returns first row as a list of strings, and shifts master_file_csvreader data to start at next row
  csv_set = set()

  for row in f_csvreader: # loop through rows in csv (excluding header row)
    first_4_col = row[0:4] # Ex. ['ABC', '00456', '5665', ' HPV, 16/15']

    if REMOVE_LEADING_ZEROS:
      first_4_col[1] = first_4_col[1].lstrip("0") # remove leading zeros from 2nd column value. Ex "001230" => "1230"
    if REMOVE_SPACES:
      first_4_col[3] = first_4_col[3].replace(" ", "") # remove spaces from 4th column value. Ex " ABC 12,13" => "ABC12,13"
    
    row_str = "~~".join(first_4_col) # Ex. 'ABC~~00456~~5665~~ HPV, 16/15'  we're using "~~" as a delimeter to separate columns since the likelyhood of two "~" showing in the csv is unlikely
    csv_set.add(row_str) # only add first 4 columns to set (as a single string)

  f.close() # close file so we don't consume excess memory

  return csv_set

# set_1 = build_set(UPDATE_FILES_FOLDER + '/test_update_file_1.csv')
# print('\n'.join(set_1))


def get_missing_rows(update_file_path, master_table):
  update_file = open(update_file_path, "r") 
  update_file_csvreader = csv.reader(update_file)
  update_file_header = next(update_file_csvreader) 
  missing_rows = [] # will contain rows (lists) to add to end of master csv file

  for row in update_file_csvreader: # loop through rows in update csv (excluding header row)
    first_4_col = row[0:4] # Ex. ['ABC', '00456', '5665', ' HPV, 16/15']

    if REMOVE_LEADING_ZEROS:
      first_4_col[1] = first_4_col[1].lstrip("0")
    if REMOVE_SPACES:
      first_4_col[3] = first_4_col[3].replace(" ", "")

    row_str = "~~".join(first_4_col)

    if row_str not in master_table: 
      missing_rows.append(row) # add entire row to missing_rows

  update_file.close()

  return missing_rows


# 1) build hash table of master file outside the loop below so we don't have to rebuild on each loop iteration
master_set = build_set(MASTER_FILE)

# 2) loop over each file path and check each file against master
for update_file_path in UPDATE_FILES:

  # 3) get missing rows (rows in update file that are not in master file)
  missing_rows = get_missing_rows(update_file_path, master_set)
  print(missing_rows)
  print("\n")

  # 4) add missing_rows to master_set
  for row in missing_rows:
    first_4_col = row[0:4] # Ex. ['ABC', '00456', '5665', ' HPV, 16/15']
    if REMOVE_LEADING_ZEROS:
      first_4_col[1] = first_4_col[1].lstrip("0") # remove leading zeros from 2nd column value. Ex "001230" => "1230"
    if REMOVE_SPACES:
      first_4_col[3] = first_4_col[3].replace(" ", "") # remove spaces from 4th column value. Ex " ABC 12,13" => "ABC12,13"

    row_str = "~~".join(first_4_col) # Ex. 'ABC~~00456~~5665~~ HPV, 16/15'  we're using "~~" as a delimeter to separate columns since the likelyhood of two "~" showing in the csv is unlikely
    master_set.add(row_str) # only add first 4 columns to set (as a single string)
    
  # 5) add missing rows to end of master csv file
  master_file = open(MASTER_FILE, "a") # "a" means append to file instead of overwriting entire file
  master_file_csvwriter = csv.writer(master_file)
  master_file_csvwriter.writerow("\n")
  master_file_csvwriter.writerows(missing_rows)
