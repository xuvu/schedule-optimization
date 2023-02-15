# a = 'TX'
# b = 'KY'
# c = 'XJ'
#
# text = '=COUNTIF(A2:A5,A4)'
# test_text = '=COUNTIF(' + a + ':' + b + ',' + '"' + c + '")'
# test_text_ = '+ COUNTIF(' + a + ':' + b + ',' + '"' + c + '")'
# print(test_text, test_text_)


count_cell_main_hospital = {'morning': [1,2,3], 'afternoon': [], 'night': []}
count_cell_main_hospital_name = ['morning', 'afternoon', 'night']
print(count_cell_main_hospital[count_cell_main_hospital_name[0]])
