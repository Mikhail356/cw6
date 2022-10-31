from bs4 import BeautifulSoup
from omegaconf import OmegaConf
import requests
from parser.parse import Parser

if __name__ == '__main__':
    args = OmegaConf.load('default.yaml')
    html = requests.get(args.istina_people).text
    soup = BeautifulSoup(html, 'html.parser')
    reference = Parser.istina_parser(soup)['publishes']
    vocabulary = Parser.get_dict(reference)
    print(len(vocabulary), vocabulary[:10])

# not work whis import
# from .parser.parse import Parser
# from jupyter notebook ...
