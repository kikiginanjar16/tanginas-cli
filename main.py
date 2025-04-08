import os
import ast
import astor
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
import openai
from typing import Dict, List

openai.api_key = "disini_api_key_anda"


class AdvancedCodeAssistant:
    def __init__(self):
        self.files: Dict[str, str] = {}
        self.current_file: str = None
        self.history: List[str] = []

    def load_file(self, filename: str) -> None:
        try:
            with open(filename, "r") as f:
                content = f.read()
            self.files[filename] = content
            self.current_file = filename
            self.history.append(f"Loaded {filename}")
            print(f"File {filename} berhasil dimuat")
        except FileNotFoundError:
            self.files[filename] = ""
            self.current_file = filename
            print(f"Membuat file baru: {filename}")

    def save_file(self, filename: str = None) -> None:
        target = filename or self.current_file
        if not target or target not in self.files:
            print("Tidak ada file yang valid untuk disimpan")
            return
        with open(target, "w") as f:
            f.write(self.files[target])
        self.history.append(f"Saved {target}")
        print(f"Perubahan disimpan ke {target}")

    def ai_suggest(self, request: str) -> None:
        if not self.current_file:
            print("Silakan load file terlebih dahulu")
            return

        prompt = f"""
        Berikan hanya kode program untuk: {request}
        Konteks saat ini:
        {self.files[self.current_file]}
        Jangan tambahkan penjelasan atau teks tambahan, hanya kode saja.
        Tolong kirimkan tanpa format markdown atau tanpa blok kode ``` ya
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Anda adalah asisten senior developer yang ahli",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            suggestion = response.choices[0].message.content
            self.files[self.current_file] += "\n\n" + suggestion
            self.history.append(f"AI suggestion for: {request}")
            print(suggestion)
        except Exception as e:
            print(f"Error saat meminta saran AI: {e}")

    def refactor_function(self, func_name: str) -> None:
        if not self.current_file or self.current_file not in self.files:
            print("Silakan load file terlebih dahulu")
            return
        try:
            tree = ast.parse(self.files[self.current_file])
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == func_name:
                    if not ast.get_docstring(node):
                        docstring = ast.Expr(
                            value=ast.Str(s=f"Function {func_name} documentation")
                        )
                        node.body.insert(0, docstring)
                    new_code = astor.to_source(tree)
                    self.files[self.current_file] = new_code
                    self.history.append(f"Refactored function {func_name}")
                    print(f"Function {func_name} telah direfaktor")
                    self._highlight_code(new_code)
                    return
            print(f"Tidak menemukan fungsi {func_name}")
        except SyntaxError:
            print("Error parsing kode")

    def _highlight_code(self, code: str) -> None:
        highlighted = highlight(code, PythonLexer(), TerminalFormatter())
        print(highlighted)

    def show_content(self, filename: str = None) -> None:
        target = filename or self.current_file
        if not target or target not in self.files:
            print("Tidak ada file yang valid untuk ditampilkan")
            return
        print(f"\nIsi file {target}:")
        self._highlight_code(self.files[target])

    def list_files(self) -> None:
        if not self.files:
            print("Belum ada file yang dimuat")
            return
        print("File yang sedang dikelola:")
        for f in self.files.keys():
            print(f"- {f} {'(aktif)' if f == self.current_file else ''}")

    def run(self) -> None:
        print("Selamat datang di Advanced Code Assistant!")
        print(
            "Perintah: load <filename>, save [filename], ai <request>, refactor <func_name>, show [filename], list, exit"
        )
        while True:
            cmd = input("> ").strip().split()
            if not cmd:
                continue
            if cmd[0] == "exit":
                print("Keluar dari Advanced Code Assistant")
                break
            elif cmd[0] == "load" and len(cmd) > 1:
                self.load_file(cmd[1])
            elif cmd[0] == "save":
                self.save_file(cmd[1] if len(cmd) > 1 else None)
            elif cmd[0] == "ai" and len(cmd) > 1:
                self.ai_suggest(" ".join(cmd[1:]))
            elif cmd[0] == "refactor" and len(cmd) > 1:
                self.refactor_function(cmd[1])
            elif cmd[0] == "show":
                self.show_content(cmd[1] if len(cmd) > 1 else None)
            elif cmd[0] == "list":
                self.list_files()
            else:
                print("Perintah tidak dikenal")


if __name__ == "__main__":
    assistant = AdvancedCodeAssistant()
    assistant.run()
