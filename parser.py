import scanner
import csv

file = open('sampleText.txt')

scanner = scanner.Scanner(file)
with open('parseTable.csv') as parseTable:
    csv_reader = csv.reader(parseTable, delimiter = ',')
    print(csv_reader)