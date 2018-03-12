# pastebin-scrapper

--------------------------------------------------------------------------------

> Scrape recent pastes of pastebin

## Data

In order to save date, hash and title we need a character to split the filename, we will use an underscore `_`.

- Filename format:

  - `date_time_hash_title`

- Filename example:

  - `2018-03-12_20:15:30_7513213165423213756_Untitled`

- which as a list look like:

  - `['2018-03-12', '20:15:30', '7513213165423213756', Untitled]`

## Requirements

- BeautifulSoup

  - `$ apt-get install python-bs4`
