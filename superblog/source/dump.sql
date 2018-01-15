CREATE DATABASE  IF NOT EXISTS `superblog` CHARACTER SET UTF8;

CREATE USER django@localhost IDENTIFIED BY 'theiB3za';
CREATE USER xss@localhost IDENTIFIED BY 'AoL5anga';

GRANT ALL PRIVILEGES ON superblog.* TO django@localhost;
GRANT ALL PRIVILEGES ON superblog.* TO xss@localhost;

FLUSH PRIVILEGES;
