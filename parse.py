from bs4 import BeautifulSoup
from omegaconf import OmegaConf
import requests
import re

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import nltk
import pymorphy2
from tqdm import tqdm


class Parser():

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

    def get_dict(reference):
        """
        Lemmatization and cleaning input list of reference vocabulary
        """
        stopwords = nltk.corpus.stopwords.words("russian")
        vectorizer = CountVectorizer(analyzer='word', stop_words=stopwords)
        vectorizer.fit_transform(reference)
        reference = vectorizer.get_feature_names_out()

        stopwords = nltk.corpus.stopwords.words("english")
        vectorizer = CountVectorizer(analyzer='word', stop_words=stopwords)
        vectorizer.fit_transform(reference)
        reference = vectorizer.get_feature_names_out()

        tmp = []
        for i in reference:
            if not re.match('\d+', i):
                tmp.append(i)
        reference = tmp

        stem = nltk.stem.WordNetLemmatizer()
        morph = pymorphy2.MorphAnalyzer()
        tmp = []
        for word in tqdm(reference):
            if re.match('[a-zA-Z]+', word):
                tmp.append(stem.lemmatize(word))
            else:
                tmp.append(morph.parse(word)[0].normal_form)
        reference = tmp

        stopwords = nltk.corpus.stopwords.words("russian")
        vectorizer = CountVectorizer(analyzer='word', stop_words=stopwords)
        vectorizer.fit_transform(reference)
        reference = vectorizer.get_feature_names_out()

        stopwords = nltk.corpus.stopwords.words("english")
        vectorizer = CountVectorizer(analyzer='word', stop_words=stopwords)
        vectorizer.fit_transform(reference)
        reference = vectorizer.get_feature_names_out()

        return reference


if __name__ == '__main__':
    args = OmegaConf.load('default.yaml')
    html = requests.get(args.istina_people).text
    soup = BeautifulSoup(html, 'html.parser')
    reference = Parser.istina_parser(soup)['publishes']
    vocabulary = Parser.get_dict(reference)
    print(len(vocabulary), vocabulary[:10])
