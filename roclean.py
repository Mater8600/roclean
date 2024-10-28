import requests 
import time
from collections import Counter
import re
import threading
import argparse 

#### Made by "all" ####
### Heavily inspired by Ruben sim ###

##### some varibles you can change ####


### the list of "sus" words ###
list_of_common_usernames = ["bbc", "czm", "czmdump", "bunny", "bun", "fill", "sus", "doll", "Bawls",
                                "bxnny", "bull", "bxll", "luv", "bulls", "buIIs", "buII", "hearts", "Hearts",
                                "12yr", "cxm", "ass", "a33", "fap", "reps", "blow", "m1kies","lov","snow","toy",
                                  "a$$", "loli","t0y","femboy", "Femboy", "cun", "4dd", "4fun", "funtime","hardr","Ag3","mommmies",
                                  "mommies","girlsFonly", "Roblox"]



werdios_groups = []
werdios_groups_names = []
werdios_ids = []

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--id", help="The to use to pwn the groups")
parser.add_argument("-v", "--verbose", help="Be Verbose")
parser.add_argument("-p", "--pages", help="How many pages of the group you want to pwn default 100",default=100)

args = parser.parse_args()
pages = int(args.pages)

print("""
█▀█ █▀█ █▀▀ █░░ █▀▀ ▄▀█ █▄░█
█▀▄ █▄█ █▄▄ █▄▄ ██▄ █▀█ █░▀█
""")

print("""
█▄▄ █▄█   ▄▀█ █░░ █░░
█▄█ ░█░   █▀█ █▄▄ █▄▄
""")

def pager_scroller(next_page,display_names_list,ids,response):
    

    for entry in response['data']:
        display_names_list.append(entry['user']['displayName'])
    for entry in response['data']:
        ids.append(entry['user']['userId'])
            

def analyzeusers(i,werdios,names_of_werdios,ids,display_names_list):
    
    if any(s in str(i) for s in list_of_common_usernames):
            
            werdios.append(ids[display_names_list.index(i)])
            names_of_werdios.append(i)
            if args.verbose != None:
                print("werdios:\n")
                print(names_of_werdios)
                print("full list (ids):\n")
                print(werdios)
                print(f"Amount of flagged users {len(names_of_werdios)}\n")

            print(f"Amount of flagged users {len(names_of_werdios)}\n")
def check_groups(i,werdios_groups,werdios_groups_names,werdios_ids,werdios):
    try:
        response_groups = requests.get(f"https://groups.roblox.com/v1/users/{i}/groups/roles?includeLocked=true")
        response_groups = response_groups.json()
        for entry in response_groups['data']:
                werdios_groups.append(entry['group']['id'])
                werdios_groups_names.append(entry['group']['name'])
                werdios_ids.append(i)
                
                if args.verbose != None:
                    print("werdios groups:\n")
                    print(werdios_groups_names)
                    print("werdios group ids")
                    print(werdios_groups)
                else:
                    
                    print("Total amount of users groups flagged "+str(len(werdios_groups_names)))
                    
    except:
        print("Uh oh!")

            

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
    
    
    print("We going to scroll through a few pages for the most people, and to avoid burner accounts...\nThis will take a while depending on the page value!!")
    for i in range(pages+1):
        if args.verbose != None:

            print(f"Scrolling through the pages. Next page Cursor: {next_page}")
            
        else:
            print(f"Scrolling through the pages! Current page: {i}")
        try:
            get_req = requests.get(f"https://groups.roblox.com/v1/groups/{id}/users?limit=100&cursor={next_page}&sortOrder=Asc")
            response = get_req.json()
            next_page = response['nextPageCursor']
            
            threading.Thread(target=pager_scroller,args=(next_page,display_names_list,ids,response,)).start()
        except:
            print("done doing the requests")
            break
    

       
    if  args.verbose != None:
        print("\nList of names:\n\n")
        print(display_names_list)  
    else:
        print(f"Amount of users in the group:{len(display_names_list)}")
    ### Now to check the usernames for "sus" words ###
    werdios = []
    names_of_werdios = []
    for i in display_names_list:
        threading.Thread(target=analyzeusers,args=(i,werdios,names_of_werdios,ids,display_names_list,)).start()
        ### Yeah, searching is fun!!! ## 
        
        
       
    print("this will take some time!")
 
    for i in werdios:
            #threading.Thread(target=check_groups,args=(i,werdios_groups,werdios_groups_names,werdios_ids,werdios,)).start()
            check_groups(i,werdios_groups,werdios_groups_names,werdios_ids,werdios)
            
    
    while True:
        active_threads = threading.active_count()
        if active_threads <= 1:
        
            group_id_count = Counter(werdios_groups)             
            common = group_id_count.most_common(40)
            print("\n\n\n\n\n\nconverting to user and groups links for ease of use!\n")
            
            for i, c in zip(werdios, range(1, len(werdios)+1)):
                print(f"{c}. https://www.roblox.com/users/{i}/profile")
                        
            print("\ncommmon groups\n")
                    
            for i, count in common:
                cleaned = re.sub(r"\(\)", '', str(i))
                print(f"https://www.roblox.com/groups/{cleaned}" + " How many are in this group: " + str(count) )
          
            break
                    

    
if args.id != None:
      main(args.id)
      print("Done\nPlease make sure to check the flagged users ids")
      print("Bye bye see you soon!")
else:
     parser.print_help()
     print("Bye bye see you soon!")
 
    
 
    
