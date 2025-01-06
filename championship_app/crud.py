from operator import itemgetter


# SIMPLE CRUD IMPLEMENTATION
# we can extend the CRUD function if ever needed

# creates a table
# pass a schema as dictionaty of 4 keys:
# * table (string) table name
# * field (array of tuples) of the following format: ( field_name, field_type, is_NOT_NULL, default_value, check )
# * primary (array) of primary key field names
# * constraint (array) of contraint declarations

def create( schema ):
    table, field, primary, constraint = itemgetter('table', 'field', 'primary', 'constraint')(schema)

    sql = f"CREATE TABLE \"{table}\"(\n"
    for (fname, ftype, isNotNull, defVal, check) in field:
        nullStatement = ""
        if isNotNull:
            nullStatement = "NOT NULL"
        chkStatement = ""
        if check != None:
            chkStatement = f" {check}"
        sql += f"\"{fname}\" {ftype} {nullStatement} DEFAULT {defVal}{chkStatement},\n"

    if constraint != None:
        for cnstr in constraint:
            sql += f"{cnstr},\n"

    pkWithQuotes = []
    for pki in primary:
        pkWithQuotes.append(f"\"{pki}\"")
    pk = ','.join(pkWithQuotes)
    sql += f"PRIMARY KEY({pk})\n)"

    return sql

## examples for application tables
## {
##     "table": 'TEAM_PLAYER',
##     "field": [
##         ("id_team_per_season", "INTEGER", True, "'0'", None),
##         ("id_player", "INTEGER", True, "'0'", None),
## 	    ("start_date", "date", False, "NULL", None)
##         ...
##     ],
##     "primary": ["id_team_per_season", "id_player"],
##     "constraint": [
##         "\"ανήκει_σε_id_ομ\" FOREIGN KEY(\"id_team_per_season\") REFERENCES \"TEAM_PER_SEASON\"(\"id_team_per_season\") ON DELETE SET DEFAULT ON UPDATE CASCADE",
##         "\"ανήκει_σε_id_ποδοσφ\" FOREIGN KEY(\"id_player\") REFERENCES \"PLAYER\"(\"id_player\") ON UPDATE CASCADE"
##     ]
## }
## 
## {
##      "table": 'ARENA',
##     "field": [
##         ...
## 	    ("type", "varchar(30)", True, "''", "CHECK(\"type\" in (\"Συνθετικός χλοοτάπητας\",\"Φυσικός χλοοτάπητας\",\"Ξερό\")")
##     ],
##     "primary": ["id_arena"],
##     "constraint": None
## }


# implements a SELECT sql statement
# query dictionary consists of the following keys
# * table (string) table name
# * field (array) field names ; if None then all fields are selected ("*")
# * where (array) of tuples ( field_name, comparison_operator, comparison_value ) applied with "AND"
# * order (array) of tuples ( field_name, order_type )
# NOTE: an easy way to extend the function is to add some extra keys to the query dictionary 
# like joins, whereOr, whereRaw, etc
def read(query):
    table, field, where, order = itemgetter('table', 'field', 'where', 'order')(query)
    fList = "*"
    if field != None:
        fList = ', '.join(field)
    sql = f"SELECT {fList}\n"
    sql += f"FROM {table}\n"
    whereStatment = ""
    if where != None:
        whereItems = []
        for (fname, operator, val) in where:
            whereItems.append(f"{fname} {operator} {val}")
        whereStatment = f"WHERE {' AND '.join(whereItems)}"
    
    # order-by is not implemented

    sql += whereStatment
    return sql


def insert(query):
    table, field, value = itemgetter('table', 'field', 'value')(query)

    sql = f"INSERT INTO \"{table}\" "

    fList = ', '.join(field)
    sql += f"({fList})"

    valList = ', '.join(value)
    sql += f"\nVALUES ({valList})"
    return sql


# in update query is a dictionaty with the following keys
# table (string)
# sets (array) of tuples (field_name, new_value)
# where (array) same as "where" key in read() query
def update( query ):
    table, sets, where = itemgetter('table', 'set', 'where')(query)

    sql = f"UPDATE \"{table}\"\nSET "

    setStatements = []
    for (f, v) in sets:
        setStatements.append(f"{f} = {v}")
    sql += ', '.join(setStatements)

    whereStatment = ""
    if where != None:
        whereItems = []
        for (fname, operator, val) in where:
            whereItems.append(f"{fname} {operator} {val}")
        whereStatment = f"\nWHERE {' AND '.join(whereItems)}"
    
    sql += whereStatment
    return sql



def delete(query):
    table, where = itemgetter('table', 'where')(query)

    sql = f"DELETE FROM \"{table}\""

    whereStatment = ""
    if where != None:
        whereItems = []
        for (fname, operator, val) in where:
            whereItems.append(f"{fname} {operator} {val}")
        whereStatment = f"\nWHERE {' AND '.join(whereItems)}"
    
    sql += whereStatment
    return sql



# demos
# ---
# sch = {
#     "table": 'TEAM_PLAYER',
#     "field": [
#         ("id_team_per_season", "INTEGER", True, "'0'", None),
#         ("id_player", "INTEGER", True, "'0'", None),
# 	    ("start_date", "date", False, "NULL", None),
#         ("type", "varchar(30)", True, "''", "CHECK(\"type\" in (\"Συνθετικός χλοοτάπητας\",\"Φυσικός χλοοτάπητας\",\"Ξερό\")")
#     ],
#     "primary": ["id_team_per_season", "id_player"],
#     "constraint": [
#         "\"ανήκει_σε_id_ομ\" FOREIGN KEY(\"id_team_per_season\") REFERENCES \"TEAM_PER_SEASON\"(\"id_team_per_season\") ON DELETE SET DEFAULT ON UPDATE CASCADE",
#         "\"ανήκει_σε_id_ποδοσφ\" FOREIGN KEY(\"id_player\") REFERENCES \"PLAYER\"(\"id_player\") ON UPDATE CASCADE"
#     ]
# }
# print(create(sch))
# ---
# q = {
#     "table": 'alfa',
#     "field": [
#         "name", "birth_year", "status"
#     ],
#     "where": [
#         ("name", "LIKE", "\"Anna%\""),
#         ("birth_year", "<", "2010")
#     ],
#     "order": None
# }
# print(read(q))
# ---
# q = {
#     "table": 'USER',
#     "set": [
#         ('"password"', '1234')
#     ],
#     "where": [
#         ('username', '=', '"spasiklaki"')
#     ]
# 
# }
# print(update(q))
# ---
# q = {
#     "table": 'USER',
#     "field": [
#         'username', 'password'
#     ],
#     "value": [
#         '"Andreas"', '"0000-1-2-3-4"'
#     ]
# 
# }
# print(insert(q))
# ---
# q = {
#     "table": 'USER',
#     "where": [
#         ('username', '=', '"spasiklaki"')
#     ]
# 
# }
# print(delete(q))
