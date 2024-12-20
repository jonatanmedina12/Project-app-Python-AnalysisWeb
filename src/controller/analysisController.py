from bs4 import BeautifulSoup

import requests
import pandas as pd

def main():
    url ="https://news.ycombinator.com/"
    response = requests.get(url)

    print(response.content)

    soup=BeautifulSoup(response.content,'html.parser')

    titles = []
    links =[]
    scores =[]
    for item in soup.find_all('tr',  class_='athing'):
        titles_lines = item.find('span',class_ ='titleline')
        if titles_lines:
            title=titles_lines.text
            titles_link =titles_lines.find('a')
            link =titles_link['href']
            score=item.find_next_sibling('tr').find('span', class_='score')
            if score:
                score = score.text
            else:
                scores=None

            titles.append(title)
            links.append(link)
            score.append(score)
        else:
            print("no se encontró nada xd ")



    df = pd.DataFrame({
        'titles': titles,
        'Link': links,
        'score': scores

    })
    print(df)
    