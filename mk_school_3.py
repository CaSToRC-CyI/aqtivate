import re, os, shutil
from collections import OrderedDict

with open('./school_1.md', 'r') as fp:
    lines = [line.rstrip('\n') for line in fp]

mappings = OrderedDict({
    "Introduction - Matrix Product States": "Intro-1-MPS.pdf",
    "Introduction - Time Evolving Block Decimation & Denity Matrix Renormalization Group": "Intro-2-TEBD-DMRG.pdf",
    "Tensor Networks for Machine Learning": "PaduaTNML.pdf",
    "Tree Tensor Networks": "SilviTTN.pdf",
    "Exercises": "TNschoolPadua.zip",
})
    
outbuf = ""
for i,line in enumerate(lines):
    outbuf += line + "\n"

for topic in mappings:
    fname = mappings[topic]
    ext = fname.split(".")[-1]
    assert ext in ["zip", "pdf"]
    s = {"zip": "archive", "pdf": "slides"}[ext]
    outbuf += f'- {topic} <span class="small-mono">[[{s}](../resources/school_3/{mappings[topic]})]</span>\n'
    source_fn = f"./material/school_3/{mappings[topic]}"
    target_fn = f"./docs/resources/school_3/{mappings[topic]}"
    if not os.path.exists(os.path.dirname(target_fn)):
        os.makedirs(os.path.dirname(target_fn))
    shutil.copy(f"{source_fn}", f"{target_fn}")

outbuf += f'- Quantum Weeks Hackathon Topics <span class="small-mono">[[listing](../resources/school_3/quantum_weeks.md)]</span>\n'
with open(f"./docs/resources/school_3/quantum_weeks.md", "w") as fp:
    for fname in sorted(os.listdir("./material/school_3/")):
        if "QuantumWeeksPadova_Hackathon_Topic" in fname:
            shutil.copy(f"./material/school_3/{fname}", f"./docs/resources/school_3/{fname}")
            listing_line = f'- <span class="mono">[{fname}](../../resources/school_3/{fname})</span>\n'
            fp.write(listing_line)
print(outbuf)


