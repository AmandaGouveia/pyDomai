"""pyDomai

A tool for checking available domain names.
"""

import pandas as pd
import pythonwhois as who
import re

cleaner = lambda x: re.sub("[^A-Za-z1-9]+", "", str(x)).lower()

domain_points = {"com": 3, "ink": 2, "codes": 2}
length_points = {7: 1, 5: 3, 4: 6}


def is_available(word, domain):
    """checks if the domain is available"""
    try:
        x = who.get_whois(word + "." + domain)
    except:
        return False

    try:
        y = x["expiration_date"]
        return False

    except:
        return True

    return True


def points(row):
    """gives scores to each url"""
    word = row["word"]
    domain = row["domain"]
    points = 0
    try:
        points += domain_points[domain]
    except:
        pass
    try:
        points += length_points[len(word)]
    except:
        pass

    return points


# wordlist = "/usr/share/dict/words"
wordlist = "./testwords"

domains = [
    "com",
    "net",
    "app",
    "org",
    "club",
    "online",
    "io",
    "cafe",
    "click",
    "city",
    "cloud",
    "codes",
    "dog",
    "fish",
    "fishing",
    "garden",
]

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