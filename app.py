from flask import Flask, render_template, request, jsonify

from elasticsearch import Elasticsearch
es = Elasticsearch('http://localhost:9200')

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dd")
def dd():
    return render_template("dependent_dropdown.html")


@app.route("/get_country", methods=['GET'])
def get_country():
    country_data = es.search(index='my_country_index_3', body={'query': {"match": {"_type": "country"}}},
              filter_path=['hits.hits._id', 'hits.hits._source'])
    if 'hits' in country_data and 'hits' in country_data['hits']:
        return jsonify({"country": [data["_source"]["name"] for data in country_data['hits']['hits']]}), 200
    else:
        return jsonify({"error": True, "message": "No data present for countries"}), 200


@app.route("/get_state", methods=['GET'])
def get_state():
    country = request.args.get("country", type=str)
    if not country:
        return jsonify({"message": "Please set the country field"}), 400
    state_data = es.search(
        index='my_country_index_3',
        body={'query': {"bool": {"must": [{"match": {"_type": "state"}}, {"match": {"country": country}}]}}},
        filter_path=['hits.hits._id', 'hits.hits._source']
    )
    if 'hits' in state_data and 'hits' in state_data['hits']:
        return jsonify({"state": [data["_source"]["name"] for data in state_data['hits']['hits']]}), 200
    else:
        return jsonify({"error": True, "message": "No state data present for country - " + country}), 200


@app.route("/get_city", methods=['GET'])
def get_city():
    state = request.args.get("state", type=str)
    if not state:
        return jsonify({"message": "Please set the state field"}), 400
    city_data = es.search(
        index='my_country_index_3',
        body={'query': {"bool": {"must": [{"match": {"_type": "city"}}, {"match": {"state": state}}]}}},
        filter_path=['hits.hits._id', 'hits.hits._source']
    )
    if 'hits' in city_data and 'hits' in city_data['hits']:
        return jsonify({"city": [data["_source"]["name"] for data in city_data['hits']['hits']]}), 200
    else:
        return jsonify({"error": True, "message": "No city data present for state - " + state}), 200


@app.route("/country")
def country():
    country_data = es.search(index='my_country_index_3', body={'query': {"match": {"_type": "country"}}},
              filter_path=['hits.hits._id', 'hits.hits._source'])
    country = []
    if 'hits' in country_data and 'hits' in country_data['hits']:
        countries = [{"id":data["_id"], "name":data["_source"]["name"]} for data in country_data['hits']['hits']]
    return render_template("crud/country/list.html", countries=countries)


if __name__ == "__main__":
    app.run(port=5005, debug=True, host="0.0.0.0")
