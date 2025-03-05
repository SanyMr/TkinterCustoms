import tkinter as tk
from tkinter import ttk
import random

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hale Music Player")
        self.root.geometry("1200x700")
        self.root.configure(bg='#1A1A2E')  # Dark background

        # Create main container
        self.create_main_layout()

    def create_main_layout(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1A1A2E')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Sidebar
        self.create_sidebar(main_frame)

        # Main Content Area
        self.create_main_content(main_frame)

        # Player Controls
        self.create_player_controls(main_frame)

    def create_sidebar(self, parent):
        # Sidebar Frame
        sidebar = tk.Frame(parent, width=250, bg='#16213E')
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Logo
        logo_label = tk.Label(sidebar, text="Hale", fg='white', bg='#16213E', font=('Arial', 24, 'bold'))
        logo_label.pack(pady=(20, 30))

        # Sidebar Menu Items
        menu_items = [
            ("Browse", "🏠"),
            ("Genres", "🎵"),
            ("Playlists", "📋"),
            ("Favorites", "❤️"),
            ("Charts", "📊")
        ]

        for text, emoji in menu_items:
            btn = tk.Button(
                sidebar, 
                text=f"{emoji}  {text}", 
                bg='#16213E', 
                fg='white', 
                borderwidth=0, 
                activebackground='#0F3460',
                activeforeground='white',
                font=('Arial', 12)
            )
            btn.pack(fill=tk.X, padx=10, pady=5)

    def create_main_content(self, parent):
        # Main Content Frame
        content_frame = tk.Frame(parent, bg='#1A1A2E')
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Recommended Section
        recommended_frame = tk.Frame(content_frame, bg='#1A1A2E')
        recommended_frame.pack(fill=tk.X)

        recommended_label = tk.Label(
            recommended_frame, 
            text="Recommended", 
            fg='white', 
            bg='#1A1A2E', 
            font=('Arial', 16, 'bold')
        )
        recommended_label.pack(anchor='w', pady=(0, 10))

        # Recommended Albums
        recommended_albums = [
            ("Imagine Dragons", "Origins", "purple"),
            ("KISS", "Alive!", "red"),
            ("Harry Styles", "Fine Line", "green")
        ]

        recommended_albums_frame = tk.Frame(content_frame, bg='#1A1A2E')
        recommended_albums_frame.pack(fill=tk.X)

        for artist, album, color in recommended_albums:
            album_frame = tk.Frame(recommended_albums_frame, bg=color, width=300, height=200)
            album_frame.pack(side=tk.LEFT, padx=10)
            album_frame.pack_propagate(False)

            album_label = tk.Label(
                album_frame, 
                text=f"{artist}\n{album}", 
                fg='white', 
                bg=color, 
                font=('Arial', 12, 'bold')
            )
            album_label.pack(expand=True)

        # Trending Artists Section
        trending_frame = tk.Frame(content_frame, bg='#1A1A2E')
        trending_frame.pack(fill=tk.X, pady=20)

        trending_label = tk.Label(
            trending_frame, 
            text="Trending Artists", 
            fg='white', 
            bg='#1A1A2E', 
            font=('Arial', 16, 'bold')
        )
        trending_label.pack(anchor='w', pady=(0, 10))

        # Trending Artists
        trending_artists_frame = tk.Frame(trending_frame, bg='#1A1A2E')
        trending_artists_frame.pack(fill=tk.X)

        trending_artists = [
            ("Old Town Road", "Lil Nas X"),
            ("Bad Guy", "Billie Eilish"),
            ("Talk", "Khalid"),
            ("No Guidance", "Chris Brown")
        ]

        for artist, song in trending_artists:
            artist_frame = tk.Frame(trending_artists_frame, bg='#16213E', width=200, height=250)
            artist_frame.pack(side=tk.LEFT, padx=10)
            artist_frame.pack_propagate(False)

            artist_label = tk.Label(
                artist_frame, 
                text=f"{artist}\n{song}", 
                fg='white', 
                bg='#16213E', 
                font=('Arial', 10)
            )
            artist_label.pack(expand=True)

    def create_player_controls(self, parent):
        # Player Controls Frame
        player_frame = tk.Frame(parent, bg='#16213E', height=80)
        player_frame.pack(side=tk.BOTTOM, fill=tk.X)
        player_frame.pack_propagate(False)

        # Current Track Info
        track_info = tk.Frame(player_frame, bg='#16213E')
        track_info.pack(side=tk.LEFT, padx=20)

        track_name = tk.Label(
            track_info, 
            text="Believer", 
            fg='white', 
            bg='#16213E', 
            font=('Arial', 12, 'bold')
        )
        track_name.pack()

        artist_name = tk.Label(
            track_info, 
            text="Imagine Dragons", 
            fg='gray', 
            bg='#16213E', 
            font=('Arial', 10)
        )
        artist_name.pack()

        # Playback Controls
        controls_frame = tk.Frame(player_frame, bg='#16213E')
        controls_frame.pack(expand=True)

        # Previous, Play/Pause, Next buttons
        control_buttons = [
            ("⏮️", "prev"),
            ("▶️", "play"),
            ("⏭️", "next")
        ]

        for symbol, action in control_buttons:
            btn = tk.Button(
                controls_frame, 
                text=symbol, 
                bg='#16213E', 
                fg='white', 
                borderwidth=0, 
                font=('Arial', 16)
            )
            btn.pack(side=tk.LEFT, padx=10)

        # Progress Bar
        progress_frame = tk.Frame(player_frame, bg='#16213E')
        progress_frame.pack(side=tk.RIGHT, padx=20)

        progress_bar = tk.Scale(
            progress_frame, 
            from_=0, 
            to=100, 
            orient=tk.HORIZONTAL, 
            length=200, 
            showvalue=0,
            bg='#16213E',
            troughcolor='gray',
            activebackground='green'
        )
        progress_bar.pack()

def main():
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
