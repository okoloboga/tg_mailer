# Telegram Mailer Bot

A Telegram bot built with Aiogram 3 to manage and schedule messages for Telegram channels. The bot allows an admin to send messages immediately, with a delay, or on a daily schedule to specified channels. It also supports editing and deleting scheduled tasks.

## Features

### Message Scheduling:
- Send messages immediately.
- Schedule messages with a delay (specific date and time).
- Schedule daily recurring messages at a fixed time.

### Channel Management:
- Select a channel from a predefined list to send messages to.

### Task Management:
- Edit existing tasks (update message text or scheduled time).
- Delete scheduled tasks.

### Interactive Interface:
- Uses inline keyboards for a seamless user experience.
- Supports navigation with "Back" buttons.

### Persistent Storage:
- Tasks are stored in a `tasks.json` file for persistence across restarts.

### Systemd Service:
- Deployed as a systemd service for reliable operation on a Linux server.

## Requirements

- Python 3.7+
- Aiogram 3.x (`aiogram`)
- Pydantic (`pydantic`)
- PyYAML (`pyyaml`)

## Installation

### Clone the Repository:
```bash
git clone git@github.com:okoloboga/tg_mailer.git
cd tg_mailer
```

### Set Up a Virtual Environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies:
```bash
pip install aiogram pydantic pyyaml
```

### Configure the Bot:
Create a `config.yaml` file in the project root with the following structure:
```yaml
bot:
  token: "your-bot-token-here"  # Get this from @BotFather
admin:
  id: "your-admin-id-here"  # Your Telegram user ID (find via @userinfobot)
channels:
  - url: "@yourchannel1"
    id: "-100123456789"  # Channel ID (find via @username_to_id_bot)
  - url: "@yourchannel2"
    id: "-100987654321"
```

Ensure the bot is added as an admin to the specified channels with permissions to send messages.

### Run the Bot Locally (for testing):
```bash
python __main__.py
```

## Deployment with Systemd

To run the bot as a background service on a Linux server:

### Copy the Project to the Server:
```bash
sudo mkdir -p /opt/tg_mailer
sudo chown $USER:$USER /opt/tg_mailer
scp -r . user@your-server-ip:/opt/tg_mailer
```

### Set Up the Environment on the Server:
```bash
cd /opt/tg_mailer
python3 -m venv venv
source venv/bin/activate
pip install aiogram pydantic pyyaml
```

### Create a Systemd Service:
Create a service file:
```bash
sudo nano /etc/systemd/system/tg_mailer.service
```
Add the following content (replace `user` with your username):
```ini
[Unit]
Description=Telegram Mailer Bot Service
After=network.target

[Service]
Type=simple
User=user
WorkingDirectory=/opt/tg_mailer
ExecStart=/opt/tg_mailer/venv/bin/python /opt/tg_mailer/__main__.py
Restart=always
RestartSec=10
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```
Save and exit (Ctrl+O, Enter, Ctrl+X in nano).

### Enable and Start the Service:
```bash
sudo systemctl daemon-reload
sudo systemctl start tg_mailer
sudo systemctl enable tg_mailer
```

### Check the Service Status:
```bash
sudo systemctl status tg_mailer
```
You should see the bot running:
```text
● tg_mailer.service - Telegram Mailer Bot Service
     Loaded: loaded (/etc/systemd/system/tg_mailer.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2025-03-03 12:00:00 UTC; 2s ago
```

### View Logs:
```bash
journalctl -u tg_mailer -f
```

## Usage

### Start the Bot:
- Send `/start` to the bot in Telegram.
- If you're the admin (as specified in `config.yaml`), you'll see a menu with two options:
  - **Create Task**: Start creating a new message.
  - **Manage Tasks**: View, edit, or delete existing tasks.

### Create a Task:
1. Choose "Create Task" and follow the prompts:
   - Enter the message text.
   - Select the schedule type:
     - **Immediate**: Sends the message right away.
     - **Delayed**: Sends the message at a specific date and time.
     - **Daily**: Sends the message every day at a fixed time.
   - For "Delayed", select the date and time.
   - For "Daily", select only the time.
   - Choose the channel to send the message to.
2. Once created, the task will be scheduled (or sent immediately for "Immediate").

### Manage Tasks:
- Choose "Manage Tasks" to see a list of scheduled tasks.
- Select a task to:
  - **Edit**: Update the message text or scheduled time.
  - **Delete**: Remove the task.
- Use the "Back" button to return to previous menus.

## Project Structure

- `__main__.py`: Entry point for the bot, initializes and starts the bot.
- `config.py`: Handles configuration loading from `config.yaml`.
- `handlers.py`: Contains all command and callback handlers for user interactions.
- `keyboards.py`: Defines inline keyboards for interactive menus.
- `utils.py`: Manages task storage (`tasks.json`) and the scheduling logic.
- `config.yaml`: Configuration file for bot token, admin ID, and channels.
- `tasks.json`: Persistent storage for scheduled tasks (created automatically).

## Task Storage Format

Tasks are stored in `tasks.json` with the following structure:
```json
[
    {
        "id": 1,
        "message": "Hello, channel!",
        "channel_id": "-100123456789",
        "schedule_type": "daily",
        "schedule_time": "12:00:00",
        "status": "pending",
        "last_sent_date": "2025-03-03"
    }
]
```

## Known Issues

- **Timezone**: The bot uses the server's local time. Ensure the server is set to the correct timezone (e.g., MSK for Moscow) to avoid scheduling issues.
- **Task Migration**: If updating the bot, you may need to manually adjust the format of `schedule_time` in `tasks.json` for existing daily tasks.

## Contributing

Feel free to submit pull requests or open issues for bug reports and feature requests.

## License

This project is licensed under the MIT License.