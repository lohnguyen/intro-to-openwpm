import sys
import math
import sqlite3
import tldextract

import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter

MODE_UBLOCK = "(ublock mode)"
MODE_VANILLA = "(vanilla mode)"
TITLE_REQUESTS = "third-party HTTP(S) requests"
TITLE_COOKIES = "third-party cookies"
TITLE_JAVASCRIPT = "third-party JavaScript API calls"

DB_VANILLA = "./db/vanilla/crawl-data.sqlite"
DB_UBLOCK = "./db/ublock/crawl-data.sqlite"
PATH_CSV = "./top-1m.csv"

QUERY_REQUESTS = "SELECT visit_id, url FROM http_requests"
QUERY_COOKIES = "SELECT visit_id, host FROM javascript_cookies"
QUERY_JAVASCRIPT = "SELECT visit_id, script_url FROM javascript"


def get_sites_from_csv():
    data = pd.read_csv(PATH_CSV)
    return data.iloc[:99, 1].values


def query_from_db(query, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(query)

    rows = c.fetchall()

    c.close()
    conn.close()

    return rows


def is_third_party(domain, url):
    domain_ext = tldextract.extract(domain)
    url_ext = tldextract.extract(url)

    if '.'.join(domain_ext[:]) == '.'.join(url_ext[:]):
        return False

    return True


def show_top_10(vanilla_counter, ublock_counter, title):
    vanilla_top_10 = vanilla_counter.most_common(10)
    ublock_top_10 = ublock_counter.most_common(10)
    indexes = []
    vanilla_domains = []
    ublock_domains = []
    vanilla_quantities = []
    ublock_quantities = []

    for i in range(len(ublock_top_10)):
        indexes.append(i + 1)
        vanilla_domains.append(vanilla_top_10[i][0])
        ublock_domains.append(ublock_top_10[i][0])
        vanilla_quantities.append(vanilla_top_10[i][1])
        ublock_quantities.append(ublock_top_10[i][1])

    df = pd.DataFrame({"Domain (vanilla)": vanilla_domains,
                       "Quantity (vanilla)": vanilla_quantities,
                       "Domain (ublock)": ublock_domains,
                       "Quantity (ublock)": ublock_quantities}, index=indexes)
    print("\n       {} {}\n".format('Top 10', title))
    print(df.to_markdown(), '\n')


def count_third_parties(third_parties, rows):
    for row in rows:
        visit_id = row[0] - 1
        url = row[1]
        ext = tldextract.extract(url)
        url = '.'.join(ext[1:])

        if is_third_party(sites[visit_id], url):
            third_parties.append(url)


def plot_histograms(vanilla_counter, ublock_counter, title, measurement):
    y_vanilla = list(vanilla_counter.values())
    y_ublock = list(ublock_counter.values())

    plt.hist([y_vanilla, y_ublock], bins="auto", alpha=.5,
             label=["vanilla mode", "ublock mode"])
    plt.title("Distribution of " + title)
    plt.xlabel("Number of " + measurement)
    plt.ylabel("Number of third-party domains")
    plt.legend()
    plt.show()


def get_rows(measurement):
    if measurement == "requests":
        return query_from_db(QUERY_REQUESTS, DB_VANILLA), query_from_db(QUERY_REQUESTS, DB_UBLOCK)
    elif measurement == "cookies":
        return query_from_db(QUERY_COOKIES, DB_VANILLA), query_from_db(QUERY_COOKIES, DB_UBLOCK)
    elif measurement == "javascript":
        return query_from_db(QUERY_JAVASCRIPT, DB_VANILLA), query_from_db(QUERY_JAVASCRIPT, DB_UBLOCK)
    else:
        exit()


def get_title(measurement):
    if measurement == "requests":
        return TITLE_REQUESTS
    elif measurement == "cookies":
        return TITLE_COOKIES
    elif measurement == "javascript":
        return TITLE_JAVASCRIPT


if __name__ == "__main__":
    measurement = sys.argv[1]
    vanilla_rows, ublock_rows = get_rows(measurement)
    sites = get_sites_from_csv()
    vanilla_third_parties = []
    ublock_third_parties = []

    count_third_parties(vanilla_third_parties, vanilla_rows)
    count_third_parties(ublock_third_parties, ublock_rows)

    vanilla_counter = Counter(vanilla_third_parties)
    ublock_counter = Counter(ublock_third_parties)

    title = get_title(measurement)
    show_top_10(vanilla_counter, ublock_counter, title)
    plot_histograms(vanilla_counter, ublock_counter, title, measurement)
