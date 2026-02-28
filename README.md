# CLI Command Manager 💻

A tool to record your terminal history into a structured database and a web interface to browse, filter, and copy common commands.

## 🌟 Features

- **Auto-Recording**: Hooks into Bash to capture every command.
- **Smart Filtering**: Ignores duplicates (increments count instead), ignores secrets (passwords/keys), and ignores leading-space commands.
- **Web Dashboard**: Clean UI to sort by "Most Frequent" or "Last Used".
- **One-Click Copy**: Copy commands back to your clipboard instantly.

## 🛠️ Installation

1.  Run the installer:
    ```bash
    cd cli_manager
    ./install.sh
    ```
2.  Restart your terminal (or run `source ~/.bashrc`).

## 🚀 Usage

### Recording
Just use your terminal as normal! Commands are saved to `~/.cli_manager.db`.

### Dashboard
Start the web server:
```bash
python3 cli_manager/app.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

## 🔒 Privacy
The recorder automatically ignores:
- Commands starting with a space (standard Bash behavior).
- Commands containing "password", "token", "secret", "api_key", or "bearer".
- Environment variable exports that look sensitive.
