"""
This file handles the server request that are made
by the app.
"""

from flask import Flask, request
from flask_restful import Resource, Api
import http.client
import json

# We need this every time.
app = Flask('__name__')
api = Api(app)

"""
This will be the endpoint that will handle the teams.
The Method will return the teams for a particular league,
the league name will be passed by the user through the api
connection made through the ios app.
"""


def get_team(name):
    if name.__eq__("EPL"):
        return get_standings("2021")   # Give a call to the method that connects to api along with league id.

    elif name.__eq__("Ligue1"):
        return get_ligue1_teams()

    elif name.__eq__("Bundesliga"):
        return get_bundesliga_teams()

    elif name.__eq__("Seria"):
        return get_seria_teams()


# This method returns all the teams in EPL.
def get_epl_teams():
    return "EPL"


# This method will return all the teams in Ligue 1
def get_ligue1_teams():
    return "L"


# This method will return all the teams in Bundesliga
def get_bundesliga_teams():
    return "Bundesliga"


# This method will return all the teams in Seria
def get_seria_teams():
    return "seria"


"""
This method connects to the api and gets all the teams.
"""


def get_teams(compid: int):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': '19cc4453060143bf9c3e4ff86f2cf1c2'}
    connection.request('GET', '/v2/competitions/'+str(compid)+'/teams', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    teams = response['teams']
    return teams


def get_standings(compid):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': '19cc4453060143bf9c3e4ff86f2cf1c2'}
    connection.request('GET', '/v2/competitions/' + compid + '/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    standings = response
    return standings


"""
These are the classes that represents the endpoints.
"""


class Team(Resource):
    def get(self,name):
        return get_team(name)
        # return {"About": name}, 200


class Default(Resource):
    def get(self):
        return {"About":"Hello World"}, 200
        # return get_data_from_api()

    def post(self):
        some_json = request.get_json()
        return {"Your": some_json}, 201


class Standings(Resource):
    def get(self):
        return "League Table"


api.add_resource(Default, '/')
api.add_resource(Team,'/team/<string:name>')
# api.add_resource(Team,'/standings/<string:name>') Make a class for standings.


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10)
