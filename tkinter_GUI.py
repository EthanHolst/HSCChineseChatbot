import tkinter as tk
import customtkinter
from tkinter import *
import re

import classMethods
import globals

globals.initialise()
userID = globals.num

customtkinter.set_appearance_mode("dark") 
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("400x580")
app.resizable(False, False)
app.title("HSC Chinese Chatbot - Log In")

def login_screen():
    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.pack(pady=20, padx=20, fill="both", expand=True)

    def button_login():
        if len(inp_password.get()) == 0 and len(inp_username.get()) == 0:
            lbl_error.configure(text="Please input your details")
        else:
            account_found = classMethods.login(inp_username.get(), inp_password.get())
            if account_found == True:
                app.withdraw()
                chatbot_screen()
                globals.num = classMethods.retrieve_userID(inp_username.get())
            else:
                lbl_error.configure(text="Account not found, please try again")
                inp_username.delete(0, "end")
                inp_password.delete(0, "end")

    def button_signup():
        app.withdraw()
        signup_screen()

    lbl_login = customtkinter.CTkLabel(master=frame_1, text="Log In", text_font=('Arial',15))
    lbl_login.place(relx=0.5, rely=0.3, anchor=CENTER)

    inp_username = customtkinter.CTkEntry(master=frame_1, placeholder_text="Username")
    inp_username.place(relx=0.5, rely=0.4, anchor=CENTER)

    inp_password = customtkinter.CTkEntry(master=frame_1, placeholder_text="Password", show='*')
    inp_password.place(relx=0.5, rely=0.5, anchor=CENTER)

    btn_login = customtkinter.CTkButton(master=frame_1, command=button_login, text="Log In")
    btn_login.place(relx=0.5, rely=0.6, anchor=CENTER)

    lbl_error = customtkinter.CTkLabel(master=frame_1, text="", text_font=('Arial',10))
    lbl_error.place(relx=0.5, rely=0.7, anchor=CENTER)
    
    btn_signup = customtkinter.CTkButton(master=frame_1, text="Sign Up", command=button_signup, width=15, height=25, text_font=('Arial',8), fg_color="#1A1A1A", text_color="#E5E5E5")
    btn_signup.place(relx=0.5, rely=0.9, anchor=CENTER)
    app.mainloop()

def signup_screen():
    signupscreen = customtkinter.CTkToplevel(master=app)
    signupscreen.geometry("400x580")
    signupscreen.resizable(False, False)
    signupscreen.title("HSC Chinese Chatbot - Sign Up")

    frame_1 = customtkinter.CTkFrame(master=signupscreen)
    frame_1.pack(pady=20, padx=20, fill="both", expand=True)

    def button_login():
        signupscreen.withdraw()
        app.deiconify()
    
    def button_signup():
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, inp_email.get())):
            if classMethods.signup(inp_email.get(), inp_username.get(), inp_password.get()) == False:
                signupscreen.withdraw()
                secondary_signup_screen()
                print(classMethods.retrieve_userID(inp_username.get()))
                globals.num = classMethods.retrieve_userID(inp_username.get())
            else:
                lbl_error.configure(text="Username or email already exists")
        else:
            lbl_error.configure(text="Please enter a valid email")
    lbl_signup = customtkinter.CTkLabel(master=frame_1, text="Sign Up", text_font=('Arial',15))
    lbl_signup.place(relx=0.5, rely=0.3, anchor=CENTER)

    inp_email = customtkinter.CTkEntry(master=frame_1, placeholder_text="Email")
    inp_email.place(relx=0.5, rely=0.4, anchor=CENTER)

    inp_username = customtkinter.CTkEntry(master=frame_1, placeholder_text="Username")
    inp_username.place(relx=0.5, rely=0.5, anchor=CENTER)

    inp_password = customtkinter.CTkEntry(master=frame_1, placeholder_text="Password", show='*')
    inp_password.place(relx=0.5, rely=0.6, anchor=CENTER)

    btn_signup = customtkinter.CTkButton(master=frame_1, command=button_signup, text="Sign Up")
    btn_signup.place(relx=0.5, rely=0.7, anchor=CENTER)

    lbl_error = customtkinter.CTkLabel(master=frame_1, text="", text_font=('Arial',10))
    lbl_error.place(relx=0.5, rely=0.8, anchor=CENTER)

    btn_login = customtkinter.CTkButton(master=frame_1, text="Log In", command=button_login, width=15, height=25, text_font=('Arial',8), fg_color="#1A1A1A", text_color="#E5E5E5")
    btn_login.place(relx=0.5, rely=0.9, anchor=CENTER)

