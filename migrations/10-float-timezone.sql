
-- Bug 646348: Allow float UTC offsets (like -5.5 for instance)
ALTER TABLE `stats_sharinghistory` CHANGE COLUMN `timezone` `timezone` float;