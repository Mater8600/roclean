import requests 
import time
from collections import Counter
import argparse
import codecs
import threading
import re
import random


### THIS VERSION OF ROCLEAN IS A REWRITE OF THE ENTIRE SCRIPT. ###
### THIS VERSION IS MORE EFFICIENT AND HAS A LOT MORE FEATURES. ###
print("""
█▀█ █▀█ █▀▀ █░░ █▀▀ ▄▀█ █▄░█
█▀▄ █▄█ █▄▄ █▄▄ ██▄ █▀█ █░▀█
      
ᵇʸ ᵐᵃᵗᵉʳ⁸⁶⁰⁰
""")
### argument parser stuff ###
parser = argparse.ArgumentParser(description="A tool that allows you to find suspious accounts in Roblox groups.")
parser.add_argument("-i", "--id", help="The id of the group to target")
parser.add_argument("-r", "--recursion", help="Continues the scan on the next groups. Set page amount to 0", action="store_true")
parser.add_argument("-v", "--verbose", help="Be Verbose",action="store_true")
parser.add_argument("-p", "--pages", help="The amount of pages to scan default 10",default=10)
parser.add_argument("-o", "--output", help="Output all found users to a file")
parser.add_argument("--animations", help="Adds useless and time consuming animations to the text for fun.", action="store_true")
parser.add_argument("-w", "--wordlist", help="Specifiy your own wordlist to use instead of the defaults...")
parser.add_argument("-wd", "--wordlistdesc", help="description word list you can specifiy")
args = parser.parse_args()


### Lists for processing ###
displaynames_involved_in_group = []
descriptions_involved_in_group =[]
userids_involved_in_group = []



### Flagged accounts ###

flagged_accounts_id = []
flagged_friends_id = []
flagged_friends_displayname = []
friends_reason = []
friends_is_banned = []
flagged_friends_description = []
flagged_accounts_displayname = []
flagged_accounts_description = []
reason_for_flag = []
flagged_accounts_groups= []
flagged_accounts_groups_name = []
is_banned = []

### Bad user/display names lists ###

### These are actually from a ton of flagged accounts that ha werid descriptions ###
### Unfortunately these are highly common in the Roblox community. ###
description_check_list = [ "trade", "rp", "💿", "studio", "dc", "roleplay" ,".-. .--.", ".-. .- .--. .", "... - ..- -.. .. ---","♠️","📸","❄️","🐇","🐂",
    "📀", "️🐰", "👻", " .- -.. -.. / -- . / ..-. --- .-. / -- --- .-. . / .. -. ..-. --- -.-.--"]


### These are actually from a ton of different groups that I have seen in the past. ###
### These are the most common ones that I have seen. ###
### If you have any suggestions for more please let me know! ###
usernames_displaynames_list = ["bbc", "czm", "czmdump", "bunny", "bun", "fill", "sus", "doll", "Bawls",
                                "bxnny", "bull", "bxll", "luv", "bulls", "buIIs", "buII", "hearts", "Hearts",
                                "12yr", "cxm", "ass", "a33", "fap", "reps", "blow", "m1kies","lov","snow","toy",
                                  "a$$", "loli","t0y","femboy", "Femboy", "cun", "4dd", "4fun", "funtime","hardr","Ag3","mommmies",
                                  "mommies","girlsFonly", "trade", "trding", "studio", "femmie", "added", "addme", "11yrs",
                                  "clap3r", "Bull", "agepla", "D1DDY", " gettinREALLLLsilly", "shotah", "Shotah", "spade", "goon", "P0unding",
                                  "checkbio", "CheckBio", "Checkbio", "checkBio", "fmboy", "fre4k", "Littlekid"]
### Wordlist for the usernames ###
if args.wordlist != None:
    usernames_displaynames_list = []
    try:
        with open(args.wordlist, "r") as fp:
            lines = fp.readlines()
            
            for line in lines:
                 usernames_displaynames_list.append(line)
                
    except Exception as exception:
        print("Error while reading the file!\n")
        print(exception)
        exit()
### Wordlist for the descriptions ###
if args.wordlistdesc != None:
     description_check_list = []
     try:
        with codecs.open(args.wordlistdesc, "r", "utf-8") as fp:
            lines = fp.readlines()
            for line in lines:
                 description_check_list.append(line)
                
     except Exception as exception:
        print("Error while reading the file!\n")
        print(exception)
        exit()
def pager_scroller(userids_involved_in_group,response):
    """Processes the data collected by the group scrapper, and adds all of the users to the user id section"""
    for entry in response['data']:
        userids_involved_in_group.append(entry['user']['userId'])
 
