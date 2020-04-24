import smtplib, ssl, csv, yaml
from random import randint

with open("config.yml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


port = int(config['port'])
password = config['password']
sender_email = config['sender']
csv_source = config['csv_source']
host = config['host']
family_members = []
random_nums = []
context = ssl.create_default_context()


class FamilyMember:
    name = None
    email = None
    assignee = None

    def __init__(self, name, email):
        self.name = name
        self.email = email


def send_email(server, family_member_list):
    for person in family_member_list:
        server.sendmail(sender_email,
                        person.email,
                        "You are the secret santa for " + family_member_list[person.assignee].name)
        print("Email sent!")


def send(family_member_list):
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender_email, password)
        send_email(server, family_member_list)


def assign(number, some_member, member_list):
    for item in member_list:
        if number == item.assignee:
            continue
        else:
            some_member.assignee = number
            break


with open(csv_source) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        member = FamilyMember(row[0], row[1])
        family_members.append(member)


for member in family_members:
    random_num = randint(0, len(family_members) - 1)
    while random_num in random_nums or random_num == family_members.index(member):
        random_num = randint(0, len(family_members) - 1)
    random_nums.append(random_num)
    assign(random_num, member, family_members)


confirm = input("Ready to send? ")
if confirm.lower() == "yes":
    send(family_members)
