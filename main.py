import requests
import json
import schedule


authorization = 'YOURAUTHORISATION'
job_name = "🛑 НЕ ВЫКУПАТЬ 🛑"
min_price = 100



def myProfile():
    url = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/start"
    global authorization
    payload = {}
    headers = {
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'authorization': authorization,
        'sec-ch-ua-mobile': '?0'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

def userProfile(user_id):

    url = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/user?id=" + str(user_id)

    global authorization
    payload = {}
    headers = {
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'authorization': authorization,
        'sec-ch-ua-mobile': '?0'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

def topUsers():
    url = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/topUsers"

    global authorization
    payload = {}
    headers = {
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'authorization': authorization,
        'sec-ch-ua-mobile': '?0'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

def jobSlave(slave_id):
    url = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/jobSlave"

    global authorization, job_name
    payload = json.dumps({
        "slave_id": slave_id,
        "name": job_name
    })
    headers = {
      'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
      'authorization': authorization,
      'sec-ch-ua-mobile': '?0',
      'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

def buyFetter(slave_id):
    url = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buyFetter"

    global authorization
    payload = json.dumps({
        "slave_id": slave_id
    })
    headers = {
      'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
      'authorization': authorization,
      'sec-ch-ua-mobile': '?0',
      'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

def buySlave(slave_id):
    url = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buySlave"
    global authorization
    payload = json.dumps({
      "slave_id": slave_id
    })
    headers = {
      'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
      'authorization': authorization,
      'sec-ch-ua-mobile': '?0',
      'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    jobSlave(slave_id)
    buyFetter(slave_id)
    return response.json()

def slaveList(user_id):
    url = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/slaveList?id=" + str(user_id)

    global authorization
    payload = {}
    headers = {
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'authorization': authorization,
        'sec-ch-ua-mobile': '?0'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['slaves']



def saleSlave(slave_id):
    url = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/saleSlave"

    global authorization
    payload = json.dumps({
        "slave_id": slave_id
    })
    headers = {
      'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
      'authorization': authorization,
      'sec-ch-ua-mobile': '?0',
      'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

def findSlave(slaves):
    schedule.run_pending()
    for slave in slaves:
        #print(str(slave["price"]))
        if int(slave["profit_per_min"]) * 60 * int(slave["fetter_hour"]) > int(slave["fetter_price"]) and \
            int(myProfile()["me"]["balance"]) >= int(slave["fetter_price"]) and int(slave["fetter_to"]) == 0 and \
                int(slave["price"]) >= min_price:
            print("Buy: " + str(slave['id']))
            buySlave(slave['id'])
        if int(slave["slaves_count"]) != 0:
            findSlave(slave["slaves"])


def Profile():
    print("Profile")
    # Run away from your master
    me = myProfile()["me"]
    if me["fetter_to"] != 0 and me["price"] <= me["balance"]:
        buySlave(me["id"])

    # Update Fetters and change job name
    for slave in myProfile()["slaves"]:
        if slave["job"]["name"] != job_name:
            jobSlave(slave["id"])
        if slave["profit_per_min"]*60*slave["fetter_hour"] > slave["fetter_price"]:
            if myProfile()["me"]["balance"] >= slave["fetter_price"] and slave["fetter_to"] == 0:
                buyFetter(slave["id"])

schedule.every(1).minutes.do(Profile)


while True:
    tops = list(topUsers()['list'])
    tops.reverse()
    for top in tops:
        print(top)
        findSlave(slaveList(int(top['id'])))
