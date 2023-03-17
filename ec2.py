EC2_INSTANCE = ''
REGION=''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
EC2_SSH_USERNAME = ""
EC2_SSH_PRIVATE_KEY = ""
########################  ABOVE VALUES ARE REQUIRED ########################

IP_RETRIVE_INTERVAL = 15  # Seconds
SSH_CONNECT_INTERVAL = 30 # After starting the Instance Waiting for 30 Seconds to Start SSH SERVICE

########################  ABOVE VALUES ARE OPTIONAL ########################

########################  Requirement ######################################
"""
Python3 is needed
Install boto3 library in python3
Configure the Above required Values
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
try:
    import boto3
    from rich import print
except:
    print("[!] Install boto3 by using 'pip install boto3 rich'")
    sys.exit()
import argparse
import time
global RESPONSE
RESPONSE = ""
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
    global RESPONSE
    print("[+] Getting Instance Status")
    RESPONSE = ec2.describe_instances(InstanceIds=[EC2_INSTANCE])
    try :
        print("Instance Name : ",RESPONSE["Reservations"][0]['Instances'][0]['KeyName'])
    except:
        print("Instance Name : ","Not Found")
    
    try :
        print("Instance PublicIp : ",RESPONSE["Reservations"][0]['Instances'][0]['PublicIpAddress'])
    except:
        print("Instance PublicIp : ","Not Found")
    
    try :
        print("Instance Status : ", RESPONSE["Reservations"][0]['Instances'][0]['State']['Name'].upper())
    except:
        print("Instance Status : ","Not Found")
    
    try :
        print("Instance Type : ",RESPONSE["Reservations"][0]['Instances'][0]['Tags'])
    except:
        print("Instance Type : ","Not Found")
    print("")
    return RESPONSE["Reservations"][0]['Instances'][0]['State']['Name'].upper()

def getInstancePublicIP():
    global RESPONSE
    print("[+] Getting Instance Status")
    RESPONSE = ec2.describe_instances(InstanceIds=[EC2_INSTANCE])
    while RESPONSE["Reservations"][0]['Instances'][0]['State']['Name'].upper() == "PENDING":
        RESPONSE = ec2.describe_instances(InstanceIds=[EC2_INSTANCE])
        print("[#] Instance Status is : ",RESPONSE["Reservations"][0]['Instances'][0]['State']['Name'].upper())
        time.sleep(IP_RETRIVE_INTERVAL)
    try :
        print("Instance PublicIp : ",RESPONSE["Reservations"][0]['Instances'][0]['PublicIpAddress'])
        return RESPONSE["Reservations"][0]['Instances'][0]['PublicIpAddress']
    except:
        print("Instance PublicIp : ","Not Found")
        print("Instance Status : ", RESPONSE["Reservations"][0]['Instances'][0]['State']['Name'].upper())

def startInstance(instanceStatus):
    global RESPONSE
    RESPONSE = ""
    if instanceStatus != "STOPPING":
        print("[+] Starting Instance")
        RESPONSE = ec2.start_instances(InstanceIds=[EC2_INSTANCE])
        getInstanceStatus()
        getInstancePublicIP()
        return RESPONSE
    else:
        print("[*] Instance is Not Stopped Yet \nTry Again After few Minutes")

def connectInstance(ip):
    global RESPONSE
    print("[+] Connecting to SSH")
    import tempfile
    import shutil
    import os
    SSH_KEY = tempfile.NamedTemporaryFile(delete=False)
    shutil.copyfile(EC2_SSH_PRIVATE_KEY,SSH_KEY.name)
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
    RESPONSE = ""
    if choice == 1:
        startInstance(instanceStatus)
    if choice == 2:
        print("[+] Stopping Instance")
        RESPONSE = ec2.stop_instances(InstanceIds=[EC2_INSTANCE])
        getInstanceStatus()
    if choice == 3:
        print("[+] Rebooting Instance")
        RESPONSE = ec2.reboot_instances(InstanceIds=[EC2_INSTANCE])
        getInstanceStatus()
    if choice == 4 :
        ip = getInstancePublicIP()
        if ip and "RUNNING" == RESPONSE["Reservations"][0]['Instances'][0]['State']['Name'].upper():
            connectInstance(ip)
        else:
            print("[*] Instance Not in Running State")

    if choice == 5 :
        startInstance(instanceStatus)
        ip = getInstancePublicIP()
        if ip and "RUNNING" == RESPONSE["Reservations"][0]['Instances'][0]['State']['Name'].upper():
            time.sleep(SSH_CONNECT_INTERVAL)
            connectInstance(ip)
        else:
            print("[*] Instance Not in Running State")
    if args.verbose:
        v_print(RESPONSE)
    
except Exception as ex:
    print("[*] ",ex,ex.with_traceback())
