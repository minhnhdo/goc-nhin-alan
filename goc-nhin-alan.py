# -*- coding: utf-8 -*-
import itertools

from calibre.web.feeds.news import BasicNewsRecipe
import BeautifulSoup
from datetime import datetime
import time


class GocNhinAlan(BasicNewsRecipe):
    title = u'Góc Nhìn Alan'
    max_articles_per_feed = 1000000
    oldest_article = 3650.0
    timeout = 30
    language = 'vi'
    publication_type = 'blog'
    encoding = 'utf8'
    remove_empty_feeds = True
    remove_javascript = True
    no_stylesheets = True
    keep_only_tags = [{'name': 'div', 'id': 'article_content'}]
    delay = 1  # seconds
    date_format = '%Y-%m-%dT%H:%M:%SZ'

    @staticmethod
    def make_url(base, upto):
        return itertools.chain([base], ((base+'?paged={}').format(i) for i in xrange(2, upto+1)))

    def parse_index(self):
        ret = []
        for title, urls in [
            (u'Khu Vườn Alan', self.make_url('http://www.gocnhinalan.com/category/bai-tieng-viet/feed/atom', 29)),
            (u'Lang Thang Phố Nhỏ', self.make_url('http://www.gocnhinalan.com/category/bai-cua-khach/feed/atom', 72)),
            (u'Sân Chơi của Khách', self.make_url('http://www.gocnhinalan.com/category/bai-tieng-anh/feed/atom', 26)),
            (u'Kí Sự Tháng Ngày',
             self.make_url('http://www.gocnhinalan.com/category/blog-cua-alan-va-bca/feed/atom', 36)),
            (u'Tư Duy Đại Dương',
             self.make_url('http://www.gocnhinalan.com/category/cac-hoat-dong-khac/hoat-dong-khac/feed/atom', 3))]:
            article_list = []
            for url in urls:
                soup = self.index_to_soup(url)
                self.report_progress(0, 'Fetched feed {}'.format(url))
                for article in soup.findAll('entry'):
                    title_node = article.find('title')
                    for t in title_node:
                        if isinstance(t, BeautifulSoup.CData):
                            title = t.contents[0].strip()
                            break
                    article_list.append({
                        'title': title,
                        'url': article.find('link').get('href').strip(),
                        'date': datetime.strptime(article.find('published').renderContents().strip(), self.date_format),
                    })
                time.sleep(self.delay)
            article_list.reverse()
            self.report_progress(0, 'Fetched {} articles for feed'.format(len(article_list)))
            ret.append((title, article_list))
        return ret