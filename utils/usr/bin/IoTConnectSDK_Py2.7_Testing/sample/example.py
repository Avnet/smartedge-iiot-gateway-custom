
import sys
import os.path
import os
import httplib
from os import environ
from iotconnect import IoTConnectSDK
import json
import time
import socket
import configparser
import wget
from datetime import datetime

from urlparse import urlparse

AUTH_BASEURL = ""
TEMPLATE_BASEURL= ""
DEVICE_BASEURL= ""

ACCESS_TOKEN = None
uniqueId = 0
cpId = None  
my_config_parser_dict = {}
my_sensor_dict = {}
sdk = None


def service_call(method, url, header=None, body=None):
    try:
        parsed_uri = urlparse(url)
        scheme = parsed_uri.scheme
        host = parsed_uri.hostname
        port = parsed_uri.port
        path = parsed_uri.path

        if parsed_uri.query:
            path = '%s?%s' % (path, parsed_uri.query)
        
        if port == None:
            if scheme == "http":
                conn = httplib.HTTPConnection(host)
            else:
                conn = httplib.HTTPSConnection(host)
        else:
            if scheme == "http":
                conn = httplib.HTTPConnection(host, port)
            else:
                conn = httplib.HTTPSConnection(host, port)
        
        if body == None:
            if header != None:
                conn.request(method, path, headers=header)
            else:
                conn.request(method, path)
        
        if body != None:
            body = json.dumps(body)
            if header != None:
                conn.request(method, path, body, headers=header)
            else:
                conn.request(method, path, body)
        
        response = conn.getresponse()
        data = None
        if response.status == 200:
            data = json.loads(response.read())
        conn.close()
        return data
    except Exception as ex:
        print(ex)
        return None

def get_auth(username, password, solution_key):
    try:
        access_token = None
        data = None
        authToken = service_call("GET", AUTH_BASEURL + "/auth/basic-token")
        if authToken <> None:
            data = str(authToken["data"])
        if data <> None:
            body = {}
            body["username"] = username
            body["password"] = password
            header = {
                "Content-type": "application/json",
                "Accept": "*/*",
                "Authorization": 'Basic %s' % data,
                "Solution-key": solution_key
            }
            data = service_call("POST", AUTH_BASEURL + "/auth/login", header, body)
            if data != None:
                access_token = str('Bearer %s' % data["access_token"])
        return access_token
    except:
        return None

def get_attribute_data_type():
    try:
        header = {
            "Content-type": "application/json",
            "Accept": "*/*",
            "Authorization": ACCESS_TOKEN
        }

        datatype = None
        response = service_call("GET", TEMPLATE_BASEURL + "/device-template/datatype", header)
        if response != None and response["data"] != None and len(response["data"]) > 0:
            datatype = {}
            for d in response["data"]:
                datatype[d["name"]] = d["guid"]
        if len(datatype) == 0:
            return None
        else:
            return datatype
    except:
        return None

def get_template(searchText):
    try:
        header = {
            "Content-type": "application/json",
            "Accept": "*/*",
            "Authorization": ACCESS_TOKEN
        }

        templates = []
        response = service_call("GET", TEMPLATE_BASEURL + "/device-template?searchText=%s" % searchText, header)
        if response != None and response["data"] != None and len(response["data"]) > 0:
            templates = response["data"]
        
        if len(templates) > 0:
            return templates[0]
        else:
            return None
    except:
        return None

def get_access_token():
    global my_config_parser_dict
    AUTH_BASEURL = my_config_parser_dict["CloudSystemControl"]["http_auth_token"]
    TEMPLATE_BASEURL = my_config_parser_dict["CloudSystemControl"]["http_device_template"]
    DEVICE_BASEURL= my_config_parser_dict["CloudSystemControl"]["http_device_create"]
    username = my_config_parser_dict["CloudSystemControl"]["username"]
    password = my_config_parser_dict["CloudSystemControl"]["password"]
    solution_key = my_config_parser_dict["CloudSystemControl"]["solution-key"]

    #print(AUTH_BASEURL)
    #print(TEMPLATE_BASEURL)
    #print(DEVICE_BASEURL)
    #print(username)
    #print(password)
    #print(solution_key)
    ACCESS_TOKEN = get_auth(username, password, solution_key)
    if ACCESS_TOKEN == None:
        print("authentication failed")
        return None

