# import openpyxl
#
# # Create a new Excel workbook
# wb = openpyxl.Workbook()
#
# # Select the active sheet
# sheet = wb.active
#
# # Write the data to the sheet
# # sheet['A1'] = 'Value1'
# # sheet['B1'] = 'Value2'
# # sheet['C1'] = 'Value3'
# # sheet['D1'] = 'Value4'
# # sheet['A2'] = 1
# # sheet['B2'] = 2
# # sheet['C2'] = 3
# # sheet['D2'] = 4
#
# sheet['B1'] = 'Morning (08.00 - 16.00)'
# sheet['C1'] = 'Afternoon (16.00-24.00)'
# sheet['D1'] = 'Night (24.00-8.00)'
#
# # For each day
# for d in range(31):
#     cell_pos = 'A'+str(d+2)
#     sheet[cell_pos] = d+1
#
#
# # Save the workbook
# wb.save("sample.xlsx")
current_cell_num = [3, 22]
for n in range(10):
    for c in range(len(current_cell_num)):
        print(c)
    current_cell_num[0] += 1
    current_cell_num[1] += 1