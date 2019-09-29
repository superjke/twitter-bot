### Description
A twitter bot for liking tweets and following users with similar interests.
Twitter recently updated their HTML code which now uses dynamic class names, making it harder for bots like selenium to hook on static class names. This bot gets around this and works on the latest Twitter code (as of 29 Sept 2019).

### To use:
1. First, edit main.py with your Twitter username/password and replace the hashtags with your own.
2. Run main.py:
	> python main.py

### Additional information
Twitter has a daily follow limit per account of 400. By default, this bot is limited to 100 per day and once the limit is reached it will wait 24 hours before resuming. To change this limit, edit the followLimit variable in TwttierBot.py.
**Note: using this bot too aggressively will likely get your account suspended.**