from builtins import classmethod


class State:
    def __init__(self):
        pass

    @classmethod
    def get_states(cls, country, es):
        state_data = es.search(
            index='my_country_index_3',
            body={
                'size': 10000,
                'query': {"bool": {"must": [{"match": {"_type": "state"}}, {"match": {"country": country}}]}}
            },
            filter_path=['hits.hits._id', 'hits.hits._source']
        )
        states = []
        if 'hits' in state_data and 'hits' in state_data['hits']:
            states = [{"id": data["_id"], "name": data["_source"]["name"]} for data in state_data['hits']['hits']]
        return states
