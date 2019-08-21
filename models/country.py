from builtins import object, classmethod, int
from datetime import datetime


class Country(object):
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
    def create_country(cls, name, es):
        id = int(datetime.timestamp(datetime.now()) * 1000)
        res = es.index(index='my_country_index_3', doc_type='country', id=id, body={"name": name})
        if "result" in res and res["result"] == "created":
            return True
        return False
