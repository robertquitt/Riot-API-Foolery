import http.client
import urllib.parse
import json
server = "NA1"
key = ""


d = getcurrentgameinfo(getidfromname(input("Get current ingame info for: ")))



def getidfromname(name):
    name = name.lower().replace(" ","")
    conn = http.client.HTTPSConnection("na.api.pvp.net")
    url = "/api/lol/na/v1.4/summoner/by-name/%s?%s" % (urllib.parse.quote(name),urllib.parse.urlencode({"api_key":key}))
    conn.request("GET",url)
    resp = conn.getresponse().read().decode('utf-8')
    d = json.loads(resp)
    conn.close()
    return d[name]["id"]

def getcurrentgame(uid):
    conn = http.client.HTTPSConnection("na.api.pvp.net")
    url = "/observer-mode/rest/consumer/getSpectatorGameInfo/%s/%s" % (server,uid)
    conn.request("GET",url)
    resp = conn.getresponse().read().decode('utf-8')
    d = json.loads(resp)
    return d