def new_template():
    get_access_token()
    template_name = "NewTemp" #Note: Template Name should not be more than 10 characters
    header = {
        "Content-type": "application/json",
        "Accept": "*/*",
        "Authorization": ACCESS_TOKEN
    }
    template = get_template(template_name)
    if template != None:
        print("Device template already exist...")
        return
    #---------------------------------------------------------------------
    # Create new template
    deviceTemplateGuid = None
    template = []
    body = {
        "name": template_name,
        "description": "",
        "firmwareguid": "",
        "code": template_name,
        "isEdgeSupport": False,
        "authType": 4, # TPM only
    }   
    response = service_call("POST", TEMPLATE_BASEURL + "/device-template", header, body)
    if response != None and response["data"] != None and len(response["data"]) > 0:
        deviceTemplateGuid = str(response["data"][0]["deviceTemplateGuid"])
    
    if deviceTemplateGuid == None:
        print("Failed to create device template...")
        return
    return deviceTemplateGuid

def new_object(Name, deviceTemplateGuid):
    # need global dictionary of this stuff!!!!!!!!!!!!!!
    # Create Attribute
    # Attribute = "Temperature"
    # TODO ADD Passed in type.
    body = {
        "localName": Name,
        "deviceTemplateGuid": deviceTemplateGuid,
        "dataTypeGuid": datatype["NUMBER"]
    }   
    response = service_call("POST", TEMPLATE_BASEURL + "/template-attribute", header, body)
    if response != None and response["data"] != None:
        print(response["message"])

def delete_object(Name, deviceTemplateGuid):
    #??? !!!!!!!!!!!!!!!!
    if len(attributes) > 0:
        print("Total Attributes : " + str(len(attributes)))
        for attr in attributes:
            attributeGuid = str(attr["guid"])
            response = service_call("DELETE", TEMPLATE_BASEURL + "/template-attribute/%s" % attributeGuid, header)
            if response != None and response["data"] != None:
                print(response["message"])
    
  
def callbackMessage(msg):
    global sdk
    if msg != None and len(msg.items()) != 0:
        cmdType = msg["cmdType"]
        #print(cmdType)
        #if msg["cmdType"] != None else None
        data = msg["data"]
        #if msg["data"] != None else None
        # For OTA updates
        if cmdType == "0x02" and data != None:
	    print(msg)
            print(str(msg['data']['ack']))
            print(str(msg['data']['ackId']))
            print(str(msg['data']['command']))
            print(str(msg['data']['uniqueId']))
	    mystring=str(msg['data']['command'])
            if [ mystring.split(" ")[0] == "ota" ]:
                #print("wget " + mystring.split(" ")[1])	
	        wget.download(mystring.split(" ")[1])
                filename=mystring.split(" ")[1]
	        #print("Split 0 " + filename.split("/")[0])
	        #print("Split 1 " + filename.split("/")[1])
	        #print("Split 2 " + filename.split("/")[2])
	        #print("Split 3 " + filename.split("/")[3])
	        #print("Split 4 " + filename.split("/")[4])
                file = filename.split("/")[4]
		file = file[0:40]
		#print("File downloaded " + file) 		
                cmd = "sudo mv " + file + " install.gz "	     
                os.system(cmd)
                cmd = "sudo gunzip -c install.gz >install"
                os.system(cmd)
                cmd = "sudo tar xf install"
                os.system(cmd)
	        os.system("sudo chmod 777 updates/install.sh")
                os.system("sudo ./updates/install.sh")
                print("GUID")
		print(msg['data']['guid'])
		header = {
  			"guid":msg['data']['guid'],
			"st":3,
			"msg":"OK"
		} 
		sdk.SendACK(11, header)
        # if not OTA then everything else send to user_callbackMessage
        if cmdType != "0x02":
            globals()['user_callbackMessage'](msg)    

