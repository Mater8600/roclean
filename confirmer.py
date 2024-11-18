import requests
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--id", help="The id of user to specifiy (required)")
parser.add_argument("-o", "--output",help="Writes all data to a file for ease of use, the filename will be the id of the target", action="store_true")
parser.add_argument("-w", "--wordlist", help="Outputs the info into a display name wordlist, good for pairing with roclean! Just make sure to put your filename in!")
args = parser.parse_args()

ids = []



def check_friends(userid):
    if args.output == True:
          try:
            with open(str(userid), "a") as fp:
                fp.write("\nFRIENDS INVOLVED WITH THIS USER!\n\n\n")
                fp.close()
          except Exception as exception:
               print("Had an error opening the file")
               print(exception)
    print(f"Friends usernames+ display names and ids\n")
    get_friends_info = requests.get(f"https://friends.roblox.com/v1/users/{userid}/friends").json()
    
    for entry in get_friends_info['data']:
                ids.append(entry['id'])
    for friends_id  in ids:
        get_userinfo= requests.get(f"https://users.roblox.com/v1/users/{friends_id}").json()
        display_name = get_userinfo['displayName']
    
        user_name = get_userinfo["name"]
        is_banned = get_userinfo["isBanned"]
        print(f"Display name: {display_name}\nUsername: {user_name}\nIs banned: {is_banned}\nUserid: {friends_id}\n")
        if args.wordlist != None:
             try:
                  with open(str(args.wordlist),"a" ) as fp:
                       fp.write(f"{display_name}\n")
                       fp.close()
             except Exception as exception:
                  print("Something went wrong when trying to open the file")
                  print(exception)
        if args.output == True:
             try:
                  with open(str(userid),"a" ) as fp:
                       fp.write(f"Display name: {display_name}\nUsername: {user_name}\nIs banned: {is_banned}\nUserid: {friends_id}\n\n")
                       fp.close()
             except Exception as exception:
                  print("Something went wrong when trying to open the file")
                  print(exception)

def check_user(userid):
    get_userinfo= requests.get(f"https://users.roblox.com/v1/users/{userid}").json()
    description = get_userinfo["description"]
    display_name = get_userinfo['displayName']
    created = get_userinfo["created"]
    user_name = get_userinfo["name"]
    is_banned = get_userinfo["isBanned"]
    
    print(f"\n\nUsername and displayname {user_name} and {display_name}\nuserid:{userid}\nDescription:\n{description}\nCreated:{created}\nTerminated:{is_banned}\n")
    if args.output == True:
             try:
                  with open(str(userid),"a" ) as fp:
                       fp.write(f"Username and displayname {user_name} and {display_name}\nuserid:{userid}\nDescription:\n{description}\nCreated:{created}\nTerminated:{is_banned}\n\n\n")
                       fp.close()
             except Exception as exception:
                  print("Something went wrong when trying to open the file")
                  print(exception)
    if args.wordlist != None:
             try:
                  with open(str(args.wordlist),"a" ) as fp:
                       fp.write(f"{display_name}\n")
                       fp.close()
             except Exception as exception:
                  print("Something went wrong when trying to open the file")
                  print(exception)
if args.id != None:
    check_user(args.id)
    check_friends(args.id)

else:
    print("No arguments given...")
    parser.print_help()
