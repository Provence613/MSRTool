import bs4
import os
import json

class TestReportAnalyzer:
    def parseHtml(self,rootdir):
        res=[]
        filepath = os.path.join(rootdir,"cobertura/frame-summary.html")
        f = open(filepath)
        html = bs4.BeautifulSoup(f.read(), 'html5lib')
        table = html.select('table')[0]
        tbody = table.select("tbody")[0]
        trs=tbody.select("tr")
        idx=1
        # 遍历该表格内的所有的tr
        for i in range(3, len(trs)):
            tr = trs[i]
            tds = tr.select("td")
            if len(tds)!=9:
                continue
            info = {}
            info['id']=idx
            info['PackageName']=tds[0].get_text()
            info['ClassNumber']=tds[1].get_text()
            info['LineNumber']=tds[2].get_text().split("/")[1]
            info['LineCoverage']=tds[3].get_text()
            info['BranchCoverage']=tds[6].get_text()
            info['complexity']=tds[8].get_text().split(";")[1]
            idx+=1
            res.append(info)
        # 写入json
        jsondic = {}
        jsondic['results'] = res
        jsonpath = os.path.join(rootdir, "covtest.json")
        file = open(jsonpath, 'w', encoding='utf-8')
        json.dump(jsondic, file, ensure_ascii=False)
        file.close()



