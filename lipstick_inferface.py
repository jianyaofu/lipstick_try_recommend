# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageDraw
from PIL import ImageTk
import face_recognition
from lipstick_web_scraping import get_lipstick_reviews
from lipstick_closest_colors import min_color_diff
from lipstick_text_mining import search_link, get_wordcloud

def UploadAction(event=None):
    global filename
    filename = filedialog.askopenfilename()
    
    if len(filename) > 0:
        image = cv2.imread(filename)
        image = cv2.resize(image,(375,300))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        label = tk.Label(image=image)
        label.image = image
        label.place(x=0, y=50)

from tkinter.colorchooser import *
def getColor():
    global r,g,b
    color = askcolor() 
    r = int(color[0][0])
    g = int(color[0][1])
    b = int(color[0][2]) 


def apply():   

    image2 = face_recognition.load_image_file(filename)
    face_landmarks_list = face_recognition.face_landmarks(image2)
    for face_landmarks in face_landmarks_list:
        pil_image = Image.fromarray(image2)
        d = ImageDraw.Draw(pil_image, 'RGBA')

        d.polygon(face_landmarks['top_lip'], fill=(r, g, b, 128))
        d.polygon(face_landmarks['bottom_lip'], fill=(r, g, b, 128))
        d.line(face_landmarks['top_lip'], fill=(r, g, b, 64), width=8)
        d.line(face_landmarks['bottom_lip'], fill=(r, g, b, 64), width=8)

        pil_image.save('1.jpg')
    output_img = cv2.imread('1.jpg')
    output_img =  cv2.resize(output_img,(375,300))
    output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)
    output_img = Image.fromarray(output_img)
    output_img = ImageTk.PhotoImage(output_img)
    label_output = tk.Label(image=output_img)
    label_output.image = output_img
    label_output.place(x=400, y=50)
    rec_list = min_color_diff(tuple([r,g,b]))
    label1['text'] =f'{rec_list[0][0]}, {rec_list[0][2]}'
    label1.bind("<Button-1>", lambda event:show_wordcloud(event,rec_list[0][0],rec_list[0][1]))
    label2['text'] = f'{rec_list[1][0]}, {rec_list[1][2]}'
    label2.bind("<Button-1>", lambda event:show_wordcloud(event,rec_list[1][0],rec_list[1][1]))
    label3['text'] = f'{rec_list[2][0]}, {rec_list[2][2]}'
    label3.bind("<Button-1>", lambda event:show_wordcloud(event,rec_list[2][0],rec_list[2][1]))
    label4['text'] = f'{rec_list[3][0]}, {rec_list[3][2]}'
    label4.bind("<Button-1>", lambda event:show_wordcloud(event,rec_list[3][0],rec_list[3][1]))
    label5['text'] = f'{rec_list[4][0]}, {rec_list[4][2]}'
    label5.bind("<Button-1>", lambda event:show_wordcloud(event,rec_list[4][0],rec_list[4][1]))

def show_wordcloud(event,brand_name, product_name):
    global label
    link = search_link(brand_name, product_name)
    print("reach here 1")
    reviews = get_lipstick_reviews(link)
    print("reach here 2")
    get_wordcloud(reviews)   
    file = 'word_cloud.jpg'
    print("reach here 3")
    if len(file) > 0:
        image = cv2.imread(file)
        image = cv2.resize(image,(375,300))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        if label is None:

            label = tk.Label(image=image)
            label.image = image
            label.place(x=400,y=350)
        else:
            label.configure(image=image)
            label.image = image
            label.place(x=400,y=350)

root = tk.Tk()
root.title('Try Lipsticks Here!')

w = 800 # width for the Tk root
h = 650 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

# create all of the main containers
top_frame = tk.Frame(root, bg='lavender', width=400, height=50, pady=3)
top_frame2 = tk.Frame(root, bg='lavender', width=200, height=50, pady=3)
top_frame3 = tk.Frame(root, bg='lavender', width=200, height=50, pady=3)
mid_frame = tk.Frame(root, bg='white', width=400, height=300, pady=3)
mid_frame2 = tk.Frame(root, bg='white', width=400, height=300, pady=3)
btm_frame_1 = tk.Frame(root, bg='light grey', width=400, height=60, pady=3)
btm_frame_2 = tk.Frame(root, bg='light grey', width=400, height=60, pady=3)
btm_frame_3 = tk.Frame(root, bg='light grey', width=400, height=60, pady=3)
btm_frame_4 = tk.Frame(root, bg='light grey', width=400, height=60, pady=3)
btm_frame_5 = tk.Frame(root, bg='light grey', width=400, height=60, pady=3)
btm_frame2 = tk.Frame(root, bg='white', width=400, height=300, pady=3)


# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, column =0,sticky="ew")
top_frame2.grid(row=0,column=1, sticky="ew")
top_frame3.grid(row=0,column=2, sticky="ew")
mid_frame.grid(row=1,column=0, rowspan = 5,columnspan=2,sticky="nsew")
mid_frame2.grid(row=1,column=1,rowspan=5,columnspan=2,sticky="nsew")
btm_frame_1.grid(row=6, column = 0,sticky="ew")
btm_frame_2.grid(row=7,column = 0,sticky="ew")
btm_frame_3.grid(row=8,column = 0,sticky="ew")
btm_frame_4.grid(row=9,column = 0,sticky="ew")
btm_frame_5.grid(row=10,column = 0,sticky="ew")
btm_frame2.grid(row=6, column = 1, rowspan = 5,columnspan=2, sticky="ew")

# create the widgets for the top frame
upload_button = tk.Button(top_frame, text='Select an image',command= UploadAction)
upload_button.grid(row=0, column=0)

color_choose_button = tk.Button(top_frame2, text='Choose a color', command=getColor)
color_choose_button.grid(row=0, column=1)
apply_button = tk.Button(top_frame3, text='Apply',command=apply)
apply_button.grid(row=0,column=2)

label = None

global label1,label2,label3,label4,label5

label1 = tk.Label(btm_frame_1,text="")
label1.grid(row=0,column=0)
label2 = tk.Label(btm_frame_2,text="")
label2.grid(row=0,column=0)
label3 = tk.Label(btm_frame_3,text="")
label3.grid(row=0,column=0)
label4 = tk.Label(btm_frame_4,text="")
label4.grid(row=0,column=0)
label5 = tk.Label(btm_frame_5,text="")
label5.grid(row=0,column=0)

root.mainloop()