import requests
from bs4 import BeautifulSoup as soup
from multiprocessing.pool import ThreadPool


class NewsScraper():
    def __init__(self):
        self.base_url = 'https://www.newsnow.co.uk'
        self.url = 'https://www.newsnow.co.uk/h/'
        self.pool = ThreadPool(4)
        self.request = requests.Session()

    def get_html(self):
        page = self.request.get(self.url)
        soup_page = soup(page.text, 'html.parser')
        return soup_page

    def get_topics_url(self):
        urls = []
        page = self.get_html()
        topics_headers = page.find_all('a', class_='rs-topic-heading__link js-topic-heading-link')
        for header in topics_headers:
            urls.append(self.base_url + header.get('href'))
        return urls

    def get_themes_from_topic(self, topic_url):
        parsed_them = []
        page = self.request.get(topic_url)
        soup_page = soup(page.text, 'html.parser')
        topic_name = soup_page.find('a', class_='rs-topic-heading__link js-topic-heading-link').text
        themes = soup_page.find_all('div', class_='hl__inner')[:19][::1][::2]
        for them in themes:
            parsed_them.append(them.find('a').text)

        with open('output.txt', 'a+') as txt_file:
            txt_file.write('Topic name: {topic_name} \n'.format(topic_name=topic_name))
            txt_file.write('Themes:\n')
            for them in parsed_them:
                txt_file.write('\t{}\n'.format(them))
            txt_file.write('\n')

    def main(self):
        self.pool.map(self.get_themes_from_topic, self.get_topics_url())
        self.pool.close()


if __name__ == '__main__':
    scraper = NewsScraper()
    scraper.main()
