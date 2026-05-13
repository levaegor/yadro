import requests
import logging


#API_URL = "https://tools-httpstatus.pickup-services.com/"
API_URL = "https://httpstat.us/"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(filename)s:%(funcName)s:%(lineno)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


class APIError(Exception):
    def __init__(self, status_code: int):
        super().__init__(f"status code: {status_code}")


def send_request(http_code: int) -> requests.Response:
    return requests.get(f"{API_URL}{http_code}")
    

def handle_response(response: requests.Response) -> None:
    if response.status_code // 100 in (1, 2 ,3):
        logging.info(f"Status code: {response.status_code}\t {response.text}")
    elif response.status_code // 100 in (4, 5):
        raise APIError(status_code=response.status_code)
    else:
        logging.error("Unexpected status code")


def test_request(http_code: int) -> None:
    try:
        response = send_request(http_code=http_code)
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return
        
    try:
        handle_response(response=response)
    except APIError as e:
        logging.error(e)
    
    
    
def main():
    for code in (202, 200, 305, 306, 418):
        test_request(code)
    

if __name__ == "__main__":
    main()
        
    
