import tkinter as tk
from tkinter import filedialog, messagebox

# Mapowanie komplementarne IUPAC (DNA)
COMPLEMENT_MAP = {
    'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G',
    'R': 'Y', 'Y': 'R', 'S': 'S', 'W': 'W',
    'K': 'M', 'M': 'K', 'B': 'V', 'V': 'B',
    'D': 'H', 'H': 'D', 'N': 'N'
}

def read_sequence(file_path):
    seq = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('>'):
                continue
            seq.append(line.upper())
    return ''.join(seq)

def reverse_complement(seq):
    try:
        return ''.join(COMPLEMENT_MAP[base] for base in reversed(seq))
    except KeyError as e:
        raise ValueError(f"Nieznany nukleotyd: {e.args[0]}")

def write_sequence(seq, file_path, line_length=60):
    with open(file_path, 'w') as f:
        for i in range(0, len(seq), line_length):
            f.write(seq[i:i+line_length] + '\n')

def process():
    input_file = input_entry.get()
    output_file = output_entry.get()

    if not input_file or not output_file:
        messagebox.showerror("Błąd", "Wybierz plik wejściowy i wyjściowy.")
        return

    try:
        sequence = read_sequence(input_file)
        rev_comp = reverse_complement(sequence)
        write_sequence(rev_comp, output_file)
        messagebox.showinfo("Sukces", "Zapisano sekwencję komplementarną.")
    except Exception as e:
        messagebox.showerror("Błąd", str(e))

def browse_input():
    file_path = filedialog.askopenfilename(
        title="Wybierz plik wejściowy",
        filetypes=[("Pliki tekstowe", "*.txt *.fasta *.fa"), ("Wszystkie pliki", "*.*")]
    )
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def browse_output():
    file_path = filedialog.asksaveasfilename(
        title="Wybierz plik wyjściowy",
        defaultextension=".txt",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
    )
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

# GUI
root = tk.Tk()
root.title("Generator sekwencji komplementarnej DNA")

tk.Label(root, text="Plik wejściowy:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Przeglądaj", command=browse_input).grid(row=0, column=2, padx=5)

tk.Label(root, text="Plik wyjściowy:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Zapisz jako", command=browse_output).grid(row=1, column=2, padx=5)

tk.Button(root, text="Generuj", command=process, width=20).grid(row=2, column=1, pady=15)

root.mainloop()
