from greglink import db

class Status(db.Model):

    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<Status id:%s name:%s>" % (self.id, self.name)
