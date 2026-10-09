import hashlib

def parse_qr_text(qr_text):
    parts = qr_text.split(";")
    params = {}
    for p in parts:
        key, val = p.split("=")
        params[key] = val
    return params

def pseudo_hash(G_desc, seed, index):
    data = f"{G_desc}:{seed}:{index}".encode()
    h = hashlib.sha256(data).hexdigest()
    return int(h, 16)

def generate_text(G_desc, seed, start, end):
    library = [
        "Boil water.",
        "Add pasta.",
        "Cook for 8–10 minutes.",
        "Drain and add sauce.",
        "Serve hot.",
        "Chop onions.",
        "Heat oil in pan.",
        "Add garlic.",
        "Simmer for 5 minutes.",
        "Season with salt.",
        "Enjoy your meal."
    ]

    output_lines = []
    for i in range(start, end):
        h = pseudo_hash(G_desc, seed, i)
        step = library[h % len(library)]
        output_lines.append(step)

    return "\n".join(output_lines)

def wrap_pdf(text):
    pdf = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj

2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj

3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]
   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj

4 0 obj
<< /Length {len(text)} >>
stream
BT
/F1 12 Tf
72 720 Td
({text.replace('(', '[').replace(')', ']')}) Tj
ET
endstream
endobj

5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj

xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000079 00000 n 
0000000148 00000 n 
0000000301 00000 n 
0000000500 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
600
%%EOF
"""
    return pdf

def save_pdf(filename, pdf_text):
    with open(filename, "wb") as f:
        f.write(pdf_text.encode("latin-1", errors="replace"))

# -------------------------
# MAIN EXECUTION
# -------------------------

qr_text = "G=10^^6;seed=987654321;start=0;end=5000"

params = parse_qr_text(qr_text)

G_desc = params["G"]
seed = int(params["seed"])
start = int(params["start"])
end = int(params["end"])

generated_text = generate_text(G_desc, seed, start, end)
pdf_output = wrap_pdf(generated_text)

save_pdf("prototype_100kb.pdf", pdf_output)

print("PDF generated: prototype_100kb.pdf")
