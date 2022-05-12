import requests
import pandas as pd
import json
import numpy as np
from sqlalchemy import create_engine
import psycopg2


#CONFIG = dotenv_values('.env')
#if not CONFIG:
#    CONFIG = os.environ

connection_uri = "postgresql+psycopg2://{}:{}@{}:{}".format(
    'postgres',
    'root',
    'localhost',
    '5432'
#    CONFIG["POSTGRES_USER"], CONFIG["POSTGRES_PASSWORD"], CONFIG['POSTGRES_HOST'], CONFIG["POSTGRES_PORT"],
)

engine = create_engine(connection_uri, pool_pre_ping=True)
engine.connect()

count_pokemons = requests.get('https://pokeapi.co/api/v2/pokemon/?offset=1').json()['count']
count_abilities = requests.get('https://pokeapi.co/api/v2/ability/?offset=1').json()['count']
count_types = requests.get('https://pokeapi.co/api/v2/type/?offset=1').json()['count']

def returnAbilities(count):
    df=pd.DataFrame()
    for i in range(1,count):
        resp = requests.get('https://pokeapi.co/api/v2/ability/'+ str(i)).json()   
        dt = pd.DataFrame(
            {
                'id_ability':[resp['id']],
                'name':[resp['name']],
                'effect_entries': resp['effect_entries'][1]['effect'] 
            }
        )
        df = pd.concat([df,dt],ignore_index=True)
    return df

def returnTypes(count):
    df=pd.DataFrame()
    for i in range(1,count):
        resp = requests.get('https://pokeapi.co/api/v2/type/'+ str(i)).json()   
        for typeDamage in resp['damage_relations']: typeDamage
        print(typeDamage)
        dt = pd.DataFrame(
            {
                'id_type':resp['id'],
                'name':resp['name'],
                'damage_relations':typeDamage,
                'id_type_relation':np.array([(typeDamage['url'].split('/')[-2]) for typeDamage in resp['damage_relations']['double_damage_to']])
            }
        )
        print(dt)
        df = pd.concat([df,dt],ignore_index=True)
        return df

def returnRelations(id_pokemon,id_item_relation,name_relation):
    df = pd.DataFrame(
        {
            'id_Pokemon':[id_pokemon],
            name_relation:[id_item_relation]
        }
    )
    return df

    
def returnPokemons(count):
    df=pd.DataFrame()
    for i in range(1,count):
        print(i)
        resp = requests.get('https://pokeapi.co/api/v2/pokemon/'+ str(i)+'/?limit=200').json()   
        dt = pd.DataFrame(
            {
                'id_pokemon':[resp['id']],
                'name':[resp['name']],
                'base_experience':[resp['base_experience']],
                'weight':[resp['weight']],
                'height':[resp['height']],
                'is_default':[resp['is_default']]
                #'order':[resp['order']]
            }
        )
        df = pd.concat([df,dt],ignore_index=True)
        df_relation = pd.DataFrame()
        for ability in resp['abilities']:
            dr = returnRelations(
                resp['id'],
                (ability['ability']['url']).split('/')[-2],
                'id_ability'
            ) 
            df_relation = pd.concat([df_relation,dr],ignore_index=True)
        print('ahgsdjaghshdah')
        print(df_relation)
    return df, df_relation



df,df_relation = returnPokemons(10)





