import pandas as pd
from connection import engine

res = pd.read_excel("test.xlsx")
df = pd.DataFrame(data=res)
df.to_sql(con=engine, if_exists="replace", name="test", index=False)

if __name__ == "__main__":
    print("Ok")
