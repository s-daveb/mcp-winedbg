from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from .winedbg_wrapper import WineDbgWrapper
import uvicorn
import os


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

async def list_tools(request):
    tools = [
        {"name": "run", "description": "Run an executable in winedbg"},
        {"name": "attach", "description": "Attach to a process"},
        {"name": "quit", "description": "Quit winedbg"},
        {"name": "detach", "description": "Detach from the process"},
        {"name": "kill", "description": "Kill the process"},
        {"name": "cont", "description": "Continue execution"},
        {"name": "break_at", "description": "Set a breakpoint"},
        {"name": "watch", "description": "Set a watchpoint"},
        {"name": "info_break", "description": "Get breakpoint info"},
        {"name": "delete_breakpoint", "description": "Delete a breakpoint"},
        {"name": "backtrace", "description": "Get a backtrace"},
        {"name": "frame", "description": "Select a stack frame"},
        {"name": "up", "description": "Move up the stack"},
        {"name": "down", "description": "Move down the stack"},
        {"name": "step", "description": "Step execution"},
        {"name": "next", "description": "Next execution"},
        {"name": "stepi", "description": "Step instruction"},
        {"name": "nexti", "description": "Next instruction"},
        {"name": "finish", "description": "Finish execution of the current function"},
        {"name": "print_var", "description": "Print a variable"},
        {"name": "examine_memory", "description": "Examine memory"},
        {"name": "info_locals", "description": "Get local variables"},
        {"name": "info_args", "description": "Get function arguments"},
        {"name": "info_proc", "description": "Get process info"},
        {"name": "info_threads", "description": "Get thread info"},
        {"name": "info_share", "description": "Get shared library info"},
        {"name": "set_debug_channel", "description": "Set the WINEDEBUG environment variable"},
        {"name": "get_debug_channels", "description": "Get the WINEDEBUG environment variable"},
    ]
    return JSONResponse(tools)

async def run(request):
    data = await request.json()
    result = winedbg.run(data["executable"])
    return JSONResponse({"result": result})

async def attach(request):
    data = await request.json()
    result = winedbg.attach(data["pid"])
    return JSONResponse({"result": result})

async def quit(request):
    result = winedbg.quit()
    return JSONResponse({"result": result})

async def detach(request):
    result = winedbg.detach()
    return JSONResponse({"result": result})

async def kill(request):
    result = winedbg.kill()
    return JSONResponse({"result": result})

async def cont(request):
    result = winedbg.cont()
    return JSONResponse({"result": result})

async def break_at(request):
    data = await request.json()
    result = winedbg.break_at(data["location"])
    return JSONResponse({"result": result})

async def watch(request):
    data = await request.json()
    result = winedbg.watch(data["address"])
    return JSONResponse({"result": result})

async def info_break(request):
    result = winedbg.info_break()
    return JSONResponse({"result": result})

async def delete_breakpoint(request):
    data = await request.json()
    result = winedbg.delete_breakpoint(data["number"])
    return JSONResponse({"result": result})

async def backtrace(request):
    result = winedbg.backtrace()
    return JSONResponse({"result": result})

async def frame(request):
    data = await request.json()
    result = winedbg.frame(data["number"])
    return JSONResponse({"result": result})

async def up(request):
    result = winedbg.up()
    return JSONResponse({"result": result})

async def down(request):
    result = winedbg.down()
    return JSONResponse({"result": result})

async def step(request):
    result = winedbg.step()
    return JSONResponse({"result": result})

async def next_step(request):
    result = winedbg.next()
    return JSONResponse({"result": result})

async def stepi(request):
    result = winedbg.stepi()
    return JSONResponse({"result": result})

async def nexti(request):
    result = winedbg.nexti()
    return JSONResponse({"result": result})

async def finish(request):
    result = winedbg.finish()
    return JSONResponse({"result": result})

async def print_var(request):
    data = await request.json()
    result = winedbg.print_var(data["expression"])
    return JSONResponse({"result": result})

async def examine_memory(request):
    data = await request.json()
    result = winedbg.examine_memory(data["address"])
    return JSONResponse({"result": result})

async def info_locals(request):
    result = winedbg.info_locals()
    return JSONResponse({"result": result})

async def info_args(request):
    result = winedbg.info_args()
    return JSONResponse({"result": result})

async def info_proc(request):
    result = winedbg.info_proc()
    return JSONResponse({"result": result})

async def info_threads(request):
    result = winedbg.info_threads()
    return JSONResponse({"result": result})

async def info_share(request):
    result = winedbg.info_share()
    return JSONResponse({"result": result})

async def set_debug_channel(request):
    data = await request.json()
    os.environ["WINEDEBUG"] = data["channels"]
    return JSONResponse({"result": f"WINEDEBUG set to {os.environ['WINEDEBUG']}"})

async def get_debug_channels(request):
    channels = os.environ.get("WINEDEBUG", "")
    return JSONResponse({"result": channels})


routes = [
    Route("/tools", endpoint=list_tools),
    Route("/run", endpoint=run, methods=["POST"]),
    Route("/attach", endpoint=attach, methods=["POST"]),
    Route("/quit", endpoint=quit, methods=["POST"]),
    Route("/detach", endpoint=detach, methods=["POST"]),
    Route("/kill", endpoint=kill, methods=["POST"]),
    Route("/cont", endpoint=cont, methods=["POST"]),
    Route("/break", endpoint=break_at, methods=["POST"]),
    Route("/watch", endpoint=watch, methods=["POST"]),
    Route("/info_break", endpoint=info_break, methods=["POST"]),
    Route("/delete_breakpoint", endpoint=delete_breakpoint, methods=["POST"]),
    Route("/backtrace", endpoint=backtrace, methods=["POST"]),
    Route("/frame", endpoint=frame, methods=["POST"]),
    Route("/up", endpoint=up, methods=["POST"]),
    Route("/down", endpoint=down, methods=["POST"]),
    Route("/step", endpoint=step, methods=["POST"]),
    Route("/next", endpoint=next_step, methods=["POST"]),
    Route("/stepi", endpoint=stepi, methods=["POST"]),
    Route("/nexti", endpoint=nexti, methods=["POST"]),
    Route("/finish", endpoint=finish, methods=["POST"]),
    Route("/print", endpoint=print_var, methods=["POST"]),
    Route("/examine", endpoint=examine_memory, methods=["POST"]),
    Route("/info_locals", endpoint=info_locals, methods=["POST"]),
    Route("/info_args", endpoint=info_args, methods=["POST"]),
    Route("/info_proc", endpoint=info_proc, methods=["POST"]),
    Route("/info_threads", endpoint=info_threads, methods=["POST"]),
    Route("/info_share", endpoint=info_share, methods=["POST"]),
    Route("/set_debug_channel", endpoint=set_debug_channel, methods=["POST"]),
    Route("/get_debug_channels", endpoint=get_debug_channels, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
