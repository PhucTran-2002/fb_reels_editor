import customtkinter as ctk
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
from tkinter import colorchooser, filedialog
from PIL import Image, ImageTk
import tkinter as tk

class VideoEditor(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.video_clip = None
        self.output_path = None
        
        # Preview frame 9:16 (1080x1920 scaled down)
        self.preview_label = ctk.CTkLabel(self, text="Chưa có video", width=360, height=640, fg_color="black")
        self.preview_label.pack(pady=10)
        
        ctk.CTkButton(self, text="Chọn Video từ Downloads", command=self.load_video).pack(pady=5)
        
        # Color Overlay
        overlay_frame = ctk.CTkFrame(self)
        overlay_frame.pack(pady=10, fill="x", padx=20)
        ctk.CTkLabel(overlay_frame, text="Lớp phủ màu").pack()
        self.color_btn = ctk.CTkButton(overlay_frame, text="Chọn màu overlay", command=self.choose_overlay_color)
        self.color_btn.pack(side="left", padx=5)
        self.opacity_slider = ctk.CTkSlider(overlay_frame, from_=0, to=100, number_of_steps=20)
        self.opacity_slider.set(30)
        self.opacity_slider.pack(side="left", padx=5)
        
        # Text Top
        text_top = ctk.CTkFrame(self)
        text_top.pack(pady=5, fill="x", padx=20)
        ctk.CTkLabel(text_top, text="Text trên").pack()
        self.text_top_entry = ctk.CTkEntry(text_top, placeholder_text="Nhập text trên")
        self.text_top_entry.pack()
        self.top_color_btn = ctk.CTkButton(text_top, text="Màu chữ trên", command=lambda: self.choose_text_color("top"))
        self.top_color_btn.pack()
        
        # Text Bottom
        text_bot = ctk.CTkFrame(self)
        text_bot.pack(pady=5, fill="x", padx=20)
        ctk.CTkLabel(text_bot, text="Text dưới").pack()
        self.text_bot_entry = ctk.CTkEntry(text_bot, placeholder_text="Nhập text dưới")
        self.text_bot_entry.pack()
        self.bot_color_btn = ctk.CTkButton(text_bot, text="Màu chữ dưới", command=lambda: self.choose_text_color("bot"))
        self.bot_color_btn.pack()
        
        ctk.CTkButton(self, text="Export Video Đã Edit (9:16)", command=self.export_video, fg_color="green").pack(pady=20)

    def load_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video", "*.mp4 *.mov")])
        if path:
            self.video_clip = VideoFileClip(path).resize(height=1920).crop(x_center=1080/2, width=1080)  # Force 9:16
            self.output_path = path
            self.show_preview()

    def show_preview(self):
        # Tạo frame preview
        frame = self.video_clip.get_frame(0)
        img = Image.fromarray(frame).resize((360, 640))
        photo = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=photo)
        self.preview_label.image = photo

    def choose_overlay_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.overlay_color = color

    def choose_text_color(self, pos):
        color = colorchooser.askcolor()[1]
        if color:
            if pos == "top":
                self.top_color = color
            else:
                self.bot_color = color

    def export_video(self):
        if not self.video_clip:
            return
        
        clips = [self.video_clip]
        
        # Overlay color
        if hasattr(self, 'overlay_color'):
            overlay = ColorClip(size=(1080, 1920), color=self.overlay_color).set_opacity(self.opacity_slider.get()/100).set_duration(self.video_clip.duration)
            clips.append(overlay)
        
        # Text top
        if self.text_top_entry.get():
            txt_top = TextClip(txt=self.text_top_entry.get(), fontsize=60, color=getattr(self, 'top_color', 'white'), font='Arial-Bold').set_position(('center', 100)).set_duration(self.video_clip.duration)
            clips.append(txt_top)
        
        # Text bottom
        if self.text_bot_entry.get():
            txt_bot = TextClip(txt=self.text_bot_entry.get(), fontsize=60, color=getattr(self, 'bot_color', 'white'), font='Arial-Bold').set_position(('center', 1700)).set_duration(self.video_clip.duration)
            clips.append(txt_bot)
        
        final = CompositeVideoClip(clips)
        out_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        final.write_videofile(out_path, fps=30, codec="libx264")
        ctk.CTkLabel(self, text=f"Xuất thành công: {out_path}").pack()