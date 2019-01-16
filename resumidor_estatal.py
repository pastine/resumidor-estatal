import praw
import time
from summa import summarizer
import config
import os

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
    stickied = reddit.submission(url='http://www.reddit.com'+comment.permalink).comments[0]
    if not stickied.replies.list(): return False
    if not stickied.author == config.REPLY_TO: return True
    for sub_comment in stickied:
        if sub_comment.author.name == config.ME:
            return True
        return False

def valid(comment):
    return comment.subreddit.display_name in config.SUBREDDITS and len(comment.body.split()) > config.WORDS_THRESHOLD

def watch_and_reply():
    possible_comments = reddit.redditor(config.REPLY_TO).comments.new(limit=20)
    valid_comments = [c for c in possible_comments if valid(c)]
    for comment in valid_comments:
        if is_replied(comment):
            continue
        comment.reply(build_child_comment(comment))

def main():
    while True:
        try:
            watch_and_reply()
        except praw.exceptions.APIException:
            print('Seems like we can\'t reply at the moment!')
        finally:
            print(f'Sleeping for {config.TIMEOUT} seconds...')
            time.sleep(config.TIMEOUT)

if __name__ == '__main__':
    main()
