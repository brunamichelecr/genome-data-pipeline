# Arquivo: models/gene_models.py

from flask_sqlalchemy import SQLAlchemy
from .disease import db # Importa a instância 'db' do seu arquivo disease.py

# Tabela de Genes
class Gene(db.Model):
    __tablename__ = 'genes'
    
    # ID INTERNO (SERIAL PK)
    id_gene = db.Column(db.Integer, primary_key=True)
    # ID UNIVERSAL (NCBI ID)
    ncbi_gene_id = db.Column(db.Text, unique=True, nullable=False) 
    gene_symbol = db.Column(db.String(50), nullable=False)
    gene_name = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relação com a tabela de associação
    disease_associations = db.relationship("GeneDiseaseAssociation", back_populates="gene")

    def __repr__(self):
        return f"<Gene {self.gene_symbol} (NCBI: {self.ncbi_gene_id})>"

# Tabela de Associação (Relacionamento N:N)
class GeneDiseaseAssociation(db.Model):
    __tablename__ = 'gene_disease_association'
    
    # FK para diseases (doença)
    id_disease = db.Column(db.Integer, db.ForeignKey('diseases.id_disease'), primary_key=True)
    # FK para genes
    id_gene = db.Column(db.Integer, db.ForeignKey('genes.id_gene'), primary_key=True)
    associated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relações bidirecionais
    disease = db.relationship("Disease", back_populates="gene_associations")
    gene = db.relationship("Gene", back_populates="disease_associations")