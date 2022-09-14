import connect

# Read
result_set = connect.engine.execute("SELECT game_name FROM games")
for r in result_set:
    print(r)
