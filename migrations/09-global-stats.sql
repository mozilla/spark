
-- Create two new tables for 'Countries Sparked' and 'Continents Sparked' stats
CREATE TABLE `stats_countrysparked` (
    `country_code` varchar(2) NOT NULL PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
CREATE TABLE `stats_continentsparked` (
    `continent_code` varchar(2) NOT NULL PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

-- Change 'value' field of GlobalStats to PositiveIntegerField since they are simple counters
ALTER TABLE `stats_globalstats` CHANGE COLUMN `value` `value` integer UNSIGNED;

-- Add two name/value records in GlobalStats to keep track of total sparks and badges
INSERT INTO stats_globalstats (name, value) VALUES 
('total_sparks',0),
('total_badges',0);