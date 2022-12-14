# ec2_bot

This ec2 program helps to manage the single EC2 instance

## Usage

> After installing the library you can run the program in intractive mode by `python ec2.py`

![](assets/info.png)

> If you like to run the program by argument follow the below commands

* `python ec2.py -c 0` To Get status of the instance
* `python ec2.py -c 1` To Start the instance
* `python ec2.py -c 2` To Stop the instance
* `python ec2.py -c 3` To Restart the instance
* `python ec2.py -c 4` Connect to SSH
* `python ec2.py -c 5` Start Instance and Connect to SSH

![](assets/command_5.png)

## Requirement

* Python3

### Library

* boto3==1.24.54
* rich==12.5.1

### Install Library

> Install the library before running the program

`pip install boto3==1.24.54 rich==12.5.1`

## Configuration

> Create IAM User with Programatic access

![](assets/20220819_123645_image.png)

> Give Full EC2 Access Policy

![](assets/20220819_123820_image.png)

> Add tag an click next then create user

![](assets/20220819_124020_image.png)

> Download The access key and copy the access and secret Key

![](assets/20220819_124258_image.png)

> Got to Your Instance Copy the Instance Id and Availability Zone

![](assets/20220819_124604_image.png)

> Give Those Copied information To  `ec2.py` program

![](assets/20220819_125745_image.png)

