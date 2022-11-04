from omegaconf import OmegaConf
import requests
from parser.parse import Parser

if __name__ == '__main__':
    args = OmegaConf.load('default.yaml')
    html = requests.get(args.istina_people).text
    parser = Parser()
    reference = parser.istina_parser(html)
    lst = reference['publishes'] + reference['place'] + args.name.split()
    # print(lst)
    vocabulary = parser.get_vocab(lst)
    print(len(vocabulary), vocabulary[:10])

# not work whis import
# from .parser.parse import Parser
# from jupyter notebook ...
