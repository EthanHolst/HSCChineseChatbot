from tkinter import *
import os

root = Tk()
root.title("HSC Chinese Conversation Bot")
root.resizable(False, False)

MyLeftPos = (root.winfo_screenwidth() - 500) / 2
myTopPos = (root.winfo_screenheight() - 300) / 2
root.geometry( "%dx%d+%d+%d" % (500, 300, MyLeftPos, myTopPos))


def sign_up():
    root.withdraw()

    global screen_signup
    screen_signup = Toplevel()
    screen_signup.title("HSC Chinese Conversation Bot - Sign Up")
    screen_signup.geometry("400x400")
    screen_signup.resizable(False, False)

    screen_signup.deiconify()
 
def log_in():
    root.withdraw()

    global screen_login
    screen_login = Toplevel()
    screen_login.title("HSC Chinese Conversation Bot - Log In")
    screen_login.geometry("400x400")
    screen_login. resizable(False, False)

    screen_login.deiconify()

btn_login = Button(root, text="Log In", command=log_in, relief=GROOVE).pack()
btn_signup = Button(root, text="Sign Up", command=sign_up, relief=GROOVE).pack()

# btn_signup.grid(column=1, row=1)
# btn_signup.grid(column=1, row=2)
 
root.mainloop()