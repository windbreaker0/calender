import requests
import logging

logging.captureWarnings(True)
s = requests.session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Connection": "keep-alive",
    "Content-Length": "560",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://hitec-homedoctor.kagoyacloud.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://hitec-homedoctor.kagoyacloud.com/dneo/dneo.cgi?cmd=schindex",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ja,zh-CN;q=0.9,zh;q=0.8,en;q=0.7"
}


def login(account, password):
    url = "https://hitec-homedoctor.kagoyacloud.com/dneo/dneor.cgi/certify/"
    data = {
        "UserID": account,
        "_word": password,
        "cmd": "certify",
        "nexturl": "dneo.cgi?cmd=login",
        "starttab": "0"
    }
    r1 = s.post(url, data=data, verify=False)
    print(r1.status_code)
    cj = r1.json()
    cookie = "dnzInfo=84; dnzLeftmenu=0; dnzPtab=S; dnzO365=; dnzSid=%s; dnzToken=%s; dnzSv=; dnzHashcmd=fin" % (
        cj["rssid"], cj["STOKEN"])
    cookies = {}
    for line in cookie.split(";"):
        key = line.split("=")[0].replace(" ", "")
        value = line.split("=")[1]
        cookies[key] = value
    cotxt = open("cookies.txt", "w")
    cotxt.write(str(cookies))
    cotxt.close()
    return cookies


if __name__ == "__main__":
    login("yinkaiyu", "LXdu3JDD")
