import hashlib
import requests
import json
import time


FCIC_CONFIG_SERVER_HTTP = "https://intelliclima.fantinicosmi.it"
FCIC_CONFIG_API_FOLDER_MONO = "/server_v1_mono/api/"


def generateReadUrl(path):
    return FCIC_CONFIG_SERVER_HTTP + FCIC_CONFIG_API_FOLDER_MONO + path


class IntelliClimaModelType:
    """Model type response format."""

    modello: str
    tipo: str


class IntelliClimaCH:
    """Not verified, converted from https://github.com/ruizmarc/homebridge-intelliclima."""

    id: str
    crono_sn: str
    multi_sn: str
    zone: str
    status: str
    online: str
    action: str
    model: IntelliClimaModelType
    name: str
    config: str | None
    appdata: str
    programs: str
    last_online: str
    creation_date: str
    agc_on: str | None
    cooler_on: str | None
    houses_id: str
    image: str
    c_mode: str
    t_amb: str
    t1w: str
    t2w: str
    t3w: str
    t1s: str
    t2s: str
    t3s: str
    jtw: str
    jts: str
    jh: str
    jm: str
    jdate: str | None
    tmans: str
    tmanw: str
    tafrost: str
    tset: str
    relay: str
    relayrh: str | None
    rh: str
    rhset: str
    rhrele: str
    rhabl: str | None
    ws: str
    day: str
    auxio: str | None
    alarms: str | None
    lastprogramwinter: str
    lastprogramsummer: str
    upd_client: str
    upd_server: str
    check_mode: str
    do_swap: str | None
    is_in_download_state: str
    fw_version: str | None
    exp_if_version: str | None
    multizona: list[str]


class IntelliClimaNLAPI:
    def setHouseAndDeviceIds(v_credential):

        v_userId = v_credential.get("Tokenid")

        apiURL = generateReadUrl("casa/elenco2/" + v_userId)
        print(apiURL)
        headers = v_credential

        r = requests.post(apiURL, headers=headers)
        print(r.content)

        response = json.loads(r.text)

        houses = response.get("houses")
        houseskey = houses.keys()
        firsthouseid = list(houseskey)[0]
        firsthouse = houses.get(firsthouseid)
        deviceId = firsthouse[0].get("id")
        return deviceId

    def getDevice(v_deviceId):

        apiURL = generateReadUrl("sync/cronos380")
        getDeviceBody = '{"IDs": "' + v_deviceId + '"}'

        termostat = IntelliClimaCH()

        r = requests.post(apiURL, getDeviceBody)
        # print(r.content)

        response = json.loads(r.text)
        data = response.get("data")
        model = ""
        sn = ""
        name = ""
        c_mode = ""
        t_amb = "0"

        if len(data) > 0:
            sn = data[0].get("crono_sn")
            model = json.loads(data[0].get("model")).get("modello")
            name = data[0].get("name")
            c_mode = data[0].get("c_mode")
            t_amb = data[0].get("t_amb")

        termostat.id = v_deviceId
        termostat.t_amb = t_amb

        print(
            "deviceid:"
            + v_deviceId
            + " modello:"
            + model
            + " sn:"
            + sn
            + " name:"
            + name
            + " modalità:"
            + c_mode
            + " current temperature:"
            + str(round(float(t_amb), 2))
        )
        return termostat

    def login(v_user, v_pass):
        username = v_user
        password = v_pass

        hashedPassword = (hashlib.sha256(password.encode())).hexdigest()

        apiURL = apiUrl = generateReadUrl(
            "user/login/" + username + "/" + hashedPassword
        )

        print(apiURL)
        r = requests.post(apiURL)

        print(r.content)

        response = json.loads(r.text)

        authToken = response.get("token")
        userId = response.get("id")

        print(authToken)
        print(userId)

        credential = {
            "Tokenid": userId,
            "Token": authToken,
        }

        return credential

    authcredential = login("zonker", "Kalanta9")
    deviceId = setHouseAndDeviceIds(authcredential)
