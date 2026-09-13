from fastmcp import FastMCP
import os

from .winedbg_wrapper import WineDbgWrapper


class _LazyWineDbg:
    def __init__(self):
        self._wrapper = None

    def _get(self):
        if self._wrapper is None:
            self._wrapper = WineDbgWrapper()
        return self._wrapper

    def __getattr__(self, name):
        return getattr(self._get(), name)


winedbg = _LazyWineDbg()

mcp = FastMCP(
    "winedbg",
    instructions="Server that wraps the Wine Debugger (winedbg) and exposes its commands as MCP tools.",
)


@mcp.tool()
def run(executable: str) -> str:
    """Run an executable in winedbg."""
    return winedbg.run(executable)


@mcp.tool()
def attach(pid: int) -> str:
    """Attach to a process by PID."""
    return winedbg.attach(pid)


@mcp.tool()
def quit() -> str:
    """Quit winedbg."""
    return winedbg.quit()


@mcp.tool()
def detach() -> str:
    """Detach from the process."""
    return winedbg.detach()


@mcp.tool()
def kill() -> str:
    """Kill the process."""
    return winedbg.kill()


@mcp.tool()
def cont() -> str:
    """Continue execution."""
    return winedbg.cont()


@mcp.tool()
def break_at(location: str) -> str:
    """Set a breakpoint at the given location."""
    return winedbg.break_at(location)


@mcp.tool()
def watch(address: str) -> str:
    """Set a watchpoint at the given address."""
    return winedbg.watch(address)


@mcp.tool()
def info_break() -> str:
    """Get breakpoint info."""
    return winedbg.info_break()


@mcp.tool()
def delete_breakpoint(number: int) -> str:
    """Delete a breakpoint by number."""
    return winedbg.delete_breakpoint(number)


@mcp.tool()
def backtrace() -> str:
    """Get a backtrace."""
    return winedbg.backtrace()


@mcp.tool()
def frame(number: int) -> str:
    """Select a stack frame by number."""
    return winedbg.frame(number)


@mcp.tool()
def up() -> str:
    """Move up the stack."""
    return winedbg.up()


@mcp.tool()
def down() -> str:
    """Move down the stack."""
    return winedbg.down()


@mcp.tool()
def step() -> str:
    """Step execution."""
    return winedbg.step()


# "next" is a Python builtin; the tool name is set explicitly.
@mcp.tool(name="next")
def next_() -> str:
    """Next execution (step over)."""
    return winedbg.next()


@mcp.tool()
def stepi() -> str:
    """Step instruction."""
    return winedbg.stepi()


@mcp.tool()
def nexti() -> str:
    """Next instruction."""
    return winedbg.nexti()


@mcp.tool()
def finish() -> str:
    """Finish execution of the current function."""
    return winedbg.finish()


@mcp.tool()
def print_var(expression: str) -> str:
    """Print a variable or expression."""
    return winedbg.print_var(expression)


@mcp.tool()
def examine_memory(address: str) -> str:
    """Examine memory at the given address."""
    return winedbg.examine_memory(address)


@mcp.tool()
def info_locals() -> str:
    """Get local variables."""
    return winedbg.info_locals()


@mcp.tool()
def info_args() -> str:
    """Get function arguments."""
    return winedbg.info_args()


@mcp.tool()
def info_proc() -> str:
    """Get process info."""
    return winedbg.info_proc()


@mcp.tool()
def info_threads() -> str:
    """Get thread info."""
    return winedbg.info_threads()


@mcp.tool()
def info_share() -> str:
    """Get shared library info."""
    return winedbg.info_share()


@mcp.tool()
def set_debug_channel(channels: str) -> str:
    """Set the WINEDEBUG environment variable."""
    os.environ["WINEDEBUG"] = channels
    return f"WINEDEBUG set to {os.environ['WINEDEBUG']}"


@mcp.tool()
def get_debug_channels() -> str:
    """Get the WINEDEBUG environment variable."""
    return os.environ.get("WINEDEBUG", "")


def main():
    mcp.run("stdio")


if __name__ == "__main__":
    main()