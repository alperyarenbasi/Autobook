# AutoBook

**Automated Housing Reservation Assistant**

AutoBook is a Python automation tool that monitors student housing availability and automatically reserves units when they become available. The tool handles authentication, session management, and continuous monitoring - but you still need to manually complete the contract signing process.

## 🚨 Important Notice

**This tool only RESERVES apartments for you** - it does NOT complete the full booking process. After a successful reservation, you must manually sign the contract within the time limit to secure your housing.

## ✨ Features

- **24/7 Monitoring**: Continuously checks for unit availability
- **Auto-Authentication**: Handles Feide login and session management  
- **Robust Error Handling**: Recovers from network issues and timeouts
- **Event Logging**: Tracks all actions with timestamps
- **Screenshot Capture**: Takes a screenshot when reservation is successful
- **Multi-Unit Support**: Configure different housing units via environment variables

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Windows, macOS, or Linux

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AutoBook.git
   cd AutoBook
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .\.venv\Scripts\activate
   
   # macOS/Linux  
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Your student portal credentials
   SIT_USER=your.email@stud.ntnu.no
   SIT_PASS=your_password
   FEIDE_DISPLAY_NAME=Your Full Name
   SIT_UNIT=unit-id-here
   ```

5. **Test the setup**
   ```bash
   python test_setup.py
   ```

## 🚀 Usage

### Basic Usage
```bash
python sit_autobook.py
```

### What happens when you run it:
1. Opens a browser window (you can watch the process)
2. Navigates to the housing portal
3. Logs in with your Feide credentials
4. Continuously monitors the specified unit
5. When available, clicks "Book now" to reserve
6. Takes a screenshot and pauses for manual contract completion

### Monitoring Output
```
Monitoring unit housing-unit-123 every 0s…
--> not available, retrying in 2.1s
--> not available, retrying in 2.3s
UNIT RESERVED!
Ready to sign contract.
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SIT_USER` | Your student email | `john.doe@stud.ntnu.no` |
| `SIT_PASS` | Your password | `SecurePassword123` |
| `FEIDE_DISPLAY_NAME` | Full name as shown in Feide | `John Doe` |
| `SIT_UNIT` | Unit ID to monitor | `ob001-201` |

### Advanced Settings

Edit the script to modify:
- `CHECK_INTERVAL`: Seconds between checks (default: 0)
- `MAX_BACKOFF`: Maximum retry delay (default: 60s)
- `headless`: Set to `True` to run without browser window

## 📁 Project Structure

```
AutoBook/
├── sit_autobook.py         # Main application
├── persistent_status.py    # Event logging system
├── test_setup.py          # Setup verification
├── test_modules.py        # Module testing
├── requirements.txt       # Dependencies
├── .env                   # Configuration (create this)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Troubleshooting

### Common Issues

**Browser crashes on startup**
```bash
# Kill existing browser processes
taskkill /F /IM chrome.exe /T
# Then restart the application
```

**Login fails repeatedly**
- Verify credentials in `.env` file
- Check if two-factor authentication is enabled
- Ensure FEIDE_DISPLAY_NAME matches exactly

**Unit not found**
- Double-check the SIT_UNIT ID
- Verify the unit is actually available for booking

### Debug Mode
Set `headless=False` in the script to watch the browser automation.

## 📊 Logging

The application creates detailed logs:
- `status-log.jsonl`: Complete event history
- `last_status.json`: Most recent status
- `booked.png`: Screenshot when reservation succeeds

## ⚖️ Legal & Ethical Considerations

- This tool is for personal use only
- Respect the housing portal's terms of service
- Do not run multiple instances simultaneously
- Be mindful of server load and rate limiting
- Use responsibly and ethically

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and personal use. Please respect all applicable terms of service and use responsibly.

## ⚠️ Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for complying with all applicable terms of service and regulations. The authors are not responsible for any consequences of using this software.

---

**Remember**: This tool only reserves apartments - you must complete the contract signing manually!
