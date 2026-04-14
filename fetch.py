import requests
import time
import re

# url = "https://store.steampowered.com/search/results/"
# params = {
#     "specials": 1,
#     "count": 25,
#     "cc": "CN",
#     "json": 1
# }

# resp = requests.get(url, params=params)
# items = resp.json().get("items", [])

# for game in items:
#     game_name = game["name"]
#     game_logo = game["logo"]
#     game_id_search = re.search(r"/apps/(\d+)/", game_logo)
#     if game_id_search == None:
#         game_id_search = re.search(r"/subs/(\d+)/", game_logo)
#     game_id = game_id_search.group(1)
    
#     detail_url = "https://store.steampowered.com/api/appdetails/"
#     detail = requests.get(detail_url, params={"appids": game_id, "cc": "CN", "filters": "price_overview"})
#     detail_data = detail.json()
#     if detail_data[game_id]["success"] == True:
#         initial_price = detail_data[game_id]["data"]["price_overview"]['initial_formatted']
#         current_price = detail_data[game_id]["data"]["price_overview"]['final_formatted']
#         print(game_name, initial_price, current_price)
#     time.sleep(1)

def api_request(url: str, detail_url: str, params: dict) -> dict:
    '''
    Return game_dict as result
    game_dict: {game_id: [game_name, initial_price, current_price, discount_off, logo]}
    '''
    game_dict = {}

    resp = requests.get(url, params=params)
    items = resp.json().get("items", [])

    for game in items:
        game_name = game["name"]
        game_logo = game["logo"]
        
        game_id_search = re.search(r"/apps/(\d+)/", game_logo)
        if game_id_search == None:
            game_id_search = re.search(r"/subs/(\d+)/", game_logo)
        game_id = game_id_search.group(1) # type: ignore
        
        detail_url = "https://store.steampowered.com/api/appdetails/"
        detail = requests.get(detail_url, params={"appids": game_id, "cc": "CN", "filters": "price_overview"})
        detail_data = detail.json()
        if detail_data[game_id]["success"] == True:
            initial_price = detail_data[game_id]["data"]["price_overview"]['initial_formatted']
            current_price = detail_data[game_id]["data"]["price_overview"]['final_formatted']   
            initial = detail_data[game_id]["data"]["price_overview"]['initial']
            current = detail_data[game_id]["data"]["price_overview"]['final']
            discount_off = "{:.2%}".format((initial - current) / initial)
            game_dict[game_id] = [game_name, initial_price, current_price, discount_off, game_logo]
        time.sleep(1)

    return game_dict

if __name__ == "__main__":
    import json
    json_path = r"config.json"
    with open(json_path, "r") as json_file:
        config = json.load(json_file)
    url = config["url"]
    detail_url = config["detail_url"]
    params = config["params"]
    game_dict = api_request(url, detail_url, params)
    print(game_dict)    