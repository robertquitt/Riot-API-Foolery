import http.client
import urllib.parse
import json
server = "NA1"
key = ""
champions = {}
teams = {100:"Blue",200:"Red"}
gametypes = {65: 'ARAM_5x5', 17: 'ODIN_5x5_DRAFT', 16: 'ODIN_5x5_BLIND', 14: 'NORMAL_5x5_DRAFT', 70: 'ONEFORALL_5x5', 73: 'FIRSTBLOOD_2x2', 72: 'FIRSTBLOOD_1x1', 75: 'SR_6x6', 41: 'RANKED_TEAM_3x3', 42: 'RANKED_TEAM_5x5', 52: 'BOT_TT_3x3', 310: 'COUNTER_PICK', 76: 'URF_5x5', 31: 'BOT_5x5_INTRO', 33: 'BOT_5x5_INTERMEDIATE', 32: 'BOT_5x5_BEGINNER', 98: 'HEXAKILL', 300: 'KING_PORO_5x5', 83: 'BOT_URF_5x5', 93: 'NIGHTMARE_BOT_5x5_RANK5', 92: 'NIGHTMARE_BOT_5x5_RANK2', 91: 'NIGHTMARE_BOT_5x5_RANK1', 61: 'GROUP_FINDER_5x5', 96: 'ASCENSION_5x5', 9: 'RANKED_PREMADE_3x3', 8: 'NORMAL_3x3', 0: 'CUSTOM', 25: 'BOT_ODIN_5x5', 2: 'NORMAL_5x5_BLIND', 4: 'RANKED_SOLO_5x5', 7: 'BOT_5x5', 6: 'RANKED_PREMADE_5x5'}
def getchamplist():
    conn = http.client.HTTPSConnection("na.api.pvp.net")
    url = "/api/lol/static-data/%s/v1.2/champion?%s" % ("na",urllib.parse.urlencode({"api_key":key}))
    conn.request("GET",url)
    resp = conn.getresponse().read().decode('utf-8')
    d = json.loads(resp)
    conn.close()
    return {d["data"][champ]["id"]:d["data"][champ]["name"] for champ in d["data"].keys()}

def getinfofromname(name):
    name = name.lower().replace(" ","")
    conn = http.client.HTTPSConnection("na.api.pvp.net")
    url = "/api/lol/na/v1.4/summoner/by-name/%s?%s" % (urllib.parse.quote(name),urllib.parse.urlencode({"api_key":key}))
    conn.request("GET",url)
    resp = conn.getresponse().read().decode('utf-8')
    d = json.loads(resp)
    if "404" in resp:
        return {}
    conn.close()
    return d[name]


def getcurrentgame(uid):
    conn = http.client.HTTPSConnection("na.api.pvp.net")
    url = "/observer-mode/rest/consumer/getSpectatorGameInfo/%s/%s?%s" % (server,uid,urllib.parse.urlencode({"api_key":key}))
    conn.request("GET",url)
    resp = conn.getresponse().read().decode('utf-8')
    if "404" in resp:
        return {}
    d = json.loads(resp)
    return d

champions = getchamplist()
info = getinfofromname(input("Get current ingame info for: "))
if not info == {}:
    d = getcurrentgame(info["id"])
    if not d == {}:
        print("%s is currently in game of type %s %s %s" % (info["name"],gametypes[d["gameQueueConfigId"]],d["gameMode"],d["gameType"]))
        print("The game length as of now is %s:%s" % (str(int(d["gameLength"]/60)),str(d["gameLength"]%60)))
        print("The players in the game are:")
        for player in d["participants"]:
            print("%s as %s on %s team, summoner spells and " % (player["summonerName"],champions[player["championId"]],teams[player["teamId"]]))
    else:
        print("%s is not currently in game, or unable to be found." % (info["name"]))
else:
    print("User not found.")
