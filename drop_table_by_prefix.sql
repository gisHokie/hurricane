
-- DROP ALL TABLES whose name has a prefix defined in the WHERE

DO
$do$
DECLARE
   _tbl text;
BEGIN
FOR _tbl  IN
    SELECT quote_ident(table_schema) || '.'
        || quote_ident(table_name)      -- escape identifier and schema-qualify!
    FROM   information_schema.tables
    WHERE  table_name LIKE 'al01' || '%'  -- your table name prefix
    AND    table_schema NOT LIKE 'pg_%'     -- exclude system schemas
LOOP
   RAISE NOTICE '%',
-- EXECUTE
  'DROP TABLE ' || _tbl;
END LOOP;
END
$do$;