from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import helper
import datetime

class TwitterBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()


    def login(self):
        bot = self.bot
        bot.get("https://twitter.com")
        time.sleep(1)
        email = bot.find_element_by_class_name('email-input')
        pwd = bot.find_element_by_name('session[password]')
        email.clear()
        pwd.clear()
        email.send_keys(self.username)
        pwd.send_keys(self.password)
        pwd.send_keys(Keys.RETURN)
        helper.wait_random_time()


    def like_tweet_follow(self, hashtags):
        def get_latest_feed(hashtag):
            url = "https://twitter.com/search?q="+hashtag+"&src=recent_search_click&f=live"
            print("Requesting latest feed for '{}'".format(hashtag))
            bot.get(url)
            helper.wait_random_time()


        def get_tweet_links():
            tweetLinks=[]
            try:
                tweetLinks = [i.get_attribute('href')
                    for i in bot.find_elements_by_xpath("//a[@role='link']")]
            except Exception as e:
                print("Something went wrong getting tweet links:", e)

            if (len(tweetLinks) == 0):
                return []

            filteredLinks = list(filter(lambda x: 'status' in x,tweetLinks))
            print("Got {} tweet links".format(len(filteredLinks)))
            
            return filteredLinks


        def like_tweet():
            unlikeFound = True
            try:
                bot.find_element_by_xpath("//div[@data-testid='unlike']")
            except:
                unlikeFound = False

            if not unlikeFound:
                try:
                    bot.find_element_by_xpath("//div[@data-testid='like']").click()
                    print("Liked tweet")
                    return True
                except Exception as e:
                    print("Failed to find like button:", e)
                    return False
            else:
                print("Tweet already liked")
                return False


        def visit_user(profileLink):
            print("Visiting user", profileLink.split("twitter.com/")[1])
            bot.get(userProfileLink)


        def follow_user():
            try:
                btnDataTestIds = [i.get_attribute('data-testid')
                    for i in bot.find_elements_by_xpath("//div[@role='button']")]
            except:
                return False
            
            followTdid = ""
            for dtid in btnDataTestIds:
                if dtid == None:
                    continue
                if "-unfollow" in dtid:
                    print("User already followed")
                    time.sleep(2)
                    break
                if "-follow" not in dtid:
                    continue    

                followTdid = dtid
                break # Use first follow link

            if followTdid == "":
                return False

            xpath = "//div[@data-testid='"+followTdid+"']"
            try:
                bot.find_element_by_xpath(xpath).click()
                print("Followed user")
                return True
            except Exception as e:
                print("Failed to find follow button:", e)
                return False


        bot = self.bot
        processedTweets = set()
        processedUsers = set()
        usersFollowedTemp = 0
        totalUsersFollowed = 0
        totalTweetsLiked = 0
        followLimit = random.randint(2, 4)
        cooloffPeriod = 2 # mins
        nextAllowedFollowTime = datetime.datetime.now()
        
        while True:
            hashtag = hashtags[random.randint(0,len(hashtags)-1)]
            get_latest_feed(hashtag)
            tweetLinks = get_tweet_links()
            
            for link in tweetLinks:
                if (helper.check_follow_limit(usersFollowedTemp, followLimit)):
                    print("Follow limit of {} reached. Will start following again in {} mins".format(followLimit, cooloffPeriod))
                    nextAllowedFollowTime = datetime.datetime.now() + datetime.timedelta(minutes=cooloffPeriod)
                    totalUsersFollowed += usersFollowedTemp
                    usersFollowedTemp = 0
                    break

                if link in processedTweets or "photo" in link:
                    continue

                print("GET ", link)
                bot.get(link)
                helper.wait_random_time()
                time.sleep(1)
                if (like_tweet()):
                    totalTweetsLiked += 1
                processedTweets.add(link)
                helper.wait_random_time()

                if datetime.datetime.now() >= nextAllowedFollowTime:
                    userProfileLink = link.split("/status/")[0]
                    if userProfileLink in processedUsers:
                        print("Skipping user {}. Already processed.".format(userProfileLink.split("twitter.com/")[1]))
                        continue

                    visit_user(userProfileLink)
                    helper.wait_random_time()

                    if (follow_user()):
                        usersFollowedTemp += 1
                    processedUsers.add(userProfileLink)
                    
                    helper.wait_random_time()

            helper.printSessionSummary(totalUsersFollowed, totalTweetsLiked)
            helper.wait_random_time()