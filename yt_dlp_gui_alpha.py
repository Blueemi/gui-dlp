#!/usr/bin/env python3
"""
YT-DLP Wrapper with Tkinter GUI (Zen Browser Style)
A cross-platform video downloader with a beautiful blue interface inspired by Zen Browser

Requirements:
- Python 3.6+
- yt-dlp
- tkinter (usually comes with Python)
- pillow (for Gaussian blur)

Installation:
pip install yt-dlp pillow
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import sys
from pathlib import Path
from PIL import Image, ImageTk, ImageFilter

# Try to import yt-dlp
try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Please install it with: pip install yt-dlp")
    sys.exit(1)

class YTDLPGUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YT-DLP Video Downloader (Zen Style)")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Blue color scheme with Zen-inspired softness
        self.colors = {
            'primary': '#1e40af',
            'secondary': '#3b82f6',
            'accent': '#60a5fa',
            'dark': '#1e3a8a',
            'light': '#dbeafe',
            'white': '#ffffff',
            'text': '#1f2937',
            'success': '#10b981',
            'error': '#ef4444',
            'warning': '#f59e0b',
            'hover_light': '#93c5fd'
        }

        # Configure root window with blur background
        self.root.configure(bg=self.colors['primary'])
        self.apply_blur_to_background(self.root, self.colors['primary'])

        # Rozszerzenie Canvas dla rounded rect
        def _create_rounded_rect(canvas, x1, y1, x2, y2, radius=25, **kwargs):
            points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
            return canvas.create_polygon(points, **kwargs, smooth=True)

        tk.Canvas.create_rounded_rect = _create_rounded_rect

        # Variables
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="best")
        self.format_var = tk.StringVar(value="mp4")
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.is_downloading = False

        # Create GUI
        self.create_widgets()

        # Center window
        self.center_window()

    def apply_blur_to_background(self, widget, color):
        """Apply Gaussian blur to widget background - Zen-style"""
        width = widget.winfo_width() or 900
        height = widget.winfo_height() or 700
        img = Image.new('RGB', (width, height), color)
        blurred = img.filter(ImageFilter.GaussianBlur(radius=3))
        photo = ImageTk.PhotoImage(blurred)
        label = tk.Label(widget, image=photo, bg=color)
        label.image = photo
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.lower()

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Create all GUI widgets"""
        main_frame = tk.Frame(self.root, bg=self.colors['primary'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.apply_blur_to_background(main_frame, self.colors['primary'])

        title_label = tk.Label(
            main_frame,
            text="YT-DLP Video Downloader",
            font=('Arial', 24, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=(0, 30))

        self.create_url_section(main_frame)
        self.create_options_section(main_frame)
        self.create_path_section(main_frame)
        self.create_progress_section(main_frame)
        self.create_download_button(main_frame)
        self.create_info_section(main_frame)

    def create_url_section(self, parent):
        """Create URL input section with blur"""
        url_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='flat')
        url_frame.pack(fill="x", pady=(0, 15))
        self.apply_blur_to_background(url_frame, self.colors['secondary'])

        url_label = tk.Label(
            url_frame,
            text="🎬 Video URL:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white']
        )
        url_label.pack(anchor="w", padx=20, pady=(15, 5))

        self.url_entry = tk.Entry(
            url_frame,
            textvariable=self.url_var,
            font=('Arial', 11),
            bg=self.colors['light'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief='flat',
            bd=5
        )
        self.url_entry.pack(fill="x", padx=20, pady=(0, 15))

        self.url_entry.insert(0, "Paste YouTube URL here...")
        self.url_entry.bind('<FocusIn>', self.on_url_focus_in)
        self.url_entry.bind('<FocusOut>', self.on_url_focus_out)

    def create_options_section(self, parent):
        """Create quality and format selection section with blur"""
        options_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='flat')
        options_frame.pack(fill="x", pady=(0, 15))
        self.apply_blur_to_background(options_frame, self.colors['secondary'])

        quality_frame = tk.Frame(options_frame, bg=self.colors['secondary'])
        quality_frame.pack(fill="x", padx=20, pady=(15, 10))

        quality_label = tk.Label(
            quality_frame,
            text="🎯 Quality:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white']
        )
        quality_label.pack(anchor="w", pady=(0, 5))

        quality_options = ["best", "worst", "720p", "1080p", "1440p", "2160p (4K)", "bestvideo+bestaudio", "bestaudio"]
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var, values=quality_options, state="readonly", font=('Arial', 10))
        self.quality_combo.pack(fill="x")

        format_frame = tk.Frame(options_frame, bg=self.colors['secondary'])
        format_frame.pack(fill="x", padx=20, pady=(10, 15))

        format_label = tk.Label(
            format_frame,
            text="📁 Output Format:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white']
        )
        format_label.pack(anchor="w", pady=(0, 5))

        format_options = ["mp4", "mkv", "webm", "mp3", "m4a", "flac", "wav"]
        self.format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, values=format_options, state="readonly", font=('Arial', 10))
        self.format_combo.pack(fill="x")

    def create_path_section(self, parent):
        """Create download path selection section with blur and rounded button"""
        path_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='flat')
        path_frame.pack(fill="x", pady=(0, 15))
        self.apply_blur_to_background(path_frame, self.colors['secondary'])

        path_label = tk.Label(
            path_frame,
            text="📂 Download Directory:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white']
        )
        path_label.pack(anchor="w", padx=20, pady=(15, 5))

        path_input_frame = tk.Frame(path_frame, bg=self.colors['secondary'])
        path_input_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.path_entry = tk.Entry(
            path_input_frame,
            textvariable=self.download_path,
            font=('Arial', 10),
            bg=self.colors['light'],
            fg=self.colors['text'],
            relief='flat',
            bd=5
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_button = self.create_rounded_button(
            path_input_frame,
            text="Browse",
            command=self.browse_directory,
            bg_color=self.colors['accent'],
            fg_color=self.colors['white'],
            hover_bg=self.colors['hover_light']
        )
        browse_button.pack(side="right")

    def create_progress_section(self, parent):
        """Create progress bar and status section with blur"""
        progress_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='flat')
        progress_frame.pack(fill="x", pady=(0, 15))
        self.apply_blur_to_background(progress_frame, self.colors['secondary'])

        progress_label = tk.Label(
            progress_frame,
            text="📊 Progress:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white']
        )
        progress_label.pack(anchor="w", padx=20, pady=(15, 5))

        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))

        self.status_label = tk.Label(
            progress_frame,
            text="Ready to download",
            font=('Arial', 10),
            bg=self.colors['secondary'],
            fg=self.colors['white']
        )
        self.status_label.pack(padx=20, pady=(0, 15))

    def create_download_button(self, parent):
        """Create the main download button - rounded with hover"""
        self.download_button = self.create_rounded_button(
            parent,
            text="⬇️ Download",
            command=self.start_download,
            bg_color=self.colors['success'],
            fg_color=self.colors['white'],
            hover_bg='#34d399',
            font=('Arial', 16, 'bold'),
            padx=40,
            pady=15,
            width=200,
            height=50
        )
        self.download_button.pack(pady=20)

    def create_info_section(self, parent):
        """Create info/help section with blur"""
        info_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='flat')
        info_frame.pack(fill="both", expand=True, pady=(0, 0))
        self.apply_blur_to_background(info_frame, self.colors['secondary'])

        info_label = tk.Label(
            info_frame,
            text="ℹ️ Information:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white']
        )
        info_label.pack(anchor="w", padx=20, pady=(15, 5))

        text_frame = tk.Frame(info_frame, bg=self.colors['secondary'])
        text_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.info_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=('Arial', 9),
            bg=self.colors['light'],
            fg=self.colors['text'],
            relief='flat',
            bd=5,
            height=8
        )
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        self.info_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        info_content = """🎬 YT-DLP Video Downloader

✨ Features:
• Download videos from YouTube and 1000+ other sites
• Multiple quality options (720p, 1080p, 4K)
• Various output formats (MP4, MKV, MP3, etc.)
• Cross-platform compatibility (Windows, Linux, macOS)
• Real-time download progress
• Audio-only downloads

📋 Instructions:
1. Paste a video URL in the input field
2. Select your preferred quality
3. Choose output format
4. Set download directory
5. Click Download

🎯 Quality Options:
• best: Best available quality
• 720p/1080p/1440p/2160p: Specific resolutions
• bestvideo+bestaudio: Best video + audio combined
• bestaudio: Audio only

🔧 Supported Formats:
• Video: MP4, MKV, WebM
• Audio: MP3, M4A, FLAC, WAV

⚠️ Note: Some sites may require additional configuration or may not be supported."""
        self.info_text.insert("1.0", info_content)
        self.info_text.config(state="disabled")

    def create_rounded_button(self, parent, text, command, bg_color, fg_color, hover_bg, font=('Arial', 10, 'bold'), padx=20, pady=10, width=120, height=30):
        """Create a rounded button with hover effect - Zen-style"""
        canvas = tk.Canvas(parent, bg=bg_color, highlightthickness=0)
        width = width + padx * 2
        height = height + pady * 2

        def draw_rounded_rect(color):
            canvas.delete("all")
            tk.Canvas.create_rounded_rect(canvas, 0, 0, width, height, radius=15, fill=color, outline="")

        draw_rounded_rect(bg_color)

        button_label = tk.Label(canvas, text=text, font=font, bg=bg_color, fg=fg_color, bd=0)
        button_label.place(relx=0.5, rely=0.5, anchor="center")

        def on_enter(e):
            draw_rounded_rect(hover_bg)
            button_label.config(bg=hover_bg)

        def on_leave(e):
            draw_rounded_rect(bg_color)
            button_label.config(bg=bg_color)

        button_label.bind("<Enter>", on_enter)
        button_label.bind("<Leave>", on_leave)
        button_label.bind("<Button-1>", lambda e: command() if not self.is_downloading else None)

        canvas.config(width=width, height=height)
        return canvas

    def on_url_focus_in(self, event):
        if self.url_entry.get() == "Paste YouTube URL here...":
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg=self.colors['text'])

    def on_url_focus_out(self, event):
        if not self.url_entry.get():
            self.url_entry.insert(0, "Paste YouTube URL here...")
            self.url_entry.config(fg='gray')

    def browse_directory(self):
        try:
            directory = filedialog.askdirectory(title="Select Download Directory", initialdir=self.download_path.get())
            if directory:
                self.download_path.set(directory)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open directory browser: {str(e)}")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                if 'total_bytes' in d and d['total_bytes']:
                    progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    self.progress_bar['value'] = progress
                    speed = d.get('speed', 0)
                    speed_str = f"{speed / 1024 / 1024:.1f} MB/s" if speed else "-- MB/s"
                    self.status_label.config(text=f"Downloading: {progress:.1f}% ({speed_str})")
                elif '_percent_str' in d:
                    percent_str = d['_percent_str'].strip('% ')
                    if percent_str and percent_str != 'N/A':
                        progress = float(percent_str)
                        self.progress_bar['value'] = progress
                        self.status_label.config(text=f"Downloading: {percent_str}%")
            except Exception:
                pass
        elif d['status'] == 'finished':
            self.progress_bar['value'] = 100
            self.status_label.config(text="Download completed successfully!")
        elif d['status'] == 'error':
            self.status_label.config(text="Download failed!")

    def download_video(self):
        try:
            url = self.url_var.get().strip()
            if not url or url == "Paste YouTube URL here...":
                self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a video URL"))
                return

            if not any(domain in url.lower() for domain in ['youtube', 'youtu.be', 'vimeo', 'dailymotion', 'twitch']) and not url.startswith(('http://', 'https://')):
                self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a valid URL"))
                return

            download_dir = Path(self.download_path.get())
            download_dir.mkdir(parents=True, exist_ok=True)

            quality = self.quality_var.get()
            output_format = self.format_var.get()

            format_selector = quality
            if quality == "720p":
                format_selector = "bestvideo[height<=720]+bestaudio/best[height<=720]"
            elif quality == "1080p":
                format_selector = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
            elif quality == "1440p":
                format_selector = "bestvideo[height<=1440]+bestaudio/best[height<=1440]"
            elif quality == "2160p (4K)":
                format_selector = "bestvideo[height<=2160]+bestaudio/best[height<=2160]"
            elif quality == "bestaudio":
                format_selector = "bestaudio/best"

            ydl_opts = {
                'format': format_selector,
                'outtmpl': str(download_dir / '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'no_warnings': False,
                'ignoreerrors': False,
            }

            if output_format in ['mp3', 'm4a', 'flac', 'wav']:
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': output_format,
                    'preferredquality': '192' if output_format == 'mp3' else 'best',
                }]
            elif output_format != 'best':
                ydl_opts['merge_output_format'] = output_format

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed successfully!"))

        except yt_dlp.DownloadError as e:
            self.root.after(0, lambda: messagebox.showerror("Download Error", f"Download failed: {str(e)}"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
        finally:
            self.is_downloading = False
            self.root.after(0, self.reset_download_button)

    def reset_download_button(self):
        """Reset download button state"""
        self.download_button.delete("all")
        tk.Canvas.create_rounded_rect(self.download_button, 0, 0, 200, 50, radius=15, fill=self.colors['success'])
        label = tk.Label(self.download_button, text="⬇️ Download", font=('Arial', 16, 'bold'), bg=self.colors['success'], fg=self.colors['white'])
        label.place(relx=0.5, rely=0.5, anchor="center")
        self.download_button.config(state="normal")

    def start_download(self):
        """Start download process"""
        if self.is_downloading:
            return

        self.is_downloading = True
        self.download_button.delete("all")
        tk.Canvas.create_rounded_rect(self.download_button, 0, 0, 200, 50, radius=15, fill=self.colors['success'])
        label = tk.Label(self.download_button, text="⏳ Downloading...", font=('Arial', 16, 'bold'), bg=self.colors['success'], fg=self.colors['white'])
        label.place(relx=0.5, rely=0.5, anchor="center")
        self.download_button.config(state="disabled")
        self.progress_bar['value'] = 0
        self.status_label.config(text="Initializing download...")

        download_thread = threading.Thread(target=self.download_video, daemon=True)
        download_thread.start()

def check_dependencies():
    try:
        import yt_dlp
        from PIL import Image, ImageTk, ImageFilter
        return True
    except ImportError:
        return False

def main():
    if not check_dependencies():
        print("Error: Required dependencies not found!")
        print("Please install yt-dlp and pillow with: pip install yt-dlp pillow")
        return

    try:
        root = tk.Tk()
        app = YTDLPGUIApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")

if __name__ == "__main__":
    main()
