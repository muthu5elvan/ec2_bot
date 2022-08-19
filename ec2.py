EC2_INSTANCE = ''
REGION=''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
EC2_SSH_USERNAME = ""
EC2_SSH_PRIVATE_KEY = ""
########################  ABOVE VALUES ARE REQUIRED ########################

IP_RETRIVE_INTERVAL = 5  # Seconds

########################  ABOVE VALUES ARE OPTIONAL ########################

########################  Requirement ######################################
"""
Python3 is needed
Install boto3 library in python3
Configure the Above required Values

To Run program
python3 ec2.py

To Run start the instance
python3 ec2.py -c 1 

To Run stop the instance
python3 ec2.py -c 2

To Run restart the instance
python3 ec2.py -c 3 

To Check Status
python3 ec2.py -c 0
"""
############################################################################
INFO = """Check The Choices:
\t1 : Instance Start
\t2 : Instance Stop
\t3 : Instance Restart
\t4 : Connect To SSH
\t5 : Start Instance and Connect
\t0 : Exit
"""


import sys
from tracemalloc import start
try:
    import boto3
except:
    print("[!] Install boto3 by using 'pip install boto3'")
    sys.exit()
from rich import print
import argparse
import time
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help = "Show Debug",action='store_true',default=False)
parser.add_argument("-c", "--choice", help = INFO,default=False)
# Read arguments from command line
args = parser.parse_args()
ec2 = boto3.client('ec2',
                   REGION,
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

#This function will describe all the instances
#with their current state 
def v_print(msg):
    print("")
    print("[-] Verbose : ")
    print(msg)
    print("[-]")

def getInstanceStatus():
    print("[+] Getting Instance Status")
    response = ec2.describe_instances(InstanceIds=[EC2_INSTANCE])
    try :
        print("Instance Name : ",response["Reservations"][0]['Instances'][0]['KeyName'])
    except:
        print("Instance Name : ","Not Found")
    
    try :
        print("Instance PublicIp : ",response["Reservations"][0]['Instances'][0]['PublicIpAddress'])
    except:
        print("Instance PublicIp : ","Not Found")
    
    try :
        print("Instance Status : ", response["Reservations"][0]['Instances'][0]['State']['Name'].upper())
    except:
        print("Instance Status : ","Not Found")
    
    try :
        print("Instance Type : ",response["Reservations"][0]['Instances'][0]['Tags'])
    except:
        print("Instance Type : ","Not Found")
    print("")
    return response["Reservations"][0]['Instances'][0]['State']['Name'].upper()

def getInstancePublicIP():
    
    print("[+] Getting Instance Status")
    response = ec2.describe_instances(InstanceIds=[EC2_INSTANCE])
    while response["Reservations"][0]['Instances'][0]['State']['Name'].upper() == "PENDING":
        time.sleep(IP_RETRIVE_INTERVAL)
        response = ec2.describe_instances(InstanceIds=[EC2_INSTANCE])
        print("[#] Instance Status is : ",response["Reservations"][0]['Instances'][0]['State']['Name'].upper())
    try :
        print("Instance PublicIp : ",response["Reservations"][0]['Instances'][0]['PublicIpAddress'])
        return response["Reservations"][0]['Instances'][0]['PublicIpAddress']
    except:
        print("Instance PublicIp : ","Not Found")
        print("Instance Status : ", response["Reservations"][0]['Instances'][0]['State']['Name'].upper())

def startInstance(instanceStatus):
    response = ""
    if instanceStatus != "STOPPING":
        print("[+] Starting Instance")
        response = ec2.start_instances(InstanceIds=[EC2_INSTANCE])
        getInstanceStatus()
        getInstancePublicIP()
        return response
    else:
        print("[*] Instance is Not Stopped Yet \nTry Again After few Minutes")

def connectInstance(ip):
    import tempfile
    import shutil
    import os
    SSH_KEY = tempfile.NamedTemporaryFile(delete=False)
    print(SSH_KEY.name)
    shutil.copyfile(EC2_SSH_PRIVATE_KEY,SSH_KEY.name)
    os.system("notepad "+SSH_KEY.name)
    os.system("ssh {username}@{ip} -i {key}".format(
        username=EC2_SSH_USERNAME,
        ip=ip,
        key=SSH_KEY.name
        ))
    SSH_KEY.close()
    os.unlink(SSH_KEY.name)


try:
    print("[#] Checking Configuration")
    instanceStatus = getInstanceStatus()
    if not args.choice :
        print(INFO)
        choice = int(input("Enter the Option Number : "))
    else:
        choice = int(args.choice)
    print("")
    response = ""
    if choice == 1:
        response = startInstance(instanceStatus)
    if choice == 2:
        print("[+] Stopping Instance")
        response = ec2.stop_instances(InstanceIds=[EC2_INSTANCE])
        getInstanceStatus()
    if choice == 3:
        print("[+] Rebooting Instance")
        response = ec2.reboot_instances(InstanceIds=[EC2_INSTANCE])
        getInstanceStatus()
    if choice == 4 :
        ip = getInstancePublicIP()
        if ip:
            connectInstance(ip)

    if choice == 5 :
        response = startInstance(instanceStatus)
        ip = getInstancePublicIP()
        if ip:
            connectInstance(ip)
    if args.verbose:
        v_print(response)
    
except Exception as ex:
    print("[*] ",ex)
