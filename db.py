import sqlite3


class Database:
    def __init__(self, db_file):
        # connecting to DB and saving connection cursor
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def get_info(self, user_id):
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM `subscriptions` WHERE `user_id` = ?", (user_id,)).fetchall()

    def add_subs(self, user_id, subs_info):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO `subscriptions` (`user_id`, `subs_info`) VALUES (?, ?)", (user_id, subs_info))

    def remove_subs(self, user_id, sub_id):
        with self.connection:
            self.cursor.execute(
                "DELETE FROM `subscriptions` WHERE `id` = ?", (sub_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `subscriptions` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def close(self):
        self.connection.close()
