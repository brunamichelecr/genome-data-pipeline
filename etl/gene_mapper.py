# etl/gene_mapper.py

# ——————————————————————————————
# 1. Imports
# ——————————————————————————————
from Bio import Entrez
import time
from sqlalchemy.orm import Session
from sqlalchemy import select 

# Assumindo que seus models estão na pasta 'models' e são acessíveis
from models.disease import Disease 
from models.gene_models import Gene, GeneDiseaseAssociation 


# ——————————————————————————————
# 2. Configuração
# ——————————————————————————————

# A variável Entrez deve ser usada após a importação
Entrez.email = "brunamichelecr@gmail.com" 


# ——————————————————————————————
# 3. Funções de Busca da API
# ——————————————————————————————

def search_medgen_uid_by_name(disease_name):
    """ 
    Busca o MedGen UID correspondente a um nome de doença na base 'medgen' do NCBI.
    """
    try:
        term_search = f'"{disease_name}"[TITL]'
        search_handle = Entrez.esearch(db="medgen", term=term_search, retmax=1)
        search_results = Entrez.read(search_handle)
        search_handle.close()
        
        return search_results["IdList"][0] if search_results["IdList"] else None
    except Exception as e:
        print(f"Erro ao buscar MedGen UID para doença '{disease_name}': {e}")
        return None

def search_gene_ids_by_medgen(medgen_uid):
    """ 
    Busca GeneIDs humanos (TaxID 9606) na base 'gene' do NCBI usando um MedGen UID.
    CORREÇÃO: Adiciona o filtro TaxID (9606) para buscar APENAS genes humanos.
    """
    try:
        # Filtra por Disease ID [DISID] AND Taxonomia Humana [taxid]
        term = f"{medgen_uid}[DISID] AND 9606[taxid]" 
        
        search_handle = Entrez.esearch(db="gene", term=term, retmax=200) 
        search_results = Entrez.read(search_handle)
        search_handle.close()
        return search_results.get("IdList", [])
    except Exception as e:
        print(f"Erro ao buscar GeneIDs para MedGen UID {medgen_uid}: {e}")
        return []

def fetch_gene_details(gene_ids):
    """ 
    Busca detalhes para uma lista de GeneIDs na base 'gene'.
    """
    if not gene_ids:
        return []
    
    id_string = ",".join(gene_ids)
    
    try:
        summary_handle = Entrez.esummary(db="gene", id=id_string)
        summary_results = Entrez.read(summary_handle)
        summary_handle.close()
        
        summaries = summary_results.get('DocumentSummarySet', {}).get('DocumentSummary')
        
        if not summaries:
            return []
            
        if isinstance(summaries, list):
            return summaries
        else:
            return [summaries]

    except Exception as e:
        print(f"Erro ao buscar detalhes de genes: {e}. Gene IDs: {gene_ids}")
        return []


# ——————————————————————————————
# 4. Funções de Persistência
# ——————————————————————————————

def _save_gene_and_association(orm_db, detail, id_disease):
    """ 
    Gerencia a criação/atualização de Gene e Associações com extração robusta do UID. 
    """
    
    # CORREÇÃO CRÍTICA: Extração robusta do ncbi_gene_id, lidando com o parsing irregular do Biopython
    ncbi_gene_id = None
    if isinstance(detail, dict) and "uid" in detail:
        ncbi_gene_id = str(detail["uid"])
    elif hasattr(detail, 'attributes') and 'uid' in detail.attributes:
        # Tenta obter o 'uid' como atributo (caso Entrez.read retorne um objeto Element)
        ncbi_gene_id = str(detail.attributes['uid'])
    
    if not ncbi_gene_id:
        # Se não conseguimos extrair o UID de forma alguma, o detalhe é inútil.
        print("Aviso: Detalhe do gene inválido. Não foi possível extrair o 'uid'. Pulando.")
        return

    # Extrai os nomes (usando NomenclatureName/Symbol se disponíveis, Description/Name como fallback)
    gene_symbol = detail.get("NomenclatureSymbol") or detail.get("Name", "N/A")
    gene_name = detail.get("NomenclatureName") or detail.get("Description", "N/A")

    # 1. Gerencia a Tabela 'genes' (Busca ou Cria)
    gene_obj = orm_db.session.execute(
        select(Gene).filter_by(ncbi_gene_id=ncbi_gene_id)
    ).scalar_one_or_none()
    
    if not gene_obj:
        gene_obj = Gene(
            ncbi_gene_id=ncbi_gene_id,
            gene_symbol=gene_symbol,
            gene_name=gene_name
        )
        orm_db.session.add(gene_obj)
        orm_db.session.flush() # Necessário para obter o id_gene antes do commit final
        print(f" - NOVO Gene: {gene_symbol} ({ncbi_gene_id})")
    
    # 2. Cria o Vínculo na Tabela 'gene_disease_association'
    association = orm_db.session.execute(
        select(GeneDiseaseAssociation).filter_by(
            id_disease=id_disease, 
            id_gene=gene_obj.id_gene
        )
    ).scalar_one_or_none()

    if not association:
        new_association = GeneDiseaseAssociation(
            id_disease=id_disease, 
            id_gene=gene_obj.id_gene
        )
        orm_db.session.add(new_association)
        print(f" - Associado: {gene_symbol} com Doença ID {id_disease}")
    

