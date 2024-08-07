from app import app, prof_manager
from app.db_account import check_account
from app.socket_api import gpon_api
from app import firmware_version

from functools import wraps
from flask import request, make_response, jsonify
import requests


def check_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        login = request.form['login']
        passw = request.form['passw']
        if check_account(login, passw):
            app.logger.info(msg=f"User: <{login}> logged")
            return f(*args, **kwargs)
        return make_response('Not Authorized', 401)
    return decorated


@app.route("/auth", methods=['POST'])
@check_auth
def auth():
    return jsonify({"auth": "success", "version": firmware_version})


@app.route("/onu_list", methods=['POST'])
@check_auth
def onu_list():
    r = gpon_api.onu_list(
        gpon=request.form["gpon"],
        slot=request.form["slot"],
        port=request.form["port"]
    )
    return jsonify(r)


@app.route("/onu_info", methods=['POST'])
@check_auth
def onu_info():
    r = gpon_api.onu_info(
        gpon=request.form["gpon"],
        slot=request.form["slot"],
        port=request.form["port"],
        iid=request.form["iid"]
    )
    return jsonify(r)


@app.route("/onu_optical_info", methods=['POST'])
@check_auth
def onu_optical_info():
    r = gpon_api.onu_optical_info(
        gpon=request.form["gpon"],
        slot=request.form["slot"],
        port=request.form["port"],
        iid=request.form["iid"]
    )
    return jsonify(r)


@app.route("/profile/<x>", methods=['POST'])
@check_auth
def profile_handle(x):
    if x == "get":
        return jsonify(prof_manager.get_profiles())
    elif x == "add":
        return jsonify(prof_manager.add_profile(
            name=request.form["name"],
            vlan=request.form["vlan"],
            gem=request.form["gem"],
            srv=request.form["srv"],
            line=request.form["line"],
        ))
    elif x == "del":
        return jsonify(prof_manager.del_profile(
            name=request.form["name"]
        ))
    else:
        return make_response("Unknown request", 400)


@app.route("/register", methods=["POST"])
@check_auth
def register_onu():
    r = gpon_api.register_onu(
        gpon=request.form["gpon"],
        slot=request.form["slot"],
        port=request.form["port"],
        name=request.form["name"],
        sn=request.form["sn"],
        srv_profile=request.form["srv_profile"],
        line_profile=request.form["line_profile"]
    )
    return jsonify(r)


@app.route("/delete", methods=["POST"])
@check_auth
def delete_onu():
    r = gpon_api.delete_onu(
        gpon=request.form["gpon"],
        slot=request.form["slot"],
        port=request.form["port"],
        onu_id=request.form["onu_id"],
    )
    return jsonify(r)


@app.route("/add_service_port", methods=["POST"])
@check_auth
def add_srv():
    r = gpon_api.add_srv_port(
        gpon=request.form["gpon"],
        slot=request.form["slot"],
        port=request.form["port"],
        onu_id=request.form["onu_id"],
        gem=request.form["gem"],
        vlan=request.form["vlan"],
        service_port=request.form["service_port"]
    )
    return jsonify(r)


@app.route("/del_service_port", methods=["POST"])
@check_auth
def del_serv():
    r = gpon_api.undo_srv_port(
        gpon=request.form["gpon"],
        service_port=request.form["service_port"],
    )
    return jsonify(r)


@app.route("/native_vlan", methods=["POST"])
@check_auth
def native_vlan():
    r = gpon_api.native_vlan(
        gpon=request.form["gpon"],
        slot=request.form["slot"],
        port=request.form["port"],
        onu_id=request.form["onu_id"],
        vlan=request.form["vlan"]
    )
    return jsonify(r)


@app.route("/traffic/<tr>", methods=["POST"])
@check_auth
def traffic(tr):
    if tr == "vlan":
        r = gpon_api.traffic_vlan(
            gpon=request.form["gpon"],
            vlan=request.form["vlan"]
        )
        return jsonify(r)
    elif tr == "port":
        r = gpon_api.traffic_port(
            gpon=request.form["gpon"],
            slot=request.form["slot"],
            port=request.form["port"]
        )
        return jsonify(r)
    return make_response("Bad Request", 400)


@app.route("/mac/<tr>", methods=["POST"])
@check_auth
def mac(tr):
    if tr == "service_port":
        r = gpon_api.mac_service_port(
            gpon=request.form["gpon"],
            service_port=request.form["service_port"]
        )
        return jsonify(r)
    elif tr == "onu_id":
        r = gpon_api.mac_onu_port(
            gpon=request.form["gpon"],
            slot=request.form["slot"],
            port=request.form["port"],
            onu_id=request.form["onu_id"]
        )
        return jsonify(r)
    elif tr == "all":
        r = gpon_api.mac_all(
            gpon=request.form["gpon"]
        )
        return jsonify(r)
    return make_response("Bad Request", 400)


@app.route("/gpon/profile/<type_>", methods=["POST"])
@check_auth
def profile(type_):
    r = gpon_api.profile(
        gpon=request.form["gpon"],
        type_profile=type_
    )
    return jsonify(r)


@app.route("/save", methods=["POST"])
@check_auth
def save():
    r = gpon_api.save_config(
        gpon=request.form["gpon"]
    )
    return jsonify(r)


@app.route("/ping", methods=["POST"])
@check_auth
def ping():
    r = gpon_api.optical_ping(
        gpon=request.form["gpon"],
        slot=request.form["slot"],
        port=request.form["port"],
        onu_id=request.form["onu_id"],
    )
    return jsonify(r)


@app.route("/autofind", methods=["POST"])
@check_auth
def autofind():
    r = gpon_api.auto_find(
        gpon=request.form["gpon"],
        slot=request.form["slot"],
        port=request.form["port"],
    )
    return jsonify(r)


@app.route("/next_free_index", methods=["POST"])
@check_auth
def next_free():
    r = gpon_api.next_free_index(
        gpon=request.form["gpon"]
    )
    return jsonify(r)


@app.route("/service_port_list", methods=["POST"])
@check_auth
def srv_port_lst():
    r = gpon_api.service_port_list(
        gpon=request.form["gpon"]
    )
    return jsonify(r)


@app.route("/pppoe", methods=["POST"])
@check_auth
def pppoe():
    login = request.form['login']
    passw = request.form['passw']
    try:
        session = requests.Session()
        session.auth = (login, passw)
        session.get(f"http://s.deil-00.ru/")
        response = session.get(f"http://s.deil-00.ru/api/pppoe/all", params={"mac": "0"}, timeout=3)
        res = []
        if response.status_code == 200:
            res = response.json()["response"]
        return jsonify(res)
    except Exception:
        pass
    return jsonify({"error": "Bad Gateway, [S.DEIL-00.RU > Internal API error]"})
