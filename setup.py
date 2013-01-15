from greglink import app
from greglink import database

app.config.from_object('greglink.config.default_config')
app.config.from_envvar('CONFIG_FILE')

if __name__ == "__main__":
    database.init_db()
