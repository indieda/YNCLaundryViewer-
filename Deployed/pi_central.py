#! /usr/bin/python3

from bluepy import btle
from time import sleep
from func_timeout import func_timeout, FunctionTimedOut
from func_timeout.StoppableThread import StoppableThread
from datetime import datetime
import time
import threading
import requests, os, sys, logging
from pathlib import Path
import secrets
#import telegram
#Create secrets file with bottoken.
#from secrets import bottoken

#Edit this channel to the telegram bot's channel name, retaining the @ at the front.
channel="@cendana_laundry_bot"
log_path = "/home/pi/YNCLaundryViewer-/Deployed/log.txt"
#log_path = str(Path.cwd()/"log.txt")
uptime_log_path = "/home/pi/YNCLaundryViewer-/Deployed/uptime.txt"
#uptime_log_path = str(Path.cwd()/"uptime.txt")
ync_url = "https://laundry.chuayunda.com/index"
new_url = "https://laundry.yale-nus.edu.sg/index"
test_url = "https://5b8f2c23.ngrok.io/index"
url = "https://enrixpn98m8gp.x.pipedream.net"
#"https://webhook.site/d9cae541-78e7-48de-8791-79d8eccf84d7"
#19th Jan https://webhook.site/#!/a03ad0ea-9a75-4928-bad7-e0cae58a3709/a5e58475-531e-4a0f-bc84-7bd0882c79ef/1
#20th Jan https://webhook.site/#!/d9cae541-78e7-48de-8791-79d8eccf84d7/7ed9cfff-c943-4f45-9166-1f33090c9fb1/1
cendana_addr = ['ec:24:b8:23:78:29','58:7A:62:17:B8:07','D4:F5:13:FD:C6:73','EC:24:B8:21:BA:1B','D4:F5:13:FD:C9:D7','D4:F5:13:FD:DD:51']
#ec:24 is washer 6.
washer_addr_reversed = [6,5,4,3,2,1]
washer_state_array = [set(),set(),set(),set(),set(),set()]
college = "Cendana"
time_prev = time.time()
time_exit = time.time()
time_elapsed = time.time() - time_prev
#kill = [0,0]
global i
i = 0
global l
l = "a"

def telegram_bot(msg):
    bot_token= bot_token
    bot_chatID=bot_chat_ID
    for members in bot_chatID:
        try:
            send_msg = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + members + '&parse_mode=Markdown&text=' + msg
            rs = requests.get(send_msg)
            print(rs.json())
        except:
            pass



def write_log(message):
    global f
    f = open(log_path,"a")
    try:
        t = str(datetime.now())
        write = f.write("Time of event: "+t+" Message: "+ message+"\n")
    except:
        pass
    finally:
        f.close()

