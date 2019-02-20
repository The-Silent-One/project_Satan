#!/usr/bin/python3

import server_oop

#################CONST####################
TCP_IIC = '192.168.8.142'
TCP_PORT = 6663
BUFFER_SIZE = 20
server_addr = (TCP_IIC,TCP_PORT)
##########################################

s=server_oop.Socket_R(server_addr=server_addr,BUFFER_SIZE=BUFFER_SIZE)

##########################
s.getOutOfTheFriendzone()
##########################
# bind + listen + accept #
##########################


while 1:
    data=s.getData().decode().strip()
    
    if data==b'#dc':
        break
    l=data.split(",")
    x=round(float(l[0].split(":")[1]))
    y=round(float(l[1].split(":")[1]))
    print(x,y)

    #Main Here!


s.close()
############################

