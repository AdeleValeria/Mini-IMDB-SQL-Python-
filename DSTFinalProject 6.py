#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import connect, sql

# for the sys.exit() method call
import sys

# import the Pygame libraries
import pygame
from pygame.locals import *

#import pandas
import pandas as pd
import pandas.io.sql as psql

#import regex
import re

# set the DB name, table, and table data to 'None'
#db_name = "DSTFinalProject"
db_name = "DSTFinalProject"
movie_title = None
time_period= None
# initialize the output with None
movie_title_return = None
director_return = None

#setting for postgreSQL
#change these globals (user name and user password) to match your settings
user_pass = "dst1234"
user_name = "postgres"

# create a class for the buttons and labels
class Button():

    # empty list for button registry
    registry = []

    # selected button (will have outline rect)
    selected = None

    # pygame RGBA colors
    light_blue = (200,255,255,1)
    dark_blue = (127,156,198,1)
    light_purple = (161,72,139,1)

    # default font color for buttons/labels is white
    def __init__(self, name, loc, color=dark_blue):

        # add button to registry
        self.registry.append(self)

        # paramater attributes
        self.name = name
        self.loc = loc
        self.color = color

        # text attr for button
        self.text = ""

        # size of button changes depending on length of text
        self.size = (int(len(self.text)*200), 200)

        # font.render(text, antialias, color, background=None) -> Surface
        self.font = font.render (
            self.name + " " + self.text, # display text
            True, # antialias on
            self.color, # font color
            #self.light_purple # background color of botton
        )

        # rect for button
        self.rect = self.font.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]

# function that connects to Postgres
def connect_postgres(db):

    # connect to PostgreSQL
    print ("\nconnecting to PostgreSQL")
    try:
        conn = connect (
            dbname = db,
            user = user_name,
            host = "localhost",
            password = user_pass
        )
    except Exception as err:
        print ("PostgreSQL Connect() ERROR:", err)
        conn = None

    # return the connection object
    return conn


# high rating work by the same director
def query1(conn):
    if movie_title== None or movie_title== '':
        return None
    SQLquery="SELECT primarytitle FROM titlebasics WHERE titlebasics.tconst IN ( SELECT tconst FROM titlecrew WHERE director1 = ( SELECT director1 FROM titlecrew WHERE tconst IN ( SELECT tconst FROM titlebasics WHERE primarytitle ILIKE \'"+str(movie_title)+"\' AND titletype='movie' ORDER BY rate(tconst) DESC LIMIT 1))OR director2 = (SELECT director1 FROM titlecrew WHERE tconst IN (SELECT tconst FROM titlebasics WHERE primarytitle ILIKE \'"+str(movie_title)+"\' AND titletype='movie' ORDER BY rate(tconst) DESC LIMIT 1))OR director3 = (SELECT director1 FROM titlecrew WHERE tconst IN (SELECT tconst FROM titlebasics WHERE primarytitle ILIKE \'"+str(movie_title)+"\' AND titletype='movie' ORDER BY rate(tconst) DESC LIMIT 1)))AND titletype='movie' ORDER BY rate(tconst) DESC LIMIT 10;"
    # instantiate a new cursor object
    print(SQLquery)
    cursor = conn.cursor()

    # (use sql.SQL() to prevent SQL injection attack)
    sql_object = sql.SQL(
        # pass SQL statement to sql.SQL() method
          SQLquery
    )

    try:
        # use the execute() method to put table data into cursor obj
        cursor.execute( sql_object )
        # use the fetchall() method to return a list of all the data
        movie_title_return = cursor.fetchall()
        # close cursor objects to avoid memory leaks
        cursor.close()
    except Exception as err:

        # print psycopg2 error and set table data to None
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
        movie_title_return = None

    return movie_title_return

