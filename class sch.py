import requests
import logging
import calendar
import jpholiday
import ast

logging.captureWarnings(True)
s = requests.session()


class sch():

    def __init__(self, year, month):
        c = calendar.Calendar(firstweekday=6)
        caI = c.itermonthdates(year, month)
        self.ca = list(caI)
        self.cast = [str(i) for i in self.ca]

    def getsch(self, co):
        url2 = "https://hitec-homedoctor.kagoyacloud.com/dneo/dneor.cgi/0/schmonth/id/84/1/schprivate/id/84/"
        mt = self.cast[8].replace("-", "")
        ms = self.cast[0].replace("-", "")
        me = self.cast[-1].replace("-", "")
        data = f"multicmd=%7B%220%22%3A%7B%22cmd%22%3A%22schmonth%22%2C%22date%22%3A%22{mt}%22%2C%22id%22%3A%2284%22%7D%2C%221%22%3A%7B%22cmd%22%3A%22schprivate%22%2C%22date%22%3A%22{mt}%22%2C%22proc%22%3A%22m%22%2C%22id%22%3A%2284%22%7D%2C%222%22%3A%7B%22cmd%22%3A%22todocmdlistsearch%22%2C%22srch_limdate_s%22%3A%22{ms}%22%2C%22srch_limdate_e%22%3A%22{me}%22%7D%2C%223%22%3A%7B%22cmd%22%3A%22schholidaylist%22%2C%22startdate%22%3A%22{ms}%22%2C%22enddate%22%3A%22{me}%22%2C%22id%22%3A%2284%22%7D%7D&{cookies['dnzToken']}=1"
        p = s.post(url2, data=data, cookies=co, verify=False)
        print(p.status_code)
        pj = p.json()
        pjsch = pj["1"]["slist"]["item"]
        return pjsch

    def schent(self, cookies):
        schl = sch.getsch(self, cookies)
        schenl = self.cast.copy()
        for sch1 in self.ca:
            if sch1.weekday() > 4 or jpholiday.is_holiday(sch1):
                schenl.remove(str(sch1))
        for v in schl:
            vsd = v["startdate"]
            ved = v["enddate"]
            vsdd = vsd[:4] + "-" + vsd[4:6] + "-" + vsd[6:]
            vedd = ved[:4] + "-" + ved[4:6] + "-" + ved[6:]
            if vedd in self.cast:
                schs = self.cast.index(vsdd)
                sche = self.cast.index(vedd)
                vl = self.cast[schs:(sche + 1)]
                if v["starttime"] != "" and vsdd == vedd and int(v["endtime"]) - int(v["starttime"]) < 400:
                    pass
                else:
                    schenl = [sch2 for sch2 in schenl if sch2 not in vl]
        url3 = "https://hitec-homedoctor.kagoyacloud.com/dneo/dneor.cgi/schcmdentry/"
        for sch4 in schenl:
            data2 = {"cmd": "schcmdentry",
                     "schcolor": "1",
                     "startdate": sch4,
                     "enddate": sch4,
                     "detail": "社内",
                     "outflg": "1",
                     "flag": "0",
                     "otherto": "84",
                     "sendhowto": "4",
                     "approv_notice_kind": "1",
                     "alarm": "0",
                     "tvmeeting_chairs": "84",
                     "tvmeeting_members": "84",
                     cookies["dnzToken"]: "1"
                     }
            q = s.post(url3, data=data2, cookies=cookies, verify=False)
            print(q.status_code)

    def schdel(self, cookies):
        schl = sch.getsch(self, cookies)
        url4 = "https://hitec-homedoctor.kagoyacloud.com/dneo/dneor.cgi/schdel/"
        for v in schl:
            schn = v["sid"]
            schd = v["detail"]
            ved = v["enddate"]
            vedd = ved[:4] + "-" + ved[4:6] + "-" + ved[6:]
            if vedd in self.cast and schd == "社内":
                data = {"cmd": "schdel",
                        "sid": schn,
                        "sendhowto": "4",
                        cookies["dnzToken"]: "1"
                        }
                r = s.post(url4, data=data, cookies=cookies, verify=False)
                print(r.status_code)


if __name__ == "__main__":
    cotxt = open("cookies.txt", "r")
    cookie = cotxt.read()
    cookies = ast.literal_eval(cookie)
    cotxt.close()
    Sch = sch(2022, 2)
    # Sch.schdel(cookies)
    Sch.schent(cookies)
