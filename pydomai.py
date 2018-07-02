"""pyDomai

A tool for checking available domain names.
"""

import pandas as pd
import pythonwhois as who
import re

cleaner = lambda x: re.sub("[^A-Za-z1-9]+", "", str(x)).lower()


def is_available(word, domain):
    """checks if the domain is available"""
    try:
        x = who.get_whois(word + "." + domain)
    except:
        return False
    try:
        y = x['expiration_date']
        return False
    except:
        return True
    return True


def points(row):
    """gives scores to each url"""
    word = row["word"]
    domain = row["domain"]
    points = 0
    if domain == "com":
        points += 3
    if len(word) < 7:
        points += 3
    if len(word) < 5:
        points += 3
    if len(word) < 4:
        points += 3
    return points


#wordlist = "/usr/share/dict/words"
wordlist = "./testwords"

domains = ["com", "net","app","org","club","online","io","cafe","click","city","cloud","codes","dog","fish","fishing","garden"]

words = pd.read_csv(wordlist)
words.columns = ["Word"]

words["Word"] = words["Word"].apply(cleaner)

urls = []
for word in words["Word"]:
    for domain in domains:
        if is_available(word, domain):
            urls.append([word, domain])
df = pd.DataFrame.from_records(urls, columns=["word", "domain"])
df["points"] = df.apply(points, axis=1)
df.sort_values(by="points", ascending=False, inplace=True)
print(df.head())
