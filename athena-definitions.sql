CREATE EXTERNAL TABLE `car`(
  `owner` string COMMENT 'from deserializer',
  `seats` string COMMENT 'from deserializer',
  `model` string COMMENT 'from deserializer',
  `parking_spot` string COMMENT 'from deserializer')
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/Car'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'transient_lastDdlTime'='1644377280')

CREATE EXTERNAL TABLE `event`(
  `event_date` string COMMENT 'from deserializer',
  `name` string COMMENT 'from deserializer',
  `pickup_time` string COMMENT 'from deserializer',
  `pickup_interval` string COMMENT 'from deserializer',
  `guest_pickup_time` string COMMENT 'from deserializer',
  `guest_pickup_interval` string COMMENT 'from deserializer',
  `guest_rides` string COMMENT 'from deserializer')
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/Event'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'transient_lastDdlTime'='1644693142')

CREATE EXTERNAL TABLE `event_driver`(
  `event_date` string COMMENT 'from deserializer',
  `user_id` string COMMENT 'from deserializer')
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/EventDriver'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'transient_lastDdlTime'='1646102589')

CREATE EXTERNAL TABLE `event_driver_inj`(
  `user_id` string COMMENT 'from deserializer')
PARTITIONED BY (
  `event_date` string)
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/EventDriver'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'projection.enabled'='true',
  'projection.event_date.type'='injected',
  'storage.location.template'='s3://battery-staple-v1/EventDriver/${event_date}',
  'transient_lastDdlTime'='1646161237')

CREATE EXTERNAL TABLE `event_car`(
  `event_date` string COMMENT 'from deserializer',
  `owner` string COMMENT 'from deserializer')
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/EventCar'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'transient_lastDdlTime'='1646102589')

CREATE EXTERNAL TABLE `event_car_inj`(
  `owner` string COMMENT 'from deserializer')
PARTITIONED BY (
  `event_date` string)
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/EventCar'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'projection.enabled'='true',
  'projection.event_date.type'='injected',
  'storage.location.template'='s3://battery-staple-v1/EventCar/${event_date}',
  'transient_lastDdlTime'='1646161237')


CREATE EXTERNAL TABLE `event_opt_out`(
  `event_date` string COMMENT 'from deserializer',
  `user_id` string COMMENT 'from deserializer')
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/EventOptOut'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'transient_lastDdlTime'='1644698468')

CREATE EXTERNAL TABLE `event_opt_out_inj`(
  `user_id` string COMMENT 'from deserializer')
PARTITIONED BY (
  `event_date` string)
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/EventOptOut'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'projection.enabled'='true',
  'projection.event_date.type'='injected',
  'storage.location.template'='s3://battery-staple-v1/EventOptOut/${event_date}',
  'transient_lastDdlTime'='1644698468')

CREATE EXTERNAL TABLE `event_opt_in`(
  `event_date` string COMMENT 'from deserializer',
  `user_id` string COMMENT 'from deserializer')
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/EventOptIn'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'transient_lastDdlTime'='1644698468')

CREATE EXTERNAL TABLE `event_opt_in_inj`(
  `user_id` string COMMENT 'from deserializer')
PARTITIONED BY (
  `event_date` string)
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/EventOptIn'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'projection.enabled'='true',
  'projection.event_date.type'='injected',
  'storage.location.template'='s3://battery-staple-v1/EventOptIn/${event_date}',
  'transient_lastDdlTime'='1644698468')

CREATE EXTERNAL TABLE `event_ride`(
  `event_date` string COMMENT 'from deserializer',
  `time` string COMMENT 'from deserializer',
  `car_id` string COMMENT 'from deserializer',
  `driver_id` string COMMENT 'from deserializer',
  `location` string COMMENT 'from deserializer',
  `user_id` string COMMENT 'from deserializer')
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/EventRide'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'transient_lastDdlTime'='1646108690')

CREATE EXTERNAL TABLE `event_ride_inj`(
  `time` string COMMENT 'from deserializer',
  `car_id` string COMMENT 'from deserializer',
  `driver_id` string COMMENT 'from deserializer',
  `location` string COMMENT 'from deserializer',
  `user_id` string COMMENT 'from deserializer')
PARTITIONED BY (
  `event_date` string)
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/EventRide'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'projection.enabled'='true',
  'projection.event_date.type'='injected',
  'storage.location.template'='s3://battery-staple-v1/EventRide/${event_date}',
  'transient_lastDdlTime'='1646108690')

