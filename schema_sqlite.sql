CREATE TABLE `tasks` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `task` TEXT,
  `project_id` INTEGER,
  `done` INTEGER ,
  `deadline` DATE,
  `priority` INTEGER,
  `user_id` INTEGER,
  `updated` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
   FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TRIGGER `triggerDate` AFTER UPDATE ON `tasks`
BEGIN
   update `tasks` SET `updated` = (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE id = NEW.id;
END;

CREATE TABLE `projects` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `project` TEXT,
  `user_id` INTEGER,
  `updated` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),

  FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TRIGGER `triggerPrjcts` AFTER UPDATE ON `projects`
BEGIN
   update `projects` SET `updated` = (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE id = NEW.id;
END;


CREATE TABLE `users` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `registered_at` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  `last_login` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  `username` VARCHAR(255),
  `password` VARCHAR(200),
  `email` VARCHAR(200)
);


CREATE TRIGGER `triggerUserLogin` AFTER UPDATE ON `users`
BEGIN
   update `users` SET `last_login` = (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE id = NEW.id;
END;

