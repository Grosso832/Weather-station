DROP TABLE IF EXISTS sensors;
CREATE TABLE IF NOT EXISTS sensors (
	name_id integer, 
    sens_desc varchar(200), 
    location varchar(200), 
    primary key(name_id) 
);
DROP TABLE IF EXISTS sensordata;
CREATE TABLE IF NOT EXISTS sensordata (
	data_year integer,
    data_month integer,
    data_day integer,
    data_time time,
    full_time datetime,
    name_id integer,
    temperature float,
    pressure float, 
    humidity float,
    PRIMARY KEY (full_time),
    FOREIGN KEY (name_id) REFERENCES sensors(name_id)
);

