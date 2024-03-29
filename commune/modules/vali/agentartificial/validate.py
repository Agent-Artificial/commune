import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()




def validate(target_address: str, testing_url: str, key: str):
    if not testing_url:
        raise ValueError("TESTING_URL not set")
    test_url = os.getenv(testing_url)
    if not test_url:
        raise ValueError("TESTING_URL not set")
    headers={'Content-Type': 'application/json'},
    request_data= make_request(
    url=test_url,
    data={},
    headers=os.getenv("HEADERS"),
    timeout=20
    )
    
    test_response = make_request(
        url=target_address,
        data=request_data,
        headers=headers,
        timeout=20
    )
    data = test_response.json()
    data[key] = os.getenv(key)
    url= os.getenv(key)
    
    if not url:
        raise ValueError("EVALUATE_KEY not set")
    
    result = make_request(url, data, headers) # 
        

    if result.content == True:
        return True

    return False



def make_request(url, data, headers, timeout=20):
    return requests.post(
        url=url,
        data=data,
        headers=headers,
        timeout=timeout
    )