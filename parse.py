from bs4 import BeautifulSoup
from omegaconf import OmegaConf
import requests

import re


def istina_parser(soup):

    #
    # Parse Istina man page and return him piblishes,
    # collaborators and also tags of html document
    #
    publishes = []
    coauthors = []
    tags = {tag.name for tag in soup.find_all()}
    for tag in tags:

        # find all element of tag
        for i in soup.find_all(tag):
            # if tag has attribute of class
            if i.has_attr("class") and len(i['class']) != 0:
                if i['class'][0] == 'activity':
                    publishes.append(i.li.a.text)
                elif i['class'][0] == 'span-21':
                    for s in i.find_all('h4'):
                        if 'Соавторы' in s.text:
                            coauthors = s.text.replace('Соавторы:', '')
                            coauthors = coauthors.replace(
                                'показать полностью...', '')
                            coauthors = coauthors.replace(
                                ',', '').split('\n')
                            for ind, i in enumerate(coauthors):
                                if re.search('[a-zA-Z0-9_а-яА-Я].+[^ ]', i):
                                    coauthors[ind] = re.search(
                                        '[a-zA-Z0-9_а-яА-Я].+[^ ]', i).group(0)
                                else:
                                    coauthors[ind] = ''
                            coauthors = list(
                                filter(lambda x: len(x) > 0, coauthors))

    return {'publishes': publishes,
            'coauthors': coauthors}


if __name__ == '__main__':
    args = OmegaConf.load('default.yaml')
    html = requests.get(args.istina_people).text
    soup = BeautifulSoup(html, 'html.parser')
    print(istina_parser(soup))
