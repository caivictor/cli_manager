# cli_manager/hook.bash

# Ensure Python environment is available or use system python
PYTHON_BIN="python3"
RECORDER_SCRIPT="/home/caiv/.openclaw/agents/dev-team/pm/cli_manager/recorder.py"

cli_manager_hook() {
    # Capture the last command from history
    # fc -ln -1 gets the last command without line numbers
    local last_command=$(fc -ln -1 2>/dev/null)
    
    # Trim leading/trailing whitespace
    last_command="${last_command#"${last_command%%[![:space:]]*}"}"
    last_command="${last_command%"${last_command##*[![:space:]]}"}"
    
    # If empty, do nothing
    if [ -z "$last_command" ]; then
        return
    fi
    
    # Run the recorder script in the background to avoid blocking the shell
    # Redirect output to /dev/null so errors don't pollute the terminal
    # Run in a subshell ( ... & ) to prevent "[1]+ Done" messages
    ( "$PYTHON_BIN" "$RECORDER_SCRIPT" "$last_command" >/dev/null 2>&1 & )
}

# Append to PROMPT_COMMAND
# Check if PROMPT_COMMAND is already set, if so append, else set
if [[ -z "$PROMPT_COMMAND" ]]; then
    PROMPT_COMMAND="cli_manager_hook"
else
    # Avoid adding it multiple times if sourced repeatedly
    if [[ "$PROMPT_COMMAND" != *"cli_manager_hook"* ]]; then
        PROMPT_COMMAND="$PROMPT_COMMAND; cli_manager_hook"
    fi
fi
