import requests 
import time
from collections import Counter
import re
import threading
#### Made by "all" ####
### Heavily inspired by Ruben sim ###



##### some varibles you can change ####

### pages is how many pages the tool will search through default = 100 ###

### this number can vary, if you want a full group scan just do 1000, but it will take forever
pages = 1000


### the list of "sus" words ###
list_of_common_usernames = ["bbc", "czm", "czmdump", "bunny", "bun", "fill", "sus", "doll", "Bawls",
                            "bxnny", "bull", "bxll", "luv", "bulls", "buIIs", "buII", "hearts", "Hearts",
                             "12yr", "cxm", "ass", "a33", "fap", "reps"]

print("""
█▀█ █▀█ █▀▀ █░░ ▄▀█ █▀▀ █▀▀ █▀▀ █▀█
█▀▄ █▄█ █▀░ █▄▄ █▀█ █▄█ █▄█ ██▄ █▀▄
""")
print("""
█▄▄ █▄█   ▄▀█ █░░ █░░
█▄█ ░█░   █▀█ █▄▄ █▄▄
""")

def pager_scroller(next_page,display_names_list,ids,response):
    
    
    print("Scrolling thru the pages")
    
    print(next_page)
    
    for entry in response['data']:
        display_names_list.append(entry['user']['displayName'])
    for entry in response['data']:
        ids.append(entry['user']['userId'])
            
                
            
    
            

    

def analyzeusers(i,werdios,names_of_werdios,ids,display_names_list):
    
    if any(s in str(i) for s in list_of_common_usernames):
            print("found a werid display username INVESTIGATE BEFORE REPORTING THESE ACCOUNTS!!!")
            werdios.append(ids[display_names_list.index(i)])
            names_of_werdios.append(i)
            print("werdios:\n")
            print(names_of_werdios)
            print("full list (ids):\n")
            print(werdios)


def check_groups(i,werdios_groups,werdios_groups_names,werdios_ids,werdios):
    try:
        response_groups = requests.get(f"https://groups.roblox.com/v1/users/{i}/groups/roles?includeLocked=true")
        response_groups = response_groups.json()
        for entry in response_groups['data']:
                werdios_groups.append(entry['group']['id'])
                werdios_groups_names.append(entry['group']['name'])
                werdios_ids.append(i)
                    
                print("werdios groups:\n")
                print(werdios_groups_names)
                print("werdios group ids")
                print(werdios_groups)
    except:
        print("Uh oh!")

            

def main(id):
    get_req = requests.get(f"https://groups.roblox.com/v1/groups/{id}/users?limit=100&sortOrder=Asc")
    print(get_req.json())    
    response = get_req.json()
    display_names_list = []
    ids = []
    usernames = []
    for entry in response['data']:
                ids.append(entry['user']['userId'])
    for entry in response['data']:
        display_names_list.append(entry['user']['displayName'])
        
    next_page = response['nextPageCursor']
    
    print(next_page)
    print("We going to scroll through a few pages for the most people, and to avoid burner accounts...\nThis will take a while depending on the page value!!")
    for i in range(pages):
        print(f"Page: {i}")
        try:
            get_req = requests.get(f"https://groups.roblox.com/v1/groups/{id}/users?limit=100&cursor={next_page}&sortOrder=Asc")
            response = get_req.json()
            next_page = response['nextPageCursor']
            
            threading.Thread(target=pager_scroller,args=(next_page,display_names_list,ids,response,)).start()
        except:
            print("done doing the requests")
            break
    
        

        
       

    print("\nList of names:\n\n")
    print(display_names_list)  
    ### Now to check the usernames for "sus" words ###
    werdios = []
    names_of_werdios = []
    for i in display_names_list:
        threading.Thread(target=analyzeusers,args=(i,werdios,names_of_werdios,ids,display_names_list,)).start()
        ### Yeah, searching is fun!!! ## 
        
        
       
    print("this will take some time!")
    werdios_groups = []
    werdios_groups_names = []
    werdios_ids = []
    for i in werdios:
            
            threading.Thread(target=check_groups,args=(i,werdios_groups,werdios_groups_names,werdios_ids,werdios,)).start()
            
    
    while True:
        active_threads = threading.active_count()
        if active_threads <= 1:
            print("\nthreads ded")
        
            
            group_id_count = Counter(werdios_groups)
                    
            print("\n\n\nGroup counts\n")
            print(group_id_count)
                        
            print("Comparing rn...")
                        
                    
                        
            print("Gottem, found these groups!\nIgnore the small numbers!\n")
            common = group_id_count.most_common(40)
            print(common)
            print("\nwerdios:\n")
            print(werdios)
                    
            print("\n\n\n\n\n\nconverting to userlinks for ease of use!\n")
                    
            for i in werdios:
                print(f"https://www.roblox.com/users/{i}/profile")
                        
            print("\ncommmon groups\n")
                    
            for i, count in common:
                cleaned = re.sub(r"\(\)", '', str(i))
                print(f"https://www.roblox.com/groups/{cleaned}" + " How many are in this group: " + str(count) )
            

            break
                    
          
    

if __name__ == "__main__":
    url = input("Enter the id: ")  
    main(url)
    print("Done\nPlease make sure to check the flagged users ids")
 
    
 
    
