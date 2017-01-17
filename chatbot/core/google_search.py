import json
import requests
import pandas as pd


def prepare_search(question):

    key = "AIzaSyB40pMzqMQ6_Y5auVAVLrUKVb4Y6eCxZjg"
    cx = "015954323978007865845:oznpb26vr60"


    url = "https://www.googleapis.com/customsearch/v1"
    parameters = {"q": question,
                  "cx": cx,
                  "key": key,
                  }
    page = requests.request("GET", url, params=parameters)
    results = json.loads(page.text)
    results.keys()
    return results

def google_search(question):

    results = prepare_search(question)
    link_list = [item["link"] for item in results["items"]]
    df = pd.DataFrame(link_list, columns=["link"])
    df["title"] = [item["title"] for item in results["items"]]
    df["snippet"] = [item["snippet"] for item in results["items"]]

    response =  "I found this on Google:\n" + df["snippet"][0].replace("\n", "") + "\nSee more: " + df["link"][0]
    return response

# print google_search("Who is Pepe?")

