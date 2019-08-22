from builtins import classmethod

from es import es


class City:
    def __init__(self):
        pass

    @classmethod
    def get_cities(cls, state):
        city_data = es.search(
            index='my_country_index_3',
            body={
                'size': 10000,
                'query': {"bool": {"must": [{"match": {"_type": "city"}}, {"match": {"state": state}}]}}
            },
            filter_path=['hits.hits._id', 'hits.hits._source']
        )
        cities = []
        if 'hits' in city_data and 'hits' in city_data['hits']:
            cities = [{"id": data["_id"], "name": data["_source"]["name"]} for data in city_data['hits']['hits']]
        return cities
