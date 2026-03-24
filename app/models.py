from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.database import Model


class Script(Model):
    __tablename__ = 'scripts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    interval: Mapped[int]
    
    outputs: Mapped[List['ScriptOutput']] = relationship(
        back_populates='script'
    )


class ScriptOutput(Model):
    __tablename__ = 'output'
    id: Mapped[int] = mapped_column(primary_key=True)
    script_id: Mapped[int] = mapped_column(ForeignKey('scripts.id'))
    error: Mapped[Optional[str]] = mapped_column(nullable=True)
    output: Mapped[Optional[str]] = mapped_column(nullable=True)
    
    script: Mapped['Script'] = relationship(
        back_populates='outputs'
    )