#import the libralies
#create 5 queues
#creating variables
#function definitions
#loop that creates threads for collecting the frames from the url provided
#the thread fetches the data from the url and puts the in  queue
#plain stream is displayed if the user entered a choice of system working as surveillance system
#face detection is done if user enters a choice to have the system work as security

import cv2 as cv
import numpy as np
import queue as q
import requests as r 
import threading as t
import imutils
import socket
import time
import webbrowser as wb
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import random

count=0
#creation of queues of infinite size to store the frames from the various cameras
ipwebcam1=q.Queue(0)
ipwebcam2=q.Queue(0)
ipwebcam3=q.Queue(0)
ipwebcam4=q.Queue(0)
ipwebcam5=q.Queue(0)
#defining the variables
q_id=1#for identifying the cameras 
ip_server_address=()#for holding ip addres of udp server created on arduino (to be used to route udp message)
url_for_camera1=""#holding url of camera 1
url_for_camera2=""#holding url for camera 2
url_for_camera3=""#for holding url for camera 3
url_for_camera4=""#for holding url for camera 4
url_for_camera5=""#for holding url for camera 5
udp_socket=""#for holding udp socket to be used to send data 

#function definitions
def send_email(filename,id):
    print(filename) 
    print(id)
    fromaddr = "tkamau047@gmail.com"
    toaddr = "tom_mburu@gmail.com"
    password="yugysssejixhglsp"  
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    # storing the senders email address   
    msg['From'] = 'tkamau047@gmail.com'  
    # storing the receivers email address  
    msg['To'] = "tom_mburu@gmail.com"
    # storing the subject  
    msg['Subject'] = "intrusion detection"
    # string to store the body of the mail 
    body = "camera number {0} detected someone!".format(id) 
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain'))  
    # open the file to be sent  
    #htfilename = "intruder.jpeg"
    attachment = open(filename, "rb")  
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream')   
    # To change the payload into encoded form 
    p.set_payload((attachment).read())  
    # encode into base64 
    encoders.encode_base64(p)    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    # attach the instance 'p' to instance 'msg' 
    msg.attach(p)   
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    s.starttls()   
    # Authentication 
    s.login(fromaddr, password)  
    # Converts the Multipart msg into a string 
    text = msg.as_string()   
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text)   
    # terminating the session 
    s.quit()   



def facedetection(ID):
    def detect(frame):
        
        gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        face_cascade=cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        #face_cascade=cv.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces=face_cascade.detectMultiScale(gray,1.04,4)
        for (x,y,w,h) in faces:
            cv.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
            random_number=random.randint(0,100)
            filename="detected{0}.png".format(random_number)
            cv.imwrite(filename,frame)
            #send_data_to_arduino(ID)
            #send_email(filename,ID)
            
                
            
        cv.imshow(f"detected{ID} ",frame)
        
            
    if ID==1:
        while 1:
            img_q1=imutils.resize(ipwebcam1.get(),width=500,height=500)
            detect(img_q1)
            
            
            if cv.waitKey(1)&0xFF==ord("q"):
                break
    if ID==2:
        while 1:
            img_q2=imutils.resize(ipwebcam2.get(),width=500,height=500)
            detect(img_q2)
            if cv.waitKey(1)&0xFF==ord("q"):
                break
    if ID==3:
        while 1:
            img_q3=imutils.resize(ipwebcam3.get(),width=500,height=500)
            detect(img_q3)
            if cv.waitKey(1)&0xFF==ord("q"):
                break
    if ID==4:
        while 1:
            img_q4=imutils.resize(ipwebcam4.get(),width=500,height=500)
            detect(img_q4)
            if cv.waitKey(1)&0xFF==ord("q"):
                break
    if ID==5:
        while 1:
            img_q4=imutils.resize(ipwebcam1.get(),width=500,height=500)
            detect(img_q4)
            if cv.waitKey(1)&0xFF==ord("q"):
                break
    cv.destroyAllWindows()
    

        
def create_udp_socket():
    try:
         udp_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#CREATING UDP SOCKET
         global udp_socket
         udp_socket=udp_client
         print("communication socket with arduino created succesfully ")
    except:
        print("socket creation failed..")
    ip=input("enter ip address given by arduino udp server  ")
    port=int(input("enter port number of arduino udp server  "))
    global ip_server_address
    ip_server_address=(ip,port)
    print("ip address of udp server is:",ip_server_address)
    return  


def send_data_to_arduino(id_for_url):
    if id_for_url==1:
        udp_socket.sendto(url_for_camera1.encode(),ip_server_address)
    if id_for_url==2:
        udp_socket.sendto(url_for_camera2.encode(),ip_server_address)
    if id_for_url==3:
        udp_socket.sendto(url_for_camera3.encode(),ip_server_address)
    if id_for_url==4:
        udp_socket.sendto(url_for_camera4.encode(),ip_server_address)
    if id_for_url==5:
        udp_socket.sendto(url_for_camera5.encode(),ip_server_address)
    return

    
