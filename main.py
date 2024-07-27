import os # For Filing
from tkinter import * # For the Whole Program
from tkinter import filedialog,messagebox # For Loading File and error pop ups
from matplotlib import pyplot as plt # For Charts
global Load_Flag
Load_Flag = False
def Main_Menu_Window():
    global File_Path
    MainMenu = Tk()
    MainMenu.geometry("450x400") # Width : 450 | Height : 400
    MainMenu.title("Basic Finance")
    #MainMenu.iconbitmap("Images\\logo.ico")
    MainMenu.resizable(False,False)
    MainMenu_Frame = Frame(MainMenu,bg="#38A773",height=500,width=450).pack()
    def GoTo_Record_Page():
        global Load_Flag
        Load_Flag = False
        MainMenu.destroy()
        Record_Page_Window()
    def Load_File():
        global File_Path,Load_Flag
        path_Folder = "C:\\Basic Finance\\Saved Data"
        File_Path = filedialog.askopenfilename(initialdir=path_Folder,title="Load Record",filetypes=(("Text Files","*.txt"),("All Files","*.*")))
        Load_Flag = True
        MainMenu.destroy()
        Record_Page_Window()
    def exit_App():
        MainMenu.destroy()
    MainMenuLogo = PhotoImage(file="Images\\Main_Menu_Logo.png")
    RecordPage_Button = Button(MainMenu_Frame,text="Record Page",height=2,width=10,command=GoTo_Record_Page,relief="raised",bg="light blue").place(x=190,y=250)
    MainMenuLogo_Label = Label(MainMenu_Frame,image=MainMenuLogo,width=200,height=200,bg="#38A773").place(x=125,y=15)
    Quit_Button = Button(MainMenu_Frame,text="Exit",height=2,width=10,command=exit_App,relief="raised",bg="light blue").place(x=190,y=350)
    Load_Button = Button(MainMenu_Frame,text="Load",height=2,width=10,command=Load_File,relief="raised",bg="light blue").place(x=190,y=300)
    MainMenu.mainloop()
