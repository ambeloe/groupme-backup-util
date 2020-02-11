from groupy import Client
import csv
import io

userToken = "replace with your token"
client = Client.from_token(userToken)

allGroups = list(client.groups.list_all())

i = 0
for group in allGroups:
    print(str(i) + ") " + group.name)
    i += 1

choice = int(input("Which group do you want to back up? "))
selGroup = allGroups[choice]

print("Backing up users...")
with io.open("userlist.csv", "w+", encoding="utf-8") as file:
    userlist = csv.writer(file, delimiter=",")
    i = 0
    for member in selGroup.members:
        userlist.writerow([str(i), member.name])
        i += 1

print("Backing up messages...")
with io.open("messages.csv", "w+", encoding="utf-8") as file:
    messages = csv.writer(file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
    i = 0
    for message in selGroup.messages.list_all():
        try:
            messages.writerow([str(i), message.name, message.text])
        except:
            pass
        i += 1
print("done")
