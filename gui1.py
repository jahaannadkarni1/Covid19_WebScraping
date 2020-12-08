# Documentation for Tkinter
# https://www.tutorialspoint.com/python/python_gui_programming.htm

# Coronavirus Website
# https://www.worldometers.info/coronavirus/


# Importing Libraries
import tkinter as tk  # importing the library
from PIL import Image, ImageTk
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
# import matplotlib as mlp
# matplotlib.use('TkAgg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt


# Application Dimensions
HEIGHT = 500
WIDTH = 600


######

# Code for DataFrame from the Website

# importing a url
url = 'https://www.worldometers.info/coronavirus/'

r = requests.get(url)

soup = bs(r.content, 'html.parser')

# Scrapping the header of the website
colum = []
table = soup.select('table#main_table_countries_today th')
for i in table:
    colum.append(i.get_text())

# Scrapping the Rows
row = []
rows = soup.select('table#main_table_countries_today tr')
for i in rows:
    row.append(i.get_text())

# Formatting the Row
new_row = []
for x in row:
    y = x.replace("\n", "$").replace('+', '')
    new_row.append(y)


# Splitting relevant rows from non relavent(rows with the required columns)
main_row = []
bad_rows = []
for i in new_row[1:]:
    j = i.split("$")
    j.pop(0)
    j.pop()
    j.pop()
    if len(j) == 16:
        main_row.append(j)
    else:
        bad_rows.append(j)

# Editting the Row headers
new_colum = []
for i in colum:
    if '\n' in i:
        j = i.replace('\n', "")
        new_colum.append(j)
    else:
        new_colum.append(i)
new_colum = new_colum[:-3]

# Creating DataFrame
df = pd.DataFrame(data=main_row, columns=new_colum)

#####

# NOTE: Always create the fucntion on the top of the code
# This function grabs the string in the entry box and uses it to find the
# row in the DataFrame and returns Text in the Application
# ## Further trying to embed vizualization in the App, on the right side.
# ## Please give any suggestions if you can??


def get_stats(entry):
    try:
        name = entry.capitalize()
        new_t = pd.DataFrame(
            index=df.loc[df['Country,Other'] == str(name)].columns)
        new_t['Values'] = df.loc[df['Country,Other']
                                 == str(name)].values.reshape(-1,).tolist()

        stats_label['text'] = new_t.Values

        viz_colum = ['TotalCases', 'TotalDeaths', 'TotalRecovered',
                     'ActiveCases', 'TotalTests', 'Population']

    except:
        name = entry.upper()
        new_t = pd.DataFrame(
            index=df.loc[df['Country,Other'] == str(name)].columns)
        new_t['Values'] = df.loc[df['Country,Other']
                                 == str(name)].values.reshape(-1,).tolist()

        stats_label['text'] = new_t.Values


# NOTE: Incase of getting the entry we need to use a lambda fucntion
# which makes it easier to trigger the fucntion without initiating it before
# clicking button


# NOTE: like we have sections in html similarly we have in tkinter
#      root is the outermost and eventually it goes it. please check the Keith video
#      to have a better understanding
root = tk.Tk()  # created an instance Tk() this initializes the root window

# now to create a bigger window we need to make a Canvas class and then pack the canvas class

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# creating a background
image_2 = Image.open('CoronavirusBall_red_CDChighrez.png')
image_1 = ImageTk.PhotoImage(image_2)

backgroud_label = tk.Label(root, image=image_1)
backgroud_label.place(relheight=1, relwidth=1)


# we create a frame so that we can add differnt widgets in it hence we can use the Frame() instance
frame = tk.Frame(root, bd=3)
frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.1, anchor='n')

# created an entry box
entry = tk.Entry(frame, font='50')
entry.place(relwidth=.65, relheight=1)

# created a button, it will trigger a function when it is clicked. ALWAYS USE LAMBDA
button = tk.Button(frame, activebackground='red',
                   text='Get Info!', command=lambda: get_stats(entry.get()))
button.place(relx=.70, relwidth=.3, relheight=1)


# Created multiple frames to adjust the space for text and viz
lower_frame = tk.Frame(root, bd=3)
lower_frame.place(relx=0.5, rely=0.3, relwidth=0.8, relheight=0.65, anchor='n')

left_frame = tk.Frame(lower_frame)
left_frame.place(relx=0, rely=0, relwidth=0.48, relheight=1)

# left_1 = tk.Frame(left_frame)
# left_1.place(relwidth=0.48,relheight=1)

# left_2 = tk.Frame(left_frame)
# left_2.place(relx=0.5,relwidth=0.48,relheight=1)

right_frame = tk.Frame(lower_frame, bd=3)
right_frame.place(relx=0.52, relwidth=0.48, relheight=1)

right_up_frame = tk.Frame(right_frame, bg='blue')
right_up_frame.place(relwidth=1, relheight=0.48)

right_down_frame = tk.Frame(right_frame, bg='red')
right_down_frame.place(rely=0.50, relwidth=1, relheight=0.5)

viz_label = tk.Label(right_up_frame)
viz_label.place(relwidth=1, relheight=1)

# Returns the DataFrame
stats_label = tk.Label(left_frame)
stats_label.place(relwidth=1, relheight=1)

# stats_label_2 = tk.Label(left_2)
# stats_label_2.place(relwidth=1,relheight=1)

button.invoke()  # output: 'the function is called!'
root.bind('<Return>', lambda event=None: button.invoke())

root.mainloop()
