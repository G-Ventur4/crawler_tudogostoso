import requests
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller

# Função para obter uma lista de proxies a partir de um arquivo de texto
def get_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

# Função para enviar uma solicitação HTTP através de um proxy
def send_request_with_proxy(url, proxy):
    proxies = {
        'http': proxy,
        'https': proxy
    }
    try:
        response = requests.get(url, proxies=proxies)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return None

# Função para obter uma nova identidade para o Tor
def renew_tor_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

# URL do site com as receitas
url = 'https://www.tudogostoso.com.br'

# Caminho para o arquivo de proxies
proxies_file_path = 'proxies.txt'

# Obtém a lista de proxies a partir do arquivo
proxies = get_proxies_from_file(proxies_file_path)

# Loop para acessar as páginas com cada proxy
for proxy in proxies:
    # Renova a identidade do Tor para cada proxy
    renew_tor_identity()
    
    # Envia a solicitação HTTP usando o proxy atual
    response = send_request_with_proxy(url, proxy)
    
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extrai as informações das receitas
        # (coloque aqui o código para extrair as informações que deseja)
        
        # Exemplo: imprimir o título das receitas
        recipes = soup.select('.recipe-title')
        for recipe in recipes:
            print(recipe.text)
    else:
        print(f"Request failed using proxy: {proxy}")


# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
