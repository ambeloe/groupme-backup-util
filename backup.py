from groupy import Client
import argparse
import csv
import io


def printAll(client):
    groups = list(client.groups.list_all())
    chats = list(client.chats.list_all())
    print("    Available Groups:")
    i = 0
    for group in groups:
        print(str(i) + ") " + group.name)
        i += 1
    print("    Available Chats:")
    i = 0
    for chat in chats:
        print(str(i) + ") " + chat.other_user['name'])
        i += 1

def storeGroupUsers(group):
    print("Backing up users for " + group.name + "...")
    with io.open(group.name + "-" + "userlist.csv", "w", encoding="utf-8", newline='') as file:
        userlist = csv.writer(file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
        userlist.writerow(["number", "nickname", "user id"])
        i = 0
        for member in group.members:
            try:
                userlist.writerow([str(i), member.name, member.user_id])
            except:
                pass
            i += 1

def storeGroupMessages(group):
    print("Backing up messages for " + group.name + "...")
    with io.open(group.name + "-" + "messages.csv", "w", encoding="utf-8", newline='') as file:
        messages = csv.writer(file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
        messages.writerow(["number", "name", "message content", "message datestamp", "user id of author"])
        i = 0
        for message in group.messages.list_all():
            try:
                messages.writerow([str(i), message.name, message.text, message.created_at, message.user_id])
            except:
                pass
            i += 1

def storeChat(chat):
    print("Backing up DMs for " + chat.other_user['name'] + "...")
    with io.open(chat.other_user['name'] + "-" + "directs.csv", "w", encoding="utf-8", newline='') as file:
        messages = csv.writer(file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
        messages.writerow(["number", "name", "message content", "message datestamp", "user id of author"])
        i = 0
        for message in chat.messages.list_all():
            try:
                messages.writerow([str(i), message.name, message.text, message.created_at, message.user_id])
            except:
                pass
            i += 1


ps = argparse.ArgumentParser(description="Utility to save GroupMe groups and chats to csv")
ps.add_argument("-t", "--token", required=True, help="Your GroupMe access token", action="store")
ps.add_argument("-l", "--list", required=False, help="Lists available groups and chats", action="store_true", default=False)
ps.add_argument("-g", "--group", required=False, help="Selects a group to save", action="store")
ps.add_argument("-c", "--chat", required=False, help="Selects a chat to save", action="store")
ps.add_argument("-a", "--autoyoink", required=False, help="Save all groups and chats", action="store_true", default=False)
args = ps.parse_args()

client = Client.from_token(args.token)

if args.list:
    printAll(client)
    raise SystemExit

allGroups = list(client.groups.list_all())
allChats = list(client.chats.list_all())

if args.autoyoink:
    for group in allGroups:
        storeGroupUsers(group)
        storeGroupMessages(group)
    for chat in allChats:
        storeChat(chat)
elif args.group is not "" and args.group is not None:
    storeGroupUsers(allGroups[int(args.group)])
    storeGroupMessages(allGroups[int(args.group)])
elif args.chat is not "" and args.chat is not None:
    storeChat(allChats[int(args.chat)])
else:
    print("No task given")
