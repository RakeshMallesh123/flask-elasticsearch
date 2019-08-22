import os
from builtins import classmethod, int
from datetime import datetime
from es import es


class Country:
    def __init__(self):
        pass

    @classmethod
    def list(cls):
        country_data = es.search(index=os.environ.get("INDEX"),
                                 body={'size': 10000, 'query': {"match": {"_type": "country"}}},
                                 filter_path=['hits.hits._id', 'hits.hits._source'])
        countries = []
        if 'hits' in country_data and 'hits' in country_data['hits']:
            countries = [{"id": data["_id"], "name": data["_source"]["name"]} for data in country_data['hits']['hits']]
        return countries

    @classmethod
    def get(cls, id):
        country_data = es.search(index=os.environ.get("INDEX"),
                                 body={'query': {"bool": {"must": [{"match": {"_type": "country"}},
                                                                   {'match': {'_id': id}}
                                                                   ]}}})
        if 'hits' in country_data and 'hits' in country_data['hits']:
            return {"id": country_data['hits']['hits'][0]['_id'],
                    "name": country_data['hits']['hits'][0]["_source"]["name"]}
        return False

    @classmethod
    def create(cls, name):
        id = int(datetime.timestamp(datetime.now()) * 1000)
        res = es.index(index=os.environ.get("INDEX"), doc_type='country', id=id, body={"name": name})
        if "created" in res and res["created"]:
            return True
        return False

    @classmethod
    def edit_country(cls, id, name):
        res = es.index(index=os.environ.get("INDEX"), doc_type='country', id=id, body={"name": name})
        if "result" in res and res["result"] == "updated":
            return True
        return False

    @classmethod
    def delete(cls, id):
        country_rec = Country.get(id)
        if country_rec:
            res = es.delete(index=os.environ.get("INDEX"), doc_type='country', id=id)
            if "found" in res and res["found"] and "result" in res and res["result"] == "deleted":
                return True
        return False
