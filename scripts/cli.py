import click

from melon import LabelGenerator

from pathlib import Path


@click.group()
def cli():
    pass


# @click.command()
# @click.option("--source_dir", help="Source directory of the files to use for generating labels file")
def generate(source_dir):
    gen = LabelGenerator()
    gen.generate_labels(source_dir)


if __name__ == "__main__":
    # cli()

    generate("/Users/rjuga255/PycharmProjects/melon/tests/resources/online_album_cut")