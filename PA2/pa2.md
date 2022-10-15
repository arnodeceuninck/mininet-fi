# note-pa2

## Tmux
POX needs to be ran in another window, but I only have the VM terminal window (since my SSH didn't work (and I'm using shared folders for transfering files)).

To solve this, I used `tmux`.

Most important tmux commands:
- `tmux new -s <session_name>`: Create a new session
- `tmux attach -t <session_name>`: Attach to a session
- `tmux ls`: List all sessions
- `tmux kill-session -t <session_name>`: Kill a session
- `tmux kill-server`: Kill all sessions
- `tmux detach`: Detach from a session
- `tmux a`: Attach to the last session

To leave active sessions, you can use following keybindings:
- `Ctrl + b` + `d`: Detach from a session
- `Ctrl + b` + `&`: Kill a session
- `Ctrl + b` + `s`: List all sessions
- `Ctrl + b` + `(`: Switch to the previous session
- `Ctrl + b` + `)` Switch to the next session

Nvm, got ssh working (and also xterm using wsl), skip the tmux part.