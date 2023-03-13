import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///db/cities.db')
connection = engine.connect()

