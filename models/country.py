from builtins import classmethod, int
from datetime import datetime


class Country:
    def __init__(self):
        pass

    @classmethod
    def get_countries(cls, es):
        country_data = es.search(index='my_country_index_3',
                                 body={'size': 10000, 'query': {"match": {"_type": "country"}}},
                                 filter_path=['hits.hits._id', 'hits.hits._source'])
        countries = []
        if 'hits' in country_data and 'hits' in country_data['hits']:
            countries = [{"id": data["_id"], "name": data["_source"]["name"]} for data in country_data['hits']['hits']]
        return countries

    @classmethod
    def get_country(cls, id, es):
        country_data = es.search(index='my_country_index_3',
                                 body={'query': {"bool": {"must": [{"match": {"_type": "country"}},
                                                                   {'match': {'_id': id}}
                                                                   ]}}})
        if 'hits' in country_data and 'hits' in country_data['hits']:
            return {"id": country_data['hits']['hits'][0]['_id'],
                    "name": country_data['hits']['hits'][0]["_source"]["name"]}
        return False

    @classmethod
    def create_country(cls, name, es):
        id = int(datetime.timestamp(datetime.now()) * 1000)
        res = es.index(index='my_country_index_3', doc_type='country', id=id, body={"name": name})
        if "result" in res and res["result"] == "created":
            return True
        return False

    @classmethod
    def edit_country(cls, id, name, es):
        res = es.index(index='my_country_index_3', doc_type='country', id=id, body={"name": name})
        if "result" in res and res["result"] == "updated":
            return True
        return False
