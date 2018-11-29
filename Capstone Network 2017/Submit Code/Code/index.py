from Balanced.Servers import CreateServer,client,SendMessage,Balanced_Control,CreateBancedServer_CPU_Memory,CreateBancedServer_Number

if __name__ == "__main__":

    print("1: Server")
    print("2: Balanced based on Number Distribution")
    print("3: Balanced based on CPU and Memory Distribution")
    print("4: Balanced Control")
    print("5: Client")
    print("-------------------------------------------------------------")
    program_index = input("Choose a number:")

    if program_index == "1":
        # This is open a balance
        print("This is open a Server.")

        # get the parameter
        Balanced_ip = input("Balance server IP is:")
        ip = input("The server ip address:")
        port = input("The server port:")
        print(SendMessage("http://%s:8080/"%Balanced_ip,"add_server%s:%s"%(ip,port)).response.read())
        new_server = CreateServer("0.0.0.0", port)
    
    elif program_index == "2":
        port = 8080
        print("Open a balanced on {} based on Number Distribution.".format(port))
        new_server = CreateBancedServer_Number('0.0.0.0', port)

    elif program_index == "3":
        port = 8080
        print("Open a balanced on {} based on CPU and Memory Distribution.".format(port))
        new_server = CreateBancedServer_CPU_Memory('0.0.0.0', port)

    elif program_index == "4":

        print("Open a balanced control.")
        Balanced_Control("0.0.0.0")

    elif program_index == "5":
        require_number = 1000
        print("Generate a client with {} require".format(require_number))
        ip = input("Input the ip address and port of balanced:(eg:54.206.115.190:8080)")
        client("http://%s/{}"%ip,require_number)
    else:
        print("This is a wrong number.")