def displayplainvideo(ID):
    if ID==1:
        while 1:
            img_q1=imutils.resize(ipwebcam1.get(),width=500,height=500)
            cv.imshow("phone cam number 1",img_q1)
            if cv.waitKey(1)&0xFF==ord("q"):
                break
    if ID==2:
        while 1:
            img_q2=imutils.resize(ipwebcam2.get(),width=500,height=500)
            cv.imshow("phone cam number 2",img_q2)
            if cv.waitKey(1)&0xFF==ord("q"):
                break
    if ID==3:
        while 1:
            img_q3=imutils.resize(ipwebcam3.get(),width=500,height=500)
            cv.imshow("phone cam number 3",img_q3)
            if cv.waitKey(1)&0xFF==ord("q"):
                break
    if ID==4:
        while 1:
            img_q4=imutils.resize(ipwebcam4.get(),width=500,height=500)
            cv.imshow("phone cam number 4",img_q4)
            if cv.waitKey(1)&0xFF==ord("q"):
                break
    if ID==5:
        while 1:
            img_q5=imutils.resize(ipwebcam1.get(),width=500,height=500)
            cv.imshow("phone cam number 5",img_q5)
            if cv.waitKey(1)&0xFF==ord("q"):
                break
    cv.destroyAllWindows()#release windows and memeory used to show the frames
    return

def obtainstream_from_ipcam(id,url,choice):
    
    def selection(select,id):
        print("hello there")
        time.sleep(1)#to give some time to fetch frames from the webcam
        if select=="1":
            thread1=t.Thread(target=displayplainvideo,args=(id,),daemon=False)
            thread1.start()
        if select=="2":
            thread1=t.Thread(target=facedetection,args=(id,),daemon=False)
            thread1.start()
        
    
    thr=t.Thread(target=selection,args=(choice,id),daemon=False)
    thr.start() 
   #while loop to continuously fetch the data from the url
    while 1:
            #imgresp=r.get(url,verify=False)
            imgresp=r.get(url)
            imgarr=np.array(bytearray(imgresp.content),dtype=np.uint8)
            img=cv.imdecode(imgarr,-1)
            if id==1:
                ipwebcam1.put(img)
            elif(id==2):
                ipwebcam2.put(img)
            elif(id==3):
                ipwebcam3.put(img)
            elif(id==4):
                ipwebcam4.put(img)
            elif(id==5):
                ipwebcam5.put(img)

def main():
  while 1:
    global q_id
    steps=f"follow following steps to obtain image url from ip webcamera {q_id}".title()
    print(f"camera number {q_id}")
    user_info=f""""{steps}
            1.enter the url given by ip webcam in the following prompt
            2.from the rendered page on the browser,click on 'javascript' on viewer row
            3.A live stream display will pop up.
            4.place the cursor within the display and right click on it
            5.scroll down on the on the menu that is given on right clicking
            6.select and copy on 'copy image address' option 
            7.paste the copied url on the following prompt
                THANK YOU"""
    print(user_info)
    ip_web_cam_url=input("enter the ip web server url")
    wb.open_new_tab(ip_web_cam_url)
    url=input("enter page address ")
        
        
    URL=str(url)
    menu=""""
                 ...........menu.........
        1. press 1 and then enter key for surveillance(plain stream from camera)
        2. press 2 and then enter key to start security system(face detection)"""
    print(menu)
    choice=input("enter choice")
    thread0=t.Thread(target=obtainstream_from_ipcam,args=(q_id,URL,choice),daemon=False)
    thread0.start()
    if q_id==1:
        global url_for_camera1
        arduino_url=URL.split("s")
        arduino_url_data=arduino_url[0].rstrip("s")
        url_for_camera1=arduino_url_data+"one"
        print("arduino info:",url_for_camera1)
    if q_id==2:
        global url_for_camera2
        arduino_url=URL.split("s")
        arduino_url_data=arduino_url[0].rstrip("s")
        url_for_camera2=arduino_url_data+"two"
        print("arduino info:",url_for_camera2)
    if q_id==3:
        global url_for_camera3
        arduino_url=URL.split("s")
        arduino_url_data=arduino_url[0].rstrip("s")
        url_for_camera3=arduino_url_data+"three"
        
        print("arduino info:",url_for_camera3)
    if q_id==4:
        global url_for_camera4
        arduino_url=URL.split("s")
        arduino_url_data=arduino_url[0].rstrip("s")
        url_for_camera4=arduino_url_data+"four"
        print("arduino info:",url_for_camera4)
    if q_id==5:
        global url_for_camera5
        arduino_url=URL.split("s")
        arduino_url_data=arduino_url[0].rstrip("s")
        url_for_camera5=arduino_url_data+"five"
        print("arduino info:",url_for_camera5)
    time.sleep(3)
    q_id+=1
    
    
    if q_id>5:
        break

create_udp_socket() #for creating udp socket      
main()  #main function to start the system

  
