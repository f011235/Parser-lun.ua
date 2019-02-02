import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def write_csv(data):
    with open('parsing.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['district'],
                         data['price_date'],
                         data['description'],
                         data['redirect']))


def get_total_page(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_="jss225 jss14").find_all('a', class_="jss61 jss35 jss46 jss49 jss58 jss226 jss228")[-1].get('href')
    total_pages = pages.split('=')[2]

    return int(total_pages)


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    announcement = soup.find_all('div', class_='jss159')
    for i in announcement:
        try:
            title = i.find('div', class_='jss170').text
        except:
            title = ''
        try:
            district = i.find('div', class_='jss175').text
        except:
            district = ''
        try:
            price_date = i.find('div', class_='jss179').text.replace('грн', 'грн. дата: ')
        except:
            price_date = ''
        try:
            description = i.find('div', class_='jss183 jss180').text.replace('комнатная', 'комнатная, площадь: ')
        except:
            description = ''
        try:
            redirect ='https://www.lun.ua' + i.find('a', class_='jss61 jss35 jss37 jss38 jss40 jss41 jss58 jss190').get('href')
        except:
            redirect = ''

        data = {'title': title,
                'district': district,
                'price_date': price_date,
                'description': description,
                'redirect': redirect}
        write_csv(data)





def main():
    url = 'https://www.lun.ua/аренда-квартир-киев?withoutBrokers=1'
    page_count = '&page='
    total_pages = get_total_page(get_html(url))

    for i in range(0, total_pages):
        url_gen = url + page_count + str(i)
        html = get_html(url_gen)
        get_page_data(html)



if __name__ == '__main__':
    main()
