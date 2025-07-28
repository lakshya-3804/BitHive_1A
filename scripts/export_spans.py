
# =========================BitHive===============================
# ===   TEAM MEMBERS:                   =========================
# ===   -> LAKSHYA PRAJAPATI            =========================
# ===   -> REBANT PRATAP SINGH          =========================
# ===   -> SATYAJIT SAHOO               =========================
# ===============================================================

import os, csv, fitz

out_csv = "data/annotations_template.csv"
pdf_folder = "data/input_pdfs"

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["pdf_file","page","text","font_size","x0","y0","flags","label"])
    for fname in os.listdir(pdf_folder):
        if not fname.lower().endswith(".pdf"): continue
        doc = fitz.open(os.path.join(pdf_folder, fname))
        for p in doc:
            for block in p.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        txt = span["text"].strip()
                        if not txt: continue
                        w.writerow([
                            fname, p.number+1, txt,
                            round(span["size"],1),
                            round(span["bbox"][0],1),
                            round(span["bbox"][1],1),
                            span["flags"], ""
                        ])
print("Template CSV →", out_csv)



# =========================BitHive===============================
# ===   TEAM MEMBERS:                   =========================
# ===   -> LAKSHYA PRAJAPATI            =========================
# ===   -> REBANT PRATAP SINGH          =========================
# ===   -> SATYAJIT SAHOO               =========================
# ===============================================================
