import praw
import re
from datetime import datetime
import time
import algorithm
import constants
import cache

# check if this is being imported or not
if __name__ != "__main__":
    raise OSError("You need to run this file directly, not import it silly!")

reddit = praw.Reddit('MemeAdviser')

replied_file = cache.AbstractFile("../replied.txt")
subscribed_file = cache.AbstractFile("../subscribed.txt")
fileLoadCache = Cache.FileCache()
replied = fileLoadCache.refresh(replied_file.get_name())
subscribed = fileLoadCache.refresh(subscribed_file.get_name())
fileLoadCache.add(replied)
fileLoadCache.add(subscribed)

subreddit = reddit.subreddit("MemeEconomy")
post_subreddit = reddit.subreddit("InsiderMemeTrading")
submissions = subreddit.hot()
submission = next(submissions)

while submission.stickied:
    submission = submissions.next()

# Find out how old the post is
minutes = int(round((time.time() - submission.created_utc) / 60))

# Store time in hours
if minutes >= 60:
    minutes = str(minutes // 60) + "h " + str(minutes % 60) + "min"
else:
    minutes = str(round((time.time() - submission.created_utc) / 60)) + " minutes"

if submission.id not in replied:
    try:
        # Update replied.txt
        replied.append(submission.id)
        for post_id in replied:
            replied.write_to_file(post_id + "\n")

        # Post to r/InsiderMemeTrading
        if submission.score < constants.Thresholds.submission:
            post_subreddit.submit(title=constants.Messages.submission.format(upvotes=submission.score, break_even=algorithm.break_even(submission.score)), url="https://reddit.com" + submission.permalink)

        # Send PM to subscribers
        if submission.score < constants.Thresholds.pm:
            for user in subscribed:
                reddit.redditor(user).message("MemeEconomy Update", constants.Messages.pm.format(link=submission.permalink, upvotes=submission.score, break_even=algorithm.break_even(submission.score)))

        # Comment on r/MemeEconomy post
        if submission.score < constants.Thresholds.comment:
            submission.reply(constants.Messages.comment.format(upvotes=str(submission.score), time=str(datetime.utcfromtimestamp(submission.created_utc).strftime('%B %d %H:%M:%S')), min=minutes, break_even=algorithm.break_even(submission.score)))

    except:
        pass

unread_messages = []

# Go through each unread message
for message in reddit.inbox.unread():
    unread_messages.append(message)

    # Check for new unsubscriptions
    if re.search("unsubscribe", message.body, re.IGNORECASE) or re.search("unsubscribe", message.subject, re.IGNORECASE):
        if message.author.name in subscribed:
            subscribed.remove(message.author.name)
            for user in subscribed:
                fileLoadCache.write_to_file(subscribed_file.get_name(), user + "\n")
            message.reply("You've unsubscribed from MemeAdviser. To subscribe, reply with 'Subscribe'")
        else:
            message.reply("You aren't subscribed to MemeAdviser! If you want to subscribe, reply with 'Subscribe'")

    # Check for new subscriptions
    elif re.search("subscribe", message.body, re.IGNORECASE) or re.search("subscribe", message.subject, re.IGNORECASE):
        if message.author.name not in subscribed:
            subscribed.append(message.author.name)
            for user in subscribed:
                fileLoadCache.write_to_file(subscribed_file.get_name(), user + "\n")
            message.reply("You've subscribed to MemeAdviser! To unsubscribe, reply with 'Unsubscribe'")
        else:
            message.reply("You're already subscribed to MemeAdviser! If you want to unsubscribe, reply with 'Unsubscribe'")

# Mark all messages as read
reddit.inbox.mark_read(unread_messages)