def CloudConfigureDevice():
    global ACCESS_TOKEN,AUTH_BASEURL,TEMPLATE_BASEURL,DEVICE_BASEURL
    global my_config_parser_dict, my_sensor_dict
    global uniqueId
    #QA API
    AUTH_BASEURL = my_config_parser_dict["CloudSystemControl"]["http_auth_token"]
    TEMPLATE_BASEURL = my_config_parser_dict["CloudSystemControl"]["http_device_template"]
    DEVICE_BASEURL= my_config_parser_dict["CloudSystemControl"]["http_device_create"]
    username = my_config_parser_dict["CloudSystemControl"]["username"]
    password = my_config_parser_dict["CloudSystemControl"]["password"]
    solution_key = my_config_parser_dict["CloudSystemControl"]["solution-key"]


    #print(AUTH_BASEURL)
    #print(TEMPLATE_BASEURL)
    #print(DEVICE_BASEURL)
    #print(username)
    #print(password)
    #print(solution_key)
    ACCESS_TOKEN = get_auth(username, password, solution_key)
    if ACCESS_TOKEN == None:
        print("authentication failed")
        return
    #---------------------------------------------------------------------
    file = open('/usr/bin/tmp0.txt')
    template_name = file.readline()
    file.close()
    #template_name = my_config_parser_dict["CloudSystemControl"]["template_name"]
    #"NewTemp3" #Note: Template Name should not be more than 10 characters
    header = {
        "Content-type": "application/json",
        "Accept": "*/*",
        "Authorization": ACCESS_TOKEN
    }
    #---------------------------------------------------------------------
    # Get template attribute by searchText
    template = get_template(template_name)
    if template != None:
        print("Device template already exist...")
        return
    #---------------------------------------------------------------------
    # Create new template
    deviceTemplateGuid = None
    template = []
    body = {
        "name": template_name,
        "description": "",
        "firmwareguid": "",
        "code": template_name,
        "isEdgeSupport": False,
        "authType": 4, # TPM only
    }   
    response = service_call("POST", TEMPLATE_BASEURL + "/device-template", header, body)
    if response != None and response["data"] != None and len(response["data"]) > 0:
        deviceTemplateGuid = str(response["data"][0]["deviceTemplateGuid"])
    
    if deviceTemplateGuid == None:
        print("Failed to create device template...")
        return
    
    header = {
        "Content-type": "application/json",
        "Accept": "*/*",
        "Authorization": ACCESS_TOKEN
    }

    # Get attribute data types
    datatype = None
    response = service_call("GET", TEMPLATE_BASEURL + "/device-template/datatype", header)
    if response != None and response["data"] != None and len(response["data"]) > 0:
        datatype = {}
        for d in response["data"]:
            datatype[d["name"]] = d["guid"]
    
    if len(datatype) == 0:
        return

