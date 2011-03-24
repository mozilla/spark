
-- Drop obsolete columns and add a new column for storing the longest chain of sharing
ALTER TABLE `users_profile` 
DROP COLUMN `short_url_poster`, 
DROP COLUMN `short_url_qr`, 
DROP COLUMN `short_url_facebook`, 
DROP COLUMN `short_url_twitter`, 
ADD COLUMN `longest_chain` integer UNSIGNED NOT NULL  AFTER `is_non_android`;

-- Get rid of this table since we store longest chain directly in the user profile
DROP TABLE `stats_personalstats`;