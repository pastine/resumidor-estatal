import praw
import time
from summa import summarizer
import config
import os
import logging
import logging.config

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'],
                     user_agent=os.environ['USER_AGENT'],
                     username=os.environ['BOT_USERNAME'],
                     password=os.environ['BOT_PASSWORD'])

def build_child_comment(parent_comment):
    reply = config.COMMENT_HEADER
    reply += summarize_news(parent_comment.body)
    reply += config.COMMENT_FOOTER
    return reply
    
def summarize_news(parent_comment_body):
    summary = '>' # Summary must be quoted
    summary += summarizer.summarize(parent_comment_body, language='spanish')
    summary = summary.replace('\n','\n>\n>') # Reddit uses markdown, where paragraphs are divided by two breaklines
    return summary

def is_replied(comment):
    logging.debug("Trying to reply to: http://www.reddit.com" + comment.permalink)
    comment.refresh()
    comment.replies.replace_more()
    if not comment.author == os.environ['REPLY_TO']: return True
    if not comment.replies.list(): return False
    for sub_comment in comment.replies.list():
        if sub_comment.author.name == os.environ['ME']:
            logging.debug("Skipping comment because it was already replied")
            return True
    return False

def valid(comment):
    return comment.subreddit.display_name in os.environ['SUBREDDITS'].split() and len(comment.body.split()) > config.WORDS_THRESHOLD

def watch_and_reply():
    possible_comments = reddit.redditor(os.environ['REPLY_TO']).comments.new(limit=20)
    valid_comments = [c for c in possible_comments if valid(c)]
    for comment in valid_comments:
        if is_replied(comment):
            continue
        comment.reply(build_child_comment(comment))
        logging.info("Replied to: http://www.reddit.com" + comment.permalink)

def main():
    loglevel = logging.DEBUG if os.environ['LOGLEVEL']=='DEBUG' else logging.INFO
    logging.config.dictConfig({'version':1,'disable_existing_loggers':True})
    logging.basicConfig(level=loglevel, format='%(asctime)s - %(levelname)s - %(message)s')
    while True:
        try:
            watch_and_reply()
        except praw.exceptions.APIException:
            logging.error('Seems like we can\'t reply at the moment!')
        finally:
            logging.info(f'Sleeping for {config.TIMEOUT} seconds...')
            time.sleep(config.TIMEOUT)

if __name__ == '__main__':
    main()
