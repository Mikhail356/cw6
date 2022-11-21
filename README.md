# cw6
My diploma work on Mechmat faculty

## Current problems
1. Not natural parser. For example you can check result for:
    ```python
    from parser.parse import Parser
    html = requests.get('https://amaslov.me/ru/about_me/')
    parser = Parser()
    text = parser.common_parser(html.text)
    print(text)
    ------
    '      马斯洛夫 •阿列克謝（英语：Maslov Alexey）  俄罗斯汉学博士，历史学家，莫斯科大学亚非学院院长 、 俄罗斯科学院远东研究所学术主任、 俄罗斯高等经济大学亚洲学学院教授。他的主要研究对象是中国及其政治文化，宗教传统， 经济史. 俄罗斯少林武术联盟会主席    '
    ```
    1. It leads to false classification using methods (tf-idf/bm25) trained on russian/english vocabulary
    1. Also not correct Unicode translation
        ```python
        html = requests.get('https://polit.ru/article/2014/02/13/ps_cmns/')
        parser = Parser()
        text = parser.common_parser(html.text)
        print(text)
        ------
        ' Ð¡Ð¾Ñ\x82Ñ\x80Ñ\x83Ð´Ð½Ð¸ÐºÐ°Ð¼Ð¸ Ð¸ Ð°Ñ\x81Ð¿Ð¸Ñ\x80Ð°Ð½Ñ\x82Ð°Ð¼Ð¸ Ð¾Ñ\x82Ð´ÐµÐ»Ð° Ð¡ÐµÐ²ÐµÑ\x80Ð° Ð¸ Ð¡Ð¸Ð±Ð¸Ñ\x80Ð¸ Ð\x98Ð½Ñ\x81Ñ\x82Ð¸Ñ\x82Ñ\x83Ñ\x82Ð° Ñ\x8dÑ\x82Ð½Ð¾Ð»Ð¾Ð³Ð¸Ð¸ Ð¸ Ð°Ð½Ñ\x82Ñ\x80Ð¾Ð¿Ð¾Ð»Ð¾Ð³Ð¸Ð¸ Ð Ð\x90Ð\x9d Ñ\x81Ð¾Ð·Ð´Ð°Ð½ Ð¸ Ð¿Ð¾Ð¿Ð¾Ð»Ð½Ñ\x8fÐµÑ\x82Ñ\x81Ñ\x8f Ñ\x8dÐ»ÐµÐºÑ\x82Ñ\x80Ð¾Ð½Ð½Ñ\x8bÐ¹ ÐºÐ¾Ñ\x80Ð¿Ñ\x83Ñ\x81 Ñ\x82ÐµÐºÑ\x81Ñ\x82Ð¾Ð² Ð½Ð° ...'
        ```
    1. If man versatile and another part of him life not enough described in media it leads to classification error
        1. For 'Шаракин Сергей Александрович' it's cite 'https://skimsu.ru/?action=news&id=750'
    1. Insufficient completeness of the site parser. For website 'https://phys.chem.msu.ru/people/nikiforov-ai/' it gets only '  Никифоров Александр Игоревич   ' (the code is similar to the case above)
1. Probably exists error in test data. As example
'https://polymer.phys.msu.ru/users/nikiforov' for 'Никифоров Александр Игоревич' recieve answer 
'   Работа  Анализ спектров электрохимического импеданса проточных ванадиевых батарей     Описание  Анализ спектров электрохимического импеданса проточных ванадиевых батарей    Специальность  02.00.06 | Высокомолекулярные соединения;    Место обучения / работы  2018-2018 | Абитуриент бакалавриата | МГУ имени М.В.Ломоносова   '

1. Errors in the classification of texts where a person is mentioned indirectly.
    Example. 'https://news.myseldon.com/ru/news/index/241515985' recieve text:
        'Утром 29 ноября 2020 года ушел из жизни талантливый физик, выдающийся человек, надежный товарищ –  Владимир Евгеньевич Фортов. Его близкие, коллеги и друзья выражают соболезнования в связи с уходом из жизни экс-президента РАН. В беседе с «Научной Россией» профессор механико-математического факультета МГУ Юрий Викторович Садовничий отметил, что Фортов отличался ироничным характером и преданно относился к друзьям.«Для меня он, бесспорно, был выдающимся ученым и человеком. Кроме того, он был порядочным, надежным и чутким товарищем. Главное направление обсуждения у него всегда было – как сделать лучше нашей науке. Он очень много уделял этому сил и времени....'

1. Probably need create ensemble of model that improve common quality, but also will increase time complexity of final solution.