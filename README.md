# NARA Catalog Parser

The national archives catalog is a free dataset on Amazon S3:
* https://www.archives.gov/developer/national-archives-catalog-dataset
* https://registry.opendata.aws/nara-national-archives-catalog/

Presumably this is the data which powers https://catalog.archives.gov/, the archives' searchable web interface.  The advantage of keeping and searching the dataset locally is to search freely without requiring the archives' API (https://github.com/usnationalarchives/Catalog-API), which is rate-limited.  The descriptions and URLs can all be parsed and searched on a minute or two on a reasonably fast desktop computer (it's only that slow because these scripts take the completely naive approach -- populating a database would be thousands of times more efficient).

Happy grepping!
