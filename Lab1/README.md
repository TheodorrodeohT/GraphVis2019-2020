# Сбор и визуализация данных [imdb.com](http://imdb.com "imdb.com")

Основным источником данных является онлайн база данных фильмов [imdb.com](http://imdb.com "imdb.com").

## Состав команды
Павлов Федор, Цхай Борис, Якушкин Николай.

## Этапы работы

Лабораторная работа поделена на три основных этапа: вначале производится демонстрация сбора данных с помощью инструментов web-crawling, затем формируется основной датасет для работы и в конце данные заносятся в СУБД.

### Сбор данных с помощью библиотеки scrapy

Для начала с сайта была собрана информация, полученная с помощью инструментов библиотеки [scrapy](https://scrapy.org/ "scrapy"). Принцип работы и составления программы (ознакомиться с кодом можно в папке [/imdb_crawler](https://github.com/TheodorrodeohT/GraphVis2019-2020/tree/master/Lab1/imdb_crawler/imdb_crawler "/imdb_crawler")) следующий:

1. В файл [movies.txt](https://github.com/TheodorrodeohT/GraphVis2019-2020/tree/master/Lab1/imdb_crawler/imdb_crawler/spiders/movies.txt "movies.txt") прописываем те фильмы, информацию о которых хотим собрать. В данном случае выбрано 23 фильма нескольких режиссеров.
2. В файл [settings.py](https://github.com/TheodorrodeohT/GraphVis2019-2020/tree/master/Lab1/imdb_crawler/imdb_crawler/settings.py "settings.py") выставляем задержку между запросами.
3. В файл [items.py](https://github.com/TheodorrodeohT/GraphVis2019-2020/tree/master/Lab1/imdb_crawler/imdb_crawler/items.py "items.py") прописываем класс `Movie`, в котором указываем поля для чтения. Также прописываем функции обработки входящих строк.
4. Сам паук прописан в файле [spider.py](https://github.com/TheodorrodeohT/GraphVis2019-2020/tree/master/Lab1/imdb_crawler/imdb_crawler/spiders/spider.py "spider.py"). Сначала считывается список фильмов для поиска. Затем для каждого фильма собирается название и дата выпуска в прокат, формируется ссылка на страницу с фильмом. В конце собираются все интересующие нас поля класса `Movie`.
5. Запустить процесс сбора информации и записать результат в файл можно из корневой папки программы с помощью команды `scrapy crawl spider -o results.csv -t csv`.

**Пример собранных данных**

|budget|cast_top3|director|genres|imdb_rating|language|release_date|runtime|title|
|-------|-------|-------|-------|-------|-------|-------|-------|-------|
|$95,875,|Joseph Cross,Timothy Reifsnyder,Dana Delany|M. Night Shyamalan|Comedy, Drama, Family|5.9| |1998|1h 28min|Wide Awake|
|$10,000,000 |Freddie Prinze Jr.,Rachael Leigh Cook,Matthew Lillard|Robert Iscove|Comedy, Romance|5.9|English|1999|1h 35min|She's All That|
|$26,681,262,|Bruce Willis,Haley Joel Osment,Toni Collette|M. Night Shyamalan|Drama, Mystery, Thriller|8.1||1999|1h 47min|The Sixth Sense|
|$133,000,000 |Michael J. Fox,Geena Davis,Hugh Laurie|Rob Minkoff|Adventure, Comedy, Family, Fantasy|5.9|English|1999|1h 24min|Stuart Little|
|$60,117,080,|Mel Gibson,Joaquin Phoenix,Rory Culkin|M. Night Shyamalan|Drama, Mystery, Sci-Fi, Thriller|6.7||2002|1h 46min|Signs|


### Формирование датасета

В качестве основного датасета, на котором будут производиться все вычисления и анализ, был выбран официальный набор данных [imdb.com/interfaces](http://imdb.com/interfaces "imdb.com/interfaces"), обновляемый ежедневно. Для составления базы данных были использованы следующие архивы: `name.basics.tsv`, `title.akas.tsv`, `title.basics.tsv`, `title.crew.tsv`, `title.ratings.tsv`. Процесс сбора и организации данных можно увидеть в jupyter-ноутбуке [GraphVisLab1.ipynb](https://github.com/TheodorrodeohT/GraphVis2019-2020/tree/master/Lab1/GraphVisLab1.ipynb "GraphVisLab1.ipynb").

В результате исполнения кода генерируются два набора данных  -- таблица `imdb_dataset_filtered.csv`, содержащая 16887 строк и таблица `imdb_dataset_visualise.csv`, содержащая 81 строку -- в следующем формате:

|titleId|title|directorId|director|year|titleType|isAdult|runtimeMins|genres|avgRating|numVotes|region|language|types|isOriginalTitle|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|tt0038813|La Otra|nm0310449|Roberto Gavaldon|1946|movie|0|98|\N|7.3|numVotes|NO|\N|imdbDisplay|0|

Датасет `imdb_dataset_filtered.csv`  является основным, т.к. содержит основной набор фильмов, удовлетворяющих следующим критериям: `avgRating` > 7.0, `numVotes` > 100, `runtimeMins` > 60.

Датасет `imdb_dataset_visualise.csv` содержит 20 режиссеров с количеством фильмов от 3 до 6 и используется для тестовой визуализации.


### Работа с СУБД

В качестве СУБД мы выбрали **Neo4j**. Загрузка датасета происходила с помощью **Cypher** запросов через **Neo4j Browser**. Был также испробован вариант использования библиотеки **py2neo**, однако из-за неудобства его использования было принято решение заносить данные напрямую через **Cypher**. Каждая вершина представлена фильмом с сопутствующей ему информацией. Связями выступают режиссеры, снявшие картины.

#### Внесение данных

Для внесения данных из готового набора формата `.csv` использовался следующий скрипт на **Cypher**:
```
LOAD CSV WITH HEADERS FROM 'file:///imdb_dataset_filtered.csv' AS line
MERGE (m:Movie {
  titleId: line.titleId, 
  title: line.title,
  year: line.year,
  titleType: line.titleType,
  isAdult: line.isAdult,
  runtime: line.runtimeMins,
  genre: line.genres,
  avgRating: line.avgRating,
  numVotes: line.numVotes,
  region: line.region,
  language: line.language,
  types: line.types,
  isOriginalTitle: line.isOriginalTitle})
```

#### Визуализация графа

Продемонстрируем несколько способов визуализировать датасет в виде графа средствами **neo4j**.

**Граф 1**

>Общая информация

|Число вершин|Общее число отношений|Отношений SameDirector (зеленые)|Отношений SameYear(фиолетовые)
|------------|-----------|------------|-----------|
|100|758|590|168|

>Код для выгрузки в neo4j

Датасет

```
LOAD CSV WITH HEADERS FROM 'file:///imdb_dataset_filtered.csv' AS line
WITH line LIMIT 5000
MERGE (m:Movie {
  titleId: line.titleId, 
  title: line.title,
  year: line.year,
  titleType: line.titleType,
  directorId: line.directorId,
  director: line.director,
  isAdult: line.isAdult,
  runtime: line.runtimeMins,
  genre: line.genres,
  avgRating: line.avgRating,
  numVotes: line.numVotes,
  region: line.region,
  language: line.language,
  types: line.types,
  isOriginalTitle: line.isOriginalTitle})
```

Связи

```
MATCH (m1:Movie)
MATCH (m2:Movie)
WHERE m1.year = m2.year AND m1.title <> m2.title
CREATE (m1)-[rel:SameYear]->(m2)
```

```
MATCH (m1:Movie)
MATCH (m2:Movie)
WHERE m1.directorId = m2.directorId AND m1.title <> m2.title
CREATE (m1)-[rel:SameDirector]->(m2)
```

Запрос

```
MATCH (m:Movie)
RETURN m
LIMIT 100
```


>Визуализация

![vis1](https://github.com/TheodorrodeohT/GraphVis2019-2020/blob/master/Lab1/img/vis1.png)

---

**Граф 2**

>Общая информация

|Число вершин|Число вершин (режиссёр)|Отношений Directed|
|------------|-----------|-----------|
|300|53|247|

>Код для выгрузки в neo4j

Датасет и связи

```
LOAD CSV WITH HEADERS FROM 'file:///imdb_dataset_filtered.csv' AS line
WITH line LIMIT 5000
MERGE (m:Movie {
  titleId: line.titleId, 
  title: line.title,
  year: line.year,
  titleType: line.titleType,
  isAdult: line.isAdult,
  runtime: line.runtimeMins,
  genre: line.genres,
  avgRating: line.avgRating,
  numVotes: line.numVotes,
  region: line.region,
  language: line.language,
  types: line.types,
  isOriginalTitle: line.isOriginalTitle})
MERGE (d:Director {
  directorId: line.directorId,
  director: line.director})
MERGE (d) -[:Directed {year: line.year}]-> (m)
```

Запрос

```
MATCH (n)
RETURN n
LIMIT 300
```

>Визуализация

![vis2](https://github.com/TheodorrodeohT/GraphVis2019-2020/blob/master/Lab1/img/vis2.png)
