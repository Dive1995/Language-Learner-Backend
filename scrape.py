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

    article = None
    gender = None

    # check for noun
    # noun_word = soup.find('div', id='pos-filters').find('button', class_='n')
    noun_word = True if soup.find('div', id='pos-filters').find('button', class_='n') else False

    # search field
    search_text = soup.find('span', class_='search-text')
    input = soup.find(id='entry').get('value')

    if noun_word:
        article = search_text.find(class_='source-article').text
        gender = search_text.find(class_='source-pos').get('title')
        print("Article ", article)
        print("Gender ", gender)

    nouns = _get_noun_meaning(soup)
    verbs = _get_verb_meaning(soup)
    adverbs = _get_adverb_meaning(soup)
    adjectives = _get_adjective_meaning(soup)

    return {
        "adj_meanings": adjectives, 
        "adv_meanings": adverbs, 
        "noun_meanings": nouns,
        "verb_meanings": verbs,
        "is_noun": noun_word, 
        "is_verb": True if len(verbs) > 0 else False, 
        "is_adj": True if len(adjectives) > 0 else False, 
        "is_adv": True if len(adverbs) > 0 else False, 
        "examples":_get_examples(soup),
        "input":input,
        "noun":{
            "article":article,
            "gender":gender,            
        }        
        }

# adjectives
def _get_adjective_meaning(soup):
    adj = soup.find('div', id='translations-content').find_all("a", class_=lambda c: 'adj' in c.split() and 'mobile-trans-hidden' not in c.split())
    adj_meanings = map(lambda item: item.find('span', class_='display-term').text, adj)
    return list(adj_meanings)

# adverbs
def _get_adverb_meaning(soup):
    adv = soup.find('div', id='translations-content').find_all("a", class_=lambda c: 'adv' in c.split() and 'mobile-trans-hidden' not in c.split())
    adv_meanings = map(lambda item: item.find('span', class_='display-term').text, adv)
    return list(adv_meanings)

# nouns
def _get_noun_meaning(soup):
    noun = soup.find('div', id='translations-content').find_all("a", class_=lambda c: 'n' in c.split() and 'mobile-trans-hidden' not in c.split())
    noun_meanings = map(lambda item: item.find('span', class_='display-term').text, noun)
    return list(noun_meanings)

# verbs
def _get_verb_meaning(soup):
    verb = soup.find('div', id='translations-content').find_all("a", class_=lambda c: 'v' in c.split() and 'mobile-trans-hidden' not in c.split())
    verb_meanings = map(lambda item: item.find('span', class_='display-term').text, verb)
    return list(verb_meanings)

# example 
def _get_examples(soup):
    example_list = soup.find_all(class_='example')
    return list(map(_list_example, example_list))

def _list_example(item):
    src = item.find(class_='src').text.strip()
    trg = item.find(class_='trg').text.strip()
    return {"src":src, "trg":trg}    


