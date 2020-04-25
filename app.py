"""A secret santa generator for groups of families or friends"""

from random import randint
import smtplib
import ssl
import csv
import yaml


with open("config.yml", "r") as ymlfile:
    CONFIG = yaml.load(ymlfile, Loader=yaml.FullLoader)


PORT = int(CONFIG['port'])
PASSWORD = CONFIG['password']
SENDER_EMAIL = CONFIG['sender']
CSV_SOURCE = CONFIG['csv_source']
HOST = CONFIG['host']
FAMILY_MEMBERS = []
RANDOM_NUMS = []
CONTEXT = ssl.create_default_context()


class FamilyMember:
    name = None
    email = None
    assignee = None

    def __init__(self, name, email):
        self.name = name
        self.email = email


def send_email(server, family_member_list):
    for person in family_member_list:
        server.sendmail(SENDER_EMAIL,
                        person.email,
                        "You are the secret santa for " + family_member_list[person.assignee].name)
        print("Email sent!")


def send(family_member_list):
    with smtplib.SMTP_SSL(HOST, PORT, context=CONTEXT) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        send_email(server, family_member_list)


def assign(number, some_member, member_list):
    for item in member_list:
        if number == item.assignee:
            continue
        some_member.assignee = number
        break


with open(CSV_SOURCE) as csv_file:
    CSV_READER = csv.reader(csv_file, delimiter=',')
    for row in CSV_READER:
        member = FamilyMember(row[0], row[1])
        FAMILY_MEMBERS.append(member)


for member in FAMILY_MEMBERS:
    random_num = randint(0, len(FAMILY_MEMBERS) - 1)
    while random_num in RANDOM_NUMS or random_num == FAMILY_MEMBERS.index(member):
        random_num = randint(0, len(FAMILY_MEMBERS) - 1)
    RANDOM_NUMS.append(random_num)
    assign(random_num, member, FAMILY_MEMBERS)


CONFIRM = input("Ready to send? ")
if CONFIRM.lower() == "yes":
    send(FAMILY_MEMBERS)
