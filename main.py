import tkinter as tk
import re
import requests 
import time
from collections import Counter
import re
import threading


list_of_common_usernames = ["bbc", "czm", "czmdump", "bunny", "bun", "fill", "sus", "doll", "Bawls",
                                "bxnny", "bull", "bxll", "luv", "bulls", "buIIs", "buII", "hearts", "Hearts",
                                "12yr", "cxm", "ass", "a33", "fap", "reps", "blow", "m1kies","lov","snow","toy", "a$$"]

def scan_bad_group(finished_lbl,id,pgs,information,information_groups):
    
    print("scanning...")
    
    
    pages = int(pgs)


    
    def pager_scroller(next_page,display_names_list,ids,response,information):
        
        
        
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
        information.set(f"Currently scanning page: {i}")
        try:
            get_req = requests.get(f"https://groups.roblox.com/v1/groups/{id}/users?limit=100&cursor={next_page}&sortOrder=Asc")
            response = get_req.json()
            next_page = response['nextPageCursor']
                
            threading.Thread(target=pager_scroller,args=(next_page,display_names_list,ids,response,information,)).start()
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
        information.set(f"Analyzing the usernames on current username {i}")    
            
            
        
    print("this will take some time!")
    werdios_groups = []
    werdios_groups_names = []
    werdios_ids = []

    for i in werdios:
            information.set(f"Analyzing the groups of flagged users {i}")  
            threading.Thread(target=check_groups,args=(i,werdios_groups,werdios_groups_names,werdios_ids,werdios,)).start()
                
        
    while True:
        active_threads = threading.active_count()
        if active_threads <= 2:
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
            def get_current_time_12h():
                """Returns the current time in 12 hour format."""

                
                datetime_obj = time.localtime()

                
                datetime_obj = time.strftime("%H:%M:%S", datetime_obj)

                
                if int(datetime_obj[:2]) >= 12:
                    
                    hour = int(datetime_obj[:2]) - 12
                    am_pm = "PM"
                else:
                    hour = int(datetime_obj[:2])
                    am_pm = "AM"

                
                time_12h = f"{hour:02d}:{datetime_obj[3:5]} {am_pm}"

                return time_12h

               
                        
            list_of_accounts = []
            
            
            for i in werdios:
                    print(f"https://www.roblox.com/users/{i}/profile")
                    display_name = requests.get(f"https://users.roblox.com/v1/users/{i}")
                    json_dis = display_name.json()
                    name = json_dis['displayName']
                    user_link = name + ":https://www.roblox.com/users/" + str(i) + "/profile"
                    list_of_accounts.append(user_link)
                    
            information.set(f"Flagged accounts:\n{str(list_of_accounts)}\n")        

            
                  
            list_of_groups = []     
            print("\ncommmon groups\n")
                        
            for i, count in common:
                    
                    cleaned = re.sub(r"\(\)", '', str(i))
                    print(f"https://www.roblox.com/groups/{cleaned}" + " How many are in this group: " + str(count) )
                    list_of_groups.append(f"https://www.roblox.com/groups/{cleaned}" + "-How many are in this group:" + str(count) )
                    information_groups.set(list_of_groups)
                    
            
            break
        
        finished_lbl.pack(fill="both",expand=True)
        
 
def make_thread(finished_lbl,uid,pgs,information,information_groups):
    print("Successfully created thread!")
    
    threading.Thread(target=scan_bad_group,args=(finished_lbl,uid,pgs,information,information_groups,)).start()


