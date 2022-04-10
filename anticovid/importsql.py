import pandas as pd;
from sqlalchemy import create_engine

df = pd.read_csv('<exact path to food_compound_simplified.csv>')

engine = create_engine('mysql://<user>:<password>@localhost/<database-name>')
df.to_sql('ingredient', con=engine)
