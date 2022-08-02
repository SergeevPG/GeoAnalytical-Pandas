from tkinter import image_types
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from datetime import datetime
pd.set_option("display.notebook_repr_html", False)
pd.set_option("display.max_columns", 30)
pd.set_option("display.max_rows", 166000)
pd.set_option("display.width", 800)
pd.set_option("display.max_colwidth", 50)

from sqlalchemy import create_engine
def connectPostgreSQL():
    engine = create_engine('postgresql://postgres:Paul1235813@localhost:5432/postgres')
    print(f"\nConnecting to PostgreSQL ...\n\t{datetime.now()}\n")
    return engine.connect()
def disconnectPostgreSQL(engine):
    print(f"\nDisonnecting from PostgreSQL ...\n\t{datetime.now()}\n")
    engine.close()
# def addToPostgreSQL():
#     # Запись в базу из CSV
#     postgreSQLConnection = connectPostgreSQL()
#     df2 = pd.read_csv(r'C:\Users\Sergeev\Desktop\GeoDataSets\CSV\region_population.csv', sep=";")
#     # df2 = df2[["regions", "2005", "2010", "2015", "2018", "2019", "2020"]]
#     df2.to_sql("region_population", postgreSQLConnection)
#     disconnectPostgreSQL(postgreSQLConnection)

# addToPostgreSQL()
# df = pd.read_csv(r'C:\Users\Sergeev\Desktop\GeoDataSets\CSV\bachelors_specialists_and_masters_degree_programs.csv', sep=";")
# # # df = df[["regions", "2005", "2010", "2015", "2018", "2019", "2020"]]
# print(f"\nOriginal DataSet Regions\nCount (rows, columns): {df.shape=}\n")
# print(df[:])
# print(df.columns)
def viewdata():
    postgreSQLConnection = connectPostgreSQL()
    df = pd.read_sql(f"SELECT * FROM region_population", postgreSQLConnection)
    df = df.iloc[1:5][['regions', '2005', '2010', '2015', '2018', '2019', '2020']]
    df.set_index(df.regions, inplace=True)
    df.drop(['regions'], axis = 1, inplace=True)
    # df = df.loc['Воронежская область']
    print(df)
    disconnectPostgreSQL(postgreSQLConnection)
    return df.T

import base64
from io import BytesIO
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(df):
    # plt.switch_backend('AGG')

    # fig, ax = plt.subplots()
    # ax.plot()


    # figure = plt.figure(figsize=(10,5), facecolor='grey')
    # ax1 = figure.add_subplot(2,2,1)
    # ax2 = figure.add_subplot(2,2,2)
    # ax3 = figure.add_subplot(2,2,3)




    # fig, axes = plt.subplots(2,2)
    df.plot(kind='bar')
    # figure.show()
    
    # df.plot(kind='bar')
    # plt.figure(figsize=(10,5))
    plt.title('SDADAS')
    plt.xticks(rotation=45)
    plt.xlabel('year')
    plt.ylabel('count')
    # plt.tight_layout()

    plt.show()
    # graph = get_graph()
    # return graph

df = viewdata()
get_plot(df)

