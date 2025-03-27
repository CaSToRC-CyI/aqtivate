import re, os, shutil
import zipfile

def zipdir(directory, zipfname):
    # Create a ZipFile object
    with zipfile.ZipFile(zipfname, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Create the full file path
                file_path = os.path.join(root, file)
                # Calculate path inside the zip
                arcname = os.path.relpath(file_path, os.path.dirname(directory))
                # Add file to zip
                zipf.write(file_path, arcname)

with open('./school_2.md', 'r') as fp:
    lines = [line.rstrip('\n') for line in fp]

mappings = {
    "1_introduction_ml": {
        "title": "Introduction to ML", "slides": "Slides_aqtivate_workshop.pdf", "exercise": "Code/",
    },
    "2_python_introduction": {
        "title": "Python introduction", "slides": "lecture/aqtivate-lecture.pdf", "exercise": "/",
    },
    "3_classical_methods": {
        "title": "Classical methods", "slides": "Slides__Classical_Methods.pdf", "exercise": "exercise/",
    },
    "4_unsupervised_learning": {
        "title": "Unsupervised Learning", "slides": "lecture/tex/clustering.pdf", "exercise": "exercise/",
    },
    "5_bayesian_methods": {
        "title": "Bayesian methods", "slides": "lecture/BM.pdf", "exercise": "/",
    },
    "6_kernel_methods": {
        "title": "Kernel methods", "slides": "kernels.pdf", "exercise": "/",
    },
    "7_neural_networks_basics": {
        "title": "Neural networks introduction", "slides": "NeuralNetworkBasicsLecture.pdf", "exercise": "neural_networks_exercise.ipynb",
    },
    "8_neural_network_tricks": {
        "title": "Neural networks tricks", "slides": "Deep_Learning_in_Practice.pdf", "exercise": "sheet_neural_network_tricks.zip",
    },
    "9_convolution_nn": {
        "title": "Convolutional neural networks", "slides": "Conv-Aqtivate-2024.pdf", "exercise": "exercises/",
    },
    "10_recurrent_neural_networks": {
        "title": "Recurrent neural networks", "slides": "recurrent_neural_networks.pdf", "exercise": "rnn_exercises.zip",
    },
    "12_generative_models": {
        "title": "Generative models", "slides": "Generative_models_new_2024.pdf"
    },
}

    
outbuf = ""
research_talks = 0
for i,line in enumerate(lines):
    for topic in mappings:
        if mappings[topic]["title"] in line:
            slides = mappings[topic]["slides"]
            slides_basename = os.path.basename(slides)
            slides_source_path = f"./material/school_2/{topic}/{slides}"
            slides_target_path = f"./docs/resources/school_2/{topic}/{slides_basename}"
            slides_href_path = f"../resources/school_2/{topic}/{slides_basename}"
            if not os.path.exists(os.path.dirname(slides_target_path)):
                os.makedirs(os.path.dirname(slides_target_path))
            shutil.copy(slides_source_path, slides_target_path)
            if "exercise" in mappings[topic]:
                exe = mappings[topic]["exercise"]
                exe_source_path = f"./material/school_2/{topic}/{exe}"
                if exe.split(".")[-1][-1] == "/":
                    exe_target_path = f"./docs/resources/school_2/{topic}/exercises.zip"
                    zipdir(exe_source_path, exe_target_path)
                    exe_href_path = f"../resources/school_2/{topic}/exercises.zip"
                else:
                    exe_target_path = f"./docs/resources/school_2/{topic}/{exe}"
                    exe_href_path = f"../resources/school_2/{topic}/{exe}"
                    shutil.copy(exe_source_path, exe_target_path)
                line = f'{line} <span class="small-mono">[[slides]({slides_href_path})|[exercise]({exe_href_path})]</span>'
            else:
                line = f'{line} <span class="small-mono">[[slides]({slides_href_path})]</span>'
                
    if '- _"' in line:
        speaker = lines[i+1].split(",")[0].strip()
        fname = "{}_{}.pdf".format(research_talks+1, speaker.split()[-1])
        pdf_href_path = f"../resources/school_2/research_talks/{fname}"
        pdf_target_path = f"./docs/resources/school_2/research_talks/{fname}"
        pdf_source_path = f"./material/school_2/research_talks/{fname}"
        if os.path.exists(pdf_source_path):
            if not os.path.exists(os.path.dirname(pdf_target_path)):
                os.makedirs(os.path.dirname(pdf_target_path))
            shutil.copy(pdf_source_path, pdf_target_path)
            title = re.match('- _"(.*)"_',line).groups()[0]
            line = f'- _"[{title}]({pdf_href_path})"_  '
        research_talks += 1
    outbuf += line + "\n"

print(outbuf)
