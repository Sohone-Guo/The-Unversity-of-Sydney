#!/usr/bin/env python3.5

from aiohttp import web
import asyncio
import random
from aiohttp import ClientSession
from itertools import islice
import sys
import urllib.request
import psutil
import time
import boto3
import numpy as np



class SendMessage(object):

    def __init__(self,url,number_of_require):
        self.response = urllib.request.urlopen('%s%s'%(url,number_of_require))
        # print(self.response.read())

# create the client
class client(object):

    def __init__(self,url,number_of_require):
        # number_of_require : int
        # url : str/ eg: "http://localhost:8080/{}"
        self.limit = 1000
        self.number_of_require = number_of_require
        self.url = url

        self.loop = asyncio.get_event_loop()
        with ClientSession() as session:
            coros = (self.fetch(self.url.format(i), session) for i in range(self.number_of_require))
            self.loop.run_until_complete(self.print_when_done(coros))

        self.loop.close()

    def limited_as_completed(self,coros, limit):
        futures = [
            asyncio.ensure_future(c)
            for c in islice(coros, 0, limit)
        ]
        async def first_to_finish():
            while True:
                await asyncio.sleep(0)
                for f in futures:
                    if f.done():
                        futures.remove(f)
                        try:
                            newf = next(coros)
                            futures.append(
                                asyncio.ensure_future(newf))
                        except StopIteration as e:
                            pass
                        return f.result()
        while len(futures) > 0:
            yield first_to_finish()

    async def fetch(self,url, session):
        async with session.get(url) as response:
            return await response.read()

    async def print_when_done(self,tasks):
        for res in self.limited_as_completed(tasks, self.limit):
            await res



# server
class CreateServer(object):

    def __init__(self,id_address,port):
        # '127.0.0.1', 8081
        self.id_address = id_address
        self.port = port

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.init())

        self.loop.run_forever()


    async def handle(self,request):
        start_time = time.time()

        name = request.match_info.get('name', "Anonymous")
        await asyncio.sleep(0)
        

        # Check the cpu and memory
        if name == "check":
            cpu = str(psutil.cpu_percent())
            memory = psutil.virtual_memory().percent
            return web.Response(text="%s,%s"%(cpu,memory))

        data = np.random.random_sample((300,100))
        random_int = np.random.randint(1,3)
        for i in range(random_int):
            data*i

        end_time = time.time()

        used_time = end_time - start_time

        print("Using the time is {}".format(used_time))

        return web.Response(text="This is from: %s:%s"%(self.id_address,self.port))

    async def init(self):
        app = web.Application()
        app.router.add_route('GET', '/{name}', self.handle)
        return await self.loop.create_server(
            app.make_handler(), self.id_address, self.port)


# balanced based on CPU and Memory
class CreateBancedServer_CPU_Memory(object):

    def __init__(self,id_address,port):
        # '127.0.0.1', 8080, [['127.0.0.1', 8081],['127.0.0.1', 8082]]
        self.id_address = id_address
        self.port = port
        
        # Read the server list
        self.balanced_ip = []

        self.balanced_load = [0 for i in range(len(self.balanced_ip))]
        self.result = []

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.init())

        self.loop.run_forever()

    async def handle(self,request):
        start_time = time.time()

        name = request.match_info.get('name', "Anonymous")
        await asyncio.sleep(0)

        if name[:10] ==  "add_server":
            ip_address = name[10:].split(":")
            self.balanced_ip.append((ip_address[0],int(ip_address[1])))
            print("Adding a new server: %s"%name[10:]," Running servers: ",self.balanced_ip)
            
            # Write it to file
            with open("Parameter/serverList.txt","w+") as w:
                w.write("{}".format(self.balanced_ip))

            return web.Response(text="Adding the server is achievement.")

        if name[:10] ==  "del_server":
            ip_address = name[10:].split(":")
            self.balanced_ip.pop(self.balanced_ip.index((ip_address[0],int(ip_address[1]))))
            print("Delete a new server: %s"%name[10:]," Running servers: ",self.balanced_ip)
            
            # Write it to file
            with open("Parameter/serverList.txt","w+") as w:
                w.write("{}".format(self.balanced_ip))

            return web.Response(text="Delete the server is achievement.")


        # this part is the algothsm

        with open("Parameter/cpu_memory.txt","r+") as r:
            cup_memory = eval(r.read())
            cup_memory = list(map(float,cup_memory))
            server_number = cup_memory.index(min(cup_memory))
        

        response = urllib.request.urlopen('http://%s:%d/%s:%d'%(self.balanced_ip[server_number][0],self.balanced_ip[server_number][1],self.id_address,self.port))
        # print(response.read())

        end_time = time.time()

        used_time = end_time - start_time
        print("Using time is {}".format(used_time))

        return web.Response(text="Hello, World!")

    async def init(self):
        app = web.Application()
        app.router.add_route('GET', '/{name}', self.handle)
        return await self.loop.create_server(
            app.make_handler(), self.id_address, self.port)



