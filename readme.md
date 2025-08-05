# dumper

**Dumper program on WXWidgets for creating and editing databases**

This program allows you to create a SQLite database, dump it into a SQL file, and also make adjustments to this dump for import into a MySQL database.

The module provides the following API features:

- Creating a new SQLite database, or connecting to an existing one  
- Table creation  
- Adding a new record to the table  
- Changing an existing record in a table  
- Deleting a record in a table  
- Getting a list of names of all tables in the database  
- Getting table parameters  
- Getting ID of the last table entry  
- Getting the value of a table record cell  
- Getting all table entries  
- Creating a database dump in SQL file  
- Adjustment of the dump file for import into the MySQL database  
- Adding a table delete request to the dump file if one exists  
- Removing quotes around the table name in the dump file  
- Adding to the dump file using the database name or to the table names the database name  
- Escaping quotes in the text, for correct addition to the database  
- Replacing the `&` character with a sequence  
- Replacement of characters (`&`, `<`, `>`, `"`) for display in HTML  
