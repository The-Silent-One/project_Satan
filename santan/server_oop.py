import socket


class Socket_R():
    conn=None
    addr=None
    
    def __init__(self,server_addr,BUFFER_SIZE):
        self.server_addr=server_addr
        self.BUFFER_SIZE=BUFFER_SIZE
        self.socket=socket.socket(
            socket.AF_INET,socket.SOCK_STREAM)  

    def bind(self):
        self.socket.bind(self.server_addr)
        
    def listen(self):
        self.socket.listen(1)

    def accept(self):
        conn,addr = self.socket.accept()
        self.conn=conn
        self.addr=addr 
    
    def close(self):
        self.conn.close()
    
    def getOutOfTheFriendzone(self):
        self.bind()
        self.listen()
        self.accept()

    def sendData(self):
        print("Connection address:",self.addr)
        while 1:
            data = self.conn.recv(self.BUFFER_SIZE)
            if not data : break # inutile
            print("Received data:",data)
            if(data=="#DC"):
                self.close()
                break

    def getData(self):
        data = self.conn.recv(self.BUFFER_SIZE)
        print("Received data:",data)
        return data