def upload_to_web():
    global l
    try:
        #t = threading.Timer(180.0,upload_to_web)
        #t.daemon = True
        #t.start()
        global washer_state_array
        print(washer_state_array)
        for idx,d in enumerate(washer_state_array,0):
            if "on" in d:
            #idx = data_decoded[1]
                #response = requests.post(url,json={"Washer {} ble message: {}".format(idx,d):"Couldn't read..."})
                #response = requests.post(url , json = {"Washer {}".format(washer_addr_reversed[idx]):"On, machine is not available for use"})
                resp = requests.post(ync_url , json = {"sensorValue":188,"college":"Cendana","machineLabel":"Washer_{}".format(washer_addr_reversed[idx])})
                #resp = requests.post(new_url , json = {"sensorValue":188,"college":"Cendana","machineLabel":"Washer_{}".format(washer_addr_reversed[idx])})
                #resp2 = requests.post(test_url , json = {"sensorValue":188,"college":"Cendana","machineLabel":"Washer_{}".format(washer_addr_reversed[idx])})
                if l != "n":
                    #tele = telegram_bot("Washer {} ".format(washer_addr_reversed[idx]) + d)
                    pass
                else:
                    pass
                l = "n"
                #response2 = requests.post(ync_url , json = {"Washer 6":"On"})
                write_log("Washer {} On".format(washer_addr_reversed[idx]))
                print("Washer {}".format(idx), d ,"and Uploaded")
                #d[1] == "f"
            elif  "off" in d:
                #idx = data_decoded[1]
                #response = requests.post(url, json = {"Washer {}".format(washer_addr_reversed[idx]):"Off, machine is available for use"})
                resp = requests.post(ync_url , json = {"sensorValue":888,"college":"Cendana","machineLabel":"Washer_{}".format(washer_addr_reversed[idx])})
                #resp = requests.post(new_url , json = {"sensorValue":888,"college":"Cendana","machineLabel":"Washer_{}".format(washer_addr_reversed[idx])})
                #resp2 = requests.post(test_url , json = {"sensorValue":888,"college":"Cendana","machineLabel":"Washer_{}".format(washer_addr_reversed[idx])})
                #response2 = requests.post(ync_url , json = {'Washer 6':'Off'})
                if l != "f":
                    #tele = telegram_bot("Washer {} ".format(washer_addr_reversed[idx]) + d)
                    pass
                else:
                    pass
                l = "f"
                write_log("Washer {} Off".format(washer_addr_reversed[idx]))
                print('Washer {}'.format(idx), d ,"and Uploaded")
                #d[1] == "r"
            elif "error" in d:
                #response = requests.post(url, json = {'Washer 6':'Error, the lock light is blinking!'})
                resp = requests.post(ync_url , json = {"sensorValue":2000,"college":"Cendana","machineLabel":"Washer_{}".format(washer_addr_reversed[idx])})
                #resp = requests.post(new_url , json = {"sensorValue":2000,"college":"Cendana","machineLabel":"Washer_{}".format(washer_addr_reversed[idx])})
                #response2 = requests.post(test_url , json = {'Washer 6':'Error'})
                write_log("Washer {} Error".format(washer_addr_reversed[idx]))
                print('Washer {}'.format(idx), d ,"and Uploaded")
                if l == "r":
                    #tele = telegram_bot("Washer {} ".format(washer_addr_reversed[idx]) +str(d))
                    #bot = telegram.Bot(token=bottoken)
                    #status = bot.send_message(chat_id=channel, text = "Washer {} error".format(washer_addr_reversed[idx]), parse_mode=telegram.ParseMode.HTML)
                    #tele = telegram_bot("Washer {} ".format(washer_addr_reversed[idx]) +str(d))
                    pass
                else:
                    pass
                l = "r"
            elif ((d == "first") or (d == "second") or (d == "third") or (d == "fourth") or (d == "fifth")  or (d == "sixth")  or (d == "seventh")  or (d == "eigth")  or (d == "ninth")  or (d == "tenth")  or (d == "max")):
                response = requests.post(url,json={"Washer {} ble message: {}".format(idx,d):"Lightval"})
                telegram_bot(d)
            else:
                #kill[idx-1] = kill[idx-1] + 1
                pass
            washer_state_array[idx] = set()
    except Exception as e:
        #print(e)
        write_log(e)
        pass


os.system("rfkill block bluetooth")
time.sleep(2.0)
os.system("rfkill unblock bluetooth")
time.sleep(2.0)
print("Restarted bluetooth")
print("Starting infinite loop")
#575 is a good time, and more than that and it tends to not start.

try:
    uptime_log = open(uptime_log_path,"a")
    t = str(datetime.now())
    write = uptime_log.write(t+ " on"+"\n")
    print("Wrote to log")
except:
    print("exception in write to log")
finally:
    uptime_log.close()

#telegram bot code

#z="test on"
#if l == "a":
#    try:
#        tele = telegram_bot("Washer {} ".format(washer_addr_reversed[0])+str(z))
#    except Exception as e:
#        print(e)
#        pass
#else:
#    pass

