from datetime import datetime
from datetime import timezone

from . import db


class Population_Data(db.Model):
    __tablename__ = "population"

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(4))
    count = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), index=True)

    __table_args__ = (
        db.UniqueConstraint("region", "timestamp", name="_region_time_uc"),
    )

    def __repr__(self):
        return f"<{self.region} count: {self.count}>"
