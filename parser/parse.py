import re
import nltk
import pymorphy2

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from tqdm import tqdm

from readability import Document
from bs4 import BeautifulSoup


class Parser:

    def __init__(self) -> None:
        pass

    def istina_parser(self, html):
        #
        # Parse Istina man page and return it's piblishes
        # and collaborators
        #
        publishes = []
        coauthors = []
        place = []
        soup = BeautifulSoup(html, 'html.parser')
        tags = {tag.name for tag in soup.find_all()}
        for tag in tags:

            # find all element of tag
            for i in soup.find_all(tag):
                # if tag has attribute of class
                if i.has_attr("class") and len(i['class']) != 0:
                    for t in i.find_all('h4')[:3]:
                        place.append(t.text)
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
                'coauthors': coauthors,
                'place': place, }

    def common_parser(self, html):
        return BeautifulSoup(Document(html).summary(), 'html.parser').text.replace('\n', ' ').replace('\xa0', ' ')

    def remove_numbers(self, word_vector):
        tmp = []
        pattern_roman = r"(?<=^)m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})(?=$)"
        pattern_arabic = r"\d+"

        for word in word_vector:
            if not (
                re.match(pattern_roman, word) or re.match(pattern_arabic, word)
            ):
                tmp.append(word)

        word_vector = tmp
        return word_vector

    def get_vocab(self, reference: list):
        """
        Lemmatization and cleaning input list of reference vocabulary
        """

        vectorizer = CountVectorizer(analyzer='word')
        vectorizer.fit_transform(reference)
        reference = vectorizer.get_feature_names_out()

        reference = self.remove_numbers(reference)

        stem = nltk.stem.WordNetLemmatizer()
        morph = pymorphy2.MorphAnalyzer()
        tmp = []
        for word in reference:
            if re.match('[a-zA-Z]+', word):
                tmp.append(stem.lemmatize(word))
            else:
                tmp.append(morph.parse(word)[0].normal_form)
        reference = tmp

        stopwords = nltk.corpus.stopwords.words("russian")
        stopwords += nltk.corpus.stopwords.words("english")
        stopwords.append('хх')

        vectorizer = CountVectorizer(analyzer='word', stop_words=stopwords)
        vectorizer.fit_transform(reference)
        reference = vectorizer.get_feature_names_out()

        return reference
