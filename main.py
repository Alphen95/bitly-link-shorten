import requests
import os

import urllib.parse
from dotenv import load_dotenv
import argparse

URL_CLICK_SUMMARY_TEMPLATE = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary"


def count_clicks(token, user_input):
    parsed_url = urllib.parse.urlparse(user_input)
    url_cut = "{}{}".format(parsed_url.netloc, parsed_url.path)
    url_full = URL_CLICK_SUMMARY_TEMPLATE.format(url_cut)
    header = {
        "Authorization": "Bearer {}".format(token)
    }
    response = requests.get(url_full, headers=header)
    if response.ok:
        usable_response = response.json()
        clicks_count = usable_response["total_clicks"]
    else:
        clicks_count = "error"
    return clicks_count


def shorten_link(token, url):
    print("a")
    bitlink_data = {"long_url": url}
    header = {
        "Authorization": "Bearer {}".format(token)
    }
    url_shorten = "https://api-ssl.bitly.com/v4/shorten"
    response = requests.post(url_shorten, headers=header, json=bitlink_data)
    if response.ok:
        usable_response = response.json()
    else:
        usable_response = {"link": "error"}
    return usable_response["link"]


def check_link(url, token):
    header = {
        "Authorization": "Bearer {}".format(token)
    }
    url_check = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(url)
    response = requests.get(url_check, headers=header)
    return response.ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bitlink", help="ссылка на сайт/битлинк")
    args = parser.parse_args()
    URL_INPUT = args.bitlink
    BITLY_TOKEN = os.getenv("BITLY_TOKEN")
    load_dotenv()
    if not check_link(URL_INPUT, BITLY_TOKEN):
        bitlink = shorten_link(BITLY_TOKEN, URL_INPUT)
        if bitlink == "error":
            print("Был введён неверный URL, попробуйте заново.")
        else:
            print("Битлинк:", bitlink)
    else:
        clicks = count_clicks(BITLY_TOKEN, URL_INPUT)
        if clicks == "error":
            print("Ошибка в программе, или в ссылке.")
        else:
            print("Количество кликов:", clicks)