# Balanced Server based on number
class CreateBancedServer_Number(object):

    def __init__(self,id_address,port):
        # '127.0.0.1', 8080, [['127.0.0.1', 8081],['127.0.0.1', 8082]]
        self.id_address = id_address
        self.port = port
        
        # Read the server list
        self.balanced_ip = []

        self.balanced_load = [0 for i in range(len(self.balanced_ip))]
        self.result = []

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.init())

        self.loop.run_forever()

    async def handle(self,request):
        start_time = time.time()

        name = request.match_info.get('name', "Anonymous")
        await asyncio.sleep(0)

        if name[:10] ==  "add_server":
            ip_address = name[10:].split(":")
            self.balanced_ip.append((ip_address[0],int(ip_address[1])))
            print("Adding a new server: %s"%name[10:]," Running servers: ",self.balanced_ip)
            
            # Write it to file
            with open("Parameter/serverList.txt","w+") as w:
                w.write("{}".format(self.balanced_ip))

            self.balanced_load = [0 for i in range(len(self.balanced_ip))]

            return web.Response(text="Adding the server is achievement.")

        if name[:10] ==  "del_server":
            ip_address = name[10:].split(":")
            self.balanced_ip.pop(self.balanced_ip.index((ip_address[0],int(ip_address[1]))))
            print("Delete a new server: %s"%name[10:]," Running servers: ",self.balanced_ip)
            
            # Write it to file
            with open("Parameter/serverList.txt","w+") as w:
                w.write("{}".format(self.balanced_ip))

            return web.Response(text="Delete the server is achievement.")


        # this part is the algothsm

        # with open("cpu_memory.txt","r+") as r:
        #     cup_memory = eval(r.read())
        #     cup_memory = list(map(float,cup_memory))
        #     server_number = cup_memory.index(min(cup_memory))

        server_number = self.balanced_load.index(min(self.balanced_load))
        self.balanced_load[server_number] += 1
        

        response = urllib.request.urlopen('http://%s:%d/%s:%d'%(self.balanced_ip[server_number][0],self.balanced_ip[server_number][1],self.id_address,self.port))
        # print(response.read())

        end_time = time.time()

        used_time = end_time - start_time
        print("Using time is {}".format(used_time))

        return web.Response(text="Hello, World!")

    async def init(self):
        app = web.Application()
        app.router.add_route('GET', '/{name}', self.handle)
        return await self.loop.create_server(
            app.make_handler(), self.id_address, self.port)



# Declare the balanced control 
class Balanced_Control(object):

    def __init__(self,balanced_ip):
        self.ec2 = boto3.resource('ec2')

        n,m = map(int,input('Please input the weight of CUP and Memory(eg:2 3):').split())

        while True:

            start_time = time.time()

            print("Balance Server Control opened.")

            total_server_status = {}

            with open("Parameter/TotalServer.txt","r+") as r:
                self.total_server = eval(r.read())

            with open("Parameter/serverList.txt","r+") as r:
                self.data = eval(r.read())

            with open("Parameter/Total_instant.txt","r+") as r:
                self.instant_Name = eval(r.read())

            if len(self.data) == 0:
                if len(list(set(self.total_server) - set(self.data)))!=0:
                    # add new
                    # list(set(self.total_server) - set(self.data))[0]
                    print("Please add a new servers now.")
                    # ids = [self.instant_Name[self.total_server[0]]]
                    # self.ec2.instances.filter(InstanceIds=ids).start()

                else:
                    print("No more servers availble.")
                
                pass
            
            tp = []
            for each_ip in self.data:

                result = SendMessage("http://%s:%d/"%(each_ip[0],each_ip[1]),"check")
                result = eval(result.response.read())

                cpu,memory = result
                total_server_status[each_ip] = (float(cpu)*0.01*n + float(memory)*0.01*m)/(n+m)
                print("CPU:",float(cpu),"%, Memory:",float(memory),"%")
                tp.append((float(cpu)*0.01*n + float(memory)*0.01*m)/(n+m))

            with open("Parameter/cpu_memory.txt","w+") as w:
                w.write("{}".format(tp))

            
            avarage_value = sum(total_server_status.values())/len(total_server_status.values())

            end_time = time.time()
            print("The avarage is: ",avarage_value," And the time spend: {}".format(end_time-start_time))
            if avarage_value < 0.1:
                if len(self.data)>1:
                    # delete server
                    print("Please delete a new servers now.")
                    # ids = [self.instant_Name[self.data[0]]]
                    # SendMessage("http://%s:8080/"%balanced_ip,"del_server%s:%s"%(self.data[0][0],self.data[0][1]))
                    # self.ec2.instances.filter(InstanceIds=ids).stop()

                    
            elif avarage_value > 0.3:
                if len(list(set(self.total_server) - set(self.data)))!=0:
                    # add new
                    # list(set(self.total_server) - set(self.data))[0]
                    print("Please add a new servers now.")
                    # ids = [self.instant_Name[list(set(self.total_server) - set(self.data))[0]]]
                    # self.ec2.instances.filter(InstanceIds=ids).start()                    
                    
                else:
                    print("No more server is a available.")


            time.sleep(0.1)



if __name__ == "__main__":
    print("This is the testing!")
    # client = client("http://localhost:8081/{}",1)
    # balanced = CreateBancedServer('127.0.0.1', 8080,[['127.0.0.1', 8081],['127.0.0.1', 8082]])
    # new_server = CreateServer('127.0.0.1', 8081)
    # send = Send(server_address="http://localhost:8081/{}",number_of_send=5)
  