#try:
#    telegram_bot("turning python script on - a")
#except:
#    pass
def read_ble(ble_no,i):
    try:
        print(i)
        conn = btle.Peripheral(ble_no, timeout=3.0)
        #This 0.8 seconds is really important, because it takes time for the connection data to load into the classes.
        #If we don't add it in, the likelihood of it returning "b'"x01\x02\x03\x04\x05\x00\x00\x00\x00\x00 is super high!!!""
        sleep(0.8)
        data = conn.readCharacteristic(0x0025)
        print("connected")
    #print(data.decode('utf8')+str(i))
        read_ble.data_decode = data.decode('utf8')
        print(read_ble.data_decode)
        washer_state_array[i].add(read_ble.data_decode)
        conn.disconnect()
        #read_ble.data_decode = data_decode
    except Exception as e:
        #conn.disconnect()
        print(e)
        read_ble.data_decode = "nil"
        return Exception

def functime(fun, addr,to, idxx):
    func_timeout(timeout=to,func=fun,args=(addr_i,idxx))


i=0
global lll
heh = threading.Lock()
lll = [threading.Thread(),threading.Thread(),threading.Thread(),threading.Thread(),threading.Thread(),threading.Thread()]
while (time.time() - time_exit < 575):
    try:
        for idxx,addr_i in enumerate(cendana_addr, 0):
            try:
                with heh:
                    lll[idxx] = threading.Thread(target=read_ble,args=(addr_i,idxx))
                    lll[idxx].start()
                #func_timeout(timeout=0.7,func=read_ble,args=(addr_i,idxx))
                #func_timeout(timeout=0.7,func=read_ble,args=(addr_i,idxx))
                #lll[idx] = func_timeout(timeout=0.7,func=read_ble,args=(addr_i,idxx))
                #lll[idxx].retry(timeout=2.0)
                
                    if ((read_ble.data_decode[1] == "n") or (read_ble.data_decode[1] == "f") or (read_ble.data_decode[1] == "r") or (read_ble.data_decode == "first") or (read_ble.data_decode == "second") or (read_ble.data_decode == "third") or (read_ble.data_decode == "fourth")or (read_ble.data_decode == "fifth") or (read_ble.data_decode == "sixth") or (read_ble.data_decode == "seventh") or (read_ble.data_decode == "eigth") or (read_ble.data_decode == "ninth") or (read_ble.data_decode == "tenth") or (read_ble.data_decode == "max")):
                        washer_state_array[idxx].add(read_ble.data_decode)
                        print(read_ble.data_decode+str(washer_addr_reversed[idxx]))
                        print(datetime.now())
                        write_log(read_ble.data_decode+str(washer_addr_reversed[idxx])+" "+datetime.now())
                    else:
                        pass
            #upload = threading.Thread(target=stdhandle, args = (read_ble.data_decode,i), daemon = True)
            except Exception as e:
                print(e)
                lll[idxx].join()
                pass
            except FunctionTimedOut as e:
                print(e)
                lll[idxx].join()
                pass
            time_elapsed = time.time() - time_prev
        print("stopped")
        lll[idxx].join()
            #if kill[i] > 30:
                #kill = [0,0]
                #print("restarting program")
                #os.fsync(fd)
                #os.execv(__file__, sys.argv)
        if (time_elapsed > 18):
            y = threading.Thread(upload_to_web())
            y.start()
            time_prev = time.time()
            y.join()
        i = i+1
        sleep(0.8)
        print(i)
    except Exception as e:
        print(e)
        pass



try:
    uptime_log = open(uptime_log_path,"a")
    t = str(datetime.now())
    write = uptime_log.write(t+ " off"+"\n")

#    try:
#        telegram_bot("turning python script off - b")
#    except:
#        pass

except:
    pass
finally:
    uptime_log.close()

#exit()