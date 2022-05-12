import requests
import pandas as pd
import json
import numpy as np
from sqlalchemy import create_engine


CONFIG = dotenv_values('.env')
if not CONFIG:
    CONFIG = os.environ

connection_uri = "postgresql+psycopg2://{}:{}@{}:{}".format(
    CONFIG["POSTGRES_USER"],
    CONFIG["POSTGRES_PASSWORD"],
    CONFIG['POSTGRES_HOST'],
    CONFIG["POSTGRES_PORT"],
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
                'id':[resp['id']],
                'name':[resp['name']],
                'effect_entries': resp['effect_entries'][1]['effect'] 
            }
        )
        df = pd.concat([df,dt],ignore_index=True)

def returnTypes(count):
    df=pd.DataFrame()
    for i in range(1,count):
        resp = requests.get('https://pokeapi.co/api/v2/type/'+ str(k)).json()   
        for typeDamage in resp['damage_relations']: typeDamage
        print(typeDamage)
        dt = pd.DataFrame(
            {
                'id':resp['id'],
                'name':resp['name'],
                'damage_relations':typeDamage,
                'pokemonRelation':np.array([(typeDamage['name']) for typeDamage in resp['damage_relations']['double_damage_to']])
            }
        )
        print(dt)
        df = pd.concat([df,dt],ignore_index=True)


    
def returnPokemons(count):
df=pd.DataFrame()
for i in range(1,10):
    resp = requests.get('https://pokeapi.co/api/v2/pokemon/'+ str(i)+'/?limit=200').json()   
    dt = pd.DataFrame(
        {
            'id':[resp['id']],
            'name':[resp['name']],
            'base_experience':[resp['base_experience']],
            'weight':[resp['weight']],
            'height':[resp['height']],
            'is_default':[resp['is_default']],
            'order':[resp['order']]
        }
    )
    df = pd.concat([df,dt],ignore_index=True)
    def returnRelations(url,id):
        print('entroooou')
        print(url)
        id_Ability = url.split('/')[-2]
        dr = pd.DataFrame(
            {
                'id_Pokemon':id,
                'id_Ability': id_Ability
            }
        )
        da = pd.concat([da,dr],ignore_index=True)
    da = pd.DataFrame(columns=['id'])
    np.array([returnRelations((ability['ability']['url']),resp['id']) for ability in resp['abilities']])





>>> with open('json_data.json', 'w') as outfile:
...     json.dump(resp,outfile)




