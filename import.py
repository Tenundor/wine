import pandas
from pprint import pprint


excel_data = pandas.read_excel('wine2.xlsx', sheet_name='Лист1')

pprint(excel_data.to_dict(orient='records'))