import os
from builtins import int, len

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from elasticsearch import Elasticsearch
from flask_bootstrap import Bootstrap

from forms.country import CountryForm, EditCountryForm
from models.country import Country
from models.state import State
from models.city import City

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
    country_data = Country.get_countries(es)
    if len(country_data) > 0:
        return jsonify({"country": country_data}), 200
    else:
        return jsonify({"error": True, "message": "No data present for countries"}), 200


@app.route("/get_state", methods=['GET'])
def get_state():
    country = request.args.get("country", type=str)
    if not country:
        return jsonify({"message": "Please set the country field"}), 400
    state_data = State.get_states(country, es)
    if len(state_data) > 0:
        return jsonify({"state": state_data}), 200
    else:
        return jsonify({"error": True, "message": "No state data present for country - " + country}), 200


@app.route("/get_city", methods=['GET'])
def get_city():
    state = request.args.get("state", type=str)
    if not state:
        return jsonify({"message": "Please set the state field"}), 400
    city_data = City.get_cities(state, es)
    if len(city_data) > 0:
        return jsonify({"city": city_data}), 200
    else:
        return jsonify({"error": True, "message": "No city data present for state - " + state}), 200


@app.route("/country", methods=['GET'])
def country():
    return render_template("crud/country/list.html", countries=Country.get_countries(es))


@app.route("/country/create", methods=['GET', 'POST'])
def country_create():
    country_form = CountryForm()
    if request.method == 'POST':
        if not country_form.validate():
            flash('All fields are required.')
            return render_template('crud/country/create.html', form=country_form)
        else:
            result = Country.create_country(request.form["name"], es)
            if result:
                flash('Country created successfully!!!')
                return redirect(url_for('country'))
            else:
                flash('Unable to create country.')
                return render_template('crud/country/create.html', form=country_form)
    else:
        return render_template('crud/country/create.html', form=country_form)


@app.route("/country/edit/<id>", methods=['GET', 'POST'])
def country_edit(id):
    print(id)
    country_form = EditCountryForm()
    if request.method == 'POST':
        if not country_form.validate():
            flash('All fields are required.')
            return render_template('crud/country/edit.html', form=country_form)
        else:
            result = Country.edit_country(request.form["id"], request.form["name"], es)
            if result:
                flash('Country edited successfully!!!')
                return redirect(url_for('country'))
            else:
                flash('Unable to edit country.')
                return render_template('crud/country/edit.html', form=country_form)
    else:
        country = Country.get_country(id, es)
        if not country:
            return redirect(url_for('country'))
        country_form.name.data = country["name"]
        country_form.id.data = country["id"]
        return render_template('crud/country/edit.html', form=country_form)


if __name__ == "__main__":
    app.run(port=5005, debug=True, host="0.0.0.0")