# most popular director in a time period
def query2(conn):
    if time_period==None or time_period=="":
        return None
    
    try:
        from_year = time_period.split("-", 1)[0]
        to_year = time_period.split("-", 1)[1]
        SQLquery = "SELECT primaryname FROM namebasics WHERE nconst IN (SELECT titlecrew.director1 FROM titlecrew INNER JOIN titlebasics ON titlecrew.tconst=titlebasics.tconst INNER JOIN ratings ON ratings.tconst=titlebasics.tconst WHERE titlebasics.titletype='movie' AND titlecrew.director1 IS NOT NULL AND startyear BETWEEN "+str(from_year)+" AND "+str(to_year)+" UNION SELECT titlecrew.director2 FROM titlecrew INNER JOIN titlebasics ON titlecrew.tconst=titlebasics.tconst INNER JOIN ratings ON ratings.tconst=titlebasics.tconst WHERE titlebasics.titletype='movie' AND titlecrew.director2 IS NOT NULL AND startyear BETWEEN "+str(from_year)+" AND "+str(to_year)+" UNION SELECT titlecrew.director3 FROM titlecrew INNER JOIN titlebasics ON titlecrew.tconst=titlebasics.tconst INNER JOIN ratings ON ratings.tconst=titlebasics.tconst WHERE titlebasics.titletype='movie' AND titlecrew.director3 IS NOT NULL AND startyear BETWEEN "+str(from_year)+" AND "+str(to_year)+" ) ORDER BY num_votes(knownfortitles1)+num_votes(knownfortitles2)+num_votes(knownfortitles3)+num_votes(knownfortitles4)+num_votes(knownfortitles5)+num_votes(knownfortitles6)+num_votes(knownfortitles7)+num_votes(knownfortitles8) DESC LIMIT 10;"        
        print(SQLquery)
    # instantiate a new cursor object
        cursor = conn.cursor()

    # (use sql.SQL() to prevent SQL injection attack)
        sql_object = sql.SQL(
        # pass SQL statement to sql.SQL() method
            SQLquery
            )

        try:
        # use the execute() method to put table data into cursor obj
            cursor.execute( sql_object )

        # use the fetchall() method to return a list of all the data
            director_return = cursor.fetchall()
        # close cursor objects to avoid memory leaks
            cursor.close()
        except Exception as err:

        # print psycopg2 error and set table data to None
            print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
            director_return = None
        return director_return
    
    except Exception:
        director_return='Invalid Input'
        return director_return

    

"""
PYGAME STARTS HERE
"""

# initialize the pygame window
pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
# change the caption/title for the Pygame app
pygame.display.set_caption("2019 DST2 Final Project Adele and Ashley", "2019 DST2 Final Project Adele and Ashley")

# calculate an int for the font size
#font_size = int(1000/65)
font_size = int(25)


try:
    font = pygame.font.SysFont('Calibri', font_size)
except Exception as err:
    print ("pygame.font ERROR:", err)
    font = pygame.font.SysFont('Arial', font_size)

# create buttons for PostgreSQL database and table
#movie = Button("Movie", (230,100))
#director = Button("Director", (730,100))
#movie = Button("Top-Rated Movies by the Same Director", (60, 100))
#director = Button("Most Popular Directors of a Time Period", (525,100))
title_button = Button("Title:", (90, 150))
period_button = Button("Period (ex: 2010-2020):", (585, 150))


# default Postgres connection is 'None'
connection = None

