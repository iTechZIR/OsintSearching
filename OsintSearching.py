
from requests import get
from fuzzywuzzy import fuzz
from googlesearch import search
from bs4 import BeautifulSoup

print('(=================================================)')
print('(===============> OsintSearching <================)')
print('(=================================================)\n\n')


query = input('[+] - Please Enter The Text: ')
results = 1000000000000000000000000000

logfile = []  
print(f'[+] - Searching {query}')
logfile.append(f'[+] - Searching {query}')

for url in search(query, stop=results):
    print(f'\n[+] - Url Detected: {url}')
    logfile.append(f'[+] - Url Detected: {url}')
    try:
        text = get(url, timeout=1).text
    except:
        continue

    soup = BeautifulSoup(text, "html.parser")
    linkdetected = []

    try:
        title = soup.title.text.replace('\n', '')
        print(f'[+] - Title: {title}')
        logfile.append(f'[+] - Title: {title}')
    except:
        print('[+] - Title: null')
        logfile.append('[+] - Title: null')

    try:
        for link in soup.findAll('a'):
            href = link.get('href')
            if not href or href in linkdetected:
                continue

            if href.startswith('http'):
                domain = url.split('/')[2]
                if domain in href:
                    linkdetected.append(href)
                elif query.lower() in href.lower():
                    print(f'--------- Requested Data Found At Link: {href}')
                    logfile.append(f'---------  Requested Data Found At Link: {href}')
                    linkdetected.append(href)
                elif fuzz.ratio(link.text, href) >= 60:
                    print(f'---------  Text and Link Are Similar: {href}')
                    logfile.append(f'---------  Text and Link Are Similar: {href}')
                    linkdetected.append(href)
    except:
        continue

    if not linkdetected:
        print('[-] - No Data Found')
        logfile.append('[-] - No Data Dound')

with open("Log.txt", "w", encoding="utf-8") as f:
    f.write('\n'.join(logfile))

print('\n[+] - All Results Have Been Saved To Log.txt')
