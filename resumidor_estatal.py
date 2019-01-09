import praw
import time
from summa import summarizer
import config

reddit = praw.Reddit('resumidor_estatal')

def build_child_comment(parent_comment):
    reply = config.HEADER
    reply += summarize_news(parent_comment.body)
    reply += config.FOOTER
    return reply
    
def summarize_news(parent_comment_body):
    summary = '>' # Summary must be quoted
    summary += summarizer.summarize(parent_comment_body, language='spanish')
    summary = summary.replace('\n','\n>\n>') # Reddit uses markdown, where paragraphs are divided by two breaklines
    return summary

def watch_and_reply(comments_replied, file):
    for comment in reddit.redditor(config.REPLY_TO).comments.new(limit=10):
        if comment.id in comments_replied:
            print('Already replied to this comment :(')
            continue
        print('Found a comment! Time to reply.')
        comment.reply(build_child_comment(comment))
        comments_replied.add(comment.id)
        file.write(comment.id+'\n')
        file.flush()


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
        except:
            print('Seems like we can\'t reply at the moment! Trying again in a minute')
            time.sleep(config.TIMEOUT)
    file.close()  #Heh


if __name__ == '__main__':
    main()