CREATE EXTERNAL TABLE `person`(
  `user_id` string COMMENT 'from deserializer',
  `name` string COMMENT 'from deserializer',
  `time` string COMMENT 'from deserializer',
  `location` string COMMENT 'from deserializer',
  `opt_in` boolean COMMENT 'from deserializer',
  `last_updated` string COMMENT 'from deserializer')
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://battery-staple-v1/Person'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'transient_lastDdlTime'='1644258294')


CREATE OR REPLACE VIEW "current_fiscal_year" AS
select current_date as today,
	date_trunc('year', current_date - interval '7' month) as starting_year,
	date_trunc('year', current_date - interval '7' month) + interval '7' month as starting_day,
	date_trunc('year', current_date - interval '7' month) + interval '7' month + interval '10' month - interval '1' day as ending_day


CREATE OR REPLACE VIEW "current_event" AS
SELECT
  event_date
, name
, pickup_time
, pickup_interval
, guest_pickup_time
, guest_pickup_interval
, guest_rides
FROM
  event
WHERE (event_date = (SELECT "min"(event_date)
FROM
  event
WHERE ("date_parse"(event_date, '%Y-%m-%d') >= "date_trunc"('day', "date_add"('hour', -7, "now"())))
))
ORDER BY event_date ASC

CREATE OR REPLACE VIEW "current_event_drivers" AS
WITH
  driver_index AS (
   SELECT
     ed.event_date
   , ed.user_id
   , "row_number"() OVER (PARTITION BY '1' ORDER BY "random"() ASC) index
   FROM
     (event_driver ed
   INNER JOIN current_event ce ON (ed.event_date = ce.event_date))
)
, car_index AS (
   SELECT
     owner
   , seats
   , model
   , parking_spot
   , "row_number"() OVER (PARTITION BY '1' ORDER BY seats DESC, "random"() ASC) index
   FROM
     car
)
SELECT
  ci.owner
, di.user_id driver_id
, CAST(ci.seats AS bigint) seats
, ci.model
, ci.parking_spot
FROM
  (driver_index di
INNER JOIN car_index ci ON (di.index = ci.index))

CREATE OR REPLACE VIEW "current_event_ride" AS
SELECT
  er.event_date
, ce.name event_name
, er.time
, er.car_id
, po.name car_owner_name
, c.model
, c.seats
, c.parking_spot
, pd.name driver_name
, er.location
, er.user_id
, COALESCE(pr.name, er.user_id) rider_name
FROM
  (((((event_ride er
INNER JOIN current_event ce ON (er.event_date = ce.event_date))
LEFT JOIN person pr ON (er.user_id = pr.user_id))
INNER JOIN person po ON (er.car_id = po.user_id))
INNER JOIN person pd ON (er.driver_id = pd.user_id))
INNER JOIN car c ON (er.car_id = c.owner))

CREATE OR REPLACE VIEW "current_riders" AS
SELECT
  p.user_id
, p.name
, p.time
, p.location
, ce.event_date
, ce.name event_name
FROM
  person p
, current_event ce
WHERE (NOT (user_id IN (SELECT user_id
FROM
  (event_opt_out eo
INNER JOIN current_event ce ON (eo.event_date = ce.event_date))
)))

PREPARE excess_driver_query
FROM
SELECT count(distinct d.user_id) - count(distinct r.driver_id) as excess_driver_count
FROM event_ride_inj r,
	event_driver_inj d
WHERE r.event_date = ?
	AND d.event_date = ?


PREPARE current_event_drivers_query
FROM WITH driver_index AS (
		SELECT ed.event_date,
			ed.user_id,
			"row_number"() OVER (
				PARTITION BY '1'
				ORDER BY "random"() ASC
			) index
		FROM event_driver_inj ed
		WHERE ed.event_date = ?
			AND NOT (
				user_id IN (
					SELECT DISTINCT driver_id
					FROM event_ride_inj
					WHERE event_date = ?
				)
			)
	),
	car_index AS (
		SELECT 1, owner,
			seats,
			model,
			parking_spot,
			"row_number"() OVER (
				PARTITION BY '1'
				ORDER BY seats DESC,
					"random"() ASC
			) index
		FROM car
		WHERE NOT (
				owner IN (
					SELECT DISTINCT car_id
					FROM event_ride_inj er
						INNER JOIN event_driver_inj ed ON (er.driver_id = ed.user_id)
					WHERE er.event_date = ?
						AND ed.event_date = ?
				)
			) AND (
        owner IN (
          SELECT owner
          FROM event_car_inj ec
          WHERE ec.event_date = ?
        )
      )
	)
