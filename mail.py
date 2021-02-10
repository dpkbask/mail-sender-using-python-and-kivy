from kivy.app import App
import smtplib
from smtplib import *
import threading as th
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

loaded = Builder.load_file("mainstyle.kv")

server = smtplib.SMTP(host='smtp.gmail.com', port=587)
server.ehlo()
server.starttls()

class WindowManager(ScreenManager):pass

sm = WindowManager()

class Loginscreen(Screen):
    user_id  =""
    def loginThread(self,user_name,password):
        login_thread = th.Thread(
            name = "LoginThread",
            target= self.login,
            args=(user_name,password)
        )
        login_thread.start()

    def login(self,user_name,password):
       try:
           id= str(user_name)
           pwd=str(password)
           server.login(id,pwd) 
       except SMTPAuthenticationError:
           print("Username or password incorrect")
       except SMTPServerDisconnected:
           print("server disconnected")
       else:
           Loginscreen.user_id = user_name 
           print("login sucessfull")
           sm.current="ms"

class Mailscreen(Loginscreen):
    
    def sendMailThread(self,text,subject,to_emails):
        sendMailThread = th.Thread(
            name = "SendMailThread",
            target= self.sendMail,
            args=(text,subject,to_emails)
        )
        sendMailThread.start()

    def sendMail(self,text,subject,to_emails):
        msg = MIMEMultipart('alternative')
        msg['From'] = Loginscreen.user_id
        msg['To'] = to_emails
        msg['Subject'] = subject
        txt_part = MIMEText(text, 'plain')
        msg.attach(txt_part)
        msg_str = msg.as_string()
        try:
            server.sendmail(Loginscreen.user_id, to_emails, msg_str)
        except:
            print("Uable to send mail")
        else:
            print("send message")

s1 = Loginscreen(name ="ls")
s2 = Mailscreen(name ="ms")

sm.add_widget(s1)
sm.add_widget(s2)

sm.current = "ls"

class MainApp(App):
    def build(self):
	    return sm

MainApp().run()
