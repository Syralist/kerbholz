from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from json import JSONEncoder

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(120), unique=True)
    email = Column(String(120), unique=False)
    active = Column(Boolean, unique=False)
    balance = Column(Integer, unique=False)
    limit = Column(Integer, unique=False)
    transactions = relationship('Transaction', lazy='dynamic', 
                                back_populates='user')

    def __init__(self, nickname=None, email=None, active=None, 
                 balance=None, limit=None):
        self.nickname = nickname
        self.email = email
        self.active = active
        self.balance = balance
        self.limit = limit

    def __repr__(self):
        return 'Name: %r' % (self.nickname)

class KerbJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'DT_RowId' : obj.id,
                'nickname' : obj.nickname,
                'email' : obj.email,
                'active' : obj.active,
                'balance' : obj.balance,
                'limit' : obj.limit,
                'transactions' : obj.transactions
            }
        elif isinstance(obj, Transaction):
            return {
                'DT_RowId' : obj.id,
                'user' : obj.user,
                'timestamp' : obj.timestamp,
                'amount' : obj.amount
            }
        return super(KerbJSONEncoder, self).default(obj)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="transactions")
    timestamp = Column(DateTime, unique=False)
    amount = Column(Integer, unique=False)

    def __init__(self, user_id=None, timestamp=None, amount=None):
        self.user_id = user_id
        self.timestamp = timestamp
        self.amount = amount

    def __repr__(self):
        return 'Amount: %r' % (self.amount)
