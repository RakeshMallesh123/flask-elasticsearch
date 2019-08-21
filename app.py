import os
from builtins import int, len

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from elasticsearch import Elasticsearch
from flask_bootstrap import Bootstrap
from datetime import datetime

from forms.country import CountryForm

es = Elasticsearch('http://localhost:9200')

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(12).hex()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dd")
def dd():
    return render_template("dependent_dropdown.html")


@app.route("/get_country", methods=['GET'])
def get_country():
    country_data = get_countries()
    if len(country_data) > 0:
        return jsonify({"country": country_data}), 200
    else:
        return jsonify({"error": True, "message": "No data present for countries"}), 200


@app.route("/get_state", methods=['GET'])
def get_state():
    country = request.args.get("country", type=str)
    if not country:
        return jsonify({"message": "Please set the country field"}), 400
    state_data = get_states(country)
    if len(state_data) > 0:
        return jsonify({"state": state_data}), 200
    else:
        return jsonify({"error": True, "message": "No state data present for country - " + country}), 200


@app.route("/get_city", methods=['GET'])
def get_city():
    state = request.args.get("state", type=str)
    if not state:
        return jsonify({"message": "Please set the state field"}), 400
    city_data = get_cities(state)
    if len(city_data) > 0:
        return jsonify({"city": city_data}), 200
    else:
        return jsonify({"error": True, "message": "No city data present for state - " + state}), 200


@app.route("/country", methods=['GET'])
def country():
    return render_template("crud/country/list.html", countries=get_countries())


@app.route("/country/create", methods=['GET', 'POST'])
def country_create():
    country_form = CountryForm()
    if request.method == 'POST':
        if not country_form.validate():
            flash('All fields are required.')
            return render_template('crud/country/create.html', form=country_form)
        else:
            result = create_country(request.form["name"])
            if result:
                flash('Country created successfully!!!')
                return redirect(url_for('country'))
            else:
                flash('Unable to create country.')
                return render_template('crud/country/create.html', form=country_form)
    elif request.method == 'GET':
        return render_template('crud/country/create.html', form=country_form)

    return render_template("crud/country/create.html", form=country_form)


def get_countries():
    country_data = es.search(index='my_country_index_3',
                             body={'size': 10000, 'query': {"match": {"_type": "country"}}},
                             filter_path=['hits.hits._id', 'hits.hits._source'])
    countries = []
    if 'hits' in country_data and 'hits' in country_data['hits']:
        countries = [{"id": data["_id"], "name": data["_source"]["name"]} for data in country_data['hits']['hits']]
    return countries


def get_states(country):
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


def get_cities(state):
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


def create_country(name):
    id = int(datetime.timestamp(datetime.now())*1000)
    res = es.index(index='my_country_index_3', doc_type='country', id=id, body={"name": name})
    if "result" in res and res["result"] == "created":
        return True
    return False


if __name__ == "__main__":
    app.run(port=5005, debug=True, host="0.0.0.0")
