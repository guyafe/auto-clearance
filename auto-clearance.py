import sys
import time
import requests
import json
import datetime
import schedule


def build_login_response(parent_id, parent_password, school_symbol):
    BODY = {'apiVersion': '3.20200528',
            'appBuild': '3.20200528',
            'appName': 'info.mashov.students',
            'appVersion': '3.20200528',
            'deviceManufacturer': '',
            'deviceModel': '',
            'devicePlatform': '',
            'deviceUuid': '',
            'deviceVersion': '',
            'password': parent_password,
            'semel': int(school_symbol),
            'username': parent_id,
            'year': 2021}
    URL = 'https://web.mashov.info/api/login'
    PARAMS = {'accept': 'application/json, text/plain, */*',
              'accept-language': 'en-US,en;q=0.9,he;q=0.8',
              'content-type': 'application/json'}
    response = requests.post(url=URL, headers=PARAMS, json=BODY)
    return response


def build_clearance_response(x_csrf_token, login_response_params, login_response_cookies):
    BASE_URL = 'https://web.mashov.info/api/students/'
    FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    FORMAT2 = '%Y-%m-%dT%H:%M:%S'
    ANSWERER_ID = login_response_params['credential']['userId']
    cookies = {'MashovSessionID': login_response_cookies['MashovSessionID'],
               'Csrf-Token': login_response_cookies['Csrf-Token']}
    for child in login_response_params['accessToken']['children']:
        now = datetime.datetime.now()
        child_guid = child['childGuid']
        print('clearancing for child: ' + child['privateName'] + ' guid: ' + child_guid)
        url = BASE_URL + child_guid + '/covid/' + now.strftime(FORMAT) + '/clearance'
        params = {'accept': 'application/json, text/plain, */*',
                  'content-type': 'application/json',
                  'X-Csrf-Token': x_csrf_token}
        body = {'answer': 3,
                'answererId': ANSWERER_ID,
                'answererName': '',
                'clearanceDate': now.strftime(FORMAT2),
                'lastAnswer': now.strftime(FORMAT2),
                'lastAnswerIsOk': True,
                'noContactWithInfected': True,
                'noHeatAndSymptoms': True,
                'studentClass': '',
                'studentName': '',
                'userId': child_guid}
        response = requests.put(url=url, headers=params, json=body, cookies=cookies)
        if response.status_code == 200:
            print('' + datetime.datetime.now().strftime(FORMAT2) + ': Succesfully sent clearance for: ' + child[
                'privateName'])


def send_clearance(parent_id, parent_password, school_symbol):
    print('Sending clearance request...')
    print('parent id: ' + parent_id + ' parent password: ' + parent_password + ' school symbol: ' + school_symbol)
    login_response = build_login_response(parent_id, parent_password, school_symbol)
    x_csrf_token = login_response.headers['x-csrf-token']
    login_response_params = json.loads(login_response.text)
    build_clearance_response(x_csrf_token, login_response_params, login_response.cookies)


def send_clearance_daily(parent_id, parent_password, school_symbol):
    schedule.every().day.at("07:00").do(send_clearance, parent_id=parent_id, parent_password=parent_password,
                                        school_symbol=school_symbol)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[4] == 'daily':
        send_clearance_daily(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        send_clearance(sys.argv[1], sys.argv[2], sys.argv[3])
