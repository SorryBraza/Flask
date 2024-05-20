import pydantic
from flask import Flask, jsonify
from flask import request
from flask.views import MethodView
from models import Ads, Session
from sqlalchemy.exc import IntegrityError
from schema import CreateAds

app = Flask("app")


def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop('ctx', None)
        raise HttpError(400, error)


class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


def get_ad_by_id(ad_id: int):
    ad = request.session.get(Ads, ad_id)
    if ad is None:
        raise HttpError(status_code=404, description="advertisement not found")
    return ad


def add_ad(ad: Ads):
    try:
        request.session.add(ad)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(status_code=409, description="advertisement already exist")
    return ad


class AdsView(MethodView):
    def get(self, ads_id: int):
        ads = get_ad_by_id(ads_id)
        return jsonify(ads.json)

    def post(self):
        json_data = validate(CreateAds, request.json)
        ad = Ads(**json_data)
        add_ad(ad)
        response = jsonify(ad.json)
        response.status_code = 201
        return response

    def delete(self, ads_id: int):
        ad = get_ad_by_id(ads_id)
        request.session.delete(ad)
        request.session.commit()
        return jsonify({"status": "success"})


ads_view = AdsView.as_view("ads_view")

app.add_url_rule(rule="/ads/", view_func=ads_view, methods=['POST'])
app.add_url_rule(rule="/ads/<int:ads_id>", view_func=ads_view,
                 methods=['GET', 'DELETE'])

app.run()
