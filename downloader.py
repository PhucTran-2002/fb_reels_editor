import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from utils import download_reel

class DownloaderTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.links = []
        
        ctk.CTkLabel(self, text="Danh sách Reels Facebook", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.entry = ctk.CTkEntry(self, placeholder_text="Dán link Reels (mỗi dòng một link)", height=100, width=600)
        self.entry.pack(pady=10)
        
        ctk.CTkButton(self, text="Thêm vào danh sách", command=self.add_links).pack(pady=5)
        
        # Bảng
        self.tree = ttk.Treeview(self, columns=("Link", "Status"), show="headings", height=10)
        self.tree.heading("Link", text="Link Reels")
        self.tree.heading("Status", text="Trạng thái")
        self.tree.column("Link", width=500)
        self.tree.column("Status", width=150)
        self.tree.pack(pady=10, fill="both", expand=True)
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Tải tất cả", command=self.download_all).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Xóa chọn", command=self.delete_selected).pack(side="left", padx=5)

    def add_links(self):
        text = self.entry.get()
        new_links = [line.strip() for line in text.split("\n") if line.strip()]
        for link in new_links:
            if link not in self.links:
                self.links.append(link)
                self.tree.insert("", "end", values=(link, "Chưa tải"))
        self.entry.delete(0, "end")

    def download_all(self):
        for item in self.tree.get_children():
            link = self.tree.item(item)["values"][0]
            try:
                filepath = download_reel(link)
                self.tree.set(item, "Status", "Đã tải: " + os.path.basename(filepath))
            except Exception as e:
                self.tree.set(item, "Status", f"Lỗi: {str(e)[:30]}")

    def delete_selected(self):
        selected = self.tree.selection()
        for item in selected:
            link = self.tree.item(item)["values"][0]
            if link in self.links:
                self.links.remove(link)
            self.tree.delete(item)