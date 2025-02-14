import streamlit as st
import pandas as pd

# Lista de jogadores pré-cadastrados
tenistas = [
    "Airton Barata", "Augusto Silveira Espíndola", "Bruno Casale", "Carlos Frederico Da Costa",
    "Danilo Alves", "Denilson Montezani", "Emivaldo Feitosa", "Fagner Bantim", "Fernando Lino",
    "Fernando Sales Guedes", "Gustavo Avila", "Italo Araújo", "Jalmir Moreno Fernandes",
    "João Paulo Sampaio Rezende", "Joel Pereira Silva", "José Humberto Silva Junior", "Júnior Neres",
    "Luiz da Trindade Soares Júnior", "Lupesse Santana", "Mateus Moury", "Matheus Costa Silva",
    "Matheus Mesquita", "Maximiliano Moura Costa", "Paulo Pedrosa", "Rhuan Teixeira", "Sandro Mesquita",
    "Sidney Santos", "Victtor Barbosa", "Vinicius Paiva", "Thiago Pinho", "Walter L", "Walmir Irineu",
    "Warwick Melo", "Willian F", "Wilson"
]

# Função para calcular o vencedor de um set (3 games, com diferença de 2)
def calcular_vencedor_set(games_jogador1, games_jogador2, pontos_tiebreak_jogador1=None, pontos_tiebreak_jogador2=None):
    if games_jogador1 >= 3 and games_jogador1 >= games_jogador2 + 2:
        return "Jogador 1"
    elif games_jogador2 >= 3 and games_jogador2 >= games_jogador1 + 2:
        return "Jogador 2"
    elif games_jogador1 == 3 and games_jogador2 == 3:
        if pontos_tiebreak_jogador1 is not None and pontos_tiebreak_jogador2 is not None:
            if pontos_tiebreak_jogador1 > pontos_tiebreak_jogador2:
                return "Jogador 1"
            else:
                return "Jogador 2"
        return "Tiebreak"
    return None

# Função para calcular o vencedor de um supertiebreak (10 pontos, com diferença de 2)
def calcular_vencedor_supertiebreak(pontos_jogador1, pontos_jogador2):
    if pontos_jogador1 >= 10 and pontos_jogador1 >= pontos_jogador2 + 2:
        return "Jogador 1"
    elif pontos_jogador2 >= 10 and pontos_jogador2 >= pontos_jogador1 + 2:
        return "Jogador 2"
    return None

# Função para atualizar a tabela de estatísticas
def atualizar_estatisticas(classe, grupo, jogador, vitoria, derrota, sets, games, saldo_tiebreaks, pontos):
    if classe not in st.session_state.estatisticas:
        st.session_state.estatisticas[classe] = {}
    if grupo not in st.session_state.estatisticas[classe]:
        st.session_state.estatisticas[classe][grupo] = {}
    if jogador not in st.session_state.estatisticas[classe][grupo]:
        st.session_state.estatisticas[classe][grupo][jogador] = {
            "Jogos": 0, "Vitórias": 0, "Derrotas": 0, "Sets": 0, "Games": 0, "Tiebreaks": 0, "Pontos": 0
        }
    st.session_state.estatisticas[classe][grupo][jogador]["Jogos"] += 1
    st.session_state.estatisticas[classe][grupo][jogador]["Vitórias"] += vitoria
    st.session_state.estatisticas[classe][grupo][jogador]["Derrotas"] += derrota
    st.session_state.estatisticas[classe][grupo][jogador]["Sets"] += sets
    st.session_state.estatisticas[classe][grupo][jogador]["Games"] += games
    st.session_state.estatisticas[classe][grupo][jogador]["Tiebreaks"] += saldo_tiebreaks
    st.session_state.estatisticas[classe][grupo][jogador]["Pontos"] += pontos

# Função para processar o resultado de uma partida
def processar_resultado(resultado):
    sets = resultado.split()
    placares = []
    for s in sets:
        if '(' in s:  # Verifica se há tiebreak
            games, tiebreak = s.split('(')
            tiebreak = tiebreak.replace(')', '')
            try:
                game_scores = games.split('/')
                tiebreak_scores = tiebreak.split('/')
                placares.append((int(game_scores[0]), int(game_scores[1]), int(tiebreak_scores[0]), int(tiebreak_scores[1])))
            except (IndexError, ValueError):
                placares.append((None, None, None, None))
        else:
            try:
                game_scores = s.split('/')
                placares.append((int(game_scores[0]), int(game_scores[1]), None, None))
            except (IndexError, ValueError):
                placares.append((None, None, None, None))
    return placares