# ——————————————————————————————
# 5. Lógica de Mapeamento (CLI Entry Points)
# ——————————————————————————————

def run_map_medgen_uids(orm_db, disease_id=None):
    """
    Executa a primeira fase do ETL: mapeia o nome da doença para o MedGen UID.
    """
    
    DISEASE_NAME_FIELD = 'disease_name' 
    print("Iniciando mapeamento de MedGen UIDs...")
    
    query = select(Disease).filter(
        getattr(Disease, DISEASE_NAME_FIELD).isnot(None),
        Disease.medgen_uid.is_(None)
    )
    if disease_id:
        query = query.filter(Disease.id_disease == disease_id)

    diseases = orm_db.session.execute(query).scalars().all()
    
    if not diseases:
        print("Nenhuma doença para mapear (ou todas já têm MedGen UID).")
        return

    for disease in diseases:
        name_to_search = getattr(disease, DISEASE_NAME_FIELD)
        print(f"Processando Doença ID {disease.id_disease} ({name_to_search})")
        
        medgen_uid = search_medgen_uid_by_name(name_to_search)
        
        if medgen_uid:
            disease.medgen_uid = medgen_uid
            print(f" - MedGen UID encontrado: {medgen_uid}. Doença atualizada.")
        else:
            print(f" - Nenhum MedGen UID encontrado para o nome: {name_to_search}")
            
        time.sleep(0.3)
        
    orm_db.session.commit()
    print("\nMapeamento de MedGen UIDs concluído com sucesso!")


def run_map_genes(orm_db, disease_id=None):
    """
    Executa a segunda fase do ETL: mapeia o MedGen UID para genes associados.
    """
    
    print("Iniciando mapeamento de genes no NCBI...")
    
    # 1. Consulta: Seleciona doenças que têm MedGen UID
    query = select(Disease.id_disease, Disease.medgen_uid).filter(Disease.medgen_uid.isnot(None))
    if disease_id:
        query = query.filter(Disease.id_disease == disease_id)

    diseases = orm_db.session.execute(query).all()
    
    if not diseases:
        print("Nenhuma doença encontrada com MedGen UID válido.")
        return

    # 2. Iteração e Mapeamento de Genes
    for id_disease, medgen_uid in diseases:
        medgen_uid = medgen_uid
        print(f"\nProcessando Doença ID {id_disease} (MedGen UID: {medgen_uid})")
        
        # Filtra automaticamente por TaxID 9606 (humano)
        ncbi_gene_ids = search_gene_ids_by_medgen(medgen_uid)
        
        if not ncbi_gene_ids:
            print(f"Nenhum GeneID humano encontrado.")
            time.sleep(0.5)
            continue
            
        gene_details_list = fetch_gene_details(ncbi_gene_ids)
        
        for detail in gene_details_list:
            # Usa a função auxiliar com extração robusta do UID
            _save_gene_and_association(orm_db, detail, id_disease)
            
        orm_db.session.commit() # Commit final das associações para esta doença
        time.sleep(0.5)
        
    print("\nMapeamento de Genes concluído com sucesso!")