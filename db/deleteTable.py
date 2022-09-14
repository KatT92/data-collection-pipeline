import connect
connect.engine.connect()
connect.engine.execute('DROP TABLE IF EXISTS games;')  # DELETE FROM games;
