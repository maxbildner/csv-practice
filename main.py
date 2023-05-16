# this script checks if any rows (values in first 4 columns only) in the update csv file are present in the master csv file, then writes those missing rows to the master file
import csv # built in csv module
MASTER_FILE = "./test_csv_files/master_file_1.csv"
UPDATE_FILE = "./test_csv_files/update_file_1.csv"


# helper function- prints a 2D list (list of lists) in a nice table format
def print_nicely(matrix):
  print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))


# 1) build hash table for fast lookup
master_file_in = open(MASTER_FILE, "r") # create object reference to csv file
master_file_csvreader = csv.reader(master_file_in) 
master_file_header = next(master_file_csvreader) # next() returns current row as a list of strings, and shifts csv data to next row
master_hash_table = set()

for row in master_file_csvreader: # loop through rows in master csv (excluding header row)
  first_4_col = row[0:4] # Ex. ['ABC', '00456', '5665', ' HPV, 16/15']
  row_str = "~~".join(first_4_col) # Ex. 'ABC~~00456~~5665~~ HPV, 16/15'  we're using "~~" as a delimeter to separate columns since the likelyhood of two "~" showing in the csv is unlikely
  master_hash_table.add(row_str) # only add first 4 columns to set (as a single string)

# print(master_hash_table)
# [ 'ABC~~1234567=~~1234~~FILTER FLAT ZERO, 16', 
#   'ERE~~TRICHV~~6007~~ROW SEED FETAL, RISK', 
#   'ERE~~123~~5566~~ANCHOR CAKE RESOURCE TIGER', 
#   'ABC~~TRICHV~~1234~~FILTER FLAT ZERO, 16', 
#   'XYZ~~8707123~~2641~~BANANA 15, 18/45', 
#   'NEV~~456=~~2480~~MATRIX SHELL PLUNGE', 
#   'ABC~~00456~~5665~~CAKE COUNTRY EARTH'
# ]


# 2) check update file
update_file_in = open(UPDATE_FILE, "r") 
update_file_csvreader = csv.reader(update_file_in)
update_file_header = next(update_file_csvreader) 
matches = [] # will contain rows (lists) to add to end of master csv file

for row in update_file_csvreader: # loop through rows in update csv (excluding header row)
  first_4_col = row[0:4]
  row_str = "~~".join(first_4_col)
  if row_str not in master_hash_table: 
    matches.append(row) # add entire row to matches

# print 2D list nicely
print_nicely(matches)
# ATL	%%92089	118	  CYCLE BLACK VIEW MIX (16,18 OTHER)				
# ERE	00456	  6007	GAS DETAIL SIX, ALERT

# [ ['ATL', '%%92089', '118', 'CYCLE BLACK VIEW MIX (16,18 OTHER)', '', '', '', ''], 
#   ['ERE', '00456', '6007', 'GAS DETAIL SIX, ALERT', '', '', '', '']
# ]


# # 3) add unique matches to end of master csv file
# master_file_in = open(MASTER_FILE, "a") # "a" means append to file instead of overwriting entire file
# master_file_csvwriter = csv.writer(master_file_in)
# master_file_csvwriter.writerow("\n")
# master_file_csvwriter.writerows(matches)




