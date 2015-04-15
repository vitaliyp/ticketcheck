import urllib 
import json
from http import cookiejar
import re
import os
import datetime

CLASS_LETTERS_UK = {
        'Л':1,
        'К':2,
        'П':3,
        'С1':4,
        'С2':5,
        'С3':6}

cjar = cookiejar.CookieJar()
opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cjar))

def get_station_id(name):
    """ Get id of the station, with matching name.
    Returns int or None if no such stations exists."""

    stations = get_stations(name)
    matching_stations = [station for station in stations if station['name']==name]
    if len(matching_stations)==1:
        return matching_stations.pop()['id']
    else:
        return None

def get_stations(name):
    page = urllib.request.urlopen(
                u"http://booking.uz.gov.ua/purchase/station/%s/"%urllib.parse.quote(name)
            ).read().decode('utf8')
    stations = json.loads(page)
    result = []
    for station in stations['value']:
        res_station = {
            'id':station['station_id'],
            'name':station['title']}
        result.append(res_station)
    return result

def get_token():
    page = opener.open("http://booking.uz.gov.ua").read().decode('utf8')
    p = re.compile(r'\$\$_=~\[\];.*\(\)\)\(\);')
    code = p.search(page).group()

    subst = [
        ['$$_.$___','8'],
        ['$$_.$__$','9'],
        ['$$_.$_$_','a'],
        ['$$_.$_$$','b'],
        ['$$_.$$__','c'],
        ['$$_.$$_$','d'],
        ['$$_.$$$_','e'],
        ['$$_.$$$$','f'],
        ['$$_.___','0'],
        ['$$_.__$','1'],
        ['$$_._$_','2'],
        ['$$_._$$','3'],
        ['$$_.$__','4'],
        ['$$_.$_$','5'],
        ['$$_.$$_','6'],
        ['$$_.$$$','7'],
        ['$$_.$_', 'c'],
        ['$$_._$', 'o'],
        ['$$_.$$', 'n'],
        ['$$_.__', 't'],
        ['$$_.$', 'r'],
        ['$$_._', 'u'],
        [r'"\\"' , '\\'],
        ["\"\\\\\\\\\"", "\\\\"],
        ["+", ""],
        ]

    for s in subst:
        code = code.replace(s[0], s[1])

    p = re.compile(r'"([0-9a-z]{32})"')
    gvtoken = p.search(code).group(1)
    return gvtoken

def get_trains(departure_station_id, destination_station_id, departure_date,
                departure_time=datetime.time(0,0)):
    url = 'http://booking.uz.gov.ua/purchase/search/'
    values = {
        'station_id_till':destination_station_id,
        'date_dep':departure_date.strftime('%d.%m.%Y'),
        'station_id_from':departure_station_id,
        'time_dep':departure_time.strftime('%H:%M')}
    headers = {
        'GV-Ajax':'1',
        'GV-Referer':'http://booking.uz.gov.ua/',
        'GV-Token':get_token()}
    data = urllib.parse.urlencode(values).encode('utf8')
    req = urllib.request.Request(url,data,headers)
    response = opener.open(req)
    jsn = response.read().decode('utf8')
    trains = json.loads(jsn)
    result_trains = []
    if not trains['error']:
        for train in trains['value']:
            rt = {}
            departure_date_str = train['from']['src_date']
            ddate = datetime.datetime.strptime(departure_date_str, '%Y-%m-%d %H:%M:%S')
            arrival_date_str = train['till']['src_date']
            adate = datetime.datetime.strptime(arrival_date_str, '%Y-%m-%d %H:%M:%S')
            rt['number'] = train['num']
            rt['departure_station_id'] = train['from']['station_id']
            rt['departure_station_name'] = train['from']['station']
            rt['departure_datetime'] = ddate
            rt['destination_station_id'] = train['till']['station_id']
            rt['destination_station_name'] = train['till']['station']
            rt['arrival_datetime'] = adate
            rt['seats'] = {}
            for t in train['types']:
               rt['seats'][CLASS_LETTERS_UK[t['letter']]] = t['places'] 
            for c in CLASS_LETTERS_UK.values():
                if not rt['seats'].get(c, None):
                    rt['seats'][c] = 0
            result_trains.append(rt)
                
    return result_trains
    
def pretty_print_trains(trains):
    for train in trains:
        print(' '.join([train["num"],train["from"]["station"],' -> ',train['till']['station']]))
        for tp in train['types']:
            print(' '.join(['\t',tp['title'],str(tp['places'])]))



if __name__=='__main__':
    pass