#    attributes = []
#    response = service_call("GET", TEMPLATE_BASEURL + "/template-attribute/%s" #% deviceTemplateGuid, header)
#    if response != None and response["data"] != None and len(response["data"]) > 0:
#        attributes = response["data"]
#    print(attributes)
    
    # Create Attribute
    # Attribute = "Temperature"

    count = int(my_config_parser_dict["CloudSystemControl"]["defaultobjectcount"])
    #section = "CloudSDKDefaultObject"
    while (count != 0):
        body = {
            "localName": my_config_parser_dict["CloudSDKDefaultObject"+str(count)]["name"],
            "deviceTemplateGuid": deviceTemplateGuid,
            "dataTypeGuid": datatype[my_config_parser_dict["CloudSDKDefaultObject"+str(count)]["value"]]
        }   
        print("Adding Object " + my_config_parser_dict["CloudSDKDefaultObject"+str(count)]["name"])
        response = service_call("POST", TEMPLATE_BASEURL + "/template-attribute", header, body)
        if response != None and response["data"] != None:
            print(response["message"])
            my_sensor_dict[my_config_parser_dict["CloudSDKDefaultObject"+str(count)]["name"]] = my_config_parser_dict["CloudSDKDefaultObject"+str(count)]["usepythoninterface"]
            print(my_sensor_dict)
        count = count - 1

    print("Added Temperature")
    # get attributes first
    header = {
        "Content-type": "application/json",
        "Accept": "*/*",
        "Authorization": ACCESS_TOKEN
    }
    attributes = []
    response = service_call("GET", TEMPLATE_BASEURL + "/template-attribute/%s" % deviceTemplateGuid, header)
    if response != None and response["data"] != None and len(response["data"]) > 0:
        attributes = response["data"]
    
    if len(attributes) > 0:
        print("Total Attributes : " + str(len(attributes)))
        for attr in attributes:
            print(attr)
            attributeGuid = str(attr["guid"]) 
            if (str(attr["localName"]) == "Temperature"):
                # delete this one.
                response = service_call("DELETE", TEMPLATE_BASEURL + "/template-attribute/%s" % attributeGuid, header)
                if response != None and response["data"] != None:
                    print(response["message"])
                    print("Deleted Temperature")
                else:
                    print("None")

    file_handle = open('/usr/bin/tmp3.txt', 'r')
    line = file_handle.readline()
    endorsementKey = line
    print(endorsementKey)
    file_handle.close()
    header = {
        "Content-type": "application/json",
        "Authorization": ACCESS_TOKEN
    }
    entityguid = my_config_parser_dict["CloudSystemControl"]["entity_guid"]
    entityguid = str(entityguid)
    body = {
	"deviceTemplateGuid":deviceTemplateGuid,
	"displayName":"MyDevice",
	"endorsementKey":endorsementKey,
	"entityGuid":entityguid,
	"note":"test",
	"uniqueID":uniqueId
    }   
    print(entityguid)
    print(ACCESS_TOKEN)
    print(TEMPLATE_BASEURL)
    print(header)
    print(body)
    response = service_call("POST", TEMPLATE_BASEURL + "/device", header, body)
    if response != None and response["data"] != None and len(response["data"]) > 0:
        print(response["message"])
        print("enrolled")
    else:
        print("enroll failed")
        print(response["message"])
    
    print("Done")

