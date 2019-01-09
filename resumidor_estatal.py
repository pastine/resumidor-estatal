import praw
import time
from summa import summarizer


reddit = praw.Reddit('resumidor_estatal')


def watch_and_reply(comments_replied, file):
    for comment in reddit.redditor('ResumidorEstatalDum').comments.new(limit=10):
        if comment.id in comments_replied:
            print('Already replied to this comment :(')
            continue
        print('Found a comment! Time to reply.')
        comment.reply(summarizer.summarize(comment.body, language='spanish'))
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
            print('Sleeping for 1 minute...')
            time.sleep(60)
        except:
            print('Seems like we can\'t reply at the moment! Trying again in a minute')
            time.sleep(60)
    file.close()  #Heh


if __name__ == '__main__':
    main()
