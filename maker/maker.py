import curses
import cursesplus
import os
import sys
import shutil
import markdown2
from platform import system as getos
import epappdata
import random

WINDOWS = getos() == "Windows"

epappdata.register_app_name("Formhelp")
APPDATA = epappdata.AppDataFile("config") # Initialize epappdata
APPDATA.setdefault({
    "helpfolder" : None
})
APPDATA.load()

if WINDOWS:
    TEMPLOC = os.path.expandvars("%TEMP%/")
else:
    TEMPLOC = "/tmp/"

def choose_custom_help_dir(stdscr) -> str:
    x = cursesplus.filedialog.openfolderdialog(stdscr,"Choose the folder with the list of help files")
    if x is None:
        cursesplus.messagebox.showerror(stdscr,["ABORTED BY USER"])#Cancel detected
        sys.exit()
    else:
        return x

def oobe(stdscr):
    prfolder = "/".join(__file__.replace("\\","/").split("/")[0:-2])
    nhfolder = prfolder + "/helps"
    if not os.path.isdir(nhfolder):
        os.mkdir(nhfolder)
    cursesplus.messagebox.showinfo(stdscr,["Welcome to FormHelp Maker.","You have not yet configured this program for this computer.","This short walkthrough will get you ready to make helpfiles in no time."])
    cursesplus.displaymsg(stdscr,["Looking for pre-made helps folder..."],False)
    
    #cursesplus.messagebox.showinfo(stdscr,[prfolder])
    if not os.path.isdir(nhfolder):
        APPDATA["helpfolder"] = choose_custom_help_dir(stdscr)
    else:
        if cursesplus.messagebox.askyesno(stdscr,["A help folder has been found at",nhfolder,"Do you accept this?"]):
            APPDATA["helpfolder"] = nhfolder
        else:
            APPDATA["helpfolder"] = choose_custom_help_dir(stdscr)
    APPDATA.write()
    
    cursesplus.messagebox.showinfo(stdscr,["FormHELP Maker is now set up."])

def generate_temp_directory() -> str:
    rn = hex(random.randint(0,2**31))[2:]
    os.mkdir(TEMPLOC+rn)
    return TEMPLOC+rn

def main(stdscr):
    cursesplus.utils.hidecursor()
    cursesplus.displaymsg(stdscr,["FormHelp Maker"],False)
    if APPDATA["helpfolder"] is None:
        oobe(stdscr)

    while True:
        wtd = cursesplus.coloured_option_menu(stdscr,["Write Help File","Quit"],"Welcome to Formhelp maker",[["quit",cursesplus.RED],["write",cursesplus.GREEN]])
        if wtd == 1:
            break
        elif wtd == 0:
            newhelpfile(stdscr)
    cursesplus.utils.showcursor()

def newhelpfile(stdscr):
    document = ""
    wtd = cursesplus.coloured_option_menu(stdscr,["Back","Write a new help file from scratch","Import a Markdown file","Import an HTML file"])
    if wtd > 0:
        cursesplus.utils.showcursor()
        wq = cursesplus.cursesinput(stdscr,"What question does this page answer? Remember- one page per question")
        cursesplus.utils.hidecursor()
        document += f"<!--{wq}-->\n"#Add title header
        rdat = ""
        if wtd == 2:
            ftu = [["*.md","Markdown File"],["*","All Files"]]
        else:
            ftu = [["*.html","HTML File"],["*","All Files"]]
        if wtd > 1:
            infile = cursesplus.filedialog.openfiledialog(stdscr,"Choose a file to import",ftu,allowcancel=False)
            with open(infile) as f:
                tdat = f.read()
        
        if wtd == 2:
            rdat = markdown2.markdown(tdat)
        elif wtd == 3:
            if "<body>" in tdat:
                rdat = tdat.split("<body>")[1].split("</body>")[0]#Strip body tags
            else:
                rdat = tdat

        if wtd == 1:
            td = generate_temp_directory()
            with open(td+"/DATA.txt","x") as f:
                f.write(f"# {wq}\n")

            cursesplus.messagebox.showinfo(stdscr,["In the next screen, you will type in the text.","Please use MARKDOWN or PLAIN TEXT format.","When you are done, save and close the editor"])
            if WINDOWS:
                cursesplus.displaymsg(stdscr,["When you are done writing, save and close Notepad."],False)
                os.system(f"notepad {td+'/DATA.txt'}")
                with open(td+"/DATA.txt") as f:
                    rdat = markdown2.markdown(f.read())
            else:
                curses.reset_shell_mode()
                os.system(f"editor {td+'/DATA.txt'}")
                curses.reset_prog_mode()

        document += "\n" + rdat
        nsname = wq.lower().replace("?","").replace(" ","-").strip()+".html"
        if os.path.isfile(APPDATA["helpfolder"]+"/"+nsname):
            if cursesplus.messagebox.askyesno(stdscr,["A help file that answers this question already exists.","Are you sure you wish to continue?"]):
                nsname = hex(random.randint(0,2**31))[2:]+".html"#Random name if already exists
            else:
                return#Abort
        with open(APPDATA["helpfolder"]+"/"+nsname,"w+") as f:
            f.write(document)
        cursesplus.messagebox.showinfo(stdscr,["Sucessfully create helpfile!"])

curses.wrapper(main)