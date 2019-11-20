# download browsed rightmove page -> price, name, location, photo
# listing data: property of Rightmove, not to use for scraping

import requests
import bs4
import re
from typing import Tuple

def get_listing(url:str) -> Tuple[int, str, str, str]:
    try:
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.content, features='lxml')
        price = (soup.find('p', attrs={'id': 'propertyHeaderPrice'})
                 .text.strip())
        price = int(re.sub(r'([,£])', '', price))
        return (
            price,
            soup.find('h1', attrs={'itemprop': 'name'}).text,
            soup.find('meta', attrs={'itemprop': 'streetAddress'})['content'],
            soup.find('meta', attrs={'name': 'twitter:image:src'})['content']
        )
    except:
        print('Oops, are you sure about that URL?')
        return (750_000, 
                '3 bed pretty home', 
                'Richmond, Surrey (not really)', 
                'https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?ixlib=rb-1.2.1&auto=format&fit=crop&w=1953&q=80')
                # Photo by https://unsplash.com/@scottwebb
