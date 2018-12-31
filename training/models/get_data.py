import pymongo
import pandas as pd
from pymongo import MongoClient
from pprint import pprint

class GetData:
    def __init__(self, host, port, database, collection):
        self.client = MongoClient(host, port)
        self.db = self.client[database]
        self.collection = self.db[collection]

    #normalize to 1 or 0 the predict value
    def norm_pred(self, prev, future):
        if future > prev:
            return 1
        else:
            return 0

    #format and process all data
    def get_all_processed_data(self):
        all_data = []
        for data in self.collection.find().sort('date'):
            columns = []
            columns.append(data['date'])
            columns.append(data['cotation'])
            columns.append(data['minimum'])
            columns.append(data['maximum'])
            columns.append(data['value_variation'])
            columns.append(data['volume'])
            all_data.append(columns)
        
        df = pd.DataFrame(all_data, columns=['data/hora', 'cotação', 'mínima', 'máxima', 'variação', 'volume'])
        df.set_index('data/hora', inplace=True)
        df['target'] = df['cotação'].shift(-1)
        df = df[:-2]
        df['target'] = list(map(self.norm_pred, df['cotação'], df['target']))
        
        return df