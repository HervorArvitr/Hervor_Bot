file = open("config.txt","r")
bot_keys = {}

for line in file:
    pair = line.split(':')
    pair_key = pair[0]
    pair_value = pair[1].rstrip()
    bot_keys[pair_key] = pair_value



class Consumer_API_Keys:
    API_Key =  bot_keys["API_Key"]
    API_Secret_Key = bot_keys["API_Secret_Key"]

class Access_Tokens:
    Access_Token =  bot_keys["Access_Token"]
    Access_Token_Secret =  bot_keys["Access_Token_Secret"]
