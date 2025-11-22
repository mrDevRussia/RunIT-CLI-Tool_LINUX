# RunIT-Linux

Linux port of the RunIT CLI tool. Provides the same commands and features using native Linux behaviors.

## Installation

- Ensure `python3` and `pip` are installed
- Run `./RunIT-Linux/install.sh`

## Usage

- Start: `./RunIT-Linux/run.sh`
- Interactive prompt: `RunIT-Linux>`

WSL setup instructions are available in `RunIT-Linux/WSL_GUIDE.md`.

## Supported Commands

- `help`, `version`, `clear`, `exit`
- `run`, `create`, `search`, `scan`, `info`
- `deploy`, `stopdeploy`, `share`, `setport`
- `preview`, `convert`, `runai`, `go`, `show`, `edit`
- `restart`, `uninstall`, `p2pmsg`, `cid`, `systeminfo`

## Differences from Windows Version

- Default openers use `xdg-open` instead of `start`
- `clear` uses `clear` instead of `cls`
- Deployment stop avoids `taskkill` and only shuts down the local server
- Batch files are executed via `bash` where possible
- No Windows-only guards; the CLI runs natively on Linux

## P2P Messaging

- Works with UDP hole punching, Diffie-Hellman (X25519), AES-GCM, HMAC
- Requires port forwarding for internet peers behind NAT
- See `docs/P2PMSG_GUIDE.md` for workflow and troubleshooting

## Known Limitations

- Public URL sharing via tunneling is disabled by default
- Some Windows-only packages may not be meaningful on Linux

## Future Improvements

- Optional tunnel integration for sharing
- Extended package ecosystem and Linux-specific helpers

## NOTE!
This is the first version of RunIT-Linux so there is no packge ecosystem made for linux yet.