# begin the pygame loop
app_running = True
while app_running == True:

    # reset the screen
    screen.fill( Button.light_blue )

    # set the clock FPS for app
    #clock = pygame.time.Clock()

     # blit instruction messages
    blit_text = "Recommend me:"
    conn_msg = font.render(blit_text, True, Button.dark_blue)
    screen.blit(conn_msg, (1000/2 - conn_msg.get_rect().width/2, 50))

    blit_text2 = "Top-Rated Movies by the Same Director"
    conn_msg2 = font.render(blit_text2, True, Button.dark_blue)
    screen.blit(conn_msg2, (1000/4 - conn_msg2.get_rect().width/2, 125))
    
    blit_text4 = "Movies"
    conn_msg4 = font.render(blit_text4, True, Button.light_purple)
    screen.blit(conn_msg4, (1000/4 - conn_msg4.get_rect().width/2, 100))

    blit_text3 = "Most Popular Directors of a Time Period"
    conn_msg3 = font.render(blit_text3, True, Button.dark_blue)
    screen.blit(conn_msg3, (1000*3/4-conn_msg3.get_rect().width/2, 125))
    
    blit_text5 = "Directors"
    conn_msg5 = font.render(blit_text5, True, Button.light_purple)
    screen.blit(conn_msg5, (1000*3/4-conn_msg5.get_rect().width/2, 100))


    # iterate over the pygame events
    for event in pygame.event.get():

        # user clicks the quit button on app window
        if event.type == QUIT:
            app_running = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()
            quit()

        # user presses a key on keyboard
        if event.type == KEYDOWN:

            if Button.selected != None:

                # get the selected button
                b = Button.selected
    

                # user presses the return key
                if event.key == K_RETURN:
                    movie_title_return = None
                    director_return = None
                    connection = connect_postgres(db_name)

                    # check if the selected button is the movie title
                    #if "Top-Rated Movies by the Same Director" in b.name:
                    #    title_button = Button("Title:", (60, 130))
        
                    #if "Most Popular Director of a Time Period" in b.name:
                    #    period_button = Button("Period (ex: 2010-2020):", (525, 130))
                        
                    if "Title" in b.name:
                        movie_title = b.text
                        movie_title_return = query1(connection)

                    if "Period" in b.name:
                        time_period = b.text
                        director_return = query2(connection)
                    

                    #connection = connect_postgres(db_name)
                    #movie_title_return = query1(connection)
                    #director_return = query2(connection)

                    # reset the button selected
                    Button.selected = None
                    print(movie_title)
                    print(time_period)
                    print(movie_title_return)
                    print(director_return)
                    

                else:
                    # get the key pressed
                    key_press = pygame.key.get_pressed()

                    # iterate over the keypresses
                    for keys in range(255):
                        if key_press[keys]:
                            if keys == 8: # backspace
                                b.text = b.text[:-1]
                            else:
                                # convert key to unicode string
                                b.text += event.unicode
                                print ("KEYPRESS:", event.unicode)

                # append the button text to button font object
                b.font = font.render(b.name + " " + b.text, True, Button.light_purple, Button.light_blue)

        # check for mouse button down events
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            print ("\nMOUSE CLICK:", event)

            # iterate over the button registry list
            for b in Button.registry:

                # check if the mouse click collided with button
                if b.rect.collidepoint(event.pos) == 1:
                    # store button object under selected attr
                    Button.selected = b


    # iterate over the button registry list
    for b in Button.registry:

        # blit the button's font to screen
        screen.blit(b.font, b.rect)

        # check if the button has been clicked by user
        if Button.selected == b:

            # blit an outline around button if selected
            rect_pos = (b.rect.x-5, b.rect.y-5, b.rect.width+10, b.rect.height+10)
            pygame.draw.rect(screen, Button.dark_blue, rect_pos, 3) # width 3 pixels


        # enumerate() the actor first name data if PostgreSQL API call successful
    if movie_title_return == []:
        text='Not Found'
        blit_text=text.encode("utf-8", "ignore")
        table_font = font.render(blit_text, True, Button.light_purple) 
        screen.blit(table_font, (90, 220))
        
    elif movie_title_return != None:
            # enumerate the list of tuple rows
        for num, row in enumerate(movie_title_return):
            # blit the table data to Pygame window
            text = re.search("(?<=[(].).+(?=.,[)])",str(row))
            try:
                blit_text = text.group(0).encode("utf-8", "ignore")
            except Exception as err:
                print('Regex err:', err)
                blit_text = ''
            table_font = font.render(blit_text, True, Button.light_purple) 
            screen.blit(table_font, (90, 220 + int(num*30)))
        

        # enumerate() the rating data if PostgreSQL API call successful
    if director_return == 'Invalid Input':
        text = 'Invalid Input'
        blit_text = text.encode("utf-8","ignore")
        table_font = font.render(blit_text, True, Button.light_purple) 
        screen.blit(table_font, (585, 220))
        
    elif director_return == []:
        text='Not Found'
        blit_text=text.encode("utf-8", "ignore")
        table_font = font.render(blit_text, True, Button.light_purple) 
        screen.blit(table_font, (585, 220))
        
    elif director_return != None:
            # enumerate the list of tuple rows
        for num, row in enumerate(director_return):
                # blit the table data to Pygame window
            text = re.search("(?<=[(].).+(?=.,[)])",str(row))
            try:
                blit_text = text.group(0).encode("utf-8", "ignore")
            except Exception as err:
                print('Regex err:', err)
                blit_text = 'error'
            table_font = font.render(blit_text, True, Button.light_purple)
            screen.blit(table_font, (585, 220 + int(num*30)))  
    
    
    
    pygame.draw.line(screen, Button.dark_blue, (500,190),(500,600))
    pygame.draw.line(screen, Button.dark_blue,(0,190),(1000,190))
    # set the clock FPS for application
    #clock.tick(25)

    # use the flip() method to display text on surface
    pygame.display.flip()
    pygame.display.update()

