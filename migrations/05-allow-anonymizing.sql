
-- Allows username, password and email to be set to NULL when users delete their account
ALTER TABLE `auth_user` CHANGE COLUMN `username` `username` VARCHAR(30) NULL, CHANGE COLUMN `email` `email` VARCHAR(75) NULL, CHANGE COLUMN `password` `password` VARCHAR(255) NULL;

-- Adds a new parent_username column so that "deleted" users can still have their username
-- displayed on their children's user dashboard, in the 'Spark started with:' section.
ALTER TABLE `users_profile` ADD COLUMN `parent_username` VARCHAR(30) NULL DEFAULT NULL AFTER `no_parent`;

-- Set the new parent_username column with the correct value for existing users in the database.
UPDATE users_profile p SET p.parent_username=(SELECT u.username FROM auth_user u, users_tree t, users_tree t2 WHERE t.user_id=p.user_id AND t2.id=t.parent_id AND u.id=t2.user_id);