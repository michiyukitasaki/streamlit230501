import streamlit as st
import requests
import pandas as pd

def call_notion_api(endpoint, method, payload=None):
    api_key = 'secret_mSmKhrhadGzVIYamkywDUGmGbIpsVlpvDZXlUIsHsWB'
    base_url = 'https://api.notion.com/v1'
    url = base_url + endpoint
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    if payload:
        response = requests.request(method, url, headers=headers, json=payload)
    else:
        response = requests.request(method, url, headers=headers)

    return response.json()

def get_notion_database_data(database_id):
    endpoint = '/databases/' + database_id + '/query'
    method = 'POST'
    payload = {
        # "filter": {}, # Add filter conditions as necessary
        # "sorts": [] # Add sort conditions as necessary
    }
    return call_notion_api(endpoint, method, payload)



def show_data_on_streamlit():
    st.title('Notion Database Data')
    database_id = 'fc8a1e3f1b65479bbe2813049405d7fd'
    data = get_notion_database_data(database_id)

    if data and data['results']:
        # Extract the necessary data and create a DataFrame
        records = []
        for result in data['results']:
            record = {
                'Title': result['properties']['title1']['title'][0]['text']['content'] if result['properties']['title1']['title'] else '',
                'カテゴリ': result['properties']['カテゴリ']['relation'][0]['id'] if result['properties']['カテゴリ']['relation'] else '',
                '日付': result['properties']['日付']['date']['start'] if result['properties']['日付']['date'] else '',
                '値段': result['properties']['値段']['number'],
                'お店': result['properties']['お店']['select']['name'] if result['properties']['お店']['select'] else '',
            }
            records.append(record)

        df = pd.DataFrame(records)
        st.write(df)

    else:
        st.write('No data found')


