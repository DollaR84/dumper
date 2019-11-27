# dumper
Dumper program on WXWidgets for creating and edting databases

This program allows you to create a sqlite database, dump it into a sql file, and also make adjustments to this dump for import into a MYSQL database.
The module provides the following API features:
• creating a new sqlite database, or connecting to an existing one
• table creation
• adding a new record to the table
• change an existing record in a table
• deleting a record in a table
• getting a list of names of all tables in the database
• getting table parameters
• getting id of the last table entry
• getting the value of a table record cell
• getting all table entries
• creating a database dump in sql file
• adjustment of the dump file for import into the MYSQL database
• adding a table delete request to the dump file if one exists
• removing quotes around the table name in the dump file
• adding to the dump file using the database name or to the table names the database name
• escaping quotes in the text, for correct addition to the database
• Replacing the & character with a sequence
• replacement of characters (&, <,>, ") for display in html
