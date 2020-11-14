import requests
import json

class _api():

    def __init__(self,url,token):
        response = requests.get("{0}/{1}/".format(url,"api/1.0/auth"),headers={ "x-api-key" : token })
        responseJson = json.loads(response.text)
        self.url = url
        self.headers = { "x-api-token" : responseJson["x-api-token"] }
        print("Authenticated")

    def api(self,method,endpoint,data=None):
        method = method.upper()
        if method == "GET":
            response = requests.get("{0}/{1}/".format(self.url,endpoint),headers=self.headers)
        elif method == "POST":
            response = requests.post("{0}/{1}/".format(self.url,endpoint),headers=self.headers,json=data)
        return response

    def getFlowCode(self,conductID,flowID):
        response = self.api("GET","conductEditor/{0}/codify/?flowID={1}&json=True".format(conductID,flowID))
        responseJson = json.loads(response.text)
        return responseJson["result"]

    def runFlowCode(self,flowCode,events):
        response = self.api("POST","codify",data={ "code" : flowCode, "events" : json.dumps(events), "eventCount" : 0 })
        responseJson = json.loads(response.text)
        return responseJson["result"]


def expectedResult(codifyResult,successActionName,event):
    found = False
    for line in codifyResult.split("\n"):
        if "'name': '{0}'".format(successActionName) in line:
            found = True
        if found:
            if "Post-Data: " in line:
                try:
                    int(event)
                except:
                    event = "'{0}'".format(event)
                if "'event': {0}".format(event) in line:
                    return True
                found = False
    return False

            