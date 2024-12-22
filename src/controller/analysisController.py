from bs4 import BeautifulSoup
import requests
import pandas as pd


def main():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    titles = []
    links = []
    scores = []

    for item in soup.find_all('tr', class_='athing'):
        title_line = item.find('span', class_='titleline')
        if title_line:
            title = title_line.text.strip()
            title_link = title_line.find('a')
            link = title_link['href'] if title_link else None

            # Find score in the next sibling tr
            score_row = item.find_next_sibling('tr')
            score = None
            if score_row:
                score_span = score_row.find('span', class_='score')
                if score_span:
                    score = score_span.text.strip()

            titles.append(title)
            links.append(link)
            scores.append(score)  # Changed from score.append(score)

    df = pd.DataFrame({
        'Title': titles,
        'Link': links,
        'Score': scores
    })

    print(df)


if __name__ == "__main__":
    main()