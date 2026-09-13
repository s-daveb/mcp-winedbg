import pexpect
import shutil

class WineDbgWrapper:
    def __init__(self):
        self.process = None
        if not self.is_winedbg_installed():
            raise RuntimeError("winedbg is not installed. Please install it to use this wrapper.")

    def is_winedbg_installed(self):
        return shutil.which("winedbg") is not None

    def start(self, command):
        self.process = pexpect.spawn(command, encoding='utf-8')
        self.process.expect(r'Wine-dbg>')
        return self.process.before

    def send_command(self, command):
        if not self.process:
            return "winedbg not running."
        
        self.process.sendline(command)
        self.process.expect(r'Wine-dbg>')
        return self.process.before

    def run(self, executable):
        return self.start(f"winedbg {executable}")

    def attach(self, pid):
        return self.start(f"winedbg --pid {pid}")

    def quit(self):
        if self.process:
            self.process.close()
            self.process = None
        return "winedbg terminated."

    def detach(self):
        return self.send_command("detach")

    def kill(self):
        return self.send_command("kill")

    def cont(self):
        return self.send_command("cont")

    def break_at(self, location):
        return self.send_command(f"break {location}")

    def watch(self, address):
        return self.send_command(f"watch {address}")

    def info_break(self):
        return self.send_command("info break")

    def delete_breakpoint(self, number):
        return self.send_command(f"delete {number}")

    def backtrace(self):
        return self.send_command("bt")

    def frame(self, number):
        return self.send_command(f"frame {number}")

    def up(self):
        return self.send_command("up")

    def down(self):
        return self.send_command("down")

    def step(self):
        return self.send_command("step")

    def next(self):
        return self.send_command("next")

    def stepi(self):
        return self.send_command("stepi")

    def nexti(self):
        return self.send_command("nexti")

    def finish(self):
        return self.send_command("finish")

    def print_var(self, expression):
        return self.send_command(f"print {expression}")

    def examine_memory(self, address):
        return self.send_command(f"x {address}")

    def info_locals(self):
        return self.send_command("info locals")

    def info_args(self):
        return self.send_command("info args")

    def info_proc(self):
        return self.send_command("info proc")

    def info_threads(self):
        return self.send_command("info threads")

    def info_share(self):
        return self.send_command("info share")
