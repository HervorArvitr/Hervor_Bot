#==========PACKAGE AND LIBRARY IMPORTS=====================================================================

import tweepy
import pandas as pd
import time
from pandas import DataFrame,set_option

set_option('display.max_colwidth',100)
pd.set_option('display.expand_frame_repr', True)


#==========FILE AND CLASS IMPORTS==========================================================================

from Config import Consumer_API_Keys
from Config import Access_Tokens
from tweets import Tweets

Greg = Tweets()
Greg_Tweets = Greg.get_content()

API_Key = Consumer_API_Keys.API_Key
API_Secret_Key = Consumer_API_Keys.API_Secret_Key

Access_Token = Access_Tokens.Access_Token
Access_Token_Secret = Access_Tokens.Access_Token_Secret

auth = tweepy.OAuthHandler(API_Key,API_Secret_Key)
auth.set_access_token(Access_Token,Access_Token_Secret)

api = tweepy.API(auth,wait_on_rate_limit = True,
wait_on_rate_limit_notify = True)

opinion = 0
if opinion == 0:
#==========DEFINING BOT FUNTIONALITIES=====================================================================

    class Functionalities:
        def __init__(self, api, auth, Greg_Tweets):
            self.api = api
            self.auth = auth
            self.Greg_Tweets = Greg_Tweets

        def Authentication(self):
            try:
                self.api.verify_credentials()
                return "Authenticated"
            except Exception as e:
                print(e)

        def Choice(self):
            choice = input("Please select a functionality to access: \n>")
            choice = choice.lower()
            return choice

        def Tweet(self):
            tweet = input("\nTweet String: \n>")
            try:
                self.api.update_status(tweet)
                return "\nTweeted Successfully"
            except Exception as e:
                print(e)

        def Get_User_Details(self):
            user = input("\nInput user to fetch details about: \n>")
            account_details = {}

            try:
                user_details = self.api.get_user(user)

                name = user_details.name
                description = user_details.description
                location = user_details.location

                account_details = {"Name ":name,"Description":description,"Location":location}

                account_details_df = DataFrame.from_dict(account_details,orient = 'index', columns = ['Details'])

                return account_details_df

                print("\nFetched Successfully")

            except Exception as e:
                return e

        def Get_recent_tweets(self):
                timeline = api.home_timeline(tweet_mode='extended')
                recent_tweets = {}

                try:
                    for tweet in timeline:
                        recent_tweets.update({tweet.user.name:tweet.full_text})

                    recent_tweets_df = DataFrame.from_dict(recent_tweets,orient = 'index',columns = ['Tweet'])

                    return recent_tweets_df

                    print("\nFetched Successfully")

                except Exception as e:
                    return e

        def Timed_Tweet(self):
            correct_input = 1
            time_between_tweets = input("Time between tweets: \n>")

            while correct_input == 1:
                try:
                    time_between_tweets = int(time_between_tweets)
                    correct_input = 0
                except ValueError:
                    time_between_tweets = input("Please input a number:")

            for tweet in Greg_Tweets:
                successful = 0
                tweet_string = ("@onision "+tweet)
                while successful == 0:
                    try:
                        time.sleep(2)
                        self.api.update_status(tweet_string)
                        print("\n000")
                        successful = 1
                        time.sleep(time_between_tweets)

                    except Exception as e:
                        print(e)

        def Terminate(self):

            return '000'


    #==========CREATING A BOT INSTANCE=========================================================================

    Session = Functionalities(api,auth,Greg_Tweets)

    print(Session.Authentication())

    #==========CHOOSING FUNCTIONALITY==========================================================================

    print("\n-Tweet \n-Search Users \n-Recent Tweets \n-Timed Tweets \n-Terminate \n")

    choice = Session.Choice()
    choice = choice.lower()

    #==========DEFINING FUNCTIONALITY CLAUSES==================================================================

    def Session_function_choice(choice):

         if choice in ('search user','user search','search users','users search'):
              return Session.Get_User_Details()

         elif choice in ('recent tweets','recents tweets'):
             output = Session.Get_recent_tweets()
             print(output)
             subchoice = int(input("\nView full tweet by row index: \n>"))
             subchoice-=1
             set_option('display.max_colwidth',1000)
             print(output.iat[subchoice,0])

         elif choice in ('tweet',"tweets"):
            return Session.Tweet()

         elif choice in ('timed tweets','timedtweets','timed tweet','timedtweet'):
            return Session.Timed_Tweet()

         elif choice in ("Terminate","terminate","end","End","Stop","stop"):
            return Session.Terminate()

    try:
        print(Session_function_choice(choice))

    except Exception as e:
        print(e)

    cont = input("Would you like like to continue?")
    if cont in ("yes","Yes","YES","yeah","Yeah,""YEAH","sure","Sure","SURE"):
        print("SURE","yes","Yes","YES","yeah","Yeah,""YEAH","sure","Sure")
