import discord
import html2text
from canvasapi import Canvas
from canvasapi.page import Page

f = open("api_key.txt", "r")

# Canvas API URL
API_URL = "https://graniteschools.instructure.com/api/v1"
# Canvas API key
API_KEY = f.readline()


def get_info():
    canvas = Canvas(API_URL, API_KEY)

    course = canvas.get_course(1337964)
    pages = [p for p in course.get_pages() if p.title.startswith("Week of")]
    page = str(html2text.html2text(Page.show_latest_revision(pages[len(pages) - 1]).body))
    # print(page)
    page_lines = [x if not x.startswith("http") else "<" + x + ">" for x in page.splitlines()]
    meeting_i_start = -1
    meeting_i_end = -1
    for i in range(len(page_lines)):
        if "Lecture/Discussion" in page_lines[i]:
            meeting_i_start = i
            break
    for j in range(len(page_lines) - 1, 0, -1):
        if "Password: " in page_lines[j]:
            meeting_i_end = j + 1
            break
    if meeting_i_end == -1 or meeting_i_start == -1:
        return "I couldn't find the meeting information for the current week."

    # print("\n".join(page_lines[meeting_i_start:meeting_i_end]))
    title = pages[len(pages) - 1].title
    return "Meetings for the " + title[0].lower() + title[1:] + ":\n" + "\n".join(page_lines[meeting_i_start:meeting_i_end])


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
            print('Triggered by {0.author}!'.format(message))
            await message.channel.send('Let me check...')
            await message.channel.send(get_info()[:1999])

        elif message.content.startswith('-'):
            await message.channel.send('Hello! I\'m a Discord bot <@449579826278563860> made!\nMy prefix is `-`\nFor '
                                       'a list of commands, type `-help` or `-info`')


client = MyClient()
client.run(f.readline())
f.close()