def Record_Page_Window():
    global RecordPage,Remove_Button
    # Initialize Window
    RecordPage = Tk()
    RecordPage.geometry("750x700") # Width : 750 | Height : 700
    RecordPage.title("Basic Finance")
    #RecordPage.iconbitmap("Images\\logo.ico")
    RecordPage.resizable(False,False)
    # class
    class Data:
        def __init__(self,RName,RPrice,RProfit_or_Loss):
            self.Name = RName
            self.Price = RPrice
            self.PL = RProfit_or_Loss
        def GetName(self):
            return self.Name
        def GetPrice(self):
            return self.Price
        def GetPL(self):
            return self.PL
        def GetDataDetails(self):
            s = f"{self.Name}   {self.Price}   {self.PL}\n"
            return s
    # Color Variables
    RecordPage_Frame_Bg_Color = "#38A773"
    Heading_Bg_Color = "#666666"
    Info_Bg_Color = "#a6a8a8"
    Warning_Bg_Color = "#6fc4d8"
    # Variables
    global RecordArray,Sum_Profit
    Check_Img = PhotoImage(file="Images\\Check.png")
    Add_Img = PhotoImage(file="Images\\Add.png")
    Remove_Img = PhotoImage(file="Images\\Remove.png") 
    Edit_Img = PhotoImage(file="Images\\Edit.png")
    Close_Edit_Img = PhotoImage(file="Images\\Close Edit.png")
    Save_Img = PhotoImage(file="Images\\Save.png")
    Chart1_Img = PhotoImage(file="Images\\Chart1.png")
    #Setting_Img = PhotoImage(file="Images\\Setting.png")
    SaveAs_Img = PhotoImage(file="Images\\Save as.png")
    Detail = StringVar()
    Price = StringVar()
    Profit_Or_Loss = IntVar() # if 1 then Profit | if 2 then Loss
    InfoLabel = StringVar()
    RecordArray = [] # Containing all the details
    Net_Profit = StringVar()
    Sum_Profit = 0
    Net_Profit.set(0)
    Status_Bar = StringVar()
    # Functions
    def Load():
        global Sum_Profit,Load_Flag
        RecordPage.title(f"Basic Finance - {File_Path[28:-4]}")
        try:
            i = 0
            dot = File_Path[0]
            while dot != ".":
                i += 1
                dot = File_Path[i]
            if File_Path[i:] != ".txt":
                raise FileNotFoundError
            f = open(File_Path,"r")
            Line_Array = f.readlines()
            for i in range(len(Line_Array)):
                Profit_Or_Loss = Line_Array[i][-7:].strip()
                for j in range(len(Line_Array[i])):
                    if Line_Array[i][j] == " " and Line_Array[i][j-1] == " " and Line_Array[i][j-2] == " ":
                        try:
                            if int(Line_Array[i][j+1]) >= 0 and int(Line_Array[i][j+1]) <= 9:
                                break
                        except ValueError:
                            continue
                Detail_Name = Line_Array[i][:j].strip()
                Price = Line_Array[i][j:-7].strip()
                y = Data(Detail_Name,Price,Profit_Or_Loss)
                if y.GetPL() == "Profit":
                    Sum_Profit += eval(y.GetPrice())
                else:
                    Sum_Profit -= eval(y.GetPrice())
                RecordArray.append(y)    
            f.close()      
            Net_Profit.set(Sum_Profit)
            display_Info_Label()  
        except FileNotFoundError:
            messagebox.showerror(title="ERROR!",message="File is not compatible\nFile should be a text document")
            RecordPage.destroy()
            Load_Flag = False
            Main_Menu_Window()
        except IndexError:
            pass
    def add_Info_Text():
        global p,Sum_Profit
        d = Detail.get()
        p = Price.get()
        pl = Profit_Or_Loss.get()
        if d.strip() == "" or p.strip() == "":
            Status_Bar.set("Enter Records in Fields First!")
            return
        pl = "Profit" if pl == 1 else "Loss"
        try:
            if pl == "Profit":
                Sum_Profit += int(p)
            else:
                Sum_Profit -= int(p)
        except ValueError:
            Status_Bar.set("Price must be an Integer!")
            return
        Net_Profit.set(Sum_Profit)
        d = Data(d,p,pl)
        RecordArray.append(d)
        Status_Bar.set("")
        display_Info_Label()
    def remove_Info_Text():   
        global Sum_Profit
        if len(RecordArray) == 0:
            Net_Profit.set(0)
            Sum_Profit = 0
            Status_Bar.set("No Records in Database")
            return
        else:    
            y = RecordArray.pop()
            if y.GetPL() == "Profit":
                Sum_Profit -= int(y.GetPrice())
            else:
                Sum_Profit += int(y.GetPrice())
            Net_Profit.set(Sum_Profit)
        display_Info_Label()
    def edit_Info_Text():
        global Remove_Button2,Edit_Label,Remove_Button3
        Edit_Label = Label(RecordPage_Frame,text="Which Record do you want to Remove Enter Above",height=1,width=42,font=25,background=RecordPage_Frame_Bg_Color)
        Edit_Label.place(x=142,y=109)
        Remove_Button2 = Button(RecordPage_Frame,image=Remove_Img,height=25,width=25,command=specific_remove_Info_Text)
        Remove_Button2.place(x=610,y=110)
        Remove_Button2.bind("<Enter>",lambda e: Heading_Label.configure(text="Specified Record will be Removed from Database"))
        Remove_Button2.bind("<Leave>",lambda e: Heading_Label.configure(text="Record Page"))
        Remove_Button3 = Button(RecordPage_Frame,image=Close_Edit_Img,height=25,width=25,command=destroy_edit_Info_Text)
        Remove_Button3.place(x=650,y=110)
        Remove_Button3.bind("<Enter>",lambda e: Heading_Label.configure(text="Close this Mode"))
        Remove_Button3.bind("<Leave>",lambda e: Heading_Label.configure(text="Record Page"))
        Remove_Button.destroy()
        Edit_Button.configure(command="")
    def specific_remove_Info_Text():
        global Sum_Profit
        d = Detail.get()
        p = Price.get()
        pl = Profit_Or_Loss.get()
        pl = "Profit" if pl == 1 else "Loss" 
        if len(RecordArray) == 0:
            Status_Bar.set("No Records in Database")
        for i in range(len(RecordArray)):
            if d == RecordArray[i].GetName() and p == RecordArray[i].GetPrice() and pl == RecordArray[i].GetPL():
                y = RecordArray.pop(i)
                if pl == "Profit":
                    Sum_Profit -= int(y.GetPrice())
                else:
                    Sum_Profit += int(y.GetPrice())
                Net_Profit.set(Sum_Profit)
                break   
        display_Info_Label()
    def destroy_edit_Info_Text():
        global Remove_Button
        Edit_Label.destroy()
        Remove_Button2.destroy()
        Remove_Button3.destroy()
        Edit_Button.configure(command=edit_Info_Text)
        Remove_Button = Button(RecordPage_Frame,image=Remove_Img,height=25,width=25,command=remove_Info_Text)
        Remove_Button.place(x=60,y=110)
    def display_Info_Label():
        display = ""
        for i in range(len(RecordArray)):
            display += RecordArray[i].GetDataDetails()
        InfoLabel.set(display)
    def GoTo_Main_Menu():
        RecordPage.destroy()
        Main_Menu_Window()
    def Save_Data():
        global fileName_Entry,fileName_Label,Check_Button,Remove_Button4
        global fileName,path_Folder
        path_Folder = "C:\\Basic Finance\\Saved Data"
        if not os.path.exists(path_Folder):
            os.makedirs(path_Folder)
        fileName = StringVar()
        fileName_Entry = Entry(RecordPage_Frame,textvariable=fileName,width=15,relief="sunken")
        fileName_Entry.place(x=645,y=580)
        fileName_Label = Label(RecordPage_Frame,text="File Name:",width=10,bg=RecordPage_Frame_Bg_Color,font=25)
        fileName_Label.place(x=530,y=573)
        Check_Button = Button(RecordPage_Frame,image=Check_Img,height=25,width=25,command=Save_Data_inFile)
        Check_Button.place(x=710,y=605)
        Remove_Button4 = Button(RecordPage_Frame,image=Remove_Img,height=25,width=25,command=Destroy_Save_Mode)
        Remove_Button4.place(x=670,y=605)
        Save_Button.configure(command="")
    def Destroy_Save_Mode():
        fileName_Entry.destroy()
        fileName_Label.destroy()
        Check_Button.destroy()
        Remove_Button4.destroy()
        SaveAs_Button.configure(command=Save_Data)
    def Save_Data_inFile():
        Fn = fileName.get().strip()
        try:
            if Fn == "":
                raise OSError
            f = open(f"{path_Folder}\\{Fn}.txt","w")
            for i in range(len(RecordArray)):
                data = RecordArray[i].GetDataDetails()
                f.write(data)
            f.close()
            Status_Bar.set("File is Saved!")
        except FileNotFoundError:
            Status_Bar.set("File Not Found")
        except OSError:
            Status_Bar.set("Invalid File Name!")
    def Save():
        global Load_Flag
        try:
            if Load_Flag == False:
                raise FileExistsError
            f = open(File_Path,"w")
            for i in range(len(RecordArray)):
                data = RecordArray[i].GetDataDetails()
                f.write(data)
            f.close()
            Status_Bar.set("File is Saved!")
            Load_Flag = False
        except FileNotFoundError:
            Status_Bar.set("File Not Found")
            Load_Flag = False
        except FileExistsError:
            Status_Bar.set("File Not Saved Prevoiusly")
            Load_Flag = False
    def Show_Chart():
        profit = 0
        loss = 0
        try:
            for i in range(len(RecordArray)):
                if RecordArray[i].GetPL() == "Profit":
                    profit += int(RecordArray[i].GetPrice())
                else:
                    loss += int(RecordArray[i].GetPrice())
            Prices = [profit,loss]
            label = ["Profit","Loss"]
            color = ["#6d904f","#fc4f30"]
            plt.pie(Prices,labels=label,colors=color,autopct="%1.1f%%",wedgeprops={"edgecolor":"black"})
            plt.title("Profit and Loss")
            plt.tight_layout()
            plt.show()
        except RuntimeWarning:
            messagebox.showerror(title="ERROR!",message="No Values Entered for charts")
        except:
            messagebox.showerror(title="ERROR!",message="Restart App")
    # Heading Label 
    Heading_Label = Label(RecordPage,text="Record Page",height=2,width=900,bg=Heading_Bg_Color,font=("Arial","15"))
    Heading_Label.pack()
    # Creating Frame for Details Page 
    RecordPage_Frame = Frame(RecordPage,bg=RecordPage_Frame_Bg_Color,height=700,width=750).pack()
    # Inputs
    Detail_Entry = Entry(RecordPage_Frame,textvariable=Detail,width=50,relief="sunken").place(x=70,y=75)
    Price_Entry = Entry(RecordPage_Frame,textvariable=Price,width=25,relief="sunken").place(x=410,y=75)
    Profit_RadioButton = Radiobutton(RecordPage_Frame,text="Profit",variable=Profit_Or_Loss,value=1,background=RecordPage_Frame_Bg_Color,font=25).place(x=580,y=68)
    Loss_RadioButton = Radiobutton(RecordPage_Frame,text="Loss",variable=Profit_Or_Loss,value=2,background=RecordPage_Frame_Bg_Color,font=25).place(x=660,y=68)
    Add_Button = Button(RecordPage_Frame,image=Add_Img,height=25,width=25,command=add_Info_Text)
    Add_Button.place(x=10,y=110)
    Remove_Button = Button(RecordPage_Frame,image=Remove_Img,height=25,width=25,command=remove_Info_Text)
    Remove_Button.place(x=60,y=110)
    Edit_Button = Button(RecordPage_Frame,image=Edit_Img,height=25,width=25,command=edit_Info_Text)
    Edit_Button.place(x=110,y=110)
    Save_Button = Button(RecordPage_Frame,image=Save_Img,height=25,width=25,command=Save)
    Save_Button.place(x=660,y=543)
    SaveAs_Button = Button(RecordPage_Frame,image=SaveAs_Img,height=25,width=25,command=Save_Data)
    SaveAs_Button.place(x=710,y=543)
    Chart1_Button = Button(RecordPage_Frame,image=Chart1_Img,height=25,width=25,command=Show_Chart)
    Chart1_Button.place(x=610,y=543)
    #Setting_Button = Button(RecordPage_Frame,image=Setting_Img,height=25,width=25)
    #Setting_Button.place(x=660,y=543)
    MainMenu_Button = Button(RecordPage_Frame,text="Main Menu",height=1,width=10,command=GoTo_Main_Menu).place(x=15,y=650)
    # Labels
    Detail_Label = Label(RecordPage_Frame,text="Detail:", height=2,width=5,font=25,background=RecordPage_Frame_Bg_Color).place(x=5,y=60)
    Price_Label = Label(RecordPage_Frame,text="Price:", height=2,width=5,font=25,background=RecordPage_Frame_Bg_Color).place(x=350,y=60)
    Info_Label = Label(RecordPage_Frame,textvariable=InfoLabel,height=25,width=104,background=Info_Bg_Color,font=("Arial",9,"bold")).place(x=9,y=150)
    Net_Profit_Label1 = Label(RecordPage_Frame,text="Net Profit:",height=2,width=9,font=25,background=RecordPage_Frame_Bg_Color).place(x=5,y=532)
    Net_Profit_Label2 = Label(RecordPage_Frame,textvariable=Net_Profit,height=1,width=5,font=25,relief="sunken").place(x=110,y=543)
    Status_Bar_Label = Label(RecordPage_Frame,textvariable=Status_Bar,height=1,width=40,font=25,background=Warning_Bg_Color,relief="sunken")
    Status_Bar_Label.place(x=8,y=580)
    # Binds
    Remove_Button.bind("<Enter>",lambda e: Heading_Label.configure(text="Removes the last Record Added"))
    Remove_Button.bind("<Leave>",lambda e: Heading_Label.configure(text="Record Page"))
    Add_Button.bind("<Enter>",lambda e: Heading_Label.configure(text="Add Record to Database"))
    Add_Button.bind("<Leave>",lambda e: Heading_Label.configure(text="Record Page"))
    Edit_Button.bind("<Enter>",lambda e: Heading_Label.configure(text="Specific Record to Remove from Database"))
    Edit_Button.bind("<Leave>",lambda e: Heading_Label.configure(text="Record Page"))
    Save_Button.bind("<Enter>",lambda e: Heading_Label.configure(text="Save File"))
    Save_Button.bind("<Leave>",lambda e: Heading_Label.configure(text="Record Page"))
    SaveAs_Button.bind("<Enter>",lambda e: Heading_Label.configure(text="Save As File"))
    SaveAs_Button.bind("<Leave>",lambda e: Heading_Label.configure(text="Record Page"))
    Chart1_Button.bind("<Enter>",lambda e: Heading_Label.configure(text="Charts"))
    Chart1_Button.bind("<Leave>",lambda e: Heading_Label.configure(text="Record Page"))
    #Setting_Button.bind("<Enter>",lambda e: Heading_Label.configure(text="Settings"))
    #Setting_Button.bind("<Leave>",lambda e: Heading_Label.configure(text="Record Page"))
    Status_Bar_Label.bind("<Enter>",lambda e: Heading_Label.configure(text="Status"))
    Status_Bar_Label.bind("<Leave>",lambda e: Heading_Label.configure(text="Record Page"))
    # Checks to see if User needs to load a file or no
    global Load_Flag
    if Load_Flag == True:
        Load()
    # main loop
    RecordPage.mainloop()
Main_Menu_Window()