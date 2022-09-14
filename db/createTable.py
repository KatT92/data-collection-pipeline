import connect
# Create
sql_command = '''CREATE TABLE IF NOT EXISTS games(
    uuid varchar(255) PRIMARY KEY,
    id int,
    url varchar(255),
    game_name varchar(255),
    img varchar(255),
    rank_names varchar(255),
    ranks_numbers varchar(255),
    min_players int,
    max_players int,
    min_time int,
    max_time int,
    designer varchar(255)
);
'''
connect.engine.execute(sql_command)
