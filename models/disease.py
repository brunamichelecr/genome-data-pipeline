# models/disease.py

# Evita import direto do app para não gerar dependência circular
from flask_sqlalchemy import SQLAlchemy

# Cria uma instância local apenas para tipagem — será substituída pelo orm_db no app
db = SQLAlchemy()

class Disease(db.Model):
    __tablename__ = 'diseases'

    id_disease = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(100), nullable=True)     # Adicionei de volta, pois é usado para MeSH
    disease_desc = db.Column(db.Text, nullable=True)            # Adicionado para MeSH
    medgen_uid = db.Column(db.String(15), nullable=True)           # Adicionado para MeSH
    disease_synonym = db.Column(db.Text, nullable=True)         # Adicionado para MeSH

    disease_name_pt = db.Column(db.String(100), nullable=False)
    disease_desc_pt = db.Column(db.Text, nullable=True)
    breve_desc = db.Column(db.Text, nullable=True)
    
    # --------------------------------------------------------
    # NOVO: Relacionamento Muitos-para-Muitos (M:M) com Genes
    # --------------------------------------------------------
    gene_associations = db.relationship(
        "GeneDiseaseAssociation", 
        back_populates="disease",
        cascade="all, delete-orphan" # Regra para exclusão (apaga associações se a doença for deletada)
    )

    def __repr__(self):
        return f"<Disease {self.disease_name_pt}>"

    def to_dict(self):
        return {
            "id_disease": self.id_disease,
            "disease_name_pt": self.disease_name_pt,
            "disease_desc_pt": self.disease_desc_pt,
            "breve_desc": self.breve_desc
            # Você pode querer adicionar os campos MeSH se for usar na API
        }