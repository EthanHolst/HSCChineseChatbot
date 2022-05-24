from tkinter import *
import os
 
root = Tk()
root.title("HSC Chinese Conversation Bot")
root.geometry("400x250")
root.eval('tk::PlaceWindow . center')
 
def sign_up():
    root.withdraw()

    global screen_signup
    screen_signup = Toplevel()
    screen_signup.title("HSC Chinese Conversation Bot - Sign Up")
    screen_signup.geometry("400x400")
    screen_signup.deiconify()
 
def log_in():
    root.withdraw()

    global screen_login
    screen_login = Toplevel()
    screen_login.title("HSC Chinese Conversation Bot - Log In")
    screen_login.geometry("400x400")
    screen_login.deiconify()

Button(root, text="Log In", command=log_in).pack(pady=10)
Button(root, text="Sign Up", command=sign_up).pack(pady=10)
 
root.mainloop()