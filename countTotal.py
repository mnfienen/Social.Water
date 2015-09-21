import sys
import csv
import os

files_in_dir = os.listdir(os.getcwd())
totalUsers = set()
bad = 0
total = 0
for files in files_in_dir:
	#print files
	if files[-3:] == 'csv' and files[-22:] != "contributionTotals.csv":
	
	#	print "gooo"
		with open(files, 'r') as csvfile:

			reader = csv.reader( csvfile, delimiter=',' )
			rows = 0		
			for row in reader:
				if rows != 0:
					if row[3] not in totalUsers:
						totalUsers.add(row[3])
						
					#print row[2]
					total += 1 
					
				rows += 1
print total, len(totalUsers)
