# models/disease.py

# Evita import direto do app para não gerar dependência circular
from flask_sqlalchemy import SQLAlchemy

# Cria uma instância local apenas para tipagem — será substituída pelo orm_db no app
db = SQLAlchemy()

class Disease(db.Model):
    __tablename__ = 'diseases'

    id_disease = db.Column(db.Integer, primary_key=True)
    disease_name_pt = db.Column(db.String, nullable=False)
    disease_desc_pt = db.Column(db.Text, nullable=True)
    breve_desc = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Disease {self.disease_name_pt}>"

    def to_dict(self):
        return {
            "id_disease": self.id_disease,
            "disease_name_pt": self.disease_name_pt,
            "disease_desc_pt": self.disease_desc_pt,
            "breve_desc": self.breve_desc
        }