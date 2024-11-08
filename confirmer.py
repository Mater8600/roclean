import requests
import argparse


###THIS TOOL IS USED TO CHECK IDS THAT IS ALL! ###
### TO DO 
### ADD GROUP CHECK TO USER SEARCH
### FRIENDS CHECK

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--id", help="The id of user to specifiy (required)")


args = parser.parse_args()



# https://friends.roblox.com/v1/users/{userid}/friends

def  check_friends():
    print()

def check_user(userid):
    get_userinfo= requests.get(f"https://users.roblox.com/v1/users/{userid}").json()
    description = get_userinfo["description"]
    display_name = get_userinfo['displayName']
    created = get_userinfo["created"]
    user_name = get_userinfo["name"]
    is_banned = get_userinfo["isBanned"]
    
    print(f"\n\nUsername and displayname {user_name} and {display_name}\nuserid:{userid}\nDescription:\n{description}\nCreated:{created}\nTerminated:{is_banned}\n")

if args.id != None:
    check_user(args.id)
else:
    print("No arguments given...")
    parser.print_help()