def page_getter(pages,groupid):
    """Like Roclean's old scanner just no display names are gather because the names are going to get gathered later..."""
    print(f"Scrolling through the many pages of the group... TODO: {pages}", flush=True,end="\r")
    print("\n")
    get_req = requests.get(f"https://groups.roblox.com/v1/groups/{groupid}/users?limit=100&sortOrder=Asc")
    response = get_req.json()
    for entry in response['data']:
                userids_involved_in_group.append(entry['user']['userId'])  
    next_page = response['nextPageCursor']
    for i in range(pages):
        if args.verbose == True:
            print(f"Scrolling through the pages. Next page Cursor: {next_page}",flush=True, end="\r")
        else:
            print(f"Scrolling through the pages! Current page: {i+1}",flush=True, end="\r")
        try:
            get_req = requests.get(f"https://groups.roblox.com/v1/groups/{groupid}/users?limit=100&cursor={next_page}&sortOrder=Asc")
            response = get_req.json()
            next_page = response['nextPageCursor']
            
            threading.Thread(target=pager_scroller,args=(userids_involved_in_group,response,)).start()
            time.sleep(.3)
        except:
            print("\n")
            break
def animate_text(flagged_accounts_id,cycles,stop_event):
    for _ in range(cycles):  
        if stop_event.is_set():
             return 
        frames = ["Current flagged", "cUrrent flagged", "cuRrent flagged", "curRent flagged", "currEnt flagged", "curreNt flagged", "currenT flagged", "current Flagged"
                  , "current fLagged", "current flAgged", "current flaGged", "current flagGed", "current flaggEd", "current flaggeD"]
        for i in range(len(frames)):
            print(f"{frames[i]}: {len(flagged_accounts_id)}",flush=True,end="\r")
            
            
            time.sleep(0.2)
            
            
def get_all_users(userid):
    """Scan all of the group members manually flagging each one..."""
    get_userinfo= requests.get(f"https://users.roblox.com/v1/users/{userid}").json()
    try:
        description = get_userinfo["description"]
        display_name = get_userinfo['displayName']
        banned = get_userinfo["isBanned"]
            
        if args.animations == False:
             print(f"Current flagged: {len(flagged_accounts_id)}", flush=True, end="\r")
        
        
        if any(s in str(display_name) for s in usernames_displaynames_list):
            flagged_accounts_id.append(userid)
            flagged_accounts_displayname.append(display_name)
            flagged_accounts_description.append(description)
            is_banned.append(banned)
            reason_for_flag.append(f"This account has a suspious username")
            rate_limited = False
            return rate_limited
        if any(s in str(description) for s in description_check_list):
            flagged_accounts_id.append(userid)
            flagged_accounts_displayname.append(display_name)
            flagged_accounts_description.append(description)
            is_banned.append(banned)
            reason_for_flag.append(f"This account has a suspious description")
            rate_limited = False
            return rate_limited
        else:
            rate_limited = False
            return rate_limited
    
    except:
        
        time.sleep(45)
        rate_limited = True
        return rate_limited
def check_friends(userid):
     """Adds the users friends to the flagged list"""
     try:
        response = requests.get(f"https://friends.roblox.com/v1/users/{userid}/friends")
        response = response.json()
        for entry in response['data']:
            flagged_friends_id.append(entry['id'])
            flagged_friends_displayname.append(entry['displayName'])
            get_description = requests.get(f"https://users.roblox.com/v1/users/{entry['id']}").json()
            flagged_friends_description.append(get_description['description'])
            friends_reason.append(f"This account is friends with a flagged user {userid}")
            friends_is_banned.append(get_description['isBanned'])
            print("Total amount of users friends added:"+str(len(flagged_friends_displayname)),flush=True, end="\r")
            return False
     except Exception as e:
        if args.verbose == True:
             
            print(f"You are being rate limited!\n{e} Slowing down the scan for 45 seconds")
            time.sleep(30)
            print("Retrying")
            return True
        else:
            time.sleep(30)
        
            return True
     
     
def check_groups(userid):
    """Scrolls through all of the flagged users groups."""
    try:
        response_groups = requests.get(f"https://groups.roblox.com/v1/users/{userid}/groups/roles?includeLocked=true")
        response_groups = response_groups.json()
        for entry in response_groups['data']:
                flagged_accounts_groups.append(entry['group']['id'])
                flagged_accounts_groups_name.append(entry['group']['name'])
                
                
                if args.verbose == True:
                    print(f"Amount of groups that flagged users are in: {len(flagged_accounts_groups)} these COULD be innocent!\n")
                    print(flagged_accounts_groups_name)
                    return False

                    
                    
                else:
                    
                    print("Total amount of users groups flagged "+str(len(flagged_accounts_groups_name)),flush=True, end="\r")
                    return False
                    
    except Exception as e:
        print(f"Uh oh!\nError\n{e}")
        return True
    
