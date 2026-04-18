import time
import requests


def get_time_range(minutes=15):
    end_time = int(time.time() * 1_000_000)
    start_time = end_time - (minutes * 60 * 1_000_000)
    return start_time, end_time


def build_search_payload(stream_name, start_time, end_time, size=100):
    return {
        "query": {
            "sql": f'SELECT * FROM "{stream_name}"',
            "start_time": start_time,
            "end_time": end_time,
            "from": 0,
            "size": size,
        }
    }


def ingest_logs(base_url, org_name, auth, stream_name, logs, timeout=30):
    url = f"{base_url}/api/{org_name}/{stream_name}/_json"
    return requests.post(url, auth=auth, json=logs, timeout=timeout)


def search_logs(base_url, org_name, auth, payload, timeout=30):
    url = f"{base_url}/api/{org_name}/_search?type=logs"
    return requests.post(url, auth=auth, json=payload, timeout=timeout)


def search_logs_with_retry(base_url, org_name, auth, stream_name, retries=5, delay=2):
    last_response = None
    last_response_json = {}
    hits = []

    for _ in range(retries):
        start_time, end_time = get_time_range(minutes=15)
        payload = build_search_payload(stream_name, start_time, end_time)

        response = search_logs(
            base_url=base_url,
            org_name=org_name,
            auth=auth,
            payload=payload,
        )

        last_response = response

        if response.status_code == 200:
            last_response_json = response.json()
            hits = last_response_json.get("hits", [])
            if len(hits) > 0:
                return response, payload, hits, last_response_json

        time.sleep(delay)

    return last_response, payload, hits, last_response_json