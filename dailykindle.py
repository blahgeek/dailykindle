import time
from datetime import datetime, timedelta, date
from os import system
import feedparser
from jinja2 import Environment, PackageLoader
from bs4 import BeautifulSoup
import logging

templates_env = Environment(loader=PackageLoader('dailykindle', 'templates'))

remove_attributes = ('class', 'id', 'title', 'style', 'width', 'height', 'onclick')
remove_tags = ('script', 'object', 'video', 'embed', 'iframe', 'noscript', 'style', 'img')
template_files = ('toc.ncx', 'content.opf', 'content.html')

def build(feeds_urls, output_dir, max_old=timedelta.max):

    logging.info('Starting...')
    feeds = [feedparser.parse(feed_url) for feed_url in feeds_urls]
    logging.info('Feed fetch complete')

    for feed_number, feed in enumerate(feeds):
        logging.info('Handling ' + feed.feed.title)
        feed.update({ 'number': feed_number + 1,
                      'title': feed.feed.title })
        for entry in feed.entries:
            entry.setdefault('author', 'Anonymous')
            entry.setdefault('date_parsed', entry.get('published_parsed', None))

        feed.entries = [entry for entry in feed.entries if \
                entry.date_parsed is not None and \
                datetime.fromtimestamp(time.mktime(time.gmtime())) \
                - datetime.fromtimestamp(time.mktime(entry.date_parsed)) <= max_old]

        for entry_number, entry in enumerate(feed.entries):
            entry.description = BeautifulSoup(entry.description).text[:200].strip()
            entry.update({'number': entry_number + 1})
            try: entry.content = entry.content[0].value;
            except: entry.content = entry.summary;

            content = BeautifulSoup(entry.content)
            for attr in remove_attributes:
                for x in content.findAll(attrs={attr:True}):
                    del x[attr]
            for x in content.findAll(remove_tags):
                x.extract()
            entry.content = content.decode('utf8')

    logging.info('Generating templates...')
    for template_name in template_files:
        template = templates_env.get_template(template_name)
        with open(path.join(output_dir, template_name), "w") as f:
            f.write(template.render(date=date.today().isoformat(), feeds=feeds))


def mobi(input_file, exec_path):
    """Execute the KindleGen binary to create a MOBI file."""
    logging.info("Running %s %s" % (exec_path, input_file))
    system("%s %s" % (exec_path, input_file))

if __name__ == "__main__":
    from config import *
    from shutil import move

    logging.basicConfig(filename=path.join(ROOT, 'main.log'), level='INFO', 
                        format='%(asctime)s [%(levelname)s] %(message)s')
    build(FEEDS_URL, OUTPUTDIR, MAXOLD)
    mobi(path.join(OUTPUTDIR, 'content.opf'), KINDLEGEN)
    move(path.join(OUTPUTDIR, 'content.mobi'), 
            path.join(OUTPUTDIR, 'content-%s.mobi' % date.today().isoformat()))
