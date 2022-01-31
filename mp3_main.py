import pygame
from tkinter import *
from tkinter import filedialog
import mysql.connector
import threading
import trace
import sys
from mutagen.mp3 import MP3


class Player:
    def __init__(self, window):
        # Build window of GUI
        window.geometry('320x500')
        window.title('mp3 Player')
        window.resizable(0, 0)

        # Initialize member variables
        self.p_list = Listbox(window, width=40, height=20)
        self.paused = False
        self.changed = False
        self.stopped = False
        self.playing = False
        self.current = ""
        self.count = 0
        self.counter = 0
        self.path = []
        self.title = []

        # create and start thread
        self.t1 = threading.Thread(target=self.continue_playing, daemon=True)
        self.t1.start()

        self.music_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="wwhh44tt"
        )

        self.mycursor = self.music_db.cursor(buffered=True)

        # Build playlist
        self.playlist(window)

        # Create and place buttons
        add_song = Button(window, text="Add", command=self.add)
        play = Button(window, text="Play", command=self.play)
        stop = Button(window, text="Stop", command=self.stop)
        pause = Button(window, text="Pause", command=self.pause)
        next = Button(window, text="Next", command=self.next_song)
        prev = Button(window, text="Previous", command=self.prev_song)
        resume = Button(window, text="Resume", command=self.resume_song)
        delete = Button(window, text="Delete", command=self.delete_song)
        add_song.place(x=20, y=350)
        prev.place(x=80, y=350)
        play.place(x=140, y=350)
        next.place(x=180, y=350)
        delete.place(x=250, y=350)
        pause.place(x=20, y=390)
        stop.place(x=130, y=390)
        resume.place(x=250, y=390)

    # Function to add new songs to playlist
    def add(self):
        # store selected song path, separate name from path, and store song title
        temp_song = filedialog.askopenfilenames(initialdir="Music/", title="Choose a song",
                                                filetypes=(("mp3 Files", "*.mp3"),))
        split_song = temp_song[0].split('/')
        song_name = split_song[-1].replace(".mp3", "")

        self.mycursor.execute("USE database2")

        # Insert song into playlist
        self.p_list.insert(self.count, song_name)

        self.path.append(temp_song[0])
        self.title.append(song_name)

        # Insert song data to database
        sql = "INSERT INTO musictable (type, filepath, name) VALUE (%s, %s, %s)"
        val = ("mp3", temp_song[0], song_name)

        self.mycursor.execute(sql, val)
        self.music_db.commit()

    # Function to play selected song
    def play(self):

        self.mycursor.execute("USE database2")

        # store selected song's index
        self.counter = self.p_list.curselection()[0]

        # Initialize and play selected song
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.path[self.counter])
        pygame.mixer.music.play()
        self.playing = True

    # Function to jump to next track
    def next_song(self):
        # Increment song index
        self.counter += 1
        self.changed = True

        # Initialize and play song
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.path[self.counter])
        pygame.mixer.music.play()

    # Function to jump to previous track
    def prev_song(self):
        # Decrement song index
        self.counter -= 1
        self.changed = True

        # Initialize and play song
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.path[self.counter])
        pygame.mixer.music.play()

    # Function to stop playing song
    def stop(self):
        pygame.mixer.music.stop()
        self.current = ""
        self.stopped = True

    # Function to pause playing song
    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True

    # Function to resume paused song
    def resume_song(self):
        pygame.mixer.music.unpause()
        self.paused = False

    # Function to delete song from playlist
    def delete_song(self):
        self.mycursor.execute("USE database2")

        song_name = ""
        # For loop to find and delete selected song
        for i in self.p_list.curselection():
            song_name = self.p_list.get(i)
            self.p_list.delete(i)

        # For loop to pop selected song from path and title lists
        for x in range(len(self.title)):
            if song_name == self.title[x]:
                self.title.pop(x)
                self.path.pop(x)

        # Delete song from database
        sql = "DELETE FROM musictable WHERE name = %s"
        val = (song_name,)

        self.mycursor.execute(sql, val)
        self.music_db.commit()

    # Function to render playlist
    def playlist(self, window):

        for x in range(len(self.database())):
            self.p_list.insert(x + 1, self.database()[x][2])
            self.path.append(self.database()[x][1])
            self.title.append(self.database()[x][2])
            self.count += 1

        self.p_list.pack()

    # Function create database
    def database(self):
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS database2")
        self.mycursor.execute("USE database2")

        self.mycursor.execute("CREATE TABLE IF NOT EXISTS musictable (type VARCHAR(10), "
                              "filepath VARCHAR(255), name VARCHAR(50))")

        self.mycursor.execute("SELECT * FROM musictable WHERE type = 'mp3'")

        song_list = self.mycursor.fetchall()

        return song_list

    # Function to continue playing music on playlist(still working on it!)
    def continue_playing(self):

        ##pygame.init()
        # pygame.mixer.init()

        temp_path = self.path

        # if self.count - 1 != self.counter:
        # pygame.mixer.music.queue(temp_path[self.counter + 1])

        MUSIC_END = pygame.USEREVENT + 1

        pygame.mixer.music.set_endevent(MUSIC_END)
        running = True

        while running:
            # checking if any event has been
            # hosted at time of playing
            if self.playing:
                for event in pygame.event.get():
                    # print(2)
                    # A event will be hosted
                    # after the end of every song
                    if event.type == MUSIC_END:
                        print('Song Finished')
                        self.counter += 1
                        # Checking our playList
                        # that if any song exist or
                        # it is empty
                        if self.changed:
                            # print(4)
                            pygame.init()
                            pygame.mixer.init()
                            pygame.mixer.music.load(temp_path[self.counter])
                            pygame.mixer.music.play()
                        if self.count - 1 > self.counter:
                            print(1)
                            pygame.mixer.music.queue(temp_path[self.counter + 1])

                        # Checking whether the
                        # player is still playing any song
                        # if yes it will return true and false otherwise
                        if not pygame.mixer.music.get_busy() or self.stopped:
                            print("Playlist completed")

                            # When the playlist has
                            # completed playing successfully
                            # we'll go out of the
                            # while-loop by using break
                            # running = False
                            # break
                self.changed = False
            # print(self.counter, self.count)
        # print(self.t1)


# Create tkinter object
root = Tk()
# Create Player object
app = Player(root)
# Launch GUI
root.mainloop()
