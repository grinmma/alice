import flask
import logging
import json

session_storage = {}

app = flask.Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route("/post", methods=["POST"])
def post_handler():
    req_json = flask.request.json
    logging.info(f"Request: {req_json!r}")
    response = {
        "session": req_json["session"],
        "version": req_json["version"],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(req_json, response)
    logging.info(f"Response: {response!r}")
    return json.dumps(response)


def handle_dialog(req_json, response):
    global session_storage
    usr_id = req_json["session"]["user_id"]

    if req_json["session"]["new"]:
        print("pre", session_storage)
        session_storage[usr_id] = {"suggests": [
            "Не хочу.", "Не буду.", "Отстань!"]}
        print("post", session_storage)
        response["response"]["text"] = "Привет! Купи слона!"
        response["response"]["buttons"] = get_suggests(usr_id)
        return
    if any(map(lambda word: word in req_json["request"]["command"].lower(), ("ладно",
                                                                             "куплю",
                                                                             "хорошо",
                                                                             "покупаю"))):
        response["response"]["text"] = "Слона можно найти на Яндекс.Маркете!"
        response["response"]["end_session"] = True
        return
    response["response"]["text"] = f"""Все говорят '{req_json["request"]["original_utterance"]}', а ты купи слона!"""
    response["response"]["buttons"] = get_suggests(usr_id)


def get_suggests(usr_id):
    global session_storage
    print(session_storage)
    session = session_storage[usr_id]
    suggests = [
        {"title": suggest, "hide": True}
        for suggest in session["suggests"][:2]
    ]
    session["suggests"] = session["suggests"][1:]
    session_storage[usr_id] = session
    if len(suggests) == 1:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })
    return suggests


if __name__ == "__main__":
    app.run()
