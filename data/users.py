import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    timer_flag = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    message_flag = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    user_timers = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='')
    user_message = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='')
    count_steps_message = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    count_steps_timer = sqlalchemy.Column(sqlalchemy.Integer, default=1)
