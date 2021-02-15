1. Design - Getting the scan reports from totalVirus API ->
    a. API to get each site results - due to limited API conditions then i decided to go scan the site separately
    b. Each site will be need to have scan + report APIs to get the results, meaning 2 requests – per site  needs to be evaluated if there is a shorter way to get the scan results
    c. Taking from the url supplied all the sites which are to be scanned
    d. Using GET endpoint to get the scan results using Python 3 all the site from the csv
    e. inserting the requests into a table on PostgresSQL
    f. Inserting the scan results into a table on PostgresSQL
    g. Fetching only sites which were not scanned in the last 30 minutes based on ‘requests’ table’


2.	installation and running
CREATE DATABASE de_test

CREATE TABLE public.requests
(
    scan_id character varying(300) COLLATE pg_catalog."default" NOT NULL,
    site character varying(100) COLLATE pg_catalog."default",
    scan_ts timestamp without time zone,
    last_site_scan timestamp without time zone
)

CREATE TABLE public.scan_results
(
    site character varying(100) COLLATE pg_catalog."default",
    scan_total_amount bigint,
    positive_scan_amount bigint,
    scan_detected_keyword character varying(1000) COLLATE pg_catalog."default",
    scan_ts timestamp without time zone
)

Install pgadmin4 -> https://www.enterprisedb.com/downloads/postgres-postgresql-downloads --> go to PGAdmin4 ->databases->postgres-> open sql ‘Query tool’ -> run the above sql queries in DATABASE created de_test


Then run python code to load latest scan results to table as well as requests.

3.	
  a.The response is often returns ‘no-content’ , seems like issues with the api key limitations. 
  b. Scan results are being inserted with the found scan results as keyword (‘phishing, malicious) – need to be adjusted according to requirements
  c. Requests are being inserted only if there was a response – might need to keep track of all the ‘no-response’ requests.
  d. Currently needs 2 requests – one for the scan and second for the report – might be a better solution aggregating both in one request. Needs to be investigated 
Storing the timestamp in sort order on the table to have the ability to quickly extract the latest scan results.


AWS - didn't have time to get to this :|
