class Tweets:
    def __init__(self):
        with open("Tweets\\greg_tweets.txt",'r') as file:
            data = file.readlines()
        self.content = [x.rstrip('\n') for x in data]

    def get_content(self):
        available_tweets = self.content
        return available_tweets
