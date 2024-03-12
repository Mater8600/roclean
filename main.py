import json
import requests 
import time
#### Made by "all" ####
### Heavily inspired by Ruben sim ###

print("""
█▀█ █▀▀ █▀▄ █▀█ █▀▀ █ █▄░█ █▀▄ █▀▀ █▀█
█▀▀ ██▄ █▄▀ █▄█ █▀░ █ █░▀█ █▄▀ ██▄ █▀▄
""")
print("""
█▄▄ █▄█   ▄▀█ █░░ █░░
█▄█ ░█░   █▀█ █▄▄ █▄▄
""")

def main(id):
    get_req = requests.get(f"https://groups.roblox.com/v1/groups/{id}/users?limit=100&sortOrder=Asc")
    print(get_req.json())
    
            
    response = get_req.json()
    
    display_names_list = []
    ids = []
    for entry in response['data']:
                ids.append(entry['user']['userId'])
    for entry in response['data']:
        display_names_list.append(entry['user']['displayName'])
        
    next_page = response['nextPageCursor']
    
    print(next_page)
    print("We going to scroll through a few pages for the most people, and to avoid burner acconnts...")
    for i in range(10):
        try:
            
            get_req = requests.get(f"https://groups.roblox.com/v1/groups/{id}/users?limit=100&cursor={next_page}&sortOrder=Asc")
            
            response = get_req.json()
            for entry in response['data']:
                display_names_list.append(entry['user']['displayName'])
            for entry in response['data']:
                ids.append(entry['user']['userId'])
            next_page = response['nextPageCursor']
            print(next_page)
        except:
            print("no such page exists, going forward without any extra :(")
        time.sleep(2)
            

    print("\nList of names:\n\n")
    print(display_names_list)
    
    ### Now to check the usernames for "sus" words ###
    
    werdios = []
    names_of_werdios = []
    for i in display_names_list:
        
        
        if "bbc" in str(i) or "czm" in str(i) or "czmdump" in str(i) or "bunny" in str(i) or "bun" in str(i)  or "fill" in str(i)  or "sus" in str(i) or "doll" in str(i) or "love" in str(i) or "bxnny" in str(i):
            print("found a werid username INVESTIGATE BEFORE REPORTING THESE ACCOUNTS!!!")
            werdios.append(ids[display_names_list.index(i)])
            names_of_werdios.append(i)
            print("werdios:\n")
            print(names_of_werdios)
            print("full list (ids):\n")
            print(werdios)
            
             

if __name__ == "__main__":
    id = input("Enter the id: ")
  
        
    main(id)
        
       
    print("Done")
 
    
