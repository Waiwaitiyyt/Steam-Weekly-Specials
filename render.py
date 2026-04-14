from jinja2 import Environment, FileSystemLoader
import datetime

def get_html(game_dict: dict) -> str:
    env = Environment(loader=FileSystemLoader("."))  # 模板在当前目录
    template = env.get_template("template.html")

    games = []
    for id, info in game_dict.items():
        info_dict = {
            "name": info[0],
            "original_price": info[1],
            "current_price": info[2],
            "discount_off": info[3],
            "logo": info[4]
        }
        games.append(info_dict)

    today = datetime.date.today()
    date = today.strftime("%Y/%m/%d")


    html = template.render(
        date=date,
        games=games
    )

    return html