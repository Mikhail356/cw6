CREATE TABLE train (
    train_id integer primary key autoincrement, 
    raw_text text default "", 
    man_id integer, 
    relevant integer, 
    train_url text
    );

CREATE TABLE man (
    man_id integer primary key autoincrement, 
    firstname text, 
    middlename text, 
    lastname text, 
    istina_url text
    );