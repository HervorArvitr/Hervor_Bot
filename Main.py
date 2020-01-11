#==========PACKAGE AND LIBRARY IMPORTS=====================================================================

import tweepy
import pandas as pd
import time
from pandas import DataFrame,set_option
from datetime import datetime

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
proceed = 1
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
                return str(e)


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
                        now = datetime.now()
                        day = now.strftime("%A %B %dth")
                        current_time = now.strftime("%I:%M:%S %p")
                        print("\nSuccessfully tweeted at " + day+" "+current_time)
                        time.sleep(time_between_tweets)
                        successful = 1

                    except Exception as e:
                        print(e)
                        successful = 1

        def Terminate(self):

            return 0


    #==========CREATING A BOT INSTANCE=========================================================================

    Session = Functionalities(api,auth,Greg_Tweets)
    authenticate = Session.Authentication()
    if (authenticate == "Authenticated"):
        print(authenticate)
    else:
        print("AUTHENTICATION ERROR CODE: "+authenticate)
        print(" \n Please verify login credentials")
        trivial_input = input("\n Press Enter key to terminate window \n >")
        proceed = Session.Terminate()
    #==========CHOOSING FUNCTIONALITY AND LOOPING==========================================================================


    while proceed==1:

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

                 subchoice = (input("\nView full tweet by row index? : \n>"))
                 if subchoice in ("yes","Yes","YES","yeah","Yeah,""YEAH","sure","Sure","SURE"):
                     subchoice_int = int(input("\nRow number: \n>"))
                     subchoice_int-=1
                     set_option('display.max_colwidth',1000)
                     print(output.iat[subchoice_int,0])
                 else:
                    print("Tweets closed")

             elif choice in ('tweet',"tweets"):
                return Session.Tweet()

             elif choice in ('timed','timed tweets','timedtweets','timed tweet','timedtweet'):
                return Session.Timed_Tweet()

             elif choice in ("Terminate","terminate","end","End","Stop","stop"):
                return Session.Terminate()

        try:
            print(Session_function_choice(choice))

        except Exception as e:
            print(e)

        cont = input("Would you like like to continue?")
        if cont not in ("y","ye","yes","Yes","YES","yeah","Yeah,""YEAH","sure","Sure","SURE"):
            #print("SURE","yes","Yes","YES","yeah","Yeah,""YEAH","sure","Sure")
            proceed = 0
