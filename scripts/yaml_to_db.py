import sqlite3 as sq
import os
from omegaconf import OmegaConf
import requests
from tqdm import tqdm


class Database(object):
    def __init__(self):
        self.name = 'database.db'
        self.filled = False

    def yaml_to_sqlite(self, path_to_yaml):
        os.system(f'sqlite3 {self.name} < scripts/create_train_db.sql')

        con = sq.connect(f'{self.name}')
        cur = con.cursor()

        paths = sorted(os.listdir(path_to_yaml))
        for ind, i in enumerate(tqdm(paths)):

            args = OmegaConf.load(f'{path_to_yaml}/{i}')
            firstname, middlename, lastname = args.name.split()
            cur.execute(
                f"""
                INSERT INTO man (firstname, middlename, lastname, istina_url)
                VALUES (?, ?, ?, ?);""",
                (firstname, middlename, lastname, args.istina_people)
            )

            for item in args.news:

                try:
                    html = requests.get(item[0])
                except:
                    cur.execute(
                        f"""INSERT INTO train (man_id, train_url, relevant)
                        VALUES (?, ?, ?);""", (ind+1, item[0], item[1]))
                    continue
                if html.status_code != 200:
                    cur.execute(
                        f"""INSERT INTO train (man_id, train_url, relevant)
                        VALUES (?, ?, ?);""", (ind+1, item[0], item[1]))
                    continue

                cur.execute(
                    f"""INSERT INTO train (raw_text, man_id, train_url, relevant)
                    VALUES (?, ?, ?, ?);""", (html.text, ind+1, item[0], item[1]))

        con.commit()
        con.close()

    def update(self):
        con = sq.connect(f'{self.name}.db')
        cur = con.cursor()

        cur.execute(
            f"""
            select train.train_url, train.train_id
            from train
            where length(raw_text)==0;""")
        search = cur.fetchall()
        for item in search:
            try:
                html = requests.get(item[0])
            except:
                continue
            if html.status_code != 200:
                continue

            cur.execute(
                f"""UPDATE train
                    SET raw_text = ?
                    WHERE train_url = ?;""",
                (html.text, item[1]))

        con.commit()
        con.close()


if __name__ == '__main__':
    Database().yaml_to_sqlite(os.path.abspath("description"))
