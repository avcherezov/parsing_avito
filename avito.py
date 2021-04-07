import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-root-2oCjZ').find_all(
        'span', class_='pagination-item-1WyVp')[-2].get('data-marker')
    total_pages = pages.split('(')[1].split(')')[0]
    return int(total_pages)


def write_csv(data):
    with open('avito.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow( (data['title'],
                          data['price'],
                          data['metro'],
                          data['url']) 
                        )


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_ ='index-root-2c0gs').find_all(
        'div', class_='item__line')
    for ad in ads:
        try:
            title = ad.find('div', class_='description').find(
                'span').text.strip()
        except:
            title = ''
        try:
            url = 'https://www.avito.ru' + ad.find(
                'div', class_='description').find('h3').find('a').get('href')
        except:
            url = ''
        try:
            price = ad.find('div', class_='snippet-price-row').text.strip()
        except:
            price = ''
        try:
            metro = ad.find('div', class_='data').find(
                'div', class_='item-address').text.split(',')[0]
        except:
            metro = ''
        data = {'title': title,
                'price': price,
                'metro': metro,
                'url': url}
        write_csv(data)


def main():
    url = 'https://www.avito.ru/moskva/avtomobili?q=kia+sportage&p=1'
    base_url = 'https://www.avito.ru/moskva/avtomobili?'
    query_part = 'q=kia+sportage&'
    page_part = 'p='

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages + 1):
        url_gen = base_url + query_part + page_part + str(i)
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()
