from peewee import *
import datetime

db = SqliteDatabase("data.db", pragmas={"foreign_keys": 1})

class BaseModel(Model):
    class Meta:
        database = db

class Player(BaseModel):
    id = AutoField()
    consent = DateTimeField(null=True)
    demographic_identifier = CharField(max_length=8, null=True)
    created = DateTimeField(default=datetime.datetime.now)
    rewards = TextField(null=True)
    total_payoff = IntegerField(default=0)
    total_time = IntegerField(default=0)
    attention_check = CharField(max_length=256, null=True)
    high_reward = CharField(max_length=10, null=True)
    low_reward = CharField(max_length=10, null=True)
    more_different = CharField(max_length=10, null=True)
    less_different = CharField(max_length=10, null=True)
    mturk_id = CharField(max_length=50, null=True)  # New field for MTurk ID
    
class GameReward(BaseModel):
    player = ForeignKeyField(Player, backref='rewards')
    image_name = CharField()
    reward = IntegerField()

class Meta:
    indexes = (
        (('player', 'image_name'), True),
    )

db.connect()
db.create_tables([Player, GameReward], safe=True)
