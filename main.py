from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from pprint import pprint
from collections import OrderedDict


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

foundation_year = 1920
company_age = datetime.datetime.today().year - foundation_year


def plural_years_rus(year):
    """returns the word "год" in the required case"""
    if str(year)[-1] in ['2', '3', '4']:
        return 'года'
    if str(year)[-1] == '1':
        return 'год'
    else:
        return 'лет'


excel_data_wine = pandas.read_excel('wine.xlsx', sheet_name='Лист1').to_dict(orient='records')

excel_wine2_df = pandas.read_excel('wine2.xlsx', sheet_name='Лист1').fillna('blank')
wine2_category = excel_wine2_df['Категория'].unique().tolist()
wine2_dict = {}
for category in wine2_category:
    wine2_dict.update({category: excel_wine2_df[excel_wine2_df.Категория == category]
                      [['Картинка', 'Название', 'Сорт', 'Цена']].to_dict(orient='records')})
wine2_ordered_dict = OrderedDict(sorted(wine2_dict.items()))
pprint(wine2_dict)


rendered_page = template.render(wines=excel_data_wine, wine_categories=wine2_ordered_dict)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
