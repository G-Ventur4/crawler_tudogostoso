import os
import csv
import requests
from bs4 import BeautifulSoup
from proxychains import proxyconfig

# URL do site com as receitas
base_url = 'https://www.tudogostoso.com.br'

# Arquivo de saída para armazenar as receitas
output_file = 'recipes.csv'

# Caminho para o arquivo contendo os proxies
proxies_file = 'proxies.txt'

# Configura o uso do proxychains
proxyconfig.set_config(proxies_file)

# Cria uma sessão HTTP com suporte a proxychains
session = requests.session()
session.proxies = proxyconfig.getproxies()

# Função para extrair as receitas do site
def scrape_recipes():
    # Lista para armazenar as receitas
    recipes = []

    # Realiza a requisição à página inicial
    response = session.get(base_url)

    # Extrai os links das receitas da página inicial
    soup = BeautifulSoup(response.content, 'html.parser')
    recipe_links = soup.select('.card a.recipe-card')

    # Percorre os links das receitas
    for link in recipe_links:
        recipe_url = base_url + link['href']

        # Realiza a requisição à página da receita
        recipe_response = session.get(recipe_url)

        # Extrai os detalhes da receita
        recipe_soup = BeautifulSoup(recipe_response.content, 'html.parser')
        title = recipe_soup.select_one('.recipe-title').text.strip()
        ingredients = [ingredient.text.strip() for ingredient in recipe_soup.select('.p-ingredient')]
        instructions = [instruction.text.strip() for instruction in recipe_soup.select('.instructions p')]

        # Adiciona a receita à lista
        recipes.append({'Title': title, 'Ingredients': ingredients, 'Instructions': instructions})

    return recipes

# Executa o crawler e salva as receitas em um arquivo CSV
if __name__ == '__main__':
    recipes = scrape_recipes()

    # Verifica se o diretório de saída existe
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Salva as receitas em um arquivo CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Ingredients', 'Instructions']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(recipes)

    print('Crawler concluído. As receitas foram salvas em', output_file)