def main():

    print("UI has started!")

    root = tk.Tk()
    txt = tk.StringVar()
    pages = tk.StringVar()
    information = tk.StringVar()
    information_groups = tk.StringVar()
    
    root.geometry("300x200")
    root.resizable(True,True)
    root.title("Roclean")
    frame = tk.Frame(root).pack(padx=10, pady=10, fill='x', expand=True)
    finished_lbl = tk.Label(master=frame,text="Finshed!\nCheck the files in caught in 4k folder\nMake sure to check the users!")
    input_id_lbl = tk.Label(master=frame,text="Group id").pack(fill="x", expand=True)
    input_group_id = tk.Entry(master=frame,textvariable=txt).pack(fill="x", expand=True)
    pages_lbl = tk.Label(master=frame,text="Enter the amount of pages you want to scan\nDepending on how many pages it will take a while").pack(fill="x", expand=True)
    pages_enter = tk.Entry(master=frame,textvariable=pages).pack(fill="x", expand=True)

    def info_of_user_window_function(data):
            """why this player was flagged as bad"""
            
          
          
            donkey_root = tk.Toplevel(root)
            donkey_root.geometry("800x200")
                

            information_lbl_for_donkey = tk.Entry(donkey_root,text=data)
            information_lbl_for_donkey.pack(fill="x",side='top')
            parts =str(data).split('/')
            user_id = parts[4]
            print(user_id)
            get_userinfo= requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
            description = get_userinfo["description"]
            characters_per_line = 100
            modified_content = '\n'.join(description[i:i+characters_per_line] for i in range(0, len(description), characters_per_line))
            created = get_userinfo["created"]
                
            name = get_userinfo["name"]
            displayname = get_userinfo["displayName"]

            information_about_donkey_user = "Name: " + str(name) + "\n" + "Displayname: " + displayname +"\n"+"Created: "+ str(created) +"\n" + "Description: " + str(modified_content)
 
            var = tk.StringVar()
            var.set(information_about_donkey_user)

            

            information_donkey_user_entry = tk.Label(donkey_root,textvariable=var).pack(side="top")
            
            donkey_root.mainloop()


       
          
    def information_window_functon():
          """this is to display what is currently happening"""
          main_scanner_scroller = tk.Toplevel(root)
          main_scanner_scroller.geometry("500x200")
          main_scanner_scroller.title("Username information")
          txt_lbl = tk.StringVar()
          label = tk.Entry(master=main_scanner_scroller,textvariable=txt_lbl)
          label.pack(side="top", fill="x")
          
          information_window = tk.Listbox(master=main_scanner_scroller,listvariable=information,activestyle='underline',name='information_window',)
          information_window.pack(fill="both",expand=True)
          def callback(event):
                selection = event.widget.curselection()
                if selection:
                    index = selection[0]
                    data = event.widget.get(index)
                    print(data)
                    pattern = r"['\[\],]"

                    data_ = re.sub(pattern,'',data)
                    txt_lbl.set(f"Selection: {data_}")
                    
                    
                    info_of_user_window_function(data=data_)
                    
          main_scanner_scroller.bind("<<ListboxSelect>>", callback)
          
                
    def information_window_groups_functon():
          """this is to display what is currently happening in the groups"""
          main_scanner_scroller_group = tk.Toplevel(root)
          main_scanner_scroller_group.geometry("500x200")
          main_scanner_scroller_group.title("Group information")
          
          txt_lbl = tk.StringVar()
          label = tk.Entry(master=main_scanner_scroller_group,textvariable=txt_lbl)
          label.pack(side="top", fill="x")
          
          information_window = tk.Listbox(master=main_scanner_scroller_group,listvariable=information_groups,activestyle='underline',name='information_window',)
          information_window.pack(fill="both",expand=True)
          def callback_g(event):
                selection = event.widget.curselection()
                if selection:
                    index = selection[0]
                    data = event.widget.get(index)
                    print(data)
                    pattern = r"['\[\],]"
                    data_ = re.sub(pattern,'',data)
                    txt_lbl.set(f"Selection: {data_}")
                      

          main_scanner_scroller_group.bind("<<ListboxSelect>>", callback_g)
          
    warned = False
    def get_txt():
         text = txt.get()
         pgs = pages.get()
         threads = threading.active_count()
         print(threads)
         if threading.active_count() > 2:
             make_thread(finished_lbl,text,pgs,information,information_groups) 
         if threading.active_count() ==1:
            threading.Thread(target=information_window_functon).start()
            threading.Thread(target=information_window_groups_functon).start()
            make_thread(finished_lbl,text,pgs,information,information_groups) 
         
                 
        
    button_to_activate = tk.Button(master=frame,text="Run",command=get_txt).pack(fill="x", expand=True)
    
    root.mainloop()
    
    

if __name__ == "__main__":
    main()