import os
import audible
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
COUNTRY_CODE = os.getenv("COUNTRY_CODE")

auth = audible.Authenticator.from_login(
    USERNAME, PASSWORD, locale=COUNTRY_CODE, with_username=False
)

# auth = audible.Authenticator.from_login_external(locale=COUNTRY_CODE)

auth.to_file("./credentials.txt")

with audible.Client(auth=auth) as client:
    library = client.get(
        "1.0/library",
        num_results=1000,
        response_groups="product_desc, product_attrs",
        sort_by="-PurchaseDate",
    )
    for book in library["items"]:
        print(book["title"])
