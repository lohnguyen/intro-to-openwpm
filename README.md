# Intro To OpenWPM

A brief introduction to web-crawling with OpenWPM. The top 100 websites are visited via Firefox (one browser) and recorded in both "vanilla mode" and "ad blocking mode" (using uBlock Origin extension).

The list of the websites is taken from Tranco (https://tranco-list.eu/download_daily/56JN) and should be located in the project's root directory. The tool OpenWPM is taken from Mozilla (https://github.com/mozilla/OpenWPM) and should be located in the project's root directory as `openwpm`.

> **_NOTE:_** top-1m.csv must start with `index,domain` for the csv reading to work properly.

## Activate virtual environment

```python3
conda activate openwpm
```

## Run the crawler

```python3
python3 crawler.py <n> <m>
```

where `<n>` is the number of sites to record and `<m>` is the mode to launch the browser in (set to `vanilla` or `ublock` to run the browser in "vanilla mode" or "ad blocking mode" respectively).

## Run the analysis

```python3
python3 analysis.py <m>
```

where `<m>` is the measurement to record (set to `requests`, `cookies`, or `javascript` to measure the number of HTTP(S) requests, cookies, and JavaScript API calls respectively).

## Analysis

### Third-party HTTP(S) requests

#### Distribution of websites with third-party HTTP(S) requests

![Distribution Requests](histogram_requests.png)

More than half of the top 100 websites make from 10 to 120 third-party HTTP(S) requests in both modes (with a lot less websites in vanilla mode than in ublock mode). Specifically, most websites in ublock mode make less than 40 requests and none makes more than 300 requests. There is an even distribution of websites in vanilla mode in the middle and upper range where each website makes anywhere from 130 to 350 requests). Also, in the range of 160-300 requests, there are clearly less websites that make less requests in ublock mode than in vanilla mode.

#### Top 10 third-party domains with HTTP(S) requests

|     | Domain (vanilla)      | Quantity (vanilla) |     | Domain (ublock)       | Quantity (ublock) |
| --: | :-------------------- | -----------------: | --- | :-------------------- | ----------------: |
|   1 | ssl-images-amazon.com |                471 |     | ssl-images-amazon.com |               537 |
|   2 | doubleclick.net       |                322 |     | msocdn.com            |               249 |
|   3 | alicdn.com            |                252 |     | cloudfront.net        |               208 |
|   4 | msocdn.com            |                249 |     | pstatic.net           |               207 |
|   5 | google.com            |                245 |     | alicdn.com            |               201 |
|   6 | googlesyndication.com |                235 |     | pinimg.com            |               195 |
|   7 | pstatic.net           |                229 |     | qhimg.com             |               150 |
|   8 | cloudfront.net        |                203 |     | awsstatic.com         |               149 |
|   9 | pinimg.com            |                200 |     | csdnimg.cn            |               138 |
|  10 | awsstatic.com         |                164 |     | twimg.com             |               118 |

Many of these domains seem to be CDN distributors (msocdn.com - for Microsoft Office, cloudfront.net, or alicdn.com). ssl-images-amazon.com, which is apparently a server that stores images for Amazon web pages, makes the most requests in both modes. Similarly, pinimg.com is Pinterest's server for images but it ranks lower in the list. Noticably, doubleclick.net by Google (placed second on the list in vanilla mode) is an advertising service which is agressively blocked in ublock mode.

### Third-party cookies

#### Distribution of websites with third-party cookies

![Distribution Cookies](histogram_cookies.png)

The majority of the top 100 websites contains about 0-25 third-party cookies (85% and 55% of the websites in vanilla mode and ublock mode respectively). The rest of the websites in ublock mode is in the range from 25 to 80 cookies. Meanwhile, websites in vanilla mode distribute quite evenly in the that same range (in more quantity) and also from 120-130 cookies. Remarkably, there are quite many websites in vanilla mode that makes over 200 cookies, with a couple even reaching over 410 cookies.

#### Top 10 third-party domains with cookies

|     | Domain (vanilla)   | Quantity (vanilla) |     | Domain (ublock) | Quantity (ublock) |
| --: | :----------------- | -----------------: | --- | :-------------- | ----------------: |
|   1 | yahoo.com          |                301 |     | amazon.com      |                64 |
|   2 | demdex.net         |                253 |     | bbc.com         |                25 |
|   3 | pubmatic.com       |                195 |     | microsoft.com   |                22 |
|   4 | rubiconproject.com |                172 |     | aliexpress.ru   |                20 |
|   5 | doubleclick.net    |                148 |     | youtube.com     |                19 |
|   6 | adsrvr.org         |                124 |     | tmall.ru        |                19 |
|   7 | casalemedia.com    |                102 |     | google.com      |                17 |
|   8 | adnxs.com          |                 86 |     | live.com        |                16 |
|   9 | linkedin.com       |                 85 |     | bing.com        |                11 |
|  10 | rlcdn.com          |                 82 |     | yahoo.com       |                 9 |

Alarmingly, most of the domains in the vanilla list (casalemedia.com, doubleclick.net, pubmatic.com, rubiconproject.com, adsrvr.org, adnxs.com) are digital from ad exchanging/tracking platforms. Also, demdex.net by Adobe Analytics is a capturer of behavioral data that tracks and identifies unique users across websites, which is ranked second in the vanilla list. With uBlock Origin in action, the number of third-party cookies drastically reduces and those aforementioned domains seem to be blocked completely. In ublock mode, most of the domains are of well-known companies like Amazon, Microsoft, Google, Yahoo, BBC News,...

### Third-party JavaScript API calls

#### Distribution of websites with third-party JavaScript API calls

![Distribution Cookies](histogram_javascript.png)

Most of the websites make from 10 to 800 third-party JavaScript API calls in both modes. In this lower range, there are many more websites in ublock mode which makes a lot less calls than in vanilla mode. Some websites makes from 1000 to 3000 calls in vanilla mode. Noticably, there are one website in ublock mode and one in vanilla mode that make up to 5000 calls and 9500 calls to third-party hosts respectively.

#### Top 10 third-party domains with JavaScript API calls

|     | Domain (vanilla)     | Quantity (vanilla) |     | Domain (ublock) | Quantity (ublock) |
| --: | :------------------- | -----------------: | --- | :-------------- | ----------------: |
|   1 | forbesimg.com        |               4347 |     | wsimg.com       |              2624 |
|   2 | media.net            |               2292 |     | alicdn.com      |              1067 |
|   3 | segment.com          |               1665 |     | itc.cn          |               782 |
|   4 | alicdn.com           |               1255 |     | youtube.com     |               422 |
|   5 | google-analytics.com |               1229 |     | guim.co.uk      |               411 |
|   6 | adobedtm.com         |                900 |     | segment.com     |               315 |
|   7 | doubleclick.net      |                867 |     | bcicdn.com      |               309 |
|   8 | itc.cn               |                847 |     | twitchcdn.net   |               305 |
|   9 | krxd.net             |                814 |     | yimg.jp         |               294 |
|  10 | googletagmanager.com |                767 |     | awsstatic.com   |               272 |

Noticably, at least three of the 10 domains in the vanilla list are from Google (googletagmanager.com, google-analytics.com, and doubleclick.net - now owned by Google), all of which make over 2000 calls and are blocked agressively by uBlock Origin. Furthermore, placed second and third in the vanilla list are media.net and segment.com - respectively an advertising platform and a customer data platform that collects and controls customer data. Also, krxd.net is a data platform that profiles users for advertisements. With uBlock Origin on, those mentioned sites are no longer in the list. Also, there is a decrease in the number of calls and the domains seems somewhat more legit in ublock mode.
