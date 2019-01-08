import os
from pathlib import Path


class LabelGenerator:

    @staticmethod
    def generate_labels(dir):
        labels_file = Path(dir) / "labels.txt"
        if labels_file.exists():
            return ValueError("Labels file already exists.")
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

        with open(labels_file, "w") as infile:
            infile.write("---\n")
            infile.write("#map\n")
            for f in files:
                file = Path(f)
                infile.write(file.name + ":\n")
