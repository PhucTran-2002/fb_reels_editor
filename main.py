import customtkinter as ctk
from downloader import DownloaderTab
from editor import VideoEditor

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FB Reels Downloader & Editor - Beautiful Tool")
        self.geometry("1200x800")
        
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        tabview.add("Downloader")
        tabview.add("Video Editor")
        
        DownloaderTab(tabview.tab("Downloader")).pack(fill="both", expand=True)
        VideoEditor(tabview.tab("Video Editor")).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()