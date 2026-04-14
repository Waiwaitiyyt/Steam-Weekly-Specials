import json
from datetime import datetime
from fetch import api_request
from render import get_html
from send import send_email


def main():
    json_path = r"config.json"
    with open(json_path, "r") as json_file:
        config = json.load(json_file)
    url = config["url"]
    detail_url = config["detail_url"]
    params = config["params"]
    password = config["password"]
    smtp_host = config["smtp_host"]
    smtp_port = config["smtp_port"]
    sender_email = config["sender_email"]
    recipients_list = config["recipients_list"]

    game_dict = api_request(url, detail_url, params)
    html = get_html(game_dict)
    title = "本周Steam特惠" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_email(
        title=title,
        html=html,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        sender=sender_email,
        recipients=recipients_list,
        password=password
    )




if __name__ == "__main__":
    main()