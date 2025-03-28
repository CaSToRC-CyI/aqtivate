import re, os, shutil
from collections import OrderedDict

with open('./lqcd.md', 'r') as fp:
    lines = [line.rstrip('\n') for line in fp]

mappings = OrderedDict({
    "Data analysis": "Data Analysis",
    "Hadron structure": "Hadron Structure/LAP-Hadron structure.pdf",
    "GPU programming for lattice QCD": "GPUs",
    "Quantum computing and tensor networks": "Quantum Computing/QC_Intro_Lattice_Practices_CyI_2024.pdf",
    "Simulation algorithms": "Simulation Algorithms",
    "Solver algorithms": "Solvers",
    "Spectrum and resonances in lattice QCD": "Scattering And Resonanses/spectro.pdf",
})
    
outbuf = ""
for i,line in enumerate(lines):
    outbuf += line + "\n"

for topic in mappings:
    fn = os.path.basename(mappings[topic])
    if fn[-3:] == "pdf":
        outbuf += f'- {topic} <span class="small-mono">[[slides](../resources/lqcd/{fn})]</span>\n'
        source_fn = f"./material/lqcd/{mappings[topic]}"
        target_fn = f"./docs/resources/lqcd/{fn}"
        if not os.path.exists(os.path.dirname(target_fn)):
            os.makedirs(os.path.dirname(target_fn))
        shutil.copy(f"{source_fn}", f"{target_fn}")
    else:
        outbuf += f'- {topic} <span class="small-mono">[[file listing](../resources/lqcd/{mappings[topic]}.md)]</span>\n'
        source_dir = f"./material/lqcd/{mappings[topic]}/"
        target_dir = f"./docs/resources/lqcd/{mappings[topic]}/"
        if not os.path.exists(os.path.dirname(target_dir)):
            os.makedirs(os.path.dirname(target_dir))
        file_list = os.listdir(source_dir)
        with open(f"./docs/resources/lqcd/{mappings[topic]}.md", "w") as fp:
            fp.write(f"# {topic}\n")
            for fname in sorted(file_list):
                shutil.copy(f"{source_dir}/{fname}", f"{target_dir}/{fname}")
                listing_line = f'- <span class="mono">[{fname}](../../resources/lqcd/{mappings[topic]}/{fname})</span>\n'
                fp.write(listing_line)
print(outbuf)