def CloudSetupObjects():
    global ACCESS_TOKEN,AUTH_BASEURL,TEMPLATE_BASEURL,DEVICE_BASEURL
    global my_config_parser_dict, my_sensor_dict
    global uniqueId
    #QA API
    AUTH_BASEURL = my_config_parser_dict["CloudSystemControl"]["http_auth_token"]
    TEMPLATE_BASEURL = my_config_parser_dict["CloudSystemControl"]["http_device_template"]
    DEVICE_BASEURL= my_config_parser_dict["CloudSystemControl"]["http_device_create"]
    username = my_config_parser_dict["CloudSystemControl"]["username"]
    password = my_config_parser_dict["CloudSystemControl"]["password"]
    solution_key = my_config_parser_dict["CloudSystemControl"]["solution-key"]


    #print(AUTH_BASEURL)
    #print(TEMPLATE_BASEURL)
    #print(DEVICE_BASEURL)
    #print(username)
    #print(password)
    #print(solution_key)
    ACCESS_TOKEN = get_auth(username, password, solution_key)
    if ACCESS_TOKEN == None:
        print("authentication failed")
        return
    #---------------------------------------------------------------------
    file = open('/usr/bin/tmp0.txt')
    template_name = file.readline()
    file.close()
    #template_name = my_config_parser_dict["CloudSystemControl"]["template_name"]
    #"NewTemp3" #Note: Template Name should not be more than 10 characters
    header = {
        "Content-type": "application/json",
        "Accept": "*/*",
        "Authorization": ACCESS_TOKEN
    }
    #---------------------------------------------------------------------
    # Get template attribute by searchText
    template = get_template(template_name)
    if template != None:
        print("Device template exists...")
    else:
        print("Device template does not exist Configuring and Registering Device on Cloud!")
        CloudConfigureDevice()
    #---------------------------------------------------------------------
    # Get attribute data types
    datatype = None
    response = service_call("GET", TEMPLATE_BASEURL + "/device-template/datatype", header)
    if response != None and response["data"] != None and len(response["data"]) > 0:
        datatype = {}
        for d in response["data"]:
            datatype[d["name"]] = d["guid"]
    
    #print(template)
    #print(template['guid'])
    deviceTemplateGuid = template['guid']
    # get attributes first
    header = {
        "Content-type": "application/json",
        "Accept": "*/*",
        "Authorization": ACCESS_TOKEN
    }
    attributes = []
    response = service_call("GET", TEMPLATE_BASEURL + "/template-attribute/%s" % deviceTemplateGuid, header)
    if response != None and response["data"] != None and len(response["data"]) > 0:
        attributes = response["data"]
    
    count = int(my_config_parser_dict["CloudSystemControl"]["defaultobjectcount"])
    #print("Object count " + count)
    #section = "CloudSDKDefaultObject"
    #while (count != 0):
    #print(attributes)
    for name in my_sensor_dict:
        create = 0
        #print(name)
        for attr in attributes:
            if (attr["localName"] == name):
                create = 1
		print("Exists " + name);
        if (create == 0):
    	     #print("Creating")
             deviceTemplateGuid = template['guid']
             body = {
                 "localName": name, 
                 "deviceTemplateGuid": deviceTemplateGuid,
                 "dataTypeGuid": datatype[my_config_parser_dict["CloudSDKDefaultObject"+str(count)]["value"]]
             }   
             #print("Creating Attribute " + name) 
             response = service_call("POST", TEMPLATE_BASEURL + "/template-attribute", header, body)
             if response != None and response["data"] != None:
                 #print(response["message"])
                 print("Created " + name)
             else:
                 print("Couldn't Create Attribute " + name)
    #TODO delete ones not in my dictionary
    for attr in attributes:
        delete = 0
        for name in my_sensor_dict:
            if (attr["localName"] == name):
                print("")
                delete = 1
        if (delete == 0):
            print(attr)
            attributeGuid = str(attr["guid"]) 
            #if (str(attr["localName"]) == "Temperature"):
            # delete this one.
            response = service_call("DELETE", TEMPLATE_BASEURL + "/template-attribute/%s" % attributeGuid, header)
            if response != None and response["data"] != None:
                print(response["message"])
                print("Deleting " + attr["localName"])
            else:
                print("None Deleted")
            
    print("Attributes synced with Cloud")    

def GetTheTemp():
    file_handle = open('/sys/class/thermal/thermal_zone0/temp', 'r')
    line = file_handle.readline()
    CpuTemperature =  float(line)/1000
    file_handle.close()
    return(CpuTemperature)

def GetTheFreq():
    file_handle = open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq', 'r')
    line = file_handle.readline()
    CpuFrequency = int(line)/100000
    file_handle.close()
    return(CpuFrequency)

def SetupDigitalInputs():
    if os.path.isdir("/sys/class/gpio/gpio200"):
        print("") 
    else:
    	os.system("echo 200 >/sys/class/gpio/export")
        os.system("echo 202 >/sys/class/gpio/export")
        os.system("echo 204 >/sys/class/gpio/export")
        os.system("echo 206 >/sys/class/gpio/export")
    

def GetDigitalInput1():
    #print("Get Digital input 1")
    file = open('/sys/class/gpio/gpio200/value','r')
    value = file.readline()
    file.close()
    return value

