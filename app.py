import os
import re
import audible
import click
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
COUNTRY_CODE = os.getenv("COUNTRY_CODE")

auth = audible.Authenticator.from_login(
    USERNAME, PASSWORD, locale=COUNTRY_CODE, with_username=False
)

auth.to_file("./credentials.txt")


def get_library():
    with audible.Client(auth=auth) as client:
        return client.get(
            "1.0/library",
            num_results=1000,
            response_groups="product_desc, product_attrs",
            sort_by="-PurchaseDate",
        )


@click.group()
def cli():
    pass


@cli.command()
def library_keys():
    library = get_library()

    if library:
        click.echo(library["items"])
        click.echo(library["response_groups"])


@cli.command()
def list_all_titles():
    library = get_library()
    for book in library["items"]:
        click.echo(book["title"])
    click.echo(f"Total number of books in your library: {
               len(library['items'])}")


@cli.command()
@click.argument('search_term')
def grab_title(search_term):
    library = get_library()
    for book in library["items"]:
        if re.search(search_term, book["title"], re.IGNORECASE):
            click.echo(f"Title found: {book['title']}")
            return
    click.echo("Title not found in your library")


if __name__ == "__main__":
    cli()
