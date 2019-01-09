import click

from melon import LabelGenerator


@click.group()
def cli():
    pass


@cli.command()
@click.option("--source_dir", prompt=True, required=True,
              help="Source directory of the images. Labels file will be generated in that directory")
def generate(source_dir):
    generator = LabelGenerator()
    try:
        generator.generate_labels(source_dir)
    except Exception as e:
        print("Failed to generate labels file. {}".format(str(e)))


if __name__ == "__main__":
    cli()
