# Importa a biblioteca Entrez da Biopython para acessar a base de dados da NCBI
from Bio import Entrez
import time

# Importa função personalizada para obter conexão com o banco de dados local
from backend.db import get_connection

# Define o e-mail obrigatório para uso da API Entrez (usado para controle e contato em caso de abuso)
Entrez.email = "brunamichelecr@gmail.com"

def fetch_mesh_info(disease_name):
    """
    Busca informações MeSH (Medical Subject Headings) para uma doença específica.
    
    Parâmetros:
        disease_name (str): Nome da doença a ser pesquisada.
    
    Retorna:
        dict: Contém o ID MeSH, descrição e sinônimos da doença.
        None: Se não encontrar resultados ou ocorrer erro.
    """
    try:
        # Realiza busca na base MeSH usando o nome da doença como termo
        search_handle = Entrez.esearch(db="mesh", term=f"{disease_name}[MeSH Terms]")
        search_results = Entrez.read(search_handle)
        search_handle.close()

        # Verifica se houve resultados; se não, retorna None
        if not search_results["IdList"]:
            return None

        # Extrai o primeiro ID MeSH encontrado
        mesh_id = str(search_results["IdList"][0])

        # Busca o resumo (descrição e sinônimos) do termo MeSH
        summary_handle = Entrez.esummary(db="mesh", id=mesh_id)
        summary_results = Entrez.read(summary_handle)
        summary_handle.close()

        # Extrai a descrição e os sinônimos (se existirem)
        description = summary_results[0].get("DS_ScopeNote", "")
        synonyms = summary_results[0].get("DS_MeshTerms", [])

        # Retorna os dados estruturados
        return {
            "mesh_id": mesh_id,
            "description": description,
            "synonym": ";".join(synonyms)  # Junta os sinônimos em uma única string separada por ponto e vírgula
        }

    except Exception as e:
        # Log de erro para facilitar depuração
        print(f"Erro ao buscar MeSH para '{disease_name}': {e}")
        return None

def update_disease_info():
    """
    Atualiza a tabela 'diseases' no banco de dados com informações MeSH:
    descrição, ID MeSH e sinônimos.
    """
    # Conecta ao banco de dados
    conn = get_connection()
    cur = conn.cursor()

    # Seleciona todos os nomes de doenças da tabela
    cur.execute("SELECT disease_name FROM diseases")
    rows = cur.fetchall()

    # Itera sobre cada doença e atualiza com dados MeSH
    for row in rows:
        disease_name = row[0]
        info = fetch_mesh_info(disease_name)

        # Exibe progresso no terminal
        print(f"🔍 {disease_name} → {info}")

        if info:
            # Atualiza os campos da doença com os dados obtidos
            cur.execute("""
                UPDATE diseases
                SET disease_desc = %s,
                    mesh_id = %s,
                    disease_synonym = %s
                WHERE disease_name = %s
            """, (
                info["description"],
                info["mesh_id"],
                info["synonym"],
                disease_name
            ))

            print(f"✅ Atualizado: {disease_name}")
        else:
            # Caso não encontre dados MeSH
            print(f"⚠️ Não encontrado: {disease_name}")

        # Pausa entre requisições para evitar sobrecarga na API da NCBI
        time.sleep(0.4)

    # Confirma as alterações no banco
    conn.commit()

    # Encerra conexão com o banco
    cur.close()
    conn.close()

# Executa a função principal ao rodar o script
update_disease_info()