def secondary_signup_screen():
    secondary_signup = customtkinter.CTkToplevel(master=app)
    secondary_signup.geometry("400x580")
    secondary_signup.resizable(False, False)
    secondary_signup.title("HSC Chinese Chatbot - Sign Up")

    frame_details = customtkinter.CTkFrame(master = secondary_signup)
    frame_details.pack(pady=20, padx=20, fill="both", expand=True) 

    def account_type_selection(choice):
        if choice != "Select...":
            opt_accountType.configure(state=DISABLED)
            lbl_schools.place(relx=0.25, rely=0.45, anchor=CENTER)
            opt_schools.place(relx=0.5, rely=0.5, anchor=CENTER)
            lbl_error.configure(text="")
        else:
            lbl_error.configure(text="Please select a valid option")

    def school_selection(choice):
        if choice != "Select school":
            opt_schools.configure(state=DISABLED)
            if opt_accountType.get() == "Student":
                opt_teachers.place(relx=0.5, rely=0.6, anchor=CENTER)
                opt_teachers.configure(values=classMethods.retrieve_teachers(choice), state=NORMAL)
                lbl_teachers.place(relx=0.26, rely=0.555, anchor=CENTER)
            else:
                btn_signup.place(relx=0.5, rely=0.8, anchor=CENTER)
            lbl_error.configure(text="")
        else:
            lbl_error.configure(text="Please select a valid option")
        
    def teacher_selection(choice):
        if choice != "Select teacher":
            opt_teachers.configure(state=DISABLED)
            lbl_error.configure(text="") 
            if opt_accountType.get() == "Student":
                btn_signup.place(relx=0.5, rely=0.8, anchor=CENTER)
        else:
            lbl_error.configure(text="Please select a valid option")

    def button_signup():
        account_type = opt_accountType.get()
        school = classMethods.retrieve_schoolID(opt_schools.get())
        if account_type == "Student":
            teacher = classMethods.retrieve_userID(opt_teachers.get())
            classMethods.signup_secondary(account_type, school, teacher)
        else:
            classMethods.signup_secondary(account_type, school, 0)
        
        globals.num = 0
        app.deiconify()
        secondary_signup.destroy()

    lbl_details = customtkinter.CTkLabel(master=frame_details, text="Account Details", text_font=('Arial',15, "bold"))
    lbl_details.place(relx=0.5, rely=0.2, anchor=CENTER)

    lbl_accountType = customtkinter.CTkLabel(master=frame_details, text="Account Type:", text_font=('Arial',8))
    lbl_accountType.place(relx=0.29, rely=0.34, anchor=CENTER)

    lbl_teachers = customtkinter.CTkLabel(master=frame_details, text="Teachers:", text_font=('Arial',8))

    opt_accountType= customtkinter.CTkOptionMenu(master=frame_details,
                                        values=["Select...","Student", "Teacher"],
                                        command=account_type_selection,
                                        bg_color="#292929",
                                        width=220)
    opt_accountType.place(relx=0.5, rely=0.4, anchor=CENTER)

    lbl_schools = customtkinter.CTkLabel(master=frame_details, text="Schools:", text_font=('Arial',8))

    opt_teachers= customtkinter.CTkOptionMenu(master=frame_details,
                                        values=["Select teachers"],
                                        command=teacher_selection,
                                        bg_color="#292929",
                                        width=220,)

    schools = classMethods.retrieve_schools()
    opt_schools= customtkinter.CTkOptionMenu(master=frame_details,
                                        values=schools,
                                        command=school_selection,
                                        bg_color="#292929",
                                        width=220)

    btn_signup = customtkinter.CTkButton(master=frame_details, command=button_signup, text="Complete Sign Up")

    lbl_error = customtkinter.CTkLabel(master=frame_details, text="", text_font=('Arial',10))
    lbl_error.place(relx=0.5, rely=0.9, anchor=CENTER)

    app.mainloop()


    home_screen = customtkinter.CTkToplevel(master=app)
    home_screen.geometry("780x520")
    home_screen.resizable(False, False)
    home_screen.title("HSC Chinese Chatbot - Main Menu")
    home_screen.grid_columnconfigure(1, weight=1)
    home_screen.grid_rowconfigure(0, weight=1)

    global current_screen
    current_screen = 0

    global chatbot_online
    chatbot_online = False
    
    # ===== FRAME - MENU =====
    def event_chatbot():
        global current_screen
        global chatbot_online

        if current_screen == 1 and chatbot_online == False:
            current_screen = 0

            btn_chatbot.configure(state=DISABLED, fg_color="#395e9c")
            btn_change_details.configure(state=NORMAL, fg_color="#3d3d3d")

    def event_change_account_details():
        global current_screen
        global chatbot_online

        if current_screen == 0 and chatbot_online == False:
            current_screen = 1

            btn_change_details.configure(state=DISABLED, fg_color="#395e9c")
            btn_chatbot.configure(state=NORMAL, fg_color="#3d3d3d")
            # frame_chatbot.grid_remove()
            sc_details()

    frame_menu = customtkinter.CTkFrame(master=home_screen, width=180, corner_radius=0)
    frame_menu.grid(row=0, column=0, sticky="nswe")
    frame_menu.grid_rowconfigure(0, minsize=10)
    frame_menu.grid_rowconfigure(5, weight=1)
    frame_menu.grid_rowconfigure(8, minsize=20)  
    frame_menu.grid_rowconfigure(11, minsize=10)

    lbl_title = customtkinter.CTkLabel(master=frame_menu,
                                                text="HSC 中文聊天机",
                                                text_font=("Roboto Medium", -16))
    lbl_title.grid(row=1, column=0, pady=10, padx=10)

    btn_chatbot = customtkinter.CTkButton(master=frame_menu,
                                        text="Chatbot",
                                        fg_color="#395e9c",
                                        command=event_chatbot,
                                        state=DISABLED)
    btn_chatbot.grid(row=2, column=0, pady=10, padx=20)

    btn_change_details = customtkinter.CTkButton(master=frame_menu,
                                                text="Change details",
                                                fg_color=("gray75", "gray30"),
                                                command=event_change_account_details)
    btn_change_details.grid(row=3, column=0, pady=10, padx=20)

    # ===== FRAME - CHATBOT =====
    frame_chatbot = customtkinter.CTkFrame(master=home_screen)
    frame_chatbot.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
    frame_chatbot.rowconfigure((0, 1, 2, 3), weight=1)
    frame_chatbot.rowconfigure(7, weight=10)
    frame_chatbot.columnconfigure((0, 1), weight=1)
    frame_chatbot.columnconfigure(2, weight=0)

    box_textbox = Text(master=frame_chatbot,
                wrap='word',
                state='disabled',background="gray30", 
                foreground="green")
    box_textbox.grid(row=0, column=0, columnspan=1, pady=20, padx=20)

    inp_chatbot = customtkinter.CTkEntry(master=frame_chatbot,
                                            width=120,
                                            placeholder_text="Input")
    inp_chatbot.grid(row=8, column=0, columnspan=1, pady=20, padx=40, sticky="we")

    # ===== FRAME - DETAILS =====

    def sc_details():
        frame_details = customtkinter.CTkFrame(master=home_screen)
        frame_details.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        frame_details.rowconfigure((0, 1, 2, 3), weight=1)
        frame_details.rowconfigure(7, weight=10)
        frame_details.columnconfigure((0, 1), weight=1)
        frame_details.columnconfigure(2, weight=0)

        def account_type_change(choice):
            if choice != "Select type":
                opt_accountType.configure(state=DISABLED)
                opt_schools.place(relx=0.5, rely=0.5, anchor=CENTER)
                lbl_error.configure(text="")
            else:
                lbl_error.configure(text="Please select a valid option")

        def school_change(choice):
            if choice != "Select school":
                opt_schools.configure(state=DISABLED)
                if opt_accountType.get() == "Student":
                    opt_teachers.place(relx=0.5, rely=0.6, anchor=CENTER)
                    opt_teachers.configure(values=classMethods.retrieve_teachers(choice), state=NORMAL)
                else:
                    btn_signup.place(relx=0.5, rely=0.8, anchor=CENTER)
                    lbl_error.configure(text="")
            else:
                lbl_error.configure(text="Please select a valid option")

        def teacher_change(choice):
            if choice != "Select teacher":
                opt_teachers.configure(state=DISABLED)
                lbl_error.configure(text="") 
                if opt_accountType.get() == "Student":
                    btn_signup.place(relx=0.5, rely=0.8, anchor=CENTER)
            else:
                lbl_error.configure(text="Please select a valid option")

        def button_signup():
            print("Pressed")
            account_type = opt_accountType.get()
            school = classMethods.retrieve_schoolID(opt_schools.get())
            if account_type == "Student":
                teacher = classMethods.retrieve_userID(opt_teachers.get())
                classMethods.signup_secondary(account_type, school, teacher)
            else:
                classMethods.signup_secondary(account_type, school, 0)
            
            global current_screen
            current_screen = 0
            btn_chatbot.configure(state=DISABLED, fg_color="#395e9c")
            btn_change_details.configure(state=NORMAL, fg_color="#3d3d3d")
            frame_details.destroy()
        
        lbl_details = customtkinter.CTkLabel(master=frame_details, text="Change Account Details", text_font=('Arial',15, "bold"))
        lbl_details.place(relx=0.5, rely=0.2, anchor=CENTER)

        opt_accountType= customtkinter.CTkOptionMenu(master=frame_details,
                                            values=["Select type","Student", "Teacher"],
                                            command=account_type_change,
                                            bg_color="#292929",
                                            width=220)
        opt_accountType.place(relx=0.5, rely=0.4, anchor=CENTER)

        schools = classMethods.retrieve_schools()
        opt_schools= customtkinter.CTkOptionMenu(master=frame_details,
                                            values=schools,
                                            command=school_change,
                                            bg_color="#292929",
                                            width=220)

        opt_teachers= customtkinter.CTkOptionMenu(master=frame_details,
                                            values=["Select teacher"],
                                            command=teacher_change,
                                            bg_color="#292929",
                                            width=220,)

        btn_signup = customtkinter.CTkButton(master=frame_details, command=button_signup, text="Change Details")

        lbl_error = customtkinter.CTkLabel(master=frame_details, text="", text_font=('Arial',10))
        lbl_error.place(relx=0.5, rely=0.9, anchor=CENTER)

