from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from pprint import pprint
from collections import OrderedDict
import argparse


parser = argparse.ArgumentParser(
    description='''Программа формирует страницу сайта-магазина по продаже крымских вин
    на основе шаблона template.html и таблицы со списком вин в формате .xlsx''')
parser.add_argument(
    '--wine_path', help='''Путь к файлу cо списком продукции''', default='wine.xlsx')
wine_path = parser.parse_args().wine_path

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

foundation_year = 1920
company_age = datetime.datetime.today().year - foundation_year


def change_year_word_endings_rus(year):
    """Returns the russian word "Год" with an ending that matches the specified number "year" """
    if str(year)[-1] in ['2', '3', '4']:
        return 'года'
    if str(year)[-1] == '1':
        return 'год'
    else:
        return 'лет'


excel_wine_df = pandas.read_excel(wine_path, sheet_name='Лист1').fillna('blank')
wine_category = excel_wine_df['Категория'].unique().tolist()
wine_dict = {}
for category in wine_category:
    wine_dict.update({category: excel_wine_df[excel_wine_df.Категория == category]
                     .drop(['Категория'], axis=1).head().to_dict(orient='records')})
wine_ordered_dict = OrderedDict(sorted(wine_dict.items()))
pprint(wine_dict)


rendered_page = template.render(wine_categories=wine_ordered_dict,
                                company_age="Уже {} {} с вами".format(
                                    company_age, change_year_word_endings_rus(company_age)),
                                )

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
