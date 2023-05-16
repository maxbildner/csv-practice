# this script checks if any rows (values in first 4 columns only) in the update csv file are present in the master csv file, then writes those missing rows to the master file
import csv # built in csv module
MASTER_FILE = "./test_csv_files/test_master_file.csv"
UPDATE_FILE = "./test_csv_files/test_update_file.csv"
REMOVE_LEADING_ZEROS = True # if true, remove leading zeros from values in 2nd column when comparing- does NOT remove leading zeros from either csv file
REMOVE_SPACES = True # if true, remove spaces from 4th column when comparing- does NOT remove spcaes from either csv file


# helper function- prints a 2D list (list of lists) in a nice table format
def print_nicely(matrix):
  print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))


# 1) build hash table for fast lookup
master_file = open(MASTER_FILE, "r") # create object reference to csv file
master_file_csvreader = csv.reader(master_file) # create csvreader object
master_file_header = next(master_file_csvreader) # next() returns first row as a list of strings, and shifts master_file_csvreader data to start at next row
master_hash_table = set()

for row in master_file_csvreader: # loop through rows in master csv (excluding header row)
  first_4_col = row[0:4] # Ex. ['ABC', '00456', '5665', ' HPV, 16/15']

  if REMOVE_LEADING_ZEROS:
    first_4_col[1] = first_4_col[1].lstrip("0") # remove leading zeros from 2nd column value. Ex "001230" => "1230"
  if REMOVE_SPACES:
    first_4_col[3] = first_4_col[3].replace(" ", "") # remove spaces from 4th column value. Ex " ABC 12,13" => "ABC12,13"

  row_str = "~~".join(first_4_col) # Ex. 'ABC~~00456~~5665~~ HPV, 16/15'  we're using "~~" as a delimeter to separate columns since the likelyhood of two "~" showing in the csv is unlikely
  master_hash_table.add(row_str) # only add first 4 columns to set (as a single string)

master_file.close() # close file so we don't consume excess memory

print('\n'.join(master_hash_table))
print('\n')
# [ 'ABC~~1234567=~~1234~~FILTER FLAT ZERO, 16', 
#   'ERE~~TRICHV~~6007~~ROW SEED FETAL, RISK', 
#   'ERE~~123~~5566~~ANCHOR CAKE RESOURCE TIGER', 
#   'ABC~~TRICHV~~1234~~FILTER FLAT ZERO, 16', 
#   'XYZ~~8707123~~2641~~BANANA 15, 18/45', 
#   'NEV~~456=~~2480~~MATRIX SHELL PLUNGE', 
#   'ABC~~456~~5665~~CAKE COUNTRY EARTH'
# ]


# 2) check update file
update_file = open(UPDATE_FILE, "r") 
update_file_csvreader = csv.reader(update_file)
update_file_header = next(update_file_csvreader) 
missing_rows = [] # will contain rows (lists) to add to end of master csv file

for row in update_file_csvreader: # loop through rows in update csv (excluding header row)
  first_4_col = row[0:4] # Ex. ['ABC', '00456', '5665', ' HPV, 16/15']

  if REMOVE_LEADING_ZEROS:
    # row[1] = first_4_col[1] = first_4_col[1].lstrip("0")
    first_4_col[1] = first_4_col[1].lstrip("0")
  if REMOVE_SPACES:
    first_4_col[3] = first_4_col[3].replace(" ", "")

  row_str = "~~".join(first_4_col)

  if row_str not in master_hash_table: 
    missing_rows.append(row) # add entire row to missing_rows

update_file.close()

# print 2D list nicely
print_nicely(missing_rows)
print("Number of Rows to Add to Master: " + str(len(missing_rows)))
# ATL	%%92089	118	  CYCLE BLACK VIEW MIX (16,18 OTHER)				
# ERE	456	    6007	GAS DETAIL SIX, ALERT 

# print(missing_rows)
# [ ['ATL', '%%92089', '118', 'CYCLE BLACK VIEW MIX (16,18 OTHER)', '', '', '', ''], 
#   ['ERE', '00456', '6007', 'GAS DETAIL SIX, ALERT', '', '', '', '']
# ]


# 3) add unique missing_rows to end of master csv file
master_file = open(MASTER_FILE, "a") # "a" means append to file instead of overwriting entire file
master_file_csvwriter = csv.writer(master_file)
master_file_csvwriter.writerow("\n")
master_file_csvwriter.writerows(missing_rows)




