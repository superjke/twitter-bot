from TwitterBot import TwitterBot

if __name__=='__main__':
    username=""
    password=""
    hashtags = ["cats", "dogs"]

    bot = TwitterBot(username, password)
    bot.login()
    bot.like_tweet_follow(hashtags)