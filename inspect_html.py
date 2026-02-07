import requests

url = "https://www.snudh.org/portal/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000258&menuNo=25010000&option1=&option6=&searchCnd=&searchWrd=&pageIndex=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, verify=False)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        # Print first 2000 chars to check structure or look for specific tags if possible
        # But simply printing raw html might be too long. 
        # Let's try to find the 'list' part. usually it's in a <table> or <ul>
        content = response.text
        print(content[:4000]) 
except Exception as e:
    print(f"Error: {e}")
