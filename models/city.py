from builtins import classmethod, int
from datetime import datetime

from models.state import State
from es import es


class City:
    def __init__(self):
        pass

    @classmethod
    def get_cities(cls, state):
        if state != "":
            city_data = es.search(
                index='my_country_index_3',
                body={
                    'size': 10000,
                    'query': {"bool": {"must": [{"match": {"_type": "city"}}, {"match": {"state": state}}]}}
                },
                filter_path=['hits.hits._id', 'hits.hits._source', 'hits.hits._parent']
            )
        else:
            city_data = es.search(
                index='my_country_index_3',
                body={
                    'size': 10000,
                    'query': {"match": {"_type": "city"}}
                },
                filter_path=['hits.hits._id', 'hits.hits._source', 'hits.hits._parent']
            )
        cities = []
        if 'hits' in city_data and 'hits' in city_data['hits']:
            cities = [
                {"id": data["_id"], "name": data["_source"]["name"], "parent": data["_parent"],
                 "state": data["_source"]["state"]}
                for data in city_data['hits']['hits']
                if "_parent" in data
            ]
        return cities

    @classmethod
    def get_city(cls, id):
        city_data = es.search(index='my_country_index_3',
                                 body={'query': {"bool": {"must": [{"match": {"_type": "city"}},
                                                                   {'match': {'_id': id}},
                                                                   ]}}})
        if 'hits' in city_data and 'hits' in city_data['hits']:
            return {"id": city_data['hits']['hits'][0]['_id'],
                    "name": city_data['hits']['hits'][0]["_source"]["name"],
                    "parent": city_data['hits']['hits'][0]["_parent"],
                    "state": city_data['hits']['hits'][0]["_source"]["state"]}
        return False

    @classmethod
    def create_city(cls, name, state):
        state_rec = State.get_state(state)
        if state_rec:
            id = int(datetime.timestamp(datetime.now()) * 1000)
            body = {"name": name, "state": state_rec["name"]}
            res = es.index(index='my_country_index_3', doc_type='city', id=id, parent=state_rec["id"], body=body)
            if "created" in res and res["created"]:
                return True
        return False

    @classmethod
    def edit_city(cls, id, name, state):
        state_rec = State.get_state(state)
        if state_rec:
            res = es.index(index='my_country_index_3', doc_type='city', id=id, parent=state_rec["id"],
                           body={"name": name, "state": state_rec["name"]})
            print(res)
            if "result" in res and res["result"] == "updated":
                return True
        return False
