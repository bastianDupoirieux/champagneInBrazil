--Create a table containing the relevant information for wines.
--Data should be added to it via an input form.
--SQLITE syntax

CREATE TABLE USER_WINE
(id integer primary key autoincrement,
name text not null, --Name of the wine, cuvee etc
producer text not null, --Producer
region text, --Region the wine is from
appellation text, --appellation if applicable (especially for old world wines)
vintage integer, --vintage, must be nullable for cases like Champagne
date_bought text, --Date the wine was bought on
buying_price real, --Price the wine was bought at
expired int, --Bool value if the entry is expired (wine has been drank) or not
notes text --optional field for notes
)
;
