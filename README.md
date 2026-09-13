# WineDbg MCP Server

This project provides a server that wraps the Wine Debugger (`winedbg`) and exposes its functionality through a simple API. This allows you to debug Windows applications running under Wine from a remote client.

## Installation

1.  Install Wine and `winedbg`.
2.  Install the package directly from GitHub (optionally inside a virtual environment):

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install git+https://github.com/s-daveb/mcp-winedbg.git
    ```

    Or, for local development:

    ```bash
    pip install -e .
    ```

## Usage

The server speaks the Model Context Protocol over **stdio** by default, so it works directly with any MCP client.

1.  Start the server:

    ```bash
    mcp-winedbg
    ```

    Or, if installed from source:

    ```bash
    python -m mcp_winedbg
    ```

`winedbg` is located by searching your `PATH`. If it lives somewhere custom (for example inside a Wine wrapper bundle on macOS), point the server at it with the `WINEDBG_PATH` environment variable:

```bash
export WINEDBG_PATH="/path/to/app/Contents/Wineskin.app/Contents/Resources/winedbg"
mcp-winedbg
```

### Legacy HTTP server

A previous version exposed the same commands over a plain HTTP API on port 8080. It is still available as `mcp-winedbg-http` (or `python -m mcp_winedbg.mcp_server`) for backwards compatibility, and `tests/test_client.py` uses it.

2.  Run the test client to see the HTTP server in action:

    ```bash
    python tests/test_client.py
    ```

## Testing with the Test App

This project includes a simple C application that can be used for testing the server.

1.  Compile the test application for 32-bit Windows:

    ```bash
    i686-w64-mingw32-gcc -o tests/test_app.exe tests/test_app.c
    ```

    If you don't have the MinGW-w64 cross-compiler, you can install it on Debian/Ubuntu with:
    `sudo apt-get install gcc-mingw-w64-i686`

2.  Run the test client:

    ```bash
    python tests/test_client.py
    ```

    The test client will automatically use the `test_app.exe` to test the server's functionality.

## MCP Client Configuration

If you are using an MCP client that supports launching stdio servers, configure it with the following JSON. Use the **full absolute path** to the `mcp-winedbg` executable (clients launched from a GUI may not have your shell's `PATH`), and set `WINEDBG_PATH` if `winedbg` is not on the client's `PATH`.

```json
{
  "mcpServers": {
    "winedbg": {
      "command": "/Users/you/.venv/bin/mcp-winedbg",
      "env": {
        "WINEDBG_PATH": "/path/to/app/Contents/Wineskin.app/Contents/Resources/winedbg"
      }
    }
  }
}
```

## Available Tools

The server exposes the following tools:

*   `run`: Run an executable in `winedbg`.
*   `attach`: Attach to a running Wine process by Windows PID (e.g. `2412`), Unix PID, or executable name (e.g. `Bonfire.exe`). The Windows PID is resolved automatically via `info proc`. Attaching requires `WINEMSYNC=1` when the target prefix's wineserver runs in msync mode (the wrapper sets it unless already defined).
*   `quit`: Quit `winedbg`.
*   `detach`: Detach from the process.
*   `kill`: Kill the process.
*   `cont`: Continue execution.
*   `break_at`: Set a breakpoint.
*   `watch`: Set a watchpoint.
*   `info_break`: Get breakpoint info.
*   `delete_breakpoint`: Delete a breakpoint.
*   `backtrace`: Get a backtrace.
*   `frame`: Select a stack frame.
*   `up`: Move up the stack.
*   `down`: Move down the stack.
*   `step`: Step execution.
*   `next`: Next execution.
*   `stepi`: Step instruction.
*   `nexti`: Next instruction.
*   `finish`: Finish execution of the current function.
*   `print_var`: Print a variable.
*   `examine_memory`: Examine memory.
*   `info_locals`: Get local variables.
*   `info_args`: Get function arguments.
*   `info_proc`: Get process info.
*   `info_threads`: Get thread info.
*   `info_share`: Get shared library info.
*   `set_debug_channel`: Set the `WINEDEBUG` environment variable.
*   `get_debug_channels`: Get the `WINEDEBUG` environment variable.
