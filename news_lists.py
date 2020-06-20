from newscatcher import Newscatcher
from newscatcher import urls
from newscatcher import describe_url


class ArticleAggregator:

    def __init__(self, topic:str, language:str='en', n=None):
        self.urls = (urls(topic=topic, language=language))
        if (n!=None):
            self.urls = self.urls[:n]
        self.topic = topic

        print(f"found {len(self.urls)} urls for {topic} topic")
        print(self.urls)
    def __len__(self):
        return len(self.urls)

    def get_articles(self):
        articles = []
        for i in self.urls:
            nc = Newscatcher(website=i,topic=self.topic)
            webart = nc.get_news(n=1)
            articles.append(webart)
        print(articles[0])
        return articles

    @staticmethod
    def available_topics():
        topics = set()
        for i in urls():
            try:
                des = describe_url(i)
                if des == None or des['topics']== None:
                    continue
                site_topics = des['topics']
                for j in site_topics:
                    topics.add(j)
            except Exception as e:
                # print(i)
                pass
        return topics

aa = ArticleAggregator("finance", "en",1)
print(aa.get_articles())