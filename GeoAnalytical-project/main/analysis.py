import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import random
# import geopandas as gpd

pd.set_option("display.notebook_repr_html", False)
pd.set_option("display.max_columns", 30)
pd.set_option("display.max_rows", 300000)
pd.set_option("display.width", 800)



def connectPostgreSQL():
    # Функция подключения к БД PostgreSQL
    engine = create_engine('postgresql://postgres:Paul1235813@localhost:5432/postgres')
    print(f"\nConnecting to PostgreSQL ...\n\t{datetime.now()}\n")
    return engine.connect()


def disconnectPostgreSQL(engine):
    # Функция отключения от БД PostgreSQL
    print(f"\nDisonnecting from PostgreSQL ...\n\t{datetime.now()}\n")
    engine.close()


def read_data(Regions, TableName,SelectedYear, postgreSQLConnection):
    # выборка первоначальных данных из БД
    df_data = pd.read_sql(f"SELECT * FROM {TableName} order by id", postgreSQLConnection)
    # установка столбца id, как index
    df_data = df_data.set_index(df_data.id)
    # выборка по интересующим нас субъектам РФ
    df_data = df_data[df_data.index.isin(Regions)]
    # выборка по интересующим нас годам
    df_data = df_data.iloc[:, SelectedYear]
    # устанавливаем регион, как индекс и удаляем лишний столбец
    df_data.set_index(df_data.regions, inplace=True)
    df_data.drop(['regions'], axis = 1, inplace=True)
    # вывод DataFrame в консоль
    print(df_data)
    # Возвращаем финальный DataFrame
    return df_data

def addToPostgreSQL(new_table_name, location ='C:/Users/Sergeev/Desktop/GeoDataSets/CSV_FILE_NAME'):
    # Запись в базу из CSV
    postgreSQLConnection = connectPostgreSQL()
    df2 = pd.read_csv(f'{location}.csv')
    df2.to_sql(new_table_name, postgreSQLConnection)
    disconnectPostgreSQL(postgreSQLConnection)

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



def get_plot_bar(df):
    plt.switch_backend('AGG')
    # Транспонируем DataFrame 
    df = df.T
    df.plot(figsize=(12,6), kind='bar')
    # 
    # Присваиваем имя графику
    plt.title('Отправленно пассажиров железнодорожным транспортом')
    # Выставляем название x оси
    plt.xlabel('Год')
    plt.xticks(rotation=45)
    # Выставляем название y оси
    plt.ylabel('тыс. чел.')
    # рисуем сетку
    plt.grid()
    plt.legend(loc="best")
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_plot_pie(df):
    plt.switch_backend('AGG')
    # Словарь лет
    # SelectedYear_Dict ={0:'2005', 1:'2010', 2:'2015', 3:'2018', 4:'2019', 5:'2020'}

    print(f"{df.shape[1]=}")
    SelectedYear = random.randint(0,df.shape[1]-1)
    print(f"{SelectedYear=}")
    df = df.iloc[:, [SelectedYear]]

    Selected_Year_Name = df.columns
    df.plot(figsize=(12,6), kind='pie', subplots=True, autopct='%.2f')
    # Присваиваем имя графику
    plt.title(f'Отправленно пассажиров железнодорожным транспортом (%) в 2020')
    plt.legend(bbox_to_anchor=(0.6, 1.2))
    plt.tight_layout() 
    graph = get_graph()
    return graph

def report_1(postgreSQLConnection):
    df_data = pd.read_sql(f"select rp.id as id, rp.regions as regions, rp.\"2020\" as population, nd.\"2020\" as dtp from region_population rp left join number_dtp nd on rp.id = nd.id order by id", postgreSQLConnection)
    df_data = df_data.set_index(df_data.regions)
    df_data.drop(['id', 'regions'], axis = 1, inplace=True)
    df_data['ds'] = round(df_data.population *1000 / df_data.dtp, 2)
    print(df_data)
    # test2.adfg()
    # shp = gpd.read_file(r"C:\Users\Sergeev\Desktop\DSMW\DSMW.shp")
    # shp.plot()
    # plt.show()



