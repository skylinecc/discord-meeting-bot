import discord
from requests import Session
from bs4 import BeautifulSoup as bs

f = open("config.txt", "r")
config_info = f.readlines()
f.close()


def scrape():
    with Session() as s:
        site = s.get("https://graniteschools.instructure.com/login/ldap")
        bs_content = bs(site.content, "html.parser")
        token = bs_content.find("input", {"name": "authenticity_token"})["value"]
        login_data = {"pseudonym_session[unique_id]": config_info[1], "pseudonym_session[password]": config_info[2],
                      "authenticity_token": token}
        s.post("https://graniteschools.instructure.com/login/ldap", login_data)
        home_page = s.get("https://graniteschools.instructure.com/courses/1337964/modules")

        soup = bs(home_page.text, 'html.parser')
        weeks = [x for x in soup.find_all("a", class_='ig-title title item_link') if x["title"].startswith("Week of ")]
        curr_week = weeks[len(weeks) - 1]
        # print(curr_week)

        curr_page = s.get("https://graniteschools.instructure.com" + curr_week["href"])
        # print(curr_page.text)
        return "https://graniteschools.instructure.com" + curr_week["href"]


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return

        elif message.content.startswith('-help') or message.content.startswith('-info'):
            await message.channel.send('To see this list of commands, type `-help` or `-info`\nTo get the information '
                                       'for the next Zoom meeting, type `-nextmeeting`')

        elif message.content.startswith('-nextmeeting'):
            await message.channel.send('Let me check...')
            await message.channel.send('The information is on this page:\n' + scrape())

        elif message.content.startswith('-'):
            await message.channel.send('Hello! I\'m a Discord bot <@449579826278563860> made!\nMy prefix is `-`\nFor '
                                       'a list of commands, type `-help` or `-info`')


client = MyClient()
client.run(config_info[0])
