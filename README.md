# YT-DLP GUI Wrapper

A beautiful, cross-platform GUI wrapper for yt-dlp with a modern blue interface.

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-F15437.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

🎬 **Multi-platform Video Downloading**
- Download from YouTube and 1000+ other sites
- Support for playlists and channels
- High-quality video downloads up to 8K

🎯 **Quality Options**
- Choose from multiple quality presets
- Custom resolution selection (720p, 1080p, 1440p, 4K)
- Audio-only downloads
- Best quality automatic selection

📁 **Format Support**
- Video: MP4, MKV, WebM
- Audio: MP3, M4A, FLAC, WAV
- Automatic format conversion

🎨 **Beautiful Interface**
- Modern blue-themed GUI
- Real-time download progress
- Cross-platform native look
- Responsive design

## Screenshots

The application features a clean, modern interface with:
- URL input field with placeholder text
- Quality and format selection dropdowns
- Directory browser for download location
- Real-time progress bar
- Informative help section

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Quick Install

1. **Download the files**
   ```bash
   # Clone or download the repository
   git clone <repository-url>
   cd yt-dlp-gui
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Launch the application**
   ```bash
   python yt_dlp_gui.py
   ```

### Manual Installation

1. **Install yt-dlp**
   ```bash
   pip install yt-dlp
   ```

2. **Run the application**
   ```bash
   python yt_dlp_gui.py
   ```

## Usage

### Basic Usage

1. **Paste URL**: Enter a video URL in the input field
2. **Select Quality**: Choose from dropdown (best, 720p, 1080p, 4K, etc.)
3. **Choose Format**: Select output format (MP4, MKV, MP3, etc.)
4. **Set Directory**: Click "Browse" to select download folder
5. **Download**: Click the download button and wait for completion

### Advanced Features

#### Quality Options
- **best**: Automatically selects the best available quality
- **720p/1080p/1440p/2160p**: Specific resolution targets
- **bestvideo+bestaudio**: Best video and audio tracks combined
- **bestaudio**: Audio-only download

#### Format Options
- **MP4**: Most compatible video format
- **MKV**: High-quality video container
- **WebM**: Web-optimized format
- **MP3**: Popular audio format
- **M4A**: High-quality audio format
- **FLAC**: Lossless audio format

### Supported Sites

The application supports downloads from:
- YouTube (videos, playlists, channels)
- Vimeo
- Dailymotion
- Twitch
- And 1000+ other sites supported by yt-dlp

## Cross-Platform Compatibility

### Windows
- Tested on Windows 10 and 11
- Compatible with Python 3.6+
- Native Windows dialogs

### Linux
- Tested on Ubuntu, Debian, CentOS
- GTK-based file dialogs
- Supports all major distributions

### macOS
- Compatible with macOS 10.14+
- Native Cocoa dialogs
- Full feature support

## File Structure

```
yt-dlp-gui/
├── yt_dlp_gui.py              # Main application (enhanced tkinter)
├── yt_dlp_wrapper_tkinter.py  # Alternative tkinter version
├── setup.py                   # Setup script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── run_gui.bat               # Windows batch file
```

## Dependencies

- **yt-dlp**: Core downloading functionality
- **tkinter**: GUI framework (included with Python)
- **pathlib**: Cross-platform path handling
- **threading**: Background downloads

## Troubleshooting

### Common Issues

1. **"yt-dlp is not installed"**
   ```bash
   pip install yt-dlp
   ```

2. **"No module named tkinter"**
   - On Ubuntu/Debian: `sudo apt install python3-tk`
   - On CentOS/RHEL: `sudo yum install tkinter`

3. **Permission errors**
   - Ensure write permissions to download directory
   - Run as administrator if needed (Windows)

4. **Download fails**
   - Check internet connection
   - Verify URL is correct
   - Some sites may require cookies or authentication

### Performance Tips

- Use SSD for download directory for better performance
- Close other applications during large downloads
- Use wired internet connection for stability

## Development

### Running from Source

```bash
# Clone repository
git clone <repository-url>
cd yt-dlp-gui

# Install dependencies
pip install -r requirements.txt

# Run application
python yt_dlp_gui.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple platforms
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **yt-dlp**: The powerful backend that makes this possible
- **Python tkinter**: For the cross-platform GUI framework
- **The open-source community**: For continuous improvements

## Support

If you encounter any issues:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Test with a simple YouTube URL
4. Check the console for error messages

---

**Note**: This application is a GUI wrapper for yt-dlp. All downloading functionality is provided by yt-dlp. Please respect the terms of service of the sites you download from.
