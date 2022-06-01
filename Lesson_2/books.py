import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint


main_url = 'https://books.toscrape.com/'
page_number = 1
books_list = []

while True:
    url = f'https://books.toscrape.com/catalogue/category/books/historical-fiction_4/page-{page_number}.html'
    headers = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) /'
                             'Chrome/101.0.4951.67 Safari/537.36'}
    response = requests.get(url=url, headers=headers)

    if response.ok:
        soup = bs(response.content, 'html.parser')

        books = soup.find_all('article')

        for book in books:
            title = book.find('h3').find('a')['title']
            instock_anchor = book.find('p', {'class': ['instock', 'availability']})
            instock = instock_anchor.text.strip()
            price = instock_anchor.find_previous_sibling('p').text
            image = book.find('div', {'class': 'image_container'}).find('img')['src']
            image_link = main_url + image

            book_dict = {
                'Image': image_link,
                'Title': title,
                'Price': price,
                'Instock': instock
            }
            books_list.append(book_dict)
        page_number += 1
    else:
        break


print(len(books_list))
pprint(books_list[0])
