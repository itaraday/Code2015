from Tkinter import *
import ttk
import tkMessageBox
from tempfile import mkstemp
import random
from string import maketrans
import tkFont
import Data as data
import tkFileDialog

def prepare(maindata, semesters, years, starting, myfield, myprov, mydest):
    try:
        semesters = int(semesters.get().strip())
        years = int(years.get().strip())
        starting = int(starting.get().strip())
        myfield = myfield.get()
        myprov = myprov.get()
        dest = mydest.get()
    except:
        print "All fields are mandatory"
        return
    if len(myprov) and len(myfield) and len(dest):
            maindata.run(semesters, years, starting, myfield, myprov, dest)
    else:
        raise Exception()

def ask_quit(root):
    if tkMessageBox.askokcancel("Quit", "You want to quit now? *sniff*"):
        root.destroy()
         
def main():   
    print "Starting!!"
    root = Tk()
    filePath = ""
    while not len(filePath):
        filePath = tkFileDialog.askdirectory(parent=root, title='folder where files are saved')
    maindata = data.dataset(filePath)
    #removing the Tkinter logo by creating a temp blank icon file
    ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
            b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
            b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            '\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

    _, ICON_PATH = mkstemp()
    with open(ICON_PATH, 'wb') as icon_file:
        icon_file.write(ICON)    
          
    root.iconbitmap(default=ICON_PATH)
    
    root.title("Code2015")
    root.protocol("WM_DELETE_WINDOW",lambda: ask_quit(root))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.resizable(0,0)
    content = Frame(root, padx=5, pady=5)
    content.grid(column=0, row=0, sticky=(N,S,E,W))
    
    Label(content, text="Please pick your location").grid(column=0, row=0, sticky=(N, S, E, W))
    provframe = Frame(content)
    x = 0
    y = 1
    provRadioButtons = {}
    myprov = StringVar()
    for prov in maindata.getprovs():
        if x > 3:
            x = 0
            y = y + 1
        provRadioButtons[prov] = Radiobutton(provframe, text=prov, variable=myprov, value=prov, indicatoron=0).grid(column=x, row=y, sticky=(N, S, E, W))
        x = x + 1
    provframe.grid(column=0, row=1, sticky=(N, S, E, W))
    
    
    Label(content, text="Please pick your field").grid(column=0, row=2, sticky=(N, S, E, W))
    fieldFrame = Frame(content)
    x = 0
    y = 1
    provRadioButtons = {}
    myfield = StringVar()
    for field in maindata.getfields():
        if x > 3:
            x = 0
            y = y + 1
        provRadioButtons[prov] = Radiobutton(fieldFrame, text=field, variable=myfield, value=field, indicatoron=0).grid(column=x, row=y, sticky=(N, S, E, W))
        x = x + 1
    fieldFrame.grid(column=0, row=3, sticky=(N, S, E, W))    

    Label(content, text="Please pick the industry you want to apply for").grid(column=0, row=4, sticky=(N, S, E, W))
    destFrame = Frame(content)
    x = 0
    y = 1
    provRadioButtons = {}
    mydest = StringVar()
    for key, field in maindata.getNAICS().iteritems():
        if x > 3:
            x = 0
            y = y + 1
        provRadioButtons[prov] = Radiobutton(destFrame, text=field, variable=mydest, value=key, indicatoron=0).grid(column=x, row=y, sticky=(N, S, E, W))
        x = x + 1
    destFrame.grid(column=0, row=5, sticky=(N, S, E, W)) 
        
    inputFrame = Frame(content, pady=10)
    Label(inputFrame, text="How many semesters per year").grid(column=0, row=0, sticky=(N, S, W))
    semesters = StringVar()
    Entry(inputFrame, textvariable=semesters).grid(column=1, row=0, sticky=(N, S, W))
    Label(inputFrame, text="How many years for your program").grid(column=0, row=1, sticky=(N, S, W))
    years = StringVar()
    Entry(inputFrame, textvariable=years).grid(column=1, row=1, sticky=(N, S, W))
    Label(inputFrame, text="What year are you starting").grid(column=0, row=2, sticky=(N, S, W))
    starting = StringVar()
    Entry(inputFrame, textvariable=starting).grid(column=1, row=2, sticky=(N, S, W))
    inputFrame.grid(column=0, row=6, sticky=(N, S, E, W))
    
    
    de=("%02x"%random.randint(0,255))
    re=("%02x"%random.randint(0,255))
    we=("%02x"%random.randint(0,255))
    code = de+re+we
    colorbg="#"+code
    #inverse color
    table = maketrans('0123456789abcdef','fedcba9876543210')
    colorfg = "#"+code.translate(table)
    helv36 = tkFont.Font(family='Helvetica', size=16, weight='bold')
    #runbtn = Button(content, background=colorbg, fg=colorfg, text="Predict the FUTURE!", command= lambda: prepare(maindata, semesters, years, starting, myfield, myprov))
    runbtn = Button(content, background=colorbg, fg=colorfg, text="Predict the FUTURE!", command= lambda: prepare(maindata, semesters, years, starting, myfield, myprov, mydest))
    runbtn['font'] = helv36
    runbtn.grid(column=0, row=8, columnspan=9, sticky=(N,S,E,W), pady=10)   
    
    root.mainloop()
    
if __name__ == '__main__':
    main() 
