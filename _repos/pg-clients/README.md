# PostgreSQL-Clients :elephant:
Overview of web-based, dockerized PostgreSQL clients

## Usage
Simply run `docker-compose up -d web`, and go to http://localhost. :whale:

To stop, run `docker-compose down`.
## Tutorial

```
CREATE TABLE cards (
  id integer NOT NULL,
  board_id integer NOT NULL,
  data jsonb
);
INSERT INTO cards VALUES (1, 1, '{"name": "Paint house", "tags": ["Improvements", "Office"], "finished": true}');
INSERT INTO cards VALUES (2, 1, '{"name": "Wash dishes", "tags": ["Clean", "Kitchen"], "finished": false}');
INSERT INTO cards VALUES (3, 1, '{"name": "Cook lunch", "tags": ["Cook", "Kitchen", "Tacos"], "ingredients": ["Tortillas", "Guacamole"], "finished": false}');
INSERT INTO cards VALUES (4, 1, '{"name": "Vacuum", "tags": ["Clean", "Bedroom", "Office"], "finished": false}');
INSERT INTO cards VALUES (5, 1, '{"name": "Hang paintings", "tags": ["Improvements", "Office"], "finished": false}');


```
## Overview

- https://github.com/scylladb/scylla-code-samples/blob/master/elasticsearch-scylla/docker-compose.yml
- https://medium.com/scalableminds/choosing-a-postgresql-client-178f0e7bbae6
- https://www.postgresqltutorial.com/postgresql-json/

### Table
<table>
    <tr>
      <th colspan="2"></th>
      <th colspan="5">✨ Features</th>
      <th colspan="3">🛢 Supported Data Types</th>
    </tr>
    <tr>
      <th style="vertical-align: bottom;">Client</th>
      <th style="vertical-align: bottom;">UI</th>
      <th style="vertical-align: bottom;">Queries</th>
      <th style="vertical-align: bottom;">Visualize</th>
      <th style="vertical-align: bottom;">Analytics</th>
      <th style="vertical-align: bottom;">Navigate</th>
      <th style="vertical-align: bottom;">Multi-DB</th>
      <th style="vertical-align: bottom;">Tables,<br>Views,<br>Schemas,<br>Indices</th>
      <th style="vertical-align: bottom;">Constraints</th>
      <th style="vertical-align: bottom;">Functions</th>
    </tr>
    <tr>
      <td><a href="https://www.adminer.org" target="_blank">Adminer</a></td>
      <td>★★</td>
      <td>✔</td><td> </td><td>(✔)</td><td>✔</td><td>✔</td>
      <td>✔</td><td>(✔)</td><td>✔</td>
    </tr>
    <tr>
      <td><a href="https://www.omnidb.org" target="_blank">OmniDB</a></td>
      <td>★★</td>
      <td>✔</td><td>✔</td><td>✔</td><td> </td><td>✔</td>
      <td>✔</td><td>✔</td><td>✔</td>
    </tr>
    <tr>
      <td><a href="https://www.pgadmin.org" target="_blank">pgAdmin 4</a></td>
      <td>★★</td>
      <td>✔</td><td> </td><td>✔</td><td> </td><td> </td>
      <td>✔</td><td>✔</td><td>✔</td>
    </tr>
    <tr>
      <td><a href="http://sosedoff.github.io/pgweb" target="_blank">pgweb</a></td>
      <td>★★★</td>
      <td>✔</td><td> </td><td> </td><td> </td><td> </td>
      <td>✔</td><td>✔</td><td> </td>
    </tr>
    <tr>
      <td><a href="http://www.teampostgresql.com" target="_blank">TeamPostgreSQL</a></td>
      <td>★</td>
      <td>✔</td><td> </td><td> </td><td>✔</td><td> </td>
      <td>✔</td><td> </td><td>✔</td>
    </tr>
</table>
