from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas


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


rendered_page = template.render(wines=excel_data_wine)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
