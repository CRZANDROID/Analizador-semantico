import tkinter as tk
from tkinter import scrolledtext
from analizadorLexico import LexerAnalyzer

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Lexer Analyzer")

        font_style = ("Consolas", 12, "normal")
        background_color = "#1e1e1e"
        foreground_color = "#d4d4d4"

        self.lexer_analyzer = LexerAnalyzer()

        self.input_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=20, font=font_style)
        self.input_text.pack(pady=10, padx=10)
        self.input_text.config(bg=background_color, fg=foreground_color, insertbackground=foreground_color)

        self.analyze_button = tk.Button(master, text="Analyze", command=self.analyze)
        self.analyze_button.pack(pady=5)

        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=20, font=font_style)
        self.result_text.pack(pady=10, padx=10)
        self.result_text.config(bg=background_color, fg=foreground_color, state='disabled')
        self.result_text.tag_config('error', foreground='red')
        self.result_text.tag_config('correct', foreground='#32CD32')  # Verdenilo

    def analyze(self):
        data = self.input_text.get("1.0", tk.END)
        lex_results = self.lexer_analyzer.analyze(data)
        success, parse_result_or_errors = self.lexer_analyzer.parse(data)
        
        self.result_text.configure(state='normal')
        self.result_text.delete('1.0', tk.END)
        
        if success:
            self.result_text.insert(tk.END, "Análisis Sintáctico Completo: Sin Errores\n", 'correct')
        else:
            for error in parse_result_or_errors:
                self.result_text.insert(tk.END, error + '\n', 'error')
                
        self.result_text.insert(tk.END, "Lista de Tokens:\n")
        for token in lex_results:
            self.result_text.insert(tk.END, f"{token}\n")
                
        self.result_text.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

