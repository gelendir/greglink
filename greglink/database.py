from greglink import db
from greglink.models.status import Status

def init_db():
    create_tables()
    create_statuses()

def create_tables():
    db.create_all()

def create_statuses():
    statuses = ['success', 'blocked', 'failed']
    for status_name in statuses:
        status = Status(name=status_name)
        db.session.add(status)

    db.session.commit()

def destroy_db():
    db.drop_all()
