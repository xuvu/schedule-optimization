import openpyxl
from openpyxl.styles import PatternFill

# Create a new Excel workbook
wb = openpyxl.Workbook()

# Select the active sheet
sheet = wb.active

# Write the formula to the cell
start = 'A1'
end = 'E1'
word = 'Apple'

sheet['A1'] = 'Apple'
sheet['B1'] = 'Apple'
sheet['C1'] = 'Apple'
sheet['D1'] = 'Apple'
sheet['E1'] = 'Apple'


test_text = '=COUNTIF(' + start + ':' + end + ',' + '"' + word + '")'
test_text_ = 'COUNTIF(' + start + ':' + end + ',' + '"' + word + '")'
sheet['B2'] = test_text

# Save the changes to the workbook
wb.save('example.xlsx')
