import praw
from praw import *
import time
from summa import summarizer
import config

reddit = praw.Reddit('resumidor_estatal')

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
    replies = comment.replies.list()
    for sub_comment in replies:
        if sub_comment.author.name == config.ME:
            return True
        return False

def watch_and_reply(comments_replied, file):
    for comment in reddit.redditor(config.REPLY_TO).comments.new(limit=10):
        if is_replied(comment):
            continue
        comment.reply(build_child_comment(comment))


def main():
    try:
        file = open('comments_ids.txt', 'r+')
    except:
        file = open('comments_ids.txt', 'a+')
    comments_replied = set(map(str.strip, file))
    while True:
        try:
            watch_and_reply(comments_replied, file)
            print(f'Sleeping for {config.TIMEOUT} seconds...')
            time.sleep(config.TIMEOUT)
        except Exception:
            print('Seems like we can\'t reply at the moment! Trying again in a minute')
            time.sleep(config.TIMEOUT)
    file.close()  #Heh


if __name__ == '__main__':
    main()
