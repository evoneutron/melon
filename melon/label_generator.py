import os
from pathlib import Path


class LabelGenerator:
    __default_labels_file_name = "labels.txt"

    @staticmethod
    def generate_labels(source_dir):
        labels_file = Path(source_dir) / LabelGenerator.__default_labels_file_name
        if labels_file.exists():
            raise ValueError("Labels file already exists.")
        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

        with open(labels_file, "w") as infile:
            infile.write("---\n")
            infile.write("#map\n")
            for f in files:
                file = Path(f)
                infile.write(file.name + ":\n")
        print("Generated labels file {} in '{}'".format(LabelGenerator.__default_labels_file_name, source_dir))