def GetDigitalInput2():
    #print("Get Digital input 2")
    file = open('/sys/class/gpio/gpio202/value','r')
    value = file.readline()
    file.close()
    return value

def GetDigitalInput3():
    #print("Get Digital input 3")
    file = open('/sys/class/gpio/gpio204/value','r')
    value = file.readline()
    file.close()
    return value

def GetDigitalInput4():
    #print("Get Digital input 4")    
    file = open('/sys/class/gpio/gpio206/value','r')
    value = file.readline()
    file.close()
    return value
    
def main(argv):
    try:
        global my_config_parser_dict
	global cpId 
        global uniqueId
	execfile("user_functions.py",globals())
        globals()['user_Initialize']()    
        SetupDigitalInputs()
        #print(GetDigitalInput1())
        #print(GetDigitalInput2())
        #print(GetDigitalInput3())
        #print(GetDigitalInput4())
        global sdk
        #print(globals())
	file_handle = open('/usr/bin/tmp4.txt', 'r')
        line = file_handle.readline()
        uniqueId = line
        #print(uniqueId)
        file_handle.close()
        config = configparser.ConfigParser()

        config.read('IoTConnectSDK.conf')
        my_config_parser_dict = {s:dict(config.items(s)) for s in config.sections()}
        scopeId = my_config_parser_dict["CloudSDKConfiguration"]["scopeid"]
        env = my_config_parser_dict["CloudSDKConfiguration"]["env"]
	print("Opening cpid file")
        line = ""
	f = open('/usr/bin/IoTConnectSDK_Py2.7_Testing/sample/cpid.txt', 'r')
        line = f.readline()
	f.close()
        cpId = line
        print(uniqueId)
        print(scopeId)
        print(env)
        print(cpId)
        #CloudConfigureDevice()
        count = int(my_config_parser_dict["CloudSystemControl"]["defaultobjectcount"])
        #section = "CloudSDKDefaultObject"
        while (count != 0):
            my_sensor_dict[my_config_parser_dict["CloudSDKDefaultObject"+str(count)]["name"]] = my_config_parser_dict["CloudSDKDefaultObject"+str(count)]["usepythoninterface"]
            #print(my_sensor_dict)
            count = count - 1
        #print(my_sensor_dict)
        CloudSetupObjects()
        DefaultDelay = my_config_parser_dict["CloudSystemControl"]["defaultsenddelayseconds"]
        print("DefaultDelay = " + DefaultDelay)
        with IoTConnectSDK(cpId, uniqueId, scopeId, callbackMessage, env) as sdk:
	    os.system("sudo touch /tmp/iotconnect.txt")
            input = 'y'
            while input == 'y':
               data = {}
               attributes = sdk.GetAttributes()
               #print(attributes)
               if len(attributes) > 0:
                    for obj in attributes:
                        if(obj["p"] == ""):
                            for ele in obj["d"]:   
                                #print(my_sensor_dict[ele["ln"]])
				#data[ele["ln"] 
				value = globals()[my_sensor_dict[ele["ln"]]]()
				data[ele["ln"]] = int(value)
				#print(ele["ln"])
                        else:
                            data[obj["p"]] = {}
                            for ele in obj["d"]:
                                #print(my_sensor_dict[ele["ln"]])
                                print("UNHANDLED")
				print(ele["ln"])
                    dataArray = []
                    obj = {
                        "uniqueId": uniqueId,
                        "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        "data": data
                    }
                    dataArray.append(obj)
                    sdk.SendData(dataArray)
                    time.sleep(float(DefaultDelay))
               else:
                    print("No attributes found")
                    input = "exit"
    except Exception as ex:
        print(ex.message)
	os.system("sudo rm /tmp/iotconnect.txt")
        sys.exit(0)
    except KeyboardInterrupt:
	os.system("sudo rm /tmp/iotconnect.txt")
        sys.exit(1)
    os.system("sudo rm /tmp/iotconnect.txt")
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv)
