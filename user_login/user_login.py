#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liuchun
# date: 20160106
# contact: cedrela_liu@163.com
# User login interface
########################################################
import getpass
import os
import time
import sys
import platform
operating_system=platform.platform()
path=sys.path[0]
if operating_system[:7]=="Windows":
    lock_file=path+"\Account.lock"
    account_file=path+"\Account.txt"
    user_login_file=path+"\login.times"
    temp_file=path+"\Temp.txt"
else:
    lock_file=path+"/Account.lock"
    account_file=path+"/Account.txt"
    user_login_file=path+"/login.times"
    temp_file=path+"/Temp.txt"
timenow=time.time()
exit_flag=False
count=0
username=-1
temp_times=0
temp_hour=0
time_diff=0

while exit_flag==False:     # loop for user login
    print("#########################################\n")     #login Page
    print("#              Login Page               #\n")
    print("#########################################")
    print("Press q to exit the system !")
    username = input("Username: ")                                #get username
    #password = input("Passowrd: ")                                #get password
    password = getpass.getpass("Password: ")
    if username.strip()=='q':
        break
    elif len(username)==0:  # input nothing
        print("Your username is empty, please re-enter..")
        break
    else:
        ###### check if user is locked     #####
        f_lock = open(lock_file,'r')
        for line in f_lock.readlines():
            if username in line:
                print("Your account is locked! You're forbidden to login system!")
                exit_flag=True # exit the program
                break
        f_lock.close()
    k=1
    ##### validate username and password####
    if exit_flag==False:
        f_account = open(account_file,'r')
        for line in f_account.readlines():
            if username==line.split(',')[0] and password==line.split(',')[1].strip():
                k += 1
                print("Welcome %s !" %username)
                exit_flag=True
                break
        if k==1:            # authentication failed, check check user login times
            print("Wrong username or password!")
            f_login_times = open(user_login_file,'r')
            if len(f_login_times.read())==0: # login.times file is empty
                temp_times=1
                newline=username+','+str(timenow)+','+str(temp_times)+','+str(temp_hour)+'\n'
                f_login_times.close()
                f_login_times = open(user_login_file,'w')
                f_login_times.write(newline+'\n')
                f_login_times.close()
            else:
                f_login_times = open(user_login_file,'r')
                f_temp = open(temp_file,'w')
                j=1
                for line in f_login_times.readlines():
                    if username in line:
                        j += 1           # means find a records in login.times
                        if int(line.split(',')[2])<3:   # user login failed times less than 3,then update the user failed times record
                            temp_times=int(line.split(',')[2])+1
                            time_diff=timenow-float(line.split(',')[1])
                            temp_hour=float(line.split(',')[3])+time_diff
                            newline=line.split(',')[0]+','+str(timenow)+','+str(temp_times)+','+str(temp_hour)+'\n'
                            line=line.replace(line,newline)
                            f_temp.write(line)
                            f_login_times.close()
                            f_temp.close()

                            if os.path.isfile(user_login_file):   # if login.times exist, and delete
                                os.remove(user_login_file)
                            os.rename(temp_file,user_login_file)

                        if int(temp_times)==3 and float(temp_hour)<10800:  # after update, if failed times is 3 and during 3hours, then user is locked
                            type(temp_times)
                            print("You've failed 3 times in 3 hours ! Your account will be locked !")
                            f_lock = open(lock_file,'a') #add username in Account.lock
                            f_lock.write('\n')
                            f_lock.write(username)
                            f_lock.close()
                            exit_flag=True
                            break
                      # add in new records in login.times
                if j==1: # means no match records find in login.times
                    f_login_times.close()
                    f_login_times = open(user_login_file,'a')
                    temp_times=1
                    newline=username+','+str(timenow)+','+str(temp_times)+','+str(temp_hour)+'\n'
                    f_login_times.write(newline)
                    f_login_times.close()
    time.sleep(2)
