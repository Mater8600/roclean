import requests 
import time
from collections import Counter
import re
import threading
import argparse 
import codecs

#### Made by "all" ####
### Heavily inspired by Ruben sim ###

print("""

██████╗░░█████╗░░█████╗░██╗░░░░░███████╗░█████╗░███╗░░██╗
██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔════╝██╔══██╗████╗░██║
██████╔╝██║░░██║██║░░╚═╝██║░░░░░█████╗░░███████║██╔██╗██║
██╔══██╗██║░░██║██║░░██╗██║░░░░░██╔══╝░░██╔══██║██║╚████║
██║░░██║╚█████╔╝╚█████╔╝███████╗███████╗██║░░██║██║░╚███║
╚═╝░░╚═╝░╚════╝░░╚════╝░╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝
      
By mater8600
""")

##### some varibles you can change ####
### the list of "sus" words ###
list_of_common_usernames = ["bbc", "czm", "czmdump", "bunny", "bun", "fill", "sus", "doll", "Bawls",
                                "bxnny", "bull", "bxll", "luv", "bulls", "buIIs", "buII", "hearts", "Hearts",
                                "12yr", "cxm", "ass", "a33", "fap", "reps", "blow", "m1kies","lov","snow","toy",
                                  "a$$", "loli","t0y","femboy", "Femboy", "cun", "4dd", "4fun", "funtime","hardr","Ag3","mommmies",
                                  "mommies","girlsFonly", "trade", "trding", "studio", "femmie", "added", "addme", "11yrs",
                                  "clap3r", "Bull", "agepla", "D1DDY"]

list_of_common_description = [
    "trade", "rp", "💿", "studio", "dc", "roleplay" ,".-. .--.", ".-. .- .--. .", "... - ..- -.. .. ---","♠️","📸","❄️","🐇","🐂",
    "📀", "️🐰", "👻"
]


#### The lists for all of the flagged usernames ###
werdios_groups = []
werdios_groups_names = []
werdios_ids = []
reason_for_flag = []
#is_banned = []## soon
### parser args and varibles ###

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--id", help="The to use to pwn the groups")
parser.add_argument("-v", "--verbose", help="Be Verbose",action="store_true")
parser.add_argument("-p", "--pages", help="How many pages of the group you want to pwn default 100",default=100)
parser.add_argument("-o", "--output", help="If you want to ouput to a file, so that you can upload it to the terminator X groups... ", default=None)
parser.add_argument("-w", "--wordlist", help="Specifiy your own wordlist to use instead of the defaults...")
parser.add_argument("-wd", "--wordlistdesc", help="description word list you can specifiy")
args = parser.parse_args()
pages = int(args.pages)

if args.wordlist != None:
    list_of_common_usernames = []
    try:
        with open(args.wordlist, "r") as fp:
            lines = fp.readlines()
            for line in lines:
                 list_of_common_usernames.append(line)
                
    except Exception as exception:
        print("Error while reading the file!\n")
        print(exception)
        exit()

if args.wordlistdesc != None:
     list_of_common_description = []
     try:
        with codecs.open(args.wordlistdesc, "r", "utf-8") as fp:
            lines = fp.readlines()
            for line in lines:
                 list_of_common_description.append(line)
                
     except Exception as exception:
        print("Error while reading the file!\n")
        print(exception)
        exit()

def description_check(normal,werdios_ids,names_of_werdios,ids,display_names_list,userid):
    """"Checks the description of users that wasn't already flagged by the first scan."""
    
    try:
            get_userinfo= requests.get(f"https://users.roblox.com/v1/users/{userid}").json()
            description = get_userinfo["description"]
            #is_banned_user = get_userinfo["isBanned"] ## soon
            if description == "'description'":

                 if args.verbose == True:
                    print("No description to check!")
                    return 
                 
                 return
            if any(s in str(description) for s in list_of_common_description):
                if args.verbose == True:
                    print(f"\nFlagged!: {normal}\n\n")
                werdios_ids.append(userid)
                names_of_werdios.append(normal)
                reason_for_flag.append(description)
                #is_banned.append(is_banned_user) ## soon

                time.sleep(.3) ### Delay to prevent rate limiting
  
            else:
                print(f"TOTAL FLAGGED:{len(werdios_ids)} Percent:{round(len(werdios_ids)/len(display_names_list)*100)}%",flush=True, end="\r")
    except Exception as e:
            
            print(f"You are probably being rate limited rerun the tool later to help with the problem, this is usually what happens when the tools is run in multiple times in a short time.\n{e}\nsleeping for a min")
            time.sleep(60)
           

def analyzeusers(displaynames,werdios_ids,names_of_werdios,ids,display_names_list):
    """Analyzes the users by comparing the usernames with the worlist (This method is unreliable since it checks for 'normal' looking usernames)"""
    if any(s in str(displaynames) for s in list_of_common_usernames):
            werdios_ids.append(ids[display_names_list.index(displaynames)])
            names_of_werdios.append(displaynames)
            reason_for_flag.append(f"Display name is potentially bad: {displaynames}")
            if args.verbose ==True:
                print(f"flagged!:  {displaynames}")
                print(f"The total amount of possible flagged users!: {len(names_of_werdios)}")
                print(f"Amount of flagged users {len(names_of_werdios)}\n")
            else:
                print(f"Amount of flagged users by username {len(names_of_werdios)}",flush=True, end="\r")
    

   