global current_screen
current_screen = 0

def chatbot_screen():
    current_screen = 0

    home_screen = customtkinter.CTkToplevel(master=app)
    home_screen.geometry("780x520")
    home_screen.resizable(False, False)
    home_screen.title("HSC Chinese Chatbot - Main Menu")
    home_screen.grid_columnconfigure(1, weight=1)
    home_screen.grid_rowconfigure(0, weight=1)

    def event_chatbot():
        pass

    def event_change_account_details():
        home_screen.destroy()
        details_screen()

    frame_menu = customtkinter.CTkFrame(master=home_screen, width=180, corner_radius=0)
    frame_menu.grid(row=0, column=0, sticky="nswe")
    frame_menu.grid_rowconfigure(0, minsize=10)
    frame_menu.grid_rowconfigure(5, weight=1)
    frame_menu.grid_rowconfigure(8, minsize=20)  
    frame_menu.grid_rowconfigure(11, minsize=10)

    lbl_title = customtkinter.CTkLabel(master=frame_menu,
                                                text="HSC 中文聊天机",
                                                text_font=("Roboto Medium", -16))
    lbl_title.grid(row=1, column=0, pady=10, padx=10)

    btn_chatbot = customtkinter.CTkButton(master=frame_menu,
                                        text="Chatbot",
                                        fg_color="#395e9c",
                                        command=event_chatbot,
                                        state=DISABLED)
    btn_chatbot.grid(row=2, column=0, pady=10, padx=20)

    btn_change_details = customtkinter.CTkButton(master=frame_menu,
                                                text="Change details",
                                                fg_color=("gray75", "gray30"),
                                                command=event_change_account_details)
    btn_change_details.grid(row=3, column=0, pady=10, padx=20)

    frame_chatbot = customtkinter.CTkFrame(master=home_screen)
    frame_chatbot.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
    frame_chatbot.rowconfigure((0, 1, 2, 3), weight=1)
    frame_chatbot.rowconfigure(7, weight=10)
    frame_chatbot.columnconfigure((0, 1), weight=1)
    frame_chatbot.columnconfigure(2, weight=0)

    box_textbox = Text(master=frame_chatbot,
                wrap='word',
                state='disabled',background="gray30", 
                foreground="green")
    box_textbox.grid(row=0, column=0, columnspan=1, pady=20, padx=20)

    inp_chatbot = customtkinter.CTkEntry(master=frame_chatbot,
                                            width=120,
                                            placeholder_text="Input")
    inp_chatbot.grid(row=8, column=0, columnspan=1, pady=20, padx=40, sticky="we")

    if current_screen == 0:
            btn_chatbot.configure(state=DISABLED, fg_color="#395e9c")
            btn_change_details.configure(state=NORMAL, fg_color="#3d3d3d")
    
    if current_screen == 1:
        btn_change_details.configure(state=DISABLED, fg_color="#395e9c")
        btn_chatbot.configure(state=NORMAL, fg_color="#3d3d3d")

    home_screen.mainloop()

