import http.client
import sys
import urllib.parse
import json
import readline
from api_utils import gametypes

server = "NA1"
with open('.apikey') as f:
    key = f.read().strip()
champions = {}
teams = {100:"Blue", 200:"Red"}


def getchamplist():
    """Polls Riot API for list of champions and returns a dict mapping champion
    ID to champion name.
    """
    conn = http.client.HTTPSConnection("na.api.pvp.net")
    url = "/api/lol/static-data/{}/v1.2/champion?{}".format(
            "na", urllib.parse.urlencode({"api_key": key}))
    conn.request("GET",url)
    resp = conn.getresponse().read().decode('utf-8')
    d = json.loads(resp)
    conn.close()
    return {d["data"][champ]["id"]: d["data"][champ]["name"]
            for champ in d["data"].keys()}

def get_info_from_name(name):
    """Returns dictionary representing GameInfo json object"""
    name = name.lower().replace(" ", "")
    conn = http.client.HTTPSConnection("na.api.pvp.net")
    url = "/api/lol/na/v1.4/summoner/by-name/{}?{}".format(
            urllib.parse.quote(name), urllib.parse.urlencode({"api_key": key}))
    conn.request("GET", url)
    resp = conn.getresponse().read().decode('utf-8')
    d = json.loads(resp)
    if "404" in resp:
        return {}
    conn.close()
    return d[name]

def getcurrentgame(uid):
    conn = http.client.HTTPSConnection("na.api.pvp.net")
    url = "/observer-mode/rest/consumer/getSpectatorGameInfo/{}/{}?{}".format(
            server, uid, urllib.parse.urlencode({"api_key":key}))
    conn.request("GET", url)
    resp = conn.getresponse().read().decode('utf-8')
    if "404" in resp:
        return {}
    d = json.loads(resp)
    return d

if __name__ == '__main__':
    try:
        champions = getchamplist()
    except e:
        print("Exception while getting champion list.")
        print(e)
    try:
        while True:
            name = input("Get current ingame info for: ")
            info = get_info_from_name(name)
            if info == {}:
                print("User \"{}\" not found.".format(name))
                continue
            d = getcurrentgame(info["id"])
            if d == {}:
                print("%s is not currently in game"
                      "" % (info["name"]))
                continue
            print("%s is currently in game of type %s %s %s"
                  "" % (info["name"], gametypes[d["gameQueueConfigId"]],
                        d["gameMode"],d["gameType"]))
            print("The game duration as of now is %s:%s"
                  "" % (str(int(d["gameLength"]/60)), str(d["gameLength"]%60)))
            print("The players in the game are:")
            for player in d["participants"]:
                print("%s as %s on %s team, summoner spells and "
                      "" % (player["summonerName"], champions[player["championId"]],
                            teams[player["teamId"]]))
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
    except KeyError as e:
        print(e)
        print(e.stacktrace)
    except:
        print("Unexpected error:", sys.exc_info()[0])