def main(groupid):
    """Main function"""
    print(f"Running a scan against: {groupid}. Report any finds to proper authorites.\n\n")
    page_getter(pages=int(args.pages), groupid=groupid)
    print("")
    stop_event = threading.Event()
    cycles = len(userids_involved_in_group)
    animation_thread = threading.Thread(target=animate_text, args=(flagged_accounts_id,cycles, stop_event,))
    animation_thread.daemon = True
    if args.animations == True:
        animation_thread.start()
    for users in userids_involved_in_group:
        get_all_users(users)
    print("") 
    stop_event.set()
     
    for users in flagged_accounts_id:
          rated = check_groups(users)
          if rated == True:
               rated = check_groups(users)
               if rated == True:
                    rated = check_groups(users)
          else:
               continue
    ### check the friends of the flagged users ###
    print("\nChecking the friends of the flagged users\n")
    for users in flagged_accounts_id:

        ratlimited_friends = check_friends(users)
        if ratlimited_friends == True:
            ratlimited_friends = check_friends(users)
            if ratlimited_friends == True:
                ratlimited_friends = check_friends(users)
        else:
            continue

               
         

    group_id_count = Counter(flagged_accounts_groups)             
    common = group_id_count.most_common(40)
    common_group_names_count = Counter(flagged_accounts_groups_name)
    common_group_names = common_group_names_count.most_common(40)
    print("\nDone flagged users:\n")
    
    for i, c, r, username, description, banned in zip(flagged_accounts_id, range(1, len(flagged_accounts_id)+1), reason_for_flag, flagged_accounts_displayname, flagged_accounts_description,is_banned):
            print(f"{c}. https://www.roblox.com/users/{i}/profile")
            if args.output != None:
                with codecs.open(args.output, "a", "utf-8") as fp:
                    fp.write(f"\nUsername:{username}\nDescription:\n{description}\nis_banned:{banned}\nReason:{r}\nurl: https://www.roblox.com/users/{i}/profile\n")
                    fp.close()
    print("\nflagged friends:\n")
    for i, c, r, username, description, banned in zip(flagged_friends_id, range(1, len(flagged_friends_id)+1), friends_reason, flagged_friends_displayname, flagged_friends_description,friends_is_banned):
            print(f"{c}. https://www.roblox.com/users/{i}/profile")
            if args.output != None:
                with codecs.open(args.output, "a", "utf-8") as fp:
                    fp.write(f"\nUsername:{username}\nDescription:\n{description}\nis_banned:{banned}\nReason:{r}\nurl: https://www.roblox.com/users/{i}/profile\n")
                    fp.close()
    print("All of the groups the flagged users are in\n")
    for (i ,count), (name, number) in zip(common, common_group_names):
                cleaned_group = re.sub(r"\(\)", '', str(i))
                print(f"Group name: {name} https://www.roblox.com/groups/{cleaned_group}" + " How many are in this group: " + str(count) )
                if args.output != None:
                    with codecs.open(args.output, "a", "utf-8") as fp:
                        fp.write(f"\nGroup name: {name} https://www.roblox.com/groups/{cleaned_group}" + " How many are in this group: " + str(count) + "\n" )



    print(f"\nTotal amount of users in scan: {len(userids_involved_in_group)}\nPercentage flagged: {round(len(flagged_accounts_id)/len(userids_involved_in_group)*100)}%")
    if args.recursion == True:
        return common
    else:
        exit()
    


if args.id != None and args.pages != None and args.recursion == False:
    main(groupid=args.id)


if args.id != None and args.recursion == True and args.pages != None:
    print(f"RECUSION MODE ENABLED!!!!\n\nThis will scan the next group in the list indefinitly!\n\n")
    common = main(groupid=args.id)
    done_groups = []
    print(common)
    while True:
         ### Lists for processing ###
        displaynames_involved_in_group = []
        descriptions_involved_in_group =[]
        userids_involved_in_group = []


### Flagged accounts ###

        flagged_accounts_id = []
        flagged_accounts_displayname = []
        flagged_accounts_description = []
        reason_for_flag = []
        flagged_accounts_groups= []
        flagged_accounts_groups_name = []
        is_banned = []

        next_group = common[0][1]
        if next_group in done_groups:
            print("this group has already been scanned")
            next_group = random.choice(common)[1]
                

            print(f"Next group to scan: {next_group}")
            next_group = main(groupid=next_group)
        
     
         
else:
     parser.print_help()
     exit()