def details_screen():
    current_screen = 1

    home_screen = customtkinter.CTkToplevel(master=app)
    home_screen.geometry("780x520")
    home_screen.resizable(False, False)
    home_screen.title("HSC Chinese Chatbot - Main Menu")
    home_screen.grid_columnconfigure(1, weight=1)
    home_screen.grid_rowconfigure(0, weight=1)

    def event_chatbot():
        home_screen.destroy()
        chatbot_screen()

    def event_change_account_details():
        pass

    frame_menu = customtkinter.CTkFrame(master=home_screen, width=180, corner_radius=0)
    frame_menu.grid(row=0, column=0, sticky="nswe")
    frame_menu.grid_rowconfigure(0, minsize=10)
    frame_menu.grid_rowconfigure(5, weight=1)
    frame_menu.grid_rowconfigure(8, minsize=20)  
    frame_menu.grid_rowconfigure(11, minsize=10)

    lbl_title = customtkinter.CTkLabel(master=frame_menu,
                                                text="HSC 中文聊天机",
                                                text_font=("Roboto Medium", -16))
    lbl_title.grid(row=1, column=0, pady=10, padx=10)

    btn_chatbot = customtkinter.CTkButton(master=frame_menu,
                                        text="Chatbot",
                                        fg_color="#395e9c",
                                        command=event_chatbot,
                                        state=DISABLED)
    btn_chatbot.grid(row=2, column=0, pady=10, padx=20)

    btn_change_details = customtkinter.CTkButton(master=frame_menu,
                                                text="Change details",
                                                fg_color=("gray75", "gray30"),
                                                command=event_change_account_details)
    btn_change_details.grid(row=3, column=0, pady=10, padx=20)

    frame_details = customtkinter.CTkFrame(master=home_screen)
    frame_details.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
    frame_details.rowconfigure((0, 1, 2, 3), weight=1)
    frame_details.rowconfigure(7, weight=10)
    frame_details.columnconfigure((0, 1), weight=1)
    frame_details.columnconfigure(2, weight=0)

    def account_type_change(choice):
        if choice != "Select type":
            opt_accountType.configure(state=DISABLED)
            opt_schools.place(relx=0.5, rely=0.5, anchor=CENTER)
            lbl_error.configure(text="")
        else:
            lbl_error.configure(text="Please select a valid option")

    def school_change(choice):
        if choice != "Select school":
            opt_schools.configure(state=DISABLED)
            if opt_accountType.get() == "Student":
                opt_teachers.place(relx=0.5, rely=0.6, anchor=CENTER)
                opt_teachers.configure(values=classMethods.retrieve_teachers(choice), state=NORMAL)
            else:
                btn_signup.place(relx=0.5, rely=0.8, anchor=CENTER)
                lbl_error.configure(text="")
        else:
            lbl_error.configure(text="Please select a valid option")

    def teacher_change(choice):
        if choice != "Select teacher":
            opt_teachers.configure(state=DISABLED)
            lbl_error.configure(text="") 
            if opt_accountType.get() == "Student":
                btn_signup.place(relx=0.5, rely=0.8, anchor=CENTER)
        else:
            lbl_error.configure(text="Please select a valid option")

    def button_signup():
        print("Pressed")
        account_type = opt_accountType.get()
        school = classMethods.retrieve_schoolID(opt_schools.get())
        if account_type == "Student":
            teacher = classMethods.retrieve_userID(opt_teachers.get())
            classMethods.signup_secondary(account_type, school, teacher)
        else:
            classMethods.signup_secondary(account_type, school, 0)
        
        global current_screen
        current_screen = 0
        home_screen.destroy()
        chatbot_screen()

    
    lbl_details = customtkinter.CTkLabel(master=frame_details, text="Change Account Details", text_font=('Arial',15, "bold"))
    lbl_details.place(relx=0.5, rely=0.2, anchor=CENTER)

    opt_accountType= customtkinter.CTkOptionMenu(master=frame_details,
                                        values=["Select type","Student", "Teacher"],
                                        command=account_type_change,
                                        bg_color="#292929",
                                        width=220)
    opt_accountType.place(relx=0.5, rely=0.4, anchor=CENTER)

    schools = classMethods.retrieve_schools()
    opt_schools= customtkinter.CTkOptionMenu(master=frame_details,
                                        values=schools,
                                        command=school_change,
                                        bg_color="#292929",
                                        width=220)

    opt_teachers= customtkinter.CTkOptionMenu(master=frame_details,
                                        values=["Select teacher"],
                                        command=teacher_change,
                                        bg_color="#292929",
                                        width=220,)

    btn_signup = customtkinter.CTkButton(master=frame_details, command=button_signup, text="Change Details")

    lbl_error = customtkinter.CTkLabel(master=frame_details, text="", text_font=('Arial',10))
    lbl_error.place(relx=0.5, rely=0.9, anchor=CENTER)

    if current_screen == 0:
        btn_chatbot.configure(state=DISABLED, fg_color="#395e9c")
        btn_change_details.configure(state=NORMAL, fg_color="#3d3d3d")
    
    if current_screen == 1:
        btn_change_details.configure(state=DISABLED, fg_color="#395e9c")
        btn_chatbot.configure(state=NORMAL, fg_color="#3d3d3d")

    home_screen.mainloop()

login_screen()