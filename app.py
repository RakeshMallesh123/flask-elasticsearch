import os
from builtins import int, len

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_bootstrap import Bootstrap

from forms.city import CityForm, EditCityForm
from forms.country import CountryForm, EditCountryForm
from forms.state import StateForm, EditStateForm
from models.country import Country
from models.state import State
from models.city import City

from es import es

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
    country_data = Country.get_countries()
    if len(country_data) > 0:
        return jsonify({"country": country_data}), 200
    else:
        return jsonify({"error": True, "message": "No data present for countries"}), 200


@app.route("/get_state", methods=['GET'])
def get_state():
    country = request.args.get("country", type=str)
    if not country:
        return jsonify({"message": "Please set the country field"}), 400
    state_data = State.get_states(country)
    if len(state_data) > 0:
        return jsonify({"state": state_data}), 200
    else:
        return jsonify({"error": True, "message": "No state data present for country - " + country}), 200


@app.route("/get_city", methods=['GET'])
def get_city():
    state = request.args.get("state", type=str)
    if not state:
        return jsonify({"message": "Please set the state field"}), 400
    city_data = City.get_cities(state)
    if len(city_data) > 0:
        return jsonify({"city": city_data}), 200
    else:
        return jsonify({"error": True, "message": "No city data present for state - " + state}), 200


@app.route("/country", methods=['GET'])
def country():
    return render_template("crud/country/list.html", countries=Country.get_countries())


@app.route("/country/create", methods=['GET', 'POST'])
def country_create():
    country_form = CountryForm()
    if request.method == 'POST':
        if not country_form.validate():
            flash('All fields are required.')
            return render_template('crud/country/create.html', form=country_form)
        else:
            result = Country.create_country(request.form["name"])
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
    country_form = EditCountryForm()
    if request.method == 'POST':
        if not country_form.validate():
            flash('All fields are required.')
            return render_template('crud/country/edit.html', form=country_form)
        else:
            result = Country.edit_country(request.form["id"], request.form["name"])
            if result:
                flash('Country edited successfully!!!')
                return redirect(url_for('country'))
            else:
                flash('Unable to edit country.')
                return render_template('crud/country/edit.html', form=country_form)
    else:
        country = Country.get_country(id)
        if not country:
            return redirect(url_for('country'))
        country_form.name.data = country["name"]
        country_form.id.data = country["id"]
        return render_template('crud/country/edit.html', form=country_form)


@app.route("/state", methods=['GET'])
def state():
    return render_template("crud/state/list.html", states=State.get_states(""))


@app.route("/state/create", methods=['GET', 'POST'])
def state_create():
    state_form = StateForm()
    if request.method == 'POST':
        if not state_form.validate():
            flash('All fields are required.')
            return render_template('crud/state/create.html', form=state_form)
        else:
            result = State.create_state(request.form["name"], request.form["country"])
            if result:
                flash('State created successfully!!!')
                return redirect(url_for('state'))
            else:
                flash('Unable to create state.')
                return render_template('crud/state/create.html', form=state_form)
    else:
        return render_template('crud/state/create.html', form=state_form)


@app.route("/state/edit/<id>/<country>", methods=['GET', 'POST'])
def state_edit(id, country):
    state_form = EditStateForm()
    if request.method == 'POST':
        if not state_form.validate():
            flash('All fields are required.')
            return render_template('crud/state/edit.html', form=state_form)
        else:
            result = State.edit_state(request.form["id"], request.form["name"], request.form["country"])
            if result:
                flash('State edited successfully!!!')
                return redirect(url_for('state'))
            else:
                flash('Unable to edit state.')
                return render_template('crud/state/edit.html', form=state_form)
    else:
        state = State.get_state(id)
        if not state:
            return redirect(url_for('state'))
        state_form.name.data = state["name"]
        state_form.country.data = state["parent"]
        state_form.id.data = state["id"]
        state_form.country_id.data = country
        return render_template('crud/state/edit.html', form=state_form)


@app.route("/city", methods=['GET'])
def city():
    return render_template("crud/city/list.html", cities=City.get_cities(""))


@app.route("/city/create", methods=['GET', 'POST'])
def city_create():
    city_form = CityForm()
    if request.method == 'POST':
        if not city_form.validate():
            flash('All fields are required.')
            return render_template('crud/city/create.html', form=city_form)
        else:
            result = City.create_city(request.form["name"], request.form["state"])
            if result:
                flash('City created successfully!!!')
                return redirect(url_for('city'))
            else:
                flash('Unable to create city.')
                return render_template('crud/city/create.html', form=city_form)
    else:
        return render_template('crud/city/create.html', form=city_form)


@app.route("/city/edit/<id>/<state>", methods=['GET', 'POST'])
def city_edit(id, state):
    city_form = EditCityForm()
    if request.method == 'POST':
        if not city_form.validate():
            flash('All fields are required.')
            return render_template('crud/city/edit.html', form=city_form)
        else:
            result = City.edit_city(request.form["id"], request.form["name"], request.form["state"])
            if result:
                flash('City edited successfully!!!')
                return redirect(url_for('city'))
            else:
                flash('Unable to edit city.')
                return render_template('crud/city/edit.html', form=city_form)
    else:
        city = City.get_city(id)
        if not city:
            return redirect(url_for('state'))
        print(city)
        city_form.name.data = city["name"]
        city_form.state.data = city["parent"]
        city_form.id.data = city["id"]
        city_form.state_id.data = city["parent"]
        return render_template('crud/city/edit.html', form=city_form)


if __name__ == "__main__":
    app.run(port=5005, debug=True, host="0.0.0.0")
