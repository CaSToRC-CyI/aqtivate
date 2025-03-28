import re, os, shutil
from collections import OrderedDict

with open('./cfd.md', 'r') as fp:
    lines = [line.rstrip('\n') for line in fp]

mappings = OrderedDict({
    "Kinetic Theory and Applications to Fluid Mechanics": "Slides_kinetic_theory_guglietta_compressed.pdf",
    "Optimal Policies for Lagrangian Turbulence": ["lecture_1.pdf", "lecture_2.pdf", "lecture_3.pdf", "lecture_4.pdf", "lecture_5.pdf"],
    "Data-Driven Tools for Eulerian Turbulence": ["Slides_Lectures_C1_C2.pdf", "Slides_Lectures_C5_C6.pdf"],
    "Exercises": "Code.zip"
})
    
outbuf = ""
for i,line in enumerate(lines):
    outbuf += line + "\n"

for topic in mappings:
    fname = mappings[topic]
    if isinstance(fname, list):
        for fn in fname:
            ext = fn.split(".")[-1]
            assert ext == "pdf"
        outbuf += f'- {topic} <span class="small-mono">[slides: '
        s = list()
        for i,fn in enumerate(fname):
            s.append(f"[{i+1}](../resources/cfd/{fn})")
            source_fn = f"./material/cfd/{fn}"
            target_fn = f"./docs/resources/cfd/{fn}"
            if not os.path.exists(os.path.dirname(target_fn)):
                os.makedirs(os.path.dirname(target_fn))
            shutil.copy(f"{source_fn}", f"{target_fn}")
        outbuf += f'{", ".join(s)}]</span>\n'
    else:
        ext = fname.split(".")[-1]
        assert ext in ["zip", "pdf"]
        s = {"zip": "archive", "pdf": "slides"}[ext]
        outbuf += f'- {topic} <span class="small-mono">[[{s}](../resources/cfd/{mappings[topic]})]</span>\n'
        source_fn = f"./material/cfd/{mappings[topic]}"
        target_fn = f"./docs/resources/cfd/{mappings[topic]}"
        if not os.path.exists(os.path.dirname(target_fn)):
            os.makedirs(os.path.dirname(target_fn))
        shutil.copy(f"{source_fn}", f"{target_fn}")
print(outbuf)


