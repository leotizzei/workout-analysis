from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
import os
from datetime import date

DB_PATH = os.getenv("DB_PATH")
Base = declarative_base()


def init_database():
    path = 'sqlite:///{}'.format(DB_PATH)
    engine = create_engine(path)
    Base.metadata.create_all(engine)


class Activity(Base):

    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    strava_activity_id = Column(Integer)
    distance = Column(Float)
    moving_time = Column(Integer)
    elapsed_time = Column(Integer)
    total_elevation_gain = Column(Integer)
    activity_type = Column(String)
    start_date = Column(Date)
    start_date_local = Column(Date)
    timezone = Column(String)
    utc_offset = Column(Integer)
    average_speed = Column(Float)
    max_speed = Column(Integer)
    has_heartrate = Column(Boolean)
    workout_type = Column(String)


class Lap(Base):

    __tablename__ = 'lap'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey(Activity.id))
    name = Column(String)
    elapsed_time = Column(Integer)
    moving_time = Column(Integer)
    start_date = Column(Date)
    start_date_local = Column(Date)
    distance = Column(Float)
    start_index= Column(Integer)
    end_index= Column(Integer)
    total_elevation_gain= Column(Integer)
    average_speed= Column(Float)
    max_speed= Column(Float)
    average_cadence= Column(Integer)

    average_watts= Column(Float)
    lap_index= Column(Integer)
    split= Column(Integer)


class ActivityConn:

    def __init__(self):
        path = 'sqlite:///{}'.format(DB_PATH)
        engine = create_engine(path)
        session = sessionmaker()
        session.configure(bind=engine)
        self.session = session()

    def insert_activity(self, activity: Activity) -> int:
        existing_activities = self.session.query(Activity).filter(
            Activity.start_date == activity.start_date,
            Activity.distance == activity.distance,
            Activity.average_speed == activity.average_speed).all()
        if len(existing_activities) == 0:
            assert isinstance(activity.start_date, date), "Error!"
            assert isinstance(activity.distance, float), "Error!"
            assert isinstance(activity.average_speed, float), "Error!"
            assert activity.activity_type is not None, "Error"
            self.session.add(activity)
            self.session.commit()
            return activity.id
        else:
            return -1

    def query_activity(self) -> list:
        activities = self.session.query(Activity).all()
        return activities


class LapConn:

    def __init__(self):
        path = 'sqlite:///{}'.format(DB_PATH)
        engine = create_engine(path)
        session = sessionmaker()
        session.configure(bind=engine)
        self.session = session()

    def insert_lap(self, lap: Lap) -> int:
        existing_laps = self.session.query(Lap).filter(
            Lap.lap_index == lap.lap_index,
            Lap.activity_id == lap.activity_id).all()
        if len(existing_laps) == 0:
            assert isinstance(lap.distance, float), "Error!"
            assert isinstance(lap.average_speed, float), "Error!"
            self.session.add(lap)
            self.session.commit()
            return lap.id

    def query_laps(self, activity_id) -> list:
        laps = self.session.query(Lap).filter(Lap.activity_id == activity_id).all()
        return laps