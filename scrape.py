from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

ua = UserAgent()
random_agent= ua.random

headers = {'User-Agent': random_agent, 'Content-Type': 'application/json'}
context_base_url = "https://context.reverso.net/translation/german-english/"



def get_context(word):
    print("word ",word)
    source = requests.get(context_base_url + word,headers=headers).text
    soup = BeautifulSoup(source, 'lxml')

    # search field
    search_text = soup.find('span', class_='search-text')
    input = soup.find(id='entry').get('value')


    article = search_text.find(class_='source-article').text if search_text.find(class_='source-article') else None
    gender = search_text.find(class_='source-pos').get('title') if search_text.find(class_='source-pos') else None

    nouns = _get_meaning(soup, 'n')
    verbs = _get_meaning(soup, 'v')
    adverbs = _get_meaning(soup, 'adv')
    adjectives = _get_meaning(soup,'adj')
    others = _get_meaning(soup,'no-pos')
    examples = _get_examples(soup)

    return {
        "adj_meanings": adjectives, 
        "adv_meanings": adverbs, 
        "noun_meanings": nouns,
        "verb_meanings": verbs,
        "other_meanings": others,
        "examples": examples,
        "is_noun": True if len(nouns) > 0 else False, 
        "input":input,
        "noun":{
            "article":article,
            "gender":gender,            
        }        
        }

def _get_meaning(soup, type):
    content = soup.find('div', id='translations-content')

    if content:
        meaning = content.find_all("a", class_=lambda c: type in c.split() and 'mobile-trans-hidden' not in c.split())
        meaning_list = map(lambda item: item.find('span', class_='display-term').text, meaning)
        return list(meaning_list)
    else:
        return []

# example 
def _get_examples(soup):
    example_list = soup.find_all(class_='example')
    return list(map(_list_example, example_list))

def _list_example(item):
    src = item.find(class_='src').text.strip()
    trg = item.find(class_='trg').text.strip()
    return {"src":src, "trg":trg}    


