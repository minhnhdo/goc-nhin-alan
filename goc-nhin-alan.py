# -*- coding: utf-8 -*-
from calibre.web.feeds.news import BasicNewsRecipe
from datetime import datetime


class GocNhinAlan(BasicNewsRecipe):
    title = u'Góc Nhìn Alan'
    description = u'Góc Nhìn Alan'
    keep_only_tags = [{'name': 'div', 'id': 'article_content', 'class': 'single_article_content'}]
    date_format = '%d / %m / %Y'

    def parse_index(self):
        ret = []
        for title, url in [(u'Khu Vườn Alan', 'http://www.gocnhinalan.com/category/bai-tieng-viet'),
                           (u'Lang Thang Phố Nhỏ', 'http://www.gocnhinalan.com/category/blog-cua-alan-va-bca'),
                           (u'Sân Chơi của Khách', 'http://www.gocnhinalan.com/category/bai-cua-khach'),
                           (u'Kí Sự Tháng Ngày', 'http://www.gocnhinalan.com/category/cac-hoat-dong-khac/hoat-dong-khac'),
                           (u'Tư Duy Đại Dương', 'http://www.gocnhinalan.com/category/bai-tieng-anh')]:
            article_list = []
            soup = self.index_to_soup(url)
            for article in soup.findAll('article'):
                article_link = article.find('h2', 'cat_article_title').find('a')
                article_date = datetime.strptime(article.find('div', 'cat_article_warap').find('div', 'article_meta')
                                                        .find('span', 'meta_date').strong.renderContents(),
                                                 self.date_format)
                article_description = article.find('div', 'cat_article_warap').find('div', 'cat_article_content')\
                                             .p.renderContents()
                article_list.append({
                    'title': article_link.renderContents().strip(),
                    'url': article_link.get('href'),
                    'date': article_date,
                    'description': article_description.strip(),
                })
            ret.append((title, article_list))
        return ret