import os
import pexpect
import re
import shutil
import subprocess

class WineDbgWrapper:
    def __init__(self, msync=True):
        self.process = None
        self.msync = msync
        self.winedbg_path = self._find_winedbg()
        if not self.winedbg_path:
            raise RuntimeError(
                "winedbg not found. Install it and add it to PATH, "
                "or set the WINEDBG_PATH environment variable to its full path."
            )

    def _find_winedbg(self):
        path = os.environ.get("WINEDBG_PATH")
        if path:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                return path
            return None
        return shutil.which("winedbg")

    def is_winedbg_installed(self):
        return self._find_winedbg() is not None

    def _spawn(self, args, timeout=30):
        assert self.winedbg_path is not None
        if self.msync and os.environ.get("WINEMSYNC") is None:
            os.environ["WINEMSYNC"] = "1"
        return pexpect.spawn(self.winedbg_path, args=args, encoding='utf-8', timeout=timeout)

    def start(self, args):
        self.process = self._spawn(args)
        self.process.expect(r'Wine-dbg>')
        return str(self.process.before or "")

    def send_command(self, command, timeout=30):
        if not self.process:
            return "winedbg not running."

        self.process.sendline(command)
        self.process.expect(r'Wine-dbg>', timeout=timeout)
        return str(self.process.before or "")

    def run(self, executable):
        return self.start([executable])

    def attach(self, target):
        resolved = self._resolve_target(target)
        if resolved is None:
            procs = self._list_processes()
            if not procs:
                return "No running Wine processes found to attach to."
            avail = ", ".join(f"{pid} ({name})" for pid, name in sorted(procs.items()))
            return f"Could not resolve target {target!r} to a running Wine process. Use: attach <windows-pid> or attach <executable-name>. Running: {avail}"
        return self.start([str(resolved)])

    def _run_command(self, command, timeout=60):
        p = self._spawn(["--command", command], timeout=timeout)
        p.expect(pexpect.EOF, timeout=timeout)
        return str(p.before or "")

    def _list_processes(self):
        out = self._run_command("info proc")
        clean = re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]|\x1b\][^\x07]*\x07|\r", "", out)
        procs = {}
        for m in re.finditer(r"([0-9a-f]+)\s+\d+\s+[^'\n]*'([^']+\.exe)'", clean):
            procs[int(m.group(1), 16)] = m.group(2)
        return procs

    def _unix_processes(self):
        out = subprocess.check_output(["ps", "-axo", "pid=,command="], text=True, errors="replace")
        procs = {}
        for line in out.splitlines():
            parts = line.split()
            if len(parts) < 2:
                continue
            cmd = " ".join(parts[1:])
            if ".exe" not in cmd.lower():
                continue
            name = re.search(r"([^\\/]+\.exe)\s*$", cmd)
            if not name:
                continue
            procs[int(parts[0])] = name.group(1)
        return procs

    def _resolve_target(self, target):
        procs = self._list_processes()
        if not procs:
            return None
        if isinstance(target, bool):
            return None
        if isinstance(target, int):
            if target in procs:
                return target
            unix = self._unix_processes()
            name = unix.get(target)
            if name:
                matched = [pid for pid, n in procs.items() if n.lower() == name.lower()]
                if len(matched) == 1:
                    return matched[0]
            return None
        name = str(target).strip().lower()
        if not name.endswith(".exe"):
            name += ".exe"
        matched = [pid for pid, n in procs.items() if n.strip().lower() == name]
        if len(matched) == 1:
            return matched[0]
        return None

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
