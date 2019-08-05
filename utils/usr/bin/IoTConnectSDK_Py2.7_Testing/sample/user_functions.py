# this function must always exist it also allows you to add hooks for
# commands sent from cloud.  It can be empty but the example prints out
# some important information.
def user_callbackMessage(msg):
    if msg != None and len(msg.items()) != 0:
        cmdType = msg["cmdType"]
        #print(cmdType)
        #if msg["cmdType"] != None else None
        data = msg["data"]
        if data != None:
            print("\n--- User Command Received ---")
	    print("Ack " + str(msg['data']['ack']))
	    print("AckID " + str(msg['data']['ackId']))
            print("Command " + str(msg['data']['command']))
            print("UniqueID " + str(msg['data']['uniqueId']))
            print("CmdType " + cmdType)

# this function must always exist it gets called on SDK startup so that you
# can setup anything custom for your user functions.
def user_Initialize():
    print("User Initialization Called")
            
# Put your user functions starting here.
#def ThisIsMyFunction():
#   print("This is my function")
#   return 0
