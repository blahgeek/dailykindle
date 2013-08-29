import time
from datetime import datetime, timedelta, date
import subprocess
import feedparser
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup
import logging
import socket
from config import *

templates_env = Environment(loader=FileSystemLoader(TEMPLATEDIR))

remove_attributes = ('class', 'id', 'title', 'style', 'width', 'height', 'onclick')
remove_tags = ('script', 'object', 'video', 'embed', 'iframe', 'noscript', 'style', 'img')
template_files = ('toc.ncx', 'content.opf', 'content.html')

def build(feeds_urls, output_dir, max_old=timedelta.max):

    socket.setdefaulttimeout(15)
    logging.info('Starting...')
    feeds = map(lambda x: feedparser.parse(x), feeds_urls)
    feeds = filter(lambda x: x.feed.has_key('title'), feeds)

    for feed in feeds:
        logging.info('Handling ' + feed.feed.title)
        for entry in feed.entries:
            entry.setdefault('author', 'Anonymous')
            entry.setdefault('date_parsed', entry.get('published_parsed', None))

        feed.entries = filter(lambda x: x.date_parsed is not None, feed.entries)
        mkstamp = lambda x: datetime.fromtimestamp(time.mktime(x))
        nowstamp = mkstamp(time.gmtime())
        feed.entries = filter(lambda x: nowstamp-mkstamp(x.date_parsed) <= max_old, feed.entries)

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

    feeds = filter(lambda x: len(x.entries) > 0, feeds)

    for feed_number, feed in enumerate(feeds):
        feed.update({ 'number': feed_number + 1,
                      'title': feed.feed.title })

    logging.info('Generating templates...')
    for template_name in template_files:
        template = templates_env.get_template(template_name)
        with open(path.join(output_dir, template_name), "w") as f:
            f.write(template.render(date=date.today().isoformat(), feeds=feeds))


def mobi(input_file, exec_path):
    """Execute the KindleGen binary to create a MOBI file."""
    logging.info("Running %s %s" % (exec_path, input_file))
    s = subprocess.Popen([exec_path, input_file], stdout=subprocess.PIPE)
    while True:
        out = s.stdout.readline().decode('utf8')
        if not out: break;
        logging.info(out.strip())

if __name__ == "__main__":
    from shutil import move

    logging.basicConfig(filename=path.join(ROOT, 'main.log'), level='INFO', 
                        format='%(asctime)s [%(levelname)s] %(message)s')
    try:
        build(FEEDS_URL, OUTPUTDIR, MAXOLD)
        mobi(path.join(OUTPUTDIR, 'content.opf'), KINDLEGEN)
    except:
        logging.exception('Got exception on main:')
        raise
