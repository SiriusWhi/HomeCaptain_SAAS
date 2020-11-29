import requests
from simple_salesforce import Salesforce

session = requests.Session()
username = 'nazir.tyrewala@homecaptain.com.sandbox42'
password = 'Connor#1'
security_token = "E54iHcjpaaQd5Zs5Ea6aqWgB7"
print("Creating sf connection")
sf = Salesforce(password=password, username=username, session=session,
                security_token=security_token, domain="test")
print("sf connection created")
print(sf.Contact.get("0030G00002l8VCH"))
print(sf.query("select l.name from lead l"))