SELECT 1 as src, ci.owner,
	di.user_id driver_id,
	CAST(ci.seats AS bigint) seats,
	ci.model,
	ci.parking_spot
FROM (
		driver_index di
		INNER JOIN car_index ci ON (di.index = ci.index)
	)
UNION ALL
SELECT DISTINCT 2 as src, er.car_id AS owner,
	er.driver_id,
	CAST(c.seats AS bigint) seats,
	c.model,
	c.parking_spot
FROM event_ride_inj er
	INNER JOIN car c ON (er.car_id = c.owner)
	INNER JOIN event_driver_inj ed ON (er.driver_id = ed.user_id)
WHERE er.event_date = ?
	AND ed.event_date = ?
  AND (
    c.owner IN (
      SELECT owner
      FROM event_car_inj ec
      WHERE ec.event_date = ?
    )
  )
ORDER BY seats desc,
	random(),
	model



PREPARE current_event_ride_query FROM
SELECT
  er.event_date
, ce.name event_name
, cast(er.time as integer) as time
, er.car_id
, po.name car_owner_name
, c.model
, c.seats
, c.parking_spot
, pd.name driver_name
, er.location
, er.user_id
, COALESCE(pr.name, er.user_id) rider_name
FROM
  (((((event_ride_inj er
INNER JOIN current_event ce ON (er.event_date = ce.event_date))
LEFT JOIN person pr ON (er.user_id = pr.user_id))
INNER JOIN person po ON (er.car_id = po.user_id))
INNER JOIN person pd ON (er.driver_id = pd.user_id))
INNER JOIN car c ON (er.car_id = c.owner))
WHERE er.event_date = ?
ORDER BY time, location, model, rider_name


PREPARE current_riders_query
FROM
-- CTE computes set of user_id's that are eligible for rides 
with valid_person as (
	select user_id,
		opt_in
	from person p,
		current_fiscal_year f
	where CAST(COALESCE(p.last_updated, '1971-01-01') AS date) between f.starting_day and f.ending_day
		AND p.location IS NOT null
		AND p.time IS NOT null
),
opt_out_person as (
	select 1,
		user_id
	from valid_person
	where not opt_in
		and user_id not in (
			select user_id
			from event_opt_out_inj
			where event_date = ?
		)
),
opt_in_person as (
	select 2,
		user_id
	from valid_person
	where opt_in
		and user_id in (
			select user_id
			from event_opt_in_inj
			where event_date = ?
		)
),
opt_all_person as (
	select *
	from opt_out_person
	union all
	select *
	from opt_in_person
),
valid_event_person as (
	select distinct user_id
	from opt_all_person
)
-- All guest rides are current riders
SELECT 3 as sequence,
    1 as stop_count,
    er.user_id,
    er.user_id as name,
    cast(er.time as integer) as time,
    er.location,
    er.car_id,
    er.driver_id,
    er.event_date,
    e.name event_name
FROM event_ride_inj er INNER JOIN event e on (er.event_date = e.event_date)
WHERE (
    er.location != 'Open'
    AND cast(er.time as integer) > 1000
    AND er.event_date = ?
    AND e.event_date = ?
)
UNION ALL
-- Valid persons, but not already scheduled for a ride
SELECT 2 as sequence,
	count(*) over (partition by p.time, p.location) as stop_count,
	p.user_id,
	p.name,
	cast(p.time as integer) as time,
	p.location,
	null as car_id,
	null as driver_id,
	e.event_date,
	e.name event_name
FROM person p,
	event e,
  current_fiscal_year f
WHERE (
    user_id in (SELECT user_id FROM valid_event_person)
    AND
		NOT (
			user_id IN (
				SELECT user_id
				FROM event_ride
				where event_date = ?
					and user_id is not null
			)
		)
	)
	AND e.event_date = ?
UNION ALL
-- Current riders (not guests, inner join with persons) having not opted-out
SELECT 1 as sequence,
	count(*) over (partition by p.time, p.location) as stop_count,
	er.user_id,
	p.name,
	cast(er.time as integer) as time,
	er.location,
	er.car_id,
	er.driver_id,
	er.event_date,
	e.name event_name
FROM event_ride er
	INNER JOIN event e on (er.event_date = e.event_date)
	INNER JOIN person p on (er.user_id = p.user_id)
WHERE (
		NOT (
			er.user_id IN (
				SELECT user_id
				FROM event_opt_out_inj
				where event_date = ?
			)
		)
	)
	AND er.event_date = ?
ORDER BY sequence,
	time,
	stop_count desc,
	location,
	random(),
	name