# Função para carregar e processar os dados do Excel
def carregar_e_processar_excel(uploaded_file):
    df = pd.read_excel(uploaded_file, sheet_name="Jogos")
    df_concluidas = df[df["STATUS"] == "Concluída"]
    
    for _, row in df_concluidas.iterrows():
        classe = row["CATEGORIA"]
        grupo = row["FASE"].split(" - ")[1]  # Extrair o grupo (ex: G1, G2)
        jogador1 = row["JOGADOR(ES) 01"]
        jogador2 = row["JOGADOR(ES) 02"]
        resultado = row["RESULTADO"]
        vencedor = row["VENCEDOR(ES)"]
        
        placares = processar_resultado(resultado)
        
        if vencedor == jogador1:
            vitoria_jogador1, vitoria_jogador2 = 1, 0
        else:
            vitoria_jogador1, vitoria_jogador2 = 0, 1
        
        sets_jogador1 = 0
        sets_jogador2 = 0
        games_jogador1 = 0
        games_jogador2 = 0
        saldo_tiebreaks_jogador1 = 0
        saldo_tiebreaks_jogador2 = 0
        
        for placar in placares:
            if placar[0] is not None and placar[1] is not None:
                games_jogador1 += int(placar[0])
                games_jogador2 += int(placar[1])
            
            if placar[2] is not None and placar[3] is not None:  # Se houve tiebreak
                if placar[2] > placar[3]:
                    saldo_tiebreaks_jogador1 += 1
                    saldo_tiebreaks_jogador2 -= 1
                else:
                    saldo_tiebreaks_jogador1 -= 1
                    saldo_tiebreaks_jogador2 += 1

        pontos_vitoria = 0  # Valor padrão

        if classe == "B":
            pontos_vitoria = 30
        elif classe == "C":
            pontos_vitoria = 15
        elif classe == "D":
            pontos_vitoria = 8
        
        atualizar_estatisticas(classe, grupo, jogador1, vitoria_jogador1, vitoria_jogador2, sets_jogador1, games_jogador1, saldo_tiebreaks_jogador1, pontos_vitoria if vencedor == jogador1 else 0)
        atualizar_estatisticas(classe, grupo, jogador2, vitoria_jogador2, vitoria_jogador1, sets_jogador2, games_jogador2, saldo_tiebreaks_jogador2, pontos_vitoria if vencedor == jogador2 else 0)

# Inicialização do Session State
if "estatisticas" not in st.session_state:
    st.session_state.estatisticas = {}
if "partidas" not in st.session_state:
    st.session_state.partidas = []

# Interface do Streamlit
st.title("Registro de Resultados de Tênis")

# Carregar a planilha Excel
uploaded_file = st.file_uploader("Carregar planilha Excel", type=["xlsx"])
if uploaded_file:
    carregar_e_processar_excel(uploaded_file)
    st.success("Dados do Excel carregados e processados com sucesso!")

# Exibição das tabelas por classe e grupo
st.header("Estatísticas por Classe e Grupo")

# Ordenar as classes em ordem alfabética
classes_ordenadas = sorted(st.session_state.estatisticas.keys())

for classe in classes_ordenadas:
    st.subheader(f"Classe {classe}")
    
def ordenar_grupos(nome_grupo):
    if nome_grupo == "Fase Final":
        return float('inf')  # Coloca "Fase Final" por último
    elif nome_grupo == "Grupo A":
        return 0  # Coloca "Grupo A" no início (ou em uma posição específica)
    else:
        try:
            return int(nome_grupo.split()[-1])
        except ValueError:
            return nome_grupo  # Ordena alfabeticamente se não for um número

    grupos_ordenados = sorted(st.session_state.estatisticas[classe].keys(), key=ordenar_grupos)
    
    for grupo in grupos_ordenados:
        st.write(f"**Grupo {grupo}**")
        
        # Obter os dados do grupo
        dados_grupo = st.session_state.estatisticas[classe][grupo]
        
        # Converter para DataFrame e ordenar os jogadores em ordem alfabética
        df_grupo = pd.DataFrame.from_dict(dados_grupo, orient='index')
        df_grupo = df_grupo.reset_index().rename(columns={'index': 'Jogador'})
        df_grupo = df_grupo.sort_values(by="Jogador")  # Ordenar por nome do jogador
        
        # Exibir a tabela
        st.dataframe(df_grupo)
