CREATE TABLE `django_content_type` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(100) NOT NULL,
    `app_label` varchar(100) NOT NULL,
    `model` varchar(100) NOT NULL,
    UNIQUE (`app_label`, `model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE `auth_permission` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `content_type_id` integer NOT NULL,
    `codename` varchar(100) NOT NULL,
    UNIQUE (`content_type_id`, `codename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `auth_permission` ADD CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

CREATE TABLE `auth_group_permissions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `group_id` integer NOT NULL,
    `permission_id` integer NOT NULL,
    UNIQUE (`group_id`, `permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `auth_group_permissions` ADD CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

CREATE TABLE `auth_group` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(80) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `auth_group_permissions` ADD CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

CREATE TABLE `auth_user_user_permissions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `permission_id` integer NOT NULL,
    UNIQUE (`user_id`, `permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `auth_user_user_permissions` ADD CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

CREATE TABLE `auth_user_groups` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `group_id` integer NOT NULL,
    UNIQUE (`user_id`, `group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `auth_user_groups` ADD CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

CREATE TABLE `auth_user` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `username` varchar(30) NOT NULL UNIQUE,
    `first_name` varchar(30) NOT NULL,
    `last_name` varchar(30) NOT NULL,
    `email` varchar(75) NOT NULL,
    `password` varchar(255) NOT NULL,
    `is_staff` bool NOT NULL,
    `is_active` bool NOT NULL,
    `is_superuser` bool NOT NULL,
    `last_login` datetime NOT NULL,
    `date_joined` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `auth_user_user_permissions` ADD CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `auth_user_groups` ADD CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

CREATE TABLE `auth_message` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `message` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `auth_message` ADD CONSTRAINT `user_id_refs_id_9af0b65a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `auth_permission_e4470c6e` ON `auth_permission` (`content_type_id`);
CREATE INDEX `auth_message_fbfc09f1` ON `auth_message` (`user_id`);

CREATE TABLE `django_site` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `domain` varchar(100) NOT NULL,
    `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE `django_session` (
    `session_key` varchar(40) NOT NULL PRIMARY KEY,
    `session_data` longtext NOT NULL,
    `expire_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE `django_admin_log` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `action_time` datetime NOT NULL,
    `user_id` integer NOT NULL,
    `content_type_id` integer,
    `object_id` longtext,
    `object_repr` varchar(200) NOT NULL,
    `action_flag` smallint UNSIGNED NOT NULL,
    `change_message` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `django_admin_log` ADD CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `django_admin_log` ADD CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);
CREATE INDEX `django_admin_log_fbfc09f1` ON `django_admin_log` (`user_id`);
CREATE INDEX `django_admin_log_e4470c6e` ON `django_admin_log` (`content_type_id`);

CREATE TABLE `djcelery_intervalschedule` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `every` integer NOT NULL,
    `period` varchar(24) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE `djcelery_crontabschedule` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `minute` varchar(64) NOT NULL,
    `hour` varchar(64) NOT NULL,
    `day_of_week` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE `djcelery_periodictasks` (
    `ident` smallint NOT NULL PRIMARY KEY,
    `last_update` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE `djcelery_periodictask` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(200) NOT NULL UNIQUE,
    `task` varchar(200) NOT NULL,
    `interval_id` integer,
    `crontab_id` integer,
    `args` longtext NOT NULL,
    `kwargs` longtext NOT NULL,
    `queue` varchar(200),
    `exchange` varchar(200),
    `routing_key` varchar(200),
    `expires` datetime,
    `enabled` bool NOT NULL,
    `last_run_at` datetime,
    `total_run_count` integer UNSIGNED NOT NULL,
    `date_changed` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `djcelery_periodictask` ADD CONSTRAINT `interval_id_refs_id_f2054349` FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`);
ALTER TABLE `djcelery_periodictask` ADD CONSTRAINT `crontab_id_refs_id_ebff5e74` FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`);

CREATE TABLE `djcelery_workerstate` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `hostname` varchar(255) NOT NULL UNIQUE,
    `last_heartbeat` datetime
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE `djcelery_taskstate` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `state` varchar(64) NOT NULL,
    `task_id` varchar(36) NOT NULL UNIQUE,
    `name` varchar(200),
    `tstamp` datetime NOT NULL,
    `args` longtext,
    `kwargs` longtext,
    `eta` datetime,
    `expires` datetime,
    `result` longtext,
    `traceback` longtext,
    `runtime` double precision,
    `worker_id` integer,
    `hidden` bool NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `djcelery_taskstate` ADD CONSTRAINT `worker_id_refs_id_4e3453a` FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`);
CREATE INDEX `djcelery_periodictask_17d2d99d` ON `djcelery_periodictask` (`interval_id`);
CREATE INDEX `djcelery_periodictask_7aa5fda` ON `djcelery_periodictask` (`crontab_id`);
CREATE INDEX `djcelery_workerstate_eb8ac7e4` ON `djcelery_workerstate` (`last_heartbeat`);
CREATE INDEX `djcelery_taskstate_52094d6e` ON `djcelery_taskstate` (`name`);
CREATE INDEX `djcelery_taskstate_f0ba6500` ON `djcelery_taskstate` (`tstamp`);
CREATE INDEX `djcelery_taskstate_20fc5b84` ON `djcelery_taskstate` (`worker_id`);

CREATE TABLE `spark_city` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `city_name` varchar(255) NOT NULL UNIQUE,
    `country_code` varchar(2) NOT NULL,
    `latitude` double precision NOT NULL,
    `longitude` double precision NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
CREATE INDEX `spark_city_761a2bbd` ON `spark_city` (`longitude`);

CREATE TABLE `challenges_challenge` (
    `id` varchar(4) NOT NULL PRIMARY KEY,
    `level` integer UNSIGNED NOT NULL,
    `number` integer UNSIGNED NOT NULL,
    `easter_egg` bool NOT NULL,
    UNIQUE (`level`, `number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
CREATE INDEX `challenges_challenge_2a8f42e8` ON `challenges_challenge` (`level`);

CREATE TABLE `users_profile` (
    `user_id` integer NOT NULL PRIMARY KEY,
    `level` integer UNSIGNED NOT NULL,
    `new_challenges` bool NOT NULL,
    `boost1_completed` bool NOT NULL,
    `latitude` double precision,
    `longitude` double precision,
    `major_city_id` integer,
    `city_name` varchar(255),
    `country_code` varchar(2),
    `us_state` varchar(2),
    `boost2_completed` bool NOT NULL,
    `no_parent` bool NOT NULL,
    `date_boost2_localtime` datetime,
    `login_desktop` bool NOT NULL,
    `is_non_android` bool NOT NULL,
    `short_url_twitter` varchar(64),
    `short_url_facebook` varchar(64),
    `short_url_qr` varchar(64),
    `short_url_poster` varchar(64)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `users_profile` ADD CONSTRAINT `user_id_refs_id_21617f27` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `users_profile` ADD CONSTRAINT `major_city_id_refs_id_7e81100f` FOREIGN KEY (`major_city_id`) REFERENCES `spark_city` (`id`);

CREATE TABLE `users_completedchallenge` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `challenge_id` varchar(4) NOT NULL,
    `profile_id` integer NOT NULL,
    `date_completed` datetime NOT NULL,
    `date_badge_earned` datetime,
    `new_badge` bool NOT NULL,
    UNIQUE (`challenge_id`, `profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `users_completedchallenge` ADD CONSTRAINT `challenge_id_refs_id_38323f3a` FOREIGN KEY (`challenge_id`) REFERENCES `challenges_challenge` (`id`);
ALTER TABLE `users_completedchallenge` ADD CONSTRAINT `profile_id_refs_user_id_7b507891` FOREIGN KEY (`profile_id`) REFERENCES `users_profile` (`user_id`);

CREATE TABLE `users_tree` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL UNIQUE,
    `parent_id` integer,
    `lft` integer UNSIGNED NOT NULL,
    `rght` integer UNSIGNED NOT NULL,
    `tree_id` integer UNSIGNED NOT NULL,
    `level` integer UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `users_tree` ADD CONSTRAINT `user_id_refs_id_39e43001` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `users_tree` ADD CONSTRAINT `parent_id_refs_id_eea8ba7b` FOREIGN KEY (`parent_id`) REFERENCES `users_tree` (`id`);
CREATE INDEX `users_profile_20aba5` ON `users_profile` (`major_city_id`);
CREATE INDEX `users_completedchallenge_dd8bebce` ON `users_completedchallenge` (`challenge_id`);
CREATE INDEX `users_completedchallenge_141c6eec` ON `users_completedchallenge` (`profile_id`);
CREATE INDEX `users_tree_63f17a16` ON `users_tree` (`parent_id`);
CREATE INDEX `users_tree_42b06ff6` ON `users_tree` (`lft`);
CREATE INDEX `users_tree_91543e5a` ON `users_tree` (`rght`);
CREATE INDEX `users_tree_efd07f28` ON `users_tree` (`tree_id`);
CREATE INDEX `users_tree_2a8f42e8` ON `users_tree` (`level`);

CREATE TABLE `stats_personalstats` (
    `user_id` integer NOT NULL PRIMARY KEY,
    `longest_chain` integer UNSIGNED NOT NULL,
    `total_shares` integer UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `stats_personalstats` ADD CONSTRAINT `user_id_refs_user_id_1ca6d184` FOREIGN KEY (`user_id`) REFERENCES `users_profile` (`user_id`);

CREATE TABLE `stats_globalstats` (
    `name` varchar(255) NOT NULL PRIMARY KEY,
    `value` double precision
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE `stats_sharinghistory` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `parent_id` integer NOT NULL,
    `date_shared` datetime NOT NULL,
    `shared_via` integer UNSIGNED NOT NULL,
    `timezone` varchar(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `stats_sharinghistory` ADD CONSTRAINT `parent_id_refs_user_id_6d8227b6` FOREIGN KEY (`parent_id`) REFERENCES `users_profile` (`user_id`);

CREATE TABLE `stats_citysharinghistory` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `city_from_id` integer NOT NULL,
    `city_to_id` integer NOT NULL,
    `sharer_id` integer NOT NULL,
    `date_shared` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
ALTER TABLE `stats_citysharinghistory` ADD CONSTRAINT `city_from_id_refs_id_1b789701` FOREIGN KEY (`city_from_id`) REFERENCES `spark_city` (`id`);
ALTER TABLE `stats_citysharinghistory` ADD CONSTRAINT `city_to_id_refs_id_1b789701` FOREIGN KEY (`city_to_id`) REFERENCES `spark_city` (`id`);
ALTER TABLE `stats_citysharinghistory` ADD CONSTRAINT `sharer_id_refs_user_id_8bb85795` FOREIGN KEY (`sharer_id`) REFERENCES `users_profile` (`user_id`);
CREATE INDEX `stats_sharinghistory_63f17a16` ON `stats_sharinghistory` (`parent_id`);
CREATE INDEX `stats_citysharinghistory_d8e066cf` ON `stats_citysharinghistory` (`city_from_id`);
CREATE INDEX `stats_citysharinghistory_51ed7bc0` ON `stats_citysharinghistory` (`city_to_id`);
CREATE INDEX `stats_citysharinghistory_a249f1c9` ON `stats_citysharinghistory` (`sharer_id`);
