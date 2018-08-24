import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()  # classses especiais que correspondem a tabelas

engine = create_engine("sqlite:///festas_de_papel.db")

class Festa(Base):
    __tablename__ = 'festa'
    id = Column('id', Integer, primary_key=True, nullable=False)
    festa_nome = Column('festa_nome', String(255), nullable=False)
    festa_descr = Column('festa_descr', String(255), nullable=False)
    festa_valor = Column('festa_valor', Integer, nullable=False)
    festa_foto = Column('festa_foto', Integer, ForeignKey('foto.id'))
    festa_tema = Column('festa_tema', Integer, ForeignKey('tema.id'))

    foto_festa = relationship('Foto', foreign_keys=festa_foto)
    tema_festa = relationship('Tema', foreign_keys=festa_tema)


class User(Base):
    __tablename__ = 'user'
    id = Column('ID', Integer, primary_key=True, nullable=False)
    user_nome = Column('user_nome', String(255),  nullable=False)
    user_email = Column('user_email', String(100),  nullable=False)
    user_apelido = Column('user_apelido', String(100),  nullable=False)
    user_password = Column('user_passwd', String(100),  nullable=False)
    user_foto = Column('user_foto', Integer, ForeignKey('foto.id'))

    foto_user = relationship('Foto', foreign_keys=user_foto)


class Arte(Base):
    __tablename__ = 'arte'
    ID = Column('ID', Integer, primary_key=True, nullable=False)
    arte_nome = Column('arte_nome', String(255),  nullable=False)
    arte_descr = Column('arte_descr', String(255),  nullable=False)
    arte_foto = Column(
        'arte_foto', Integer, ForeignKey('foto.id'))
    arte_obj = Column('arte_obj', Integer, ForeignKey('objeto.id'))
    arte_tema = Column('arte_tema', Integer, ForeignKey('tema.id'))

    tema_arte = relationship('Tema', foreign_keys=arte_tema)
    obj_arte = relationship('Objeto', foreign_keys=arte_obj)
    foto_arte = relationship('Foto', foreign_keys=arte_foto)

    @property
    def serialize(self):
        return{
            'nome': self.arte_nome,
            'descricao': self.arte_descr,
            'objeto': self.arte_obj,
            'tema': self.tema_id,
        }


class ItensFesta(Base):
    __tablename__ = 'itens_festa'
    id = Column('id', Integer, primary_key=True, nullable=False)
    festa_id = Column('festa_id', Integer, ForeignKey('festa.id'))
    arte_id = Column('arte_id', Integer, ForeignKey('arte.ID'))

    arte = relationship('Arte', foreign_keys=arte_id)
    festa = relationship('Festa', foreign_keys=festa_id)


class Foto(Base):
    __tablename__ = 'foto'
    id = Column('id', Integer, primary_key=True, nullable=False)
    foto_caminho = Column('foto_caminho', String(255))
    arte_id = Column('arte_ID', Integer, ForeignKey('arte.ID'))

    arte = relationship('Arte', foreign_keys=arte_id)


class FormatoArquivo(Base):
    __tablename__ = 'formato_arquivo'
    id = Column('id', Integer, primary_key=True, nullable=False)
    formato_nome = Column('String(255)', String(255))


class Arquivo(Base):
    __tablename__ = 'arquivo'
    id = Column('id', Integer, primary_key=True, nullable=False)
    arq_caminho = Column('arq_caminho', String(255))
    arq_caract = Column('arq_caract', String(255))
    arq_valor = Column('arq_valor', Integer)
    arte_id = Column('arte_ID', Integer, ForeignKey('arte.ID'))
    formato_id = Column('formato_id', Integer,
                        ForeignKey('formato_arquivo.id'))

    arte = relationship('Arte', foreign_keys=arte_id)

    formato = relationship('FormatoArquivo', foreign_keys=formato_id)

class Tema(Base):
    __tablename__ = 'tema'
    id = Column('id', Integer, primary_key=True, nullable=False)
    tema_nome = Column('tema_nome', String(255))
    tema_descr = Column('tema_descr', String(255))
    tema_foto = Column(
        'tema_foto', Integer, ForeignKey('foto.id'))

    foto_tema = relationship('Foto', foreign_keys=tema_foto)


class Objeto(Base):
    __tablename__ = 'objeto'
    id = Column('id', Integer, primary_key=True, nullable=False)
    obj_nome = Column('obj_nome', String(255))
    obj_foto = Column(
        'obj_foto', Integer, ForeignKey('foto.id'))

    foto_obj = relationship('Foto', foreign_keys=obj_foto)

Base.metadata.create_all(engine)
