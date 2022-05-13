import requests
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
import re

from sqlalchemy.orm import scoped_session, sessionmaker


#CONFIG = dotenv_values('.env')
#if not CONFIG:
#    CONFIG = os.environ

connection_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    'postgres',
    'root',
    'localhost',
    '5432',
    'data_challenge'
#    CONFIG["POSTGRES_USER"], CONFIG["POSTGRES_PASSWORD"], CONFIG['POSTGRES_HOST'], CONFIG["POSTGRES_PORT"],
)

engine = create_engine(connection_uri, pool_pre_ping=True)

#db = scoped_session(sessionmaker(bind=engine))
conn = engine.connect()

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


def loadAbilities(count):
    for i in range(1,count):
        resp = requests.get('https://pokeapi.co/api/v2/ability/'+ str(i)).json()  
        id = resp['id']
        print(resp['id'])
        name = resp['name']
        effect = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]','',(resp['effect_entries'][1]['effect']))
        query = "INSERT INTO public.db_abilities(id_ability, name, effect_entries) VALUES(%s,\'%s\', \'%s\');" % (id,name,effect)
        print(query)
        conn.execute(query)


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


def loadTypes(count):
    for i in range(1,count):
        resp = requests.get('https://pokeapi.co/api/v2/type/'+ str(i)).json()   
        id = resp['id']
        name=resp['name']
        damage_relations = str(resp['damage_relations']).replace('\'','"')
        query = "INSERT INTO public.db_types(id_type, name, damage_relations) VALUES(%s,\'%s\', \'%s\');" % (id,name,damage_relations)
        print(query)
        conn.execute(query)
    

def loadRelations(id_pokemon,id_item_relation,name_relation):
    print(name_relation)
    query = "INSERT INTO public.db_vinc_pokemon_%s (id_pokemon,id_%s) VALUES(%s,%s);" % (name_relation,name_relation,id_pokemon,id_item_relation)
    conn.execute(query)


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
    df_relation_abilities = pd.DataFrame()
    df_relation_types = pd.DataFrame()
    for i in range(1,count):
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
        da = returnRelations(
            resp['id'],
            np.array([(ability['ability']['url'].split('/')[-2]) for ability in resp['abilities']]) ,
            'id_ability'
        )
        dt = returnRelations(
            resp['id'],
            np.array([(type['type']['url'].split('/')[-2]) for type in resp['types']]) ,
            'id_type'
        ) 
        df_relation_abilities = pd.concat([df_relation_abilities,da],ignore_index=True)
        df_relation_types = pd.concat([df_relation_types,dt],ignore_index=True)
    return df, df_relation_abilities, df_relation_types


def loadPokemons(count):
    for i in range(1,count):
        resp = requests.get('https://pokeapi.co/api/v2/pokemon/'+ str(i)+'/?limit=200').json()   
        id_pokemon=resp['id']
        name=resp['name']
        base_experience=resp['base_experience']
        weight=resp['weight']
        height=resp['height']
        is_default=resp['is_default']
        #'order':[resp['order']]
        
        query = "INSERT INTO public.db_pokemon (id_pokemon, name, base_experience, weight, height, is_default) VALUES(%s, \'%s\', %s, %s, %s, %s);" % (id_pokemon,name,base_experience,weight,height,is_default)
        print(query)
        conn.execute(query)

        for ability in resp['abilities']:
            loadRelations(
                resp['id'],
                (ability['ability']['url'].split('/')[-2]) ,
                'ability'
            )     
        
        for type in resp['types']:
            loadRelations(
                resp['id'],
                (type['type']['url'].split('/')[-2]),
                'type'
            )   

