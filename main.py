import argparse
from collections import OrderedDict
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


def change_year_word_endings_rus(year):
    """Returns the russian word "Год" with an ending that matches the specified number "year" """
    if str(year)[-1] in ['2', '3', '4']:
        return 'года'
    if str(year)[-1] == '1':
        return 'год'
    else:
        return 'лет'


parser = argparse.ArgumentParser(
    description='''Программа формирует страницу сайта-магазина по продаже крымских вин
    на основе шаблона template.html и таблицы со списком вин в формате .xlsx'''
)
parser.add_argument(
    '--wine_path', help='''Путь к файлу cо списком продукции''', default='wine.xlsx'
)
wine_path = parser.parse_args().wine_path

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

foundation_year = 1920
company_age = datetime.datetime.today().year - foundation_year

wines_description_df = pandas.read_excel(
    wine_path, keep_default_na=False)
wine_categories = wines_description_df['Категория'].unique().tolist()
wines_description_by_categories = {}
for category in wine_categories:
    wines_in_category = wines_description_df[wines_description_df.Категория == category].drop(
        ['Категория'], axis=1
    )
    wines_description_by_categories.update(
        {category: wines_in_category.to_dict(orient='records')}
    )
wines_description_by_categories_sorted = OrderedDict(
    sorted(wines_description_by_categories.items())
)
rendered_page = template.render(wines_by_categories=wines_description_by_categories_sorted,
                                company_age="Уже {} {} с вами".format(
                                    company_age, change_year_word_endings_rus(company_age)),
                                )

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
