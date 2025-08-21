import requests
from scripts import constants
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


cookie = ""
item = ""

headers = {
    "Authorization": "Bearer",
    "User-Agent": "MyApp/1.0",
    "Accept": "application/json",
    "Cookie": cookie
}

def lazy_paginated_request():
    page = 50
    while True:
        pagination = "500"
        url = "https://bbva-lrba.appspot.com/gateway/ecs-live-02/lrba/v0/status?paginationKey={page}&pageSize={pagination}&jobName={item}&runId=&jobVersion=&status=SUCCESS&size=&priorityClassName=&namespace=&startDate=1733029200000000000&endDate=&sort=running%2Cdesc&sort=finishDate%2Cdesc&sort=startDate%2Cdesc".format(pagination=pagination,page=page,item=item)
        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            pagination = data.get("pagination")
            items = data.get('result', [])
            print(items)
            if not items:
                break
            yield from items
            page += 1
            print("---------PAGE------------", page)
        else:
            print("Request failed")
            data = response.json()
            break


def create_request(token):
# if __name__ == "__main__":
    cookie = token
    all_results = list(lazy_paginated_request())
    print("Total:", len(all_results))
    #return all_results
