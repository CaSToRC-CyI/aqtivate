import re, os, shutil
from collections import OrderedDict

with open('./school_1.md', 'r') as fp:
    lines = [line.rstrip('\n') for line in fp]

mappings = OrderedDict({
    "Computer architectures": "computer_architectures",
    "Parallel algorithms": "parallel_algorithms",
    "Performance modelling and performance engineering": "performance",
    "GPU Programming": "gpu",
    "Parallel programming using MPI": "mpi",
    "Data management": "data_management",
})
    
outbuf = ""
for i,line in enumerate(lines):
    outbuf += line + "\n"

for topic in mappings:
    outbuf += f'- {topic} <span class="small-mono">[[file listing](../resources/school_1/{mappings[topic]}.md)]</span>\n'
    source_dir = f"./material/school_1/{mappings[topic]}/"
    target_dir = f"./docs/resources/school_1/{mappings[topic]}/"
    if not os.path.exists(os.path.dirname(target_dir)):
        os.makedirs(os.path.dirname(target_dir))
    file_list = os.listdir(source_dir)
    with open(f"./docs/resources/school_1/{mappings[topic]}.md", "w") as fp:
        fp.write(f"# {topic}\n")
        for fname in sorted(file_list):
            shutil.copy(f"{source_dir}/{fname}", f"{target_dir}/{fname}")
            listing_line = f'- <span class="mono">[{fname}](../../resources/school_1/{mappings[topic]}/{fname})</span>\n'
            fp.write(listing_line)
print(outbuf)


