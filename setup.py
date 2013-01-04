from greglink import app, models, db

app.config.from_object('greglink.default_config')
app.config.from_envvar('CONFIG_FILE')

def create_tables():
    db.create_all()

def create_statuses():
    statuses = ['success', 'blocked', 'failed']
    for status_name in statuses:
        status = models.Status(name=status_name)
        db.session.add(status)

    db.session.commit()


if __name__ == "__main__":
    create_tables()
    create_statuses()
