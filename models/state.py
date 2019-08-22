from builtins import classmethod, int
from datetime import datetime

from models.country import Country

from es import es


class State:
    def __init__(self):
        pass

    @classmethod
    def get_states(cls, country):
        if country != "":
            state_data = es.search(
                index='my_country_index_3',
                body={
                    'size': 10000,
                    'query': {"bool": {"must": [{"match": {"_type": "state"}}, {"match": {"country": country}}]}}
                },
                filter_path=['hits.hits._id', 'hits.hits._source', 'hits.hits._parent']
            )
        else:
            state_data = es.search(
                index='my_country_index_3',
                body={
                    'size': 10000,
                    'query': {"match": {"_type": "state"}}
                },
                filter_path=['hits.hits._id', 'hits.hits._source', 'hits.hits._parent']
            )
        states = []
        if 'hits' in state_data and 'hits' in state_data['hits']:
            states = [
                {"id": data["_id"], "name": data["_source"]["name"]+" - "+data["_parent"], "parent": data["_parent"],
                 "country": data["_source"]["country"]}
                for data in state_data['hits']['hits']
                if "_parent" in data
            ]
        return states

    @classmethod
    def get_state(cls, id):
        state_data = es.search(index='my_country_index_3',
                                 body={'query': {"bool": {"must": [{"match": {"_type": "state"}},
                                                                   {'match': {'_id': id}},
                                                                   ]}}})
        if 'hits' in state_data and 'hits' in state_data['hits']:
            return {"id": state_data['hits']['hits'][0]['_id'],
                    "name": state_data['hits']['hits'][0]["_source"]["name"],
                    "parent": state_data['hits']['hits'][0]["_parent"],
                    "country": state_data['hits']['hits'][0]["_source"]["country"]}
        return False

    @classmethod
    def create_state(cls, name, country):
        country_rec = Country.get_country(country)
        if country_rec:
            id = int(datetime.timestamp(datetime.now()) * 1000)
            body = {"name": name, "country": country_rec["name"]}
            res = es.index(index='my_country_index_3', doc_type='state', id=id, parent=country_rec["id"], body=body)
            if "created" in res and res["created"]:
                return True
        return False

    @classmethod
    def edit_state(cls, id, name, country):
        country_rec = Country.get_country(country)
        if country_rec:
            res = es.index(index='my_country_index_3', doc_type='state', id=id, parent=country_rec["id"],
                           body={"name": name, "country": country_rec["name"]})
            print(res)
            if "result" in res and res["result"] == "updated":
                return True
        return False
