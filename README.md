# Osvaldo Cobacho Aguilera

## Clase 2

Exercise 1

Add basic fields to the Real Estate Property table.

Add the following basic fields to the table:


| Field  | Type |
| ------------- | ------------- |
| name  | Char  |
| description  | Text  |
| postcode  | Char  |
| date_availability  | Date  |
| expected_price  | Float  |
| selling_price  | Float  |
| bedrooms  | Integer  |
| living_area  | Integer  |
| facades  | Integer  |
| garage  | Boolean  |
| garden  | Boolean  |
| garden_area  | Integer  |
| garden_orientation  | Selection  |

The garden_orientation field must have 4 possible values: ‘North’, ‘South’, ‘East’ and ‘West’. The selection list is defined as a list of tuples

### Test Clase 2 exercise 1

Connect to database 
```shell script
$ psql -d databasename

```

Shows all the fields created for the estate_property table
```shell script
$ databasename=# \d estate_property;

```
