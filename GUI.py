import os
import gooeypie as gp
import os

app = gp.GooeyPieApp('HSC ChineseChatbot - Login and Signup')

def login_screen_1():
    screen = gp.Window(app, "Login")
    screen.set_size(500, 500)
    screen.set_resizable(False)

    # path = os.path.dirname(os.path.abspath(__file__))
    # icon_path = os.path.join(path, 'Chinese_Flag.png')
    # screen.set_icon(icon_path)

    signup_btn = gp.Button(screen, 'Sign up', signup_screen)
    login_btn = gp.Button(screen, 'Log in', login_screen_2)

    screen.set_grid(2, 1)
    screen.add(signup_btn, 1, 1, align='center', valign='bottom', margins=['auto', 'auto', 20, 'auto'])
    screen.add(login_btn, 2, 1, align='center', valign='top', margins=[20, 'auto', 'auto', 'auto'])

    screen.show()
    app.run()


def login_screen_2(event):
    login = gp.Window(app, "Login")
    login.show()
    login.set_size(500, 500)
    login.set_resizable(False)

def signup_screen(event):
    print("hello")

login_screen_1()