def pager_scroller(next_page,display_names_list,ids,response):
    for entry in response['data']:
        display_names_list.append(entry['user']['displayName'])
    for entry in response['data']:
        ids.append(entry['user']['userId'])
    

def check_groups(i,werdios_groups,werdios_groups_names,werdios_ids):
    try:
        response_groups = requests.get(f"https://groups.roblox.com/v1/users/{i}/groups/roles?includeLocked=true")
        response_groups = response_groups.json()
        for entry in response_groups['data']:
                werdios_groups.append(entry['group']['id'])
                werdios_groups_names.append(entry['group']['name'])
                
                
                if args.verbose == True:
                    print(f"Amount of groups that flagged users are in: {len(werdios_groups)} these COULD be innocent!\n")
                    print(werdios_groups_names)
                    
                    
                else:
                    
                    print("Total amount of users groups flagged "+str(len(werdios_groups_names)),flush=True, end="\r")
                    
    except Exception as e:
        print(f"Uh oh!\nError\n{e}")

        


def main(id):
    get_req = requests.get(f"https://groups.roblox.com/v1/groups/{id}/users?limit=100&sortOrder=Asc")
      
    response = get_req.json()
    display_names_list = []
    ids = []
    
    for entry in response['data']:
                ids.append(entry['user']['userId'])
    for entry in response['data']:
        display_names_list.append(entry['user']['displayName'])
        
    next_page = response['nextPageCursor']
    
    
    print("We going to scroll through a few pages for the most people, and to avoid burner accounts...\nThis will take a while depending on the page value!!\n")
    for i in range(pages):
        if args.verbose == True:

            print(f"Scrolling through the pages. Next page Cursor: {next_page}",flush=True, end="\r")
            
        else:
            print(f"Scrolling through the pages! Current page: {i+1}",flush=True, end="\r")
        try:
            get_req = requests.get(f"https://groups.roblox.com/v1/groups/{id}/users?limit=100&cursor={next_page}&sortOrder=Asc")
            response = get_req.json()
            next_page = response['nextPageCursor']
            
            threading.Thread(target=pager_scroller,args=(next_page,display_names_list,ids,response,)).start()
            time.sleep(.3)
        except:
            print("\n\n")
            print("done doing the requests")
            break
    

       
    if  args.verbose == True:
        print("\nList of names:\n\n")
        print(display_names_list)  
    else:
        print("\n")
        print(f"Amount of users in the group:{len(display_names_list)}",flush=True, end="\r")
    ### Now to check the usernames for "sus" words ###
    print("\n")
    names_of_werdios = []
    for i in display_names_list:
        threading.Thread(target=analyzeusers,args=(i,werdios_ids,names_of_werdios,ids,display_names_list,)).start()
        ### Yeah, searching is fun!!! ## 
    print("\n")
    for normal, userid in zip(display_names_list,ids):
        
        if normal in names_of_werdios:
            if args.verbose == True:
                print(f"Already flagged: {normal}")
            continue
        
        description_check(normal,werdios_ids,names_of_werdios,ids,display_names_list,userid)
       
        
    print(len(werdios_ids))
    
    if args.verbose ==True:
        print("done checking everything...") 
        
        
       
    
 
    for i in werdios_ids:
           
            if len(werdios_groups) >= 100000:
                break
            else:
                check_groups(i,werdios_groups,werdios_groups_names,werdios_ids)

     
    while True:
        active_threads = threading.active_count()
        if active_threads <= 1:
        
            group_id_count = Counter(werdios_groups)             
            common = group_id_count.most_common(40)
            print("\nconverting to user and groups links for ease of use!\n")
            
            for i, c, r in zip(werdios_ids, range(1, len(werdios_ids)+1), reason_for_flag):
                print(f"{c}. https://www.roblox.com/users/{i}/profile")
                if args.output != None:
                     with codecs.open(str(args.output), "a", "utf-8") as fp:
                          
                          try:
                            fp.write(f"\nReason for flag:\n{r}\nhttps://www.roblox.com/users/{i}/profile\n\n")
                            fp.close()
                          except Exception as e:
                            print(f"looks like something was in their profile that caused an error\nError code:\n{e}")
                            fp.write(f"Reason for flag:\nError occured, please check manually\nhttps://www.roblox.com/users/{i}/profile\n\n")
                            fp.close()
                        
            print("\ncommmon groups\n")
                    
            for i, count in common:
                cleaned = re.sub(r"\(\)", '', str(i))
                print(f"https://www.roblox.com/groups/{cleaned}" + " How many are in this group: " + str(count) )


            print(f"Total amount of users in scan: {len(display_names_list)}\nPercentage flagged: {round(len(names_of_werdios)/len(display_names_list)*100)}%")
            break
                    

    
if args.id != None:
      main(args.id)
      print("Done\nPlease make sure to check the flagged users ids")
      print("Bye bye see you soon!")
      
if args.id == None:
     parser.print_help()
     print("Bye bye see you soon!")
 
    
 
    
