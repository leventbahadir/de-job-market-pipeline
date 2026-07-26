import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER_SUPABASE')}:{os.getenv('DB_PASSWORD_SUPABASE')}"
    f"@{os.getenv('DB_HOST_SUPABASE')}:{os.getenv('DB_PORT_SUPABASE')}"
    f"/{os.getenv('DB_NAME_SUPABASE')}"
)


df = pd.read_csv('uscities.csv')

df.to_sql(
    name='dim_location',
    schema='marts',
    con=engine,
    if_exists='replace',  # or 'append'
    index=False
)

print(f"Loaded {len(df)} rows")