# models/disease.py


from db import get_connection

class Disease(db.Model):
    """
    Modelo para armazenar informações de doenças, incluindo traduções
    e UIDs do MedGen/NCBI.
    """
    __tablename__ = 'diseases'

    id_disease = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(100), nullable=True)     
    disease_desc = db.Column(db.Text, nullable=True)             
    medgen_uid = db.Column(db.String(15), nullable=True)           
    disease_synonym = db.Column(db.Text, nullable=True)         

    disease_name_pt = db.Column(db.String(100), nullable=False)
    disease_desc_pt = db.Column(db.Text, nullable=True)
    breve_desc = db.Column(db.Text, nullable=True)
    
    # Relação Muitos-para-Muitos (M:M) com Genes, usando a instância db
    gene_associations = db.relationship(
        "GeneDiseaseAssociation", 
        back_populates="disease",
        cascade="all, delete-orphan" # Regra para exclusão
    )

    def __repr__(self):
        return f"<Disease {self.disease_name_pt}>"

    def to_dict(self):
        return {
            "id_disease": self.id_disease,
            "disease_name_pt": self.disease_name_pt,
            "disease_desc_pt": self.disease_desc_pt,
            "breve_desc": self.breve_desc
        }