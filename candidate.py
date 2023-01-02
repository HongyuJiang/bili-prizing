import requests
import jsonpath_ng

endpoint = "http://api.bilibili.com/x/web-interface/search/type?search_type=video&order=pubdate&keyword="

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Host": "api.bilibili.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Connection": "keep-alive",
    #"Cookie": "bsource=search_google; i-wanna-go-back=-1; innersign=0; b_lsid=76FC38BC_1856B009F56; bp_video_offset_14136471=746021397020540900; CURRENT_FNVAL=4048; buvid4=69B87E13-5D2B-509E-95B8-0F364F89CCAF59888-022063023-cSrFUaBpzyEYsb%2B64kFi7A%3D%3D; buvid_fp=6ecb213c7ad0e781dd5cd630c7f65099; buvid_fp_plain=undefined; fingerprint=6ecb213c7ad0e781dd5cd630c7f65099; PVID=1; hit-new-style-dyn=0; sid=86vi7sr9; DedeUserID=14136471; DedeUserID__ckMd5=fb4107af02297a9a; bili_jct=e788c902e414a7723fb2c612098b35e3; hit-dyn-v2=1; _uuid=7F10F82B6-38CB-7D63-CE59-F10F8FF2CEA2677561infoc; rpdid=|(ummY~mY~YR0J'uYY)Yuu~kY; b_nut=100; nostalgia_conf=-1; LIVE_BUVID=AUTO9616459490283628; b_ut=5; buvid3=8CEA4508-859C-7EE2-0972-640A6CE3937680956infoc"
  }


def search(cookies, keywords):
    cookie_dict = {}
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']

    cookie_str = ";".join([cookie['name'] + '=' + cookie['value']  for cookie in cookies])
    keywords_str = '+'.join(keywords)
    headers['Cookie'] = cookie_str
    res = requests.get(endpoint + keywords_str, cookies=cookie_dict, headers=headers)
    data = res.json()
    return parse(data)


def parse(data):
    jsonpath_expr = jsonpath_ng.parse('data.result[*].mid')
    list_val = [str(match.value) for match in jsonpath_expr.find(data)]
    return list_val
    