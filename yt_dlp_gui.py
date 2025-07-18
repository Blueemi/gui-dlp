#!/usr/bin/env python3
"""
YT-DLP Wrapper with Tkinter GUI
A cross-platform video downloader with a beautiful blue interface

Requirements:
- Python 3.6+
- yt-dlp
- tkinter (usually comes with Python)

Installation:
pip install yt-dlp

Usage:
python yt_dlp_gui.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import sys
from pathlib import Path
import subprocess
import platform

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
        self.root.title("YT-DLP Video Downloader")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Blue color scheme
        self.colors = {
            'primary': '#1e40af',      # Primary blue
            'secondary': '#3b82f6',    # Secondary blue
            'accent': '#60a5fa',       # Accent blue
            'dark': '#1e3a8a',         # Dark blue
            'light': '#dbeafe',        # Light blue
            'white': '#ffffff',        # White
            'text': '#1f2937',         # Dark text
            'success': '#10b981',      # Success green
            'error': '#ef4444',        # Error red
            'warning': '#f59e0b'       # Warning orange
        }

        # Configure root window
        self.root.configure(bg=self.colors['primary'])

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
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['primary'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(
            main_frame, 
            text="YT-DLP Video Downloader",
            font=('Arial', 24, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=(0, 30))

        # URL Section
        self.create_url_section(main_frame)

        # Options Section
        self.create_options_section(main_frame)

        # Download Path Section
        self.create_path_section(main_frame)

        # Progress Section
        self.create_progress_section(main_frame)

        # Download Button
        self.create_download_button(main_frame)

        # Info Section
        self.create_info_section(main_frame)

    def create_url_section(self, parent):
        """Create URL input section"""
        url_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='raised', bd=2)
        url_frame.pack(fill="x", pady=(0, 15))

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

        # Add placeholder text functionality
        self.url_entry.insert(0, "Paste YouTube URL here...")
        self.url_entry.bind('<FocusIn>', self.on_url_focus_in)
        self.url_entry.bind('<FocusOut>', self.on_url_focus_out)

    def create_options_section(self, parent):
        """Create quality and format selection section"""
        options_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='raised', bd=2)
        options_frame.pack(fill="x", pady=(0, 15))

        # Quality selection
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

        quality_options = [
            "best", "worst", "720p", "1080p", "1440p", "2160p (4K)",
            "bestvideo+bestaudio", "bestaudio"
        ]

        self.quality_combo = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=quality_options,
            state="readonly",
            font=('Arial', 10)
        )
        self.quality_combo.pack(fill="x")

        # Format selection
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

        self.format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.format_var,
            values=format_options,
            state="readonly",
            font=('Arial', 10)
        )
        self.format_combo.pack(fill="x")

    def create_path_section(self, parent):
        """Create download path selection section"""
        path_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='raised', bd=2)
        path_frame.pack(fill="x", pady=(0, 15))

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

        browse_button = tk.Button(
            path_input_frame,
            text="Browse",
            command=self.browse_directory,
            font=('Arial', 10, 'bold'),
            bg=self.colors['accent'],
            fg=self.colors['white'],
            relief='flat',
            bd=0,
            padx=20,
            cursor='hand2'
        )
        browse_button.pack(side="right")

        # Add hover effect
        browse_button.bind('<Enter>', lambda e: browse_button.config(bg=self.colors['dark']))
        browse_button.bind('<Leave>', lambda e: browse_button.config(bg=self.colors['accent']))

    def create_progress_section(self, parent):
        """Create progress bar and status section"""
        progress_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='raised', bd=2)
        progress_frame.pack(fill="x", pady=(0, 15))

        progress_label = tk.Label(
            progress_frame,
            text="📊 Progress:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white']
        )
        progress_label.pack(anchor="w", padx=20, pady=(15, 5))

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            length=400,
            mode='determinate'
        )
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
        """Create the main download button"""
        self.download_button = tk.Button(
            parent,
            text="⬇️ Download",
            command=self.start_download,
            font=('Arial', 16, 'bold'),
            bg=self.colors['success'],
            fg=self.colors['white'],
            relief='flat',
            bd=0,
            padx=40,
            pady=15,
            cursor='hand2'
        )
        self.download_button.pack(pady=20)

        # Add hover effect
        self.download_button.bind('<Enter>', lambda e: self.download_button.config(bg='#059669'))
        self.download_button.bind('<Leave>', lambda e: self.download_button.config(bg=self.colors['success']))

    def create_info_section(self, parent):
        """Create info/help section"""
        info_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='raised', bd=2)
        info_frame.pack(fill="both", expand=True, pady=(0, 0))

        info_label = tk.Label(
            info_frame,
            text="ℹ️ Information:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white']
        )
        info_label.pack(anchor="w", padx=20, pady=(15, 5))

        # Create text widget with scrollbar
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

        # Add info content
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

    def on_url_focus_in(self, event):
        """Handle URL entry focus in"""
        if self.url_entry.get() == "Paste YouTube URL here...":
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg=self.colors['text'])

    def on_url_focus_out(self, event):
        """Handle URL entry focus out"""
        if not self.url_entry.get():
            self.url_entry.insert(0, "Paste YouTube URL here...")
            self.url_entry.config(fg='gray')

    def browse_directory(self):
        """Open directory browser"""
        try:
            directory = filedialog.askdirectory(
                title="Select Download Directory",
                initialdir=self.download_path.get()
            )
            if directory:
                self.download_path.set(directory)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open directory browser: {str(e)}")

    def progress_hook(self, d):
        """Handle download progress updates"""
        if d['status'] == 'downloading':
            try:
                if 'total_bytes' in d and d['total_bytes']:
                    progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    self.progress_bar['value'] = progress
                    speed = d.get('speed', 0)
                    if speed:
                        speed_str = f"{speed / 1024 / 1024:.1f} MB/s"
                    else:
                        speed_str = "-- MB/s"
                    self.status_label.config(text=f"Downloading: {progress:.1f}% ({speed_str})")
                elif '_percent_str' in d:
                    percent_str = d['_percent_str'].strip('% ')
                    if percent_str and percent_str != 'N/A':
                        try:
                            progress = float(percent_str)
                            self.progress_bar['value'] = progress
                            self.status_label.config(text=f"Downloading: {percent_str}%")
                        except ValueError:
                            pass
            except Exception:
                pass
        elif d['status'] == 'finished':
            self.progress_bar['value'] = 100
            self.status_label.config(text="Download completed successfully!")
        elif d['status'] == 'error':
            self.status_label.config(text="Download failed!")

    def download_video(self):
        """Download video in separate thread"""
        try:
            url = self.url_var.get().strip()
            if not url or url == "Paste YouTube URL here...":
                self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a video URL"))
                return

            # Validate URL
            if not any(domain in url.lower() for domain in ['youtube', 'youtu.be', 'vimeo', 'dailymotion', 'twitch']):
                if not url.startswith(('http://', 'https://')):
                    self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a valid URL"))
                    return

            # Create download directory
            download_dir = Path(self.download_path.get())
            try:
                download_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Cannot create directory: {str(e)}"))
                return

            # Configure yt-dlp options
            quality = self.quality_var.get()
            output_format = self.format_var.get()

            # Format selection logic
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

            # Base yt-dlp options
            ydl_opts = {
                'format': format_selector,
                'outtmpl': str(download_dir / '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'no_warnings': False,
                'ignoreerrors': False,
            }

            # Add post-processing for audio formats
            if output_format in ['mp3', 'm4a', 'flac', 'wav']:
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': output_format,
                    'preferredquality': '192' if output_format == 'mp3' else 'best',
                }]
            elif output_format != 'best':
                ydl_opts['merge_output_format'] = output_format

            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Show success message
            self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed successfully!"))

        except yt_dlp.DownloadError as e:
            error_msg = f"Download failed: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Download Error", error_msg))
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        finally:
            self.is_downloading = False
            self.root.after(0, self.reset_download_button)

    def reset_download_button(self):
        """Reset download button state"""
        self.download_button.config(text="⬇️ Download", state="normal")

    def start_download(self):
        """Start download process"""
        if self.is_downloading:
            return

        self.is_downloading = True
        self.download_button.config(text="⏳ Downloading...", state="disabled")
        self.progress_bar['value'] = 0
        self.status_label.config(text="Initializing download...")

        # Start download in separate thread
        download_thread = threading.Thread(target=self.download_video, daemon=True)
        download_thread.start()

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import yt_dlp
        return True
    except ImportError:
        return False

def main():
    """Main application entry point"""
    if not check_dependencies():
        print("Error: Required dependencies not found!")
        print("Please install yt-dlp with: pip install yt-dlp")
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
