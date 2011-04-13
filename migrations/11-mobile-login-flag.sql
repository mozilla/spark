
-- Bug 649652: Multi-sparker badge requires a new profile flag since registration is now available on desktop
ALTER TABLE `users_profile` ADD COLUMN `login_mobile` bool NOT NULL AFTER `login_desktop`;