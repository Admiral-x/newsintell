import threading
import numpy as np
import pandas as pd
import tqdm
from joblib import Parallel, delayed
from newscatcher import Newscatcher
from newspaper import Article
from newscatcher import urls

def parse_article(url: str):
    article = Article(url, language="en")
    article.download()
    article.parse()
    article.nlp()
    result = {}
    result["main_text"] = article.text
    result["keywords"] = article.keywords
    result["publish_date"] = article.publish_date
    result["images_list"] = article.images
    result["summary"] = article.summary
    result["meta_data"] = article.meta_data
    result["meta_description"] = article.meta_description
    result["source_url"] = article.source_url
    result["title"] = article.title
    return result


def catch_trends(website: str, topic=None):
    nc = Newscatcher(website=website, topic=topic)
    results = nc.get_news()
    keywords = []
    articles = results['articles']
    articles_count = len(articles)
    for article_num in tqdm.tqdm(range(articles_count)[:2]):
        article = articles[article_num]
        link = articles[article_num]["link"]
        try:
            parsed = parse_article(link)
        except Exception as e:
            print(link)
            continue
        article_keywords = parsed["keywords"]
        keywords += article_keywords
    return (keywords)

def get_trend_for_website(website:str, top_n:int=10):
    try:
        keyword_list = catch_trends(website)
        df = pd.DataFrame(np.array(keyword_list), columns=['keyword'])
    # count = df['keyword'].value_counts(dropna=False)[:10].index.tolist()
        a = (df['keyword'].value_counts(dropna=False)[:top_n])
        return a
    except Exception as e:
        print(website)
        return None

    # print(a+a)
    # for c in count:
    #
    #     print(f"{c}:{keyword_list.count(c)}")

def download_all_sites(sites):
    r = Parallel(n_jobs=8,verbose=10)(delayed(get_trend_for_website)(i,10000) for i in sites)
    # res, i = zip(*r)
    df = r[0]
    for i in range(1,len(r)):
        if (not r[i] is None):
            df = df.add(r[i], fill_value=0)
    df = pd.DataFrame(df)
    print(df.sort_values())

    # a = (df['keyword'].value_counts(dropna=False)[:20])
    # print(a)
    # print(df.columns.values)
    # print(df.sort(['ke', 'B'], ascending=[1, 0]))
print(len(urls(language="en")))
sites = urls(language="en")[:2]
print(sites)
download_all_sites(sites)