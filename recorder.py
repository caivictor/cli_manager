import sys
import re
import os
from database import init_db, upsert_command

# Initialize DB on first run if needed
if not os.path.exists(os.path.expanduser("~/.cli_manager.db")):
    init_db()

def is_secret(cmd):
    """
    Check if a command looks like it contains sensitive info.
    """
    cmd_lower = cmd.lower()
    
    # Check for leading space (often used to hide commands in history)
    if cmd.startswith(" "):
        return True
        
    # Check for common keywords often associated with secrets
    secret_keywords = ["password", "token", "secret", "api_key", "bearer "]
    for keyword in secret_keywords:
        if keyword in cmd_lower:
            return True
            
    # Check for environment variable assignments that look sensitive
    # e.g., EXPORT MY_KEY=...
    if re.search(r'(export\s+)?([A-Z_]+_?(KEY|TOKEN|SECRET|PASSWORD)\s*=\s*\S+)', cmd, re.IGNORECASE):
        return True
        
    return False

def record_command(cmd):
    if not cmd or not cmd.strip():
        return
    
    # Filter out empty commands or just whitespace
    cmd = cmd.strip()
    
    if is_secret(cmd):
        return

    try:
        upsert_command(cmd)
    except Exception as e:
        # Fail silently so we don't break the user's shell
        pass

if __name__ == "__main__":
    # Command is passed as arguments (joined by space to reconstruct)
    # The shell hook might split arguments, so we join them back.
    if len(sys.argv) > 1:
        full_command = " ".join(sys.argv[1:])
        record_command(full_command)
