from requests import Session
from bs4 import BeautifulSoup as bs

f = open("config.txt", "r")
config_info = f.readlines()
f.close()

with Session() as s:
    site = s.get("https://graniteschools.instructure.com/login/ldap")
    bs_content = bs(site.content, "html.parser")
    token = bs_content.find("input", {"name": "authenticity_token"})["value"]
    login_data = {"pseudonym_session[unique_id]": config_info[1], "pseudonym_session[password]": config_info[2],
                  "authenticity_token": token} 
    s.post("https://graniteschools.instructure.com/login/ldap", login_data)
    home_page = s.get("https://graniteschools.instructure.com")
    print(home_page.content)

