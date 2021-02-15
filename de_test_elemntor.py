#!/usr/bin/env python3
import sys
import psycopg2
import pandas as pd
import requests
import json
import base64


def connect_to_pg(dbname, user, host, port, password):
    try:
        engine_pg = psycopg2.connect("dbname={} user={} host={} port={} password={}".format(dbname, user, host, port, password))
        return engine_pg
    except psycopg2.DatabaseError:
        sys.exit('Failed to connect to database')

def get_urls_csv(url, engine):
    r = requests.get(url)
    text = r.iter_lines()
    lst = []
    scanned_sites = get_scanned_sites(engine)
    for row in text:
        site = str(row).replace("b'","").replace("'","")
        if site.strip() == 'stackoverflow.com' :
            site = 'www.stackoverflow.com'
        if site.strip() not in scanned_sites:
            lst.append(site)
    return lst

def get_site_scan_result(url_to_scan='www.google.com',apikey='a72fde9e24aee114b05649b8fa209e2e8918b534576966a758a31c5f87d11757'):
    # REST API URL
    url = 'https://www.virustotal.com/vtapi/v2/url/scan'
    params = {'apikey': apikey, 'url': url_to_scan}
    response = requests.post(url, data=params)

    # Get Response
    # TODO - add try catch
    if response.status_code == 204: #No content
        res = response.text
        return (None, None)
    s = response.text

    # Get results as dictionary using json
    json_acceptable_string = s.replace("'", "\"")
    scan_results = json.loads(json_acceptable_string)
    request = scan_results

    url = 'https://www.virustotal.com/vtapi/v2/url/report'
    params = {'apikey': apikey, 'resource': scan_results.get("scan_id")}
    response = requests.get(url, params=params)

    # Get Response
    # TODO - add try catch
    scan_report = response.text

    # Get results as dictionary using json
    json_acceptable_string = scan_report.replace("'", "\"")
    scan_report_results = json.loads(json_acceptable_string)

    return scan_report_results, request

def get_scanned_sites(engine):
    cursor = engine.cursor()
    final_lst= []
    get_scanned_sites_list ="SELECT distinct site from requests where scan_ts::timestamp > (now()::timestamp - INTERVAL '30 min')"

    df = pd.read_sql_query(get_scanned_sites_list, con=engine)
    scanned_sites_list = df.values.tolist()
    for site in scanned_sites_list :
        final_lst.append(site[0])
    return final_lst

def insert_requests(engine, requests_list):
    cursor = engine.cursor()
    cols = 'scan_id, site, scan_ts, last_site_scan'
    table = 'public.requests'
    for request in requests_list:
        url = (request.get("url")).replace("http://","").replace("/","")
        if url == 'stackoverflow.com':
            url = 'www.stackoverflow.com'
        query = "INSERT INTO "+table+"("+cols+") VALUES ('"+request.get("scan_id")+"', '"+url+"', now()::timestamp , '"+request.get("scan_date")+"');".format(table = table, cols= cols)
        cursor.execute(query)
        engine.commit()

def insert_scan_results(engine, scan_results_list):
    cursor = engine.cursor()
    cols = 'site, scan_total_amount, positive_scan_amount, scan_detected_keyword, scan_ts'
    table = 'public.scan_results'
    keyword_str = ''
    for scan_result in scan_results_list:
        for scan_res in scan_result.get("scans").values():
            if scan_res.get("detected") == False:
                continue
            keyword_str += scan_res.get("result") +","
        query = "INSERT INTO "+table+"("+cols+") VALUES ('"+scan_result.get("url").replace("http://","").replace("/","")+"', "+str(scan_result.get("total"))+", "+str(scan_result.get("positives"))+", '"+keyword_str[:-1]+"' , '"+scan_result.get("scan_date")+"');".format(table = table, cols= cols)

        cursor.execute(query)
        engine.commit()


if __name__ == '__main__':
    # TODO - move hard code connection to config file
    engine = connect_to_pg("de_test", "postgres", "localhost", "5432", base64.b64decode("RHJvbmU5OTYzIQ==").decode("utf-8"))
    site_list = get_urls_csv("https://elementor-pub.s3.eu-central-1.amazonaws.com/Data-Enginner/Challenge1/request1.csv", engine)
    scan_results_list = []
    requests_list = []
    for site in site_list:
        site_scan_result, request = get_site_scan_result(site)
        if site_scan_result is not None:
            print('scanned site -->'+site)
            scan_results_list.append(site_scan_result)
            requests_list.append(request)
        else:
            print('No content received from site -->' + site)
    insert_requests(engine, requests_list)
    insert_scan_results(engine, scan_results_list)
    # set_arr_user_currency(engine)


