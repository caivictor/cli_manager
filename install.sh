#!/bin/bash

# Get absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_FILE="$PROJECT_DIR/hook.bash"
RECORDER_SCRIPT="$PROJECT_DIR/recorder.py"

echo "🔧 Setting up CLI Command Manager..."

# 1. Install Dependencies
echo "📦 Installing Python dependencies..."
pip install -r "$PROJECT_DIR/requirements.txt"

# 2. Initialize Database
echo "🗄️  Initializing database..."
python3 "$PROJECT_DIR/database.py"

# 3. Update Hook Script Paths
# We need to make sure hook.bash points to the correct absolute path of recorder.py
# (The current hook.bash uses $HOME/cli_manager/recorder.py which might be wrong if cloned elsewhere)
# Let's dynamically update it or just assume standard install location.
# Better: Let's sed/replace the path in hook.bash to be safe.
sed -i "s|RECORDER_SCRIPT=\".*\"|RECORDER_SCRIPT=\"$RECORDER_SCRIPT\"|" "$HOOK_FILE"

# 4. Link to Shell
SHELL_RC="$HOME/.bashrc"
SOURCE_CMD="source \"$HOOK_FILE\""

if grep -Fxq "$SOURCE_CMD" "$SHELL_RC"; then
    echo "✅ Hook already present in $SHELL_RC"
else
    echo "" >> "$SHELL_RC"
    echo "# CLI Command Manager Hook" >> "$SHELL_RC"
    echo "$SOURCE_CMD" >> "$SHELL_RC"
    echo "🔗 Added hook to $SHELL_RC"
fi

echo "🎉 Installation complete!"
echo "👉 Restart your shell or run 'source ~/.bashrc' to start recording."
echo "👉 To view commands, run: python3 $PROJECT_DIR/app.py"
