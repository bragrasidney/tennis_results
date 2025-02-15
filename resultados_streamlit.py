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
def atualizar_estatisticas(classe, grupo, jogador, vitoria, derrota, sets_vencidos, sets_perdidos, games_vencidos, games_perdidos, tiebreaks_vencidos, tiebreaks_perdidos, pontos):
    if classe not in st.session_state.estatisticas:
        st.session_state.estatisticas[classe] = {}
    if grupo not in st.session_state.estatisticas[classe]:
        st.session_state.estatisticas[classe][grupo] = {}
    if jogador not in st.session_state.estatisticas[classe][grupo]:
        st.session_state.estatisticas[classe][grupo][jogador] = {
            "Jogos": 0, "Vitórias": 0, "Derrotas": 0, "Sets Vencidos": 0, "Sets Perdidos": 0, "Games Vencidos": 0, "Games Perdidos": 0, "Tiebreaks Vencidos": 0, "Tiebreaks Perdidos": 0, "Pontos": 0
        }
    st.session_state.estatisticas[classe][grupo][jogador]["Jogos"] += 1
    st.session_state.estatisticas[classe][grupo][jogador]["Vitórias"] += vitoria
    st.session_state.estatisticas[classe][grupo][jogador]["Derrotas"] += derrota
    st.session_state.estatisticas[classe][grupo][jogador]["Sets Vencidos"] += sets_vencidos
    st.session_state.estatisticas[classe][grupo][jogador]["Sets Perdidos"] += sets_perdidos
    st.session_state.estatisticas[classe][grupo][jogador]["Games Vencidos"] += games_vencidos
    st.session_state.estatisticas[classe][grupo][jogador]["Games Perdidos"] += games_perdidos
    st.session_state.estatisticas[classe][grupo][jogador]["Tiebreaks Vencidos"] += tiebreaks_vencidos
    st.session_state.estatisticas[classe][grupo][jogador]["Tiebreaks Perdidos"] += tiebreaks_perdidos
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
        tiebreaks_jogador1 = 0
        tiebreaks_jogador2 = 0
        
        for placar in placares:
            if placar[0] is not None and placar[1] is not None:
                games_jogador1 += int(placar[0])
                games_jogador2 += int(placar[1])
            
            if placar[2] is not None and placar[3] is not None:  # Se houve tiebreak
                if placar[0] == 3 and placar[1] == 3:  # Set decidido por tiebreak
                    if placar[2] > placar[3]:
                        tiebreaks_jogador1 += 1
                        tiebreaks_jogador2 += 0
                        games_jogador1 += 1  # Tiebreak vencido conta como game vencido
                        games_jogador2 += 0  # Tiebreak perdido conta como game perdido
                    else:
                        tiebreaks_jogador1 += 0
                        tiebreaks_jogador2 += 1
                        games_jogador1 += 0  # Tiebreak perdido conta como game perdido
                        games_jogador2 += 1  # Tiebreak vencido conta como game vencido

        # Contabilizar sets vencidos e perdidos
        sets_jogador1 = sum(1 for placar in placares if placar[0] is not None and placar[1] is not None and placar[0] > placar[1])
        sets_jogador2 = sum(1 for placar in placares if placar[0] is not None and placar[1] is not None and placar[1] > placar[0])

        pontos_vitoria = 0  # Valor padrão

        if classe == "B":
            pontos_vitoria = 30
        elif classe == "C":
            pontos_vitoria = 15
        elif classe == "D":
            pontos_vitoria = 8
        
        atualizar_estatisticas(classe, grupo, jogador1, vitoria_jogador1, vitoria_jogador2, sets_jogador1, len(placares) - sets_jogador1, games_jogador1, games_jogador2, tiebreaks_jogador1, tiebreaks_jogador2, pontos_vitoria if vencedor == jogador1 else 0)
        atualizar_estatisticas(classe, grupo, jogador2, vitoria_jogador2, vitoria_jogador1, sets_jogador2, len(placares) - sets_jogador2, games_jogador2, games_jogador1, tiebreaks_jogador2, tiebreaks_jogador1, pontos_vitoria if vencedor == jogador2 else 0)

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
    
    # Função para ordenar os grupos
    def ordenar_grupos(nome_grupo):
        if nome_grupo == "Fase Final":
            return float('inf')  # Coloca "Fase Final" por último
        elif nome_grupo == "Grupo A":
            return 0  # Coloca "Grupo A" no início (ou em uma posição específica)
        else:
            try:
                return int(nome_grupo.split()[-1])  # Ordena por número do grupo
            except ValueError:
                return nome_grupo  # Ordena alfabeticamente se não for um número
    
    # Ordenar os grupos
    grupos_ordenados = sorted(st.session_state.estatisticas[classe].keys(), key=ordenar_grupos)
    
    for grupo in grupos_ordenados:
        st.write(f"**Grupo {grupo}**")
        
        # Obter os dados do grupo
        dados_grupo = st.session_state.estatisticas[classe][grupo]
        
        # Converter para DataFrame
        df_grupo = pd.DataFrame.from_dict(dados_grupo, orient='index')
        df_grupo = df_grupo.reset_index().rename(columns={'index': 'Jogador'})
        
        # Calcular saldos
        df_grupo["Saldo de Sets"] = df_grupo["Sets Vencidos"] - df_grupo["Sets Perdidos"]
        df_grupo["Saldo de Games"] = df_grupo["Games Vencidos"] - df_grupo["Games Perdidos"]
        df_grupo["Saldo de Tiebreaks"] = df_grupo["Tiebreaks Vencidos"] - df_grupo["Tiebreaks Perdidos"]
        
        # Ordenar por Vitórias, Saldo de Sets, Saldo de Games e Saldo de Tiebreaks
        df_grupo = df_grupo.sort_values(
            by=["Vitórias", "Saldo de Sets", "Saldo de Games", "Saldo de Tiebreaks"],
            ascending=[False, False, False, False]
        )
        
        # Adicionar coluna de Posição
        df_grupo["Posição"] = range(1, len(df_grupo) + 1)
        
        # Selecionar e reordenar as colunas
        df_grupo = df_grupo[["Posição", "Jogador", "Jogos", "Vitórias", "Derrotas", "Saldo de Sets", "Saldo de Games", "Saldo de Tiebreaks"]]
        
        # Exibir a tabela
        st.dataframe(df_grupo)
