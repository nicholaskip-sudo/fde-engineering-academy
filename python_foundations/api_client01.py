import requests

def fetch_http_example() -> None:

    url="https://httpbin.org/get"

    params= {
        "site": "OULU BTS 001"
    }

    headers = {
        "Accept": "application/json",
        "X-Customer-ID": "demo-customer"
    }

    timeout=10

    response = requests.get(url,params=params, headers=headers, timeout=timeout)
    data = response.json()

    print(data["headers"]["X-Customer-Id"])
    print(response.status_code)
    print(response.headers.get("Content-Type"))
    print(data["method"])
    print(data["url"])
    print(data["args"])

    print(f"\nURL: {data['url']}")
    print(f"Site: {data['args']['site']}")
    print(f"Customer: {data['headers']['X-Customer-Id']}")

def inspect_http_status(url: str) -> None:

    try:
        timeout = 10
        response = requests.get(url, timeout=timeout)

        print(f"HTTP Status: {response.status_code}")

        response.raise_for_status()

        print("Request successful")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP Error: {error}")


    except requests.exceptions.Timeout as error:
        print(f"ERROR: The HTTP request timed out: {error}")

    except requests.exceptions.ConnectionError as error:
        print(f"ERROR: Unable to connect to remote server: {error}")

def main():

    fetch_http_example()

    urls = [ "https://httpbin.org/get", "https://httpbin.org/status/404",
        "https://httpbin.org/status/500", "http://127.0.0.1:1"
        ]

    for url in urls:
        print("\n ----- INSPECTING URLS ----")
        inspect_http_status(url)


if __name__ == "__main__":
    main()
