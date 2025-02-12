import streamlit as st
import pandas as pd

# Função para calcular o vencedor de um set
def calcular_vencedor_set(games_jogador1, games_jogador2):
    if games_jogador1 >= 4 and games_jogador1 >= games_jogador2 + 2:
        return "Jogador 1"
    elif games_jogador2 >= 4 and games_jogador2 >= games_jogador1 + 2:
        return "Jogador 2"
    elif games_jogador1 == 6 and games_jogador2 == 6:
        return "Tiebreak"
    return None

# Função para calcular o vencedor de um tiebreak
def calcular_vencedor_tiebreak(pontos_jogador1, pontos_jogador2):
    if pontos_jogador1 >= 7 and pontos_jogador1 >= pontos_jogador2 + 2:
        return "Jogador 1"
    elif pontos_jogador2 >= 7 and pontos_jogador2 >= pontos_jogador1 + 2:
        return "Jogador 2"
    return None

# Função para calcular o vencedor de um supertiebreak
def calcular_vencedor_supertiebreak(pontos_jogador1, pontos_jogador2):
    if pontos_jogador1 >= 10 and pontos_jogador1 >= pontos_jogador2 + 2:
        return "Jogador 1"
    elif pontos_jogador2 >= 10 and pontos_jogador2 >= pontos_jogador1 + 2:
        return "Jogador 2"
    return None

# Função para atualizar a tabela de estatísticas
def atualizar_estatisticas(jogador, vitoria, derrota, sets, games, tiebreaks, pontos):
    if jogador not in estatisticas:
        estatisticas[jogador] = {"Jogos": 0, "Vitórias": 0, "Derrotas": 0, "Sets": 0, "Games": 0, "Tiebreaks": 0, "Pontos": 0}
    estatisticas[jogador]["Jogos"] += 1
    estatisticas[jogador]["Vitórias"] += vitoria
    estatisticas[jogador]["Derrotas"] += derrota
    estatisticas[jogador]["Sets"] += sets
    estatisticas[jogador]["Games"] += games
    estatisticas[jogador]["Tiebreaks"] += tiebreaks
    estatisticas[jogador]["Pontos"] += pontos

# Inicialização das estatísticas
estatisticas = {}

# Interface do Streamlit
st.title("Registro de Resultados de Tênis")

# Seleção de classe e grupo
classe = st.selectbox("Selecione a Classe", ["B", "C", "D"])
grupo = st.selectbox("Selecione o Grupo", ["Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4"])

# Entrada de resultados
st.header("Registrar Resultados")
jogador1 = st.text_input("Nome do Jogador 1")
jogador2 = st.text_input("Nome do Jogador 2")

st.subheader("Primeiro Set")
games_jogador1_set1 = st.number_input("Games do Jogador 1 - Set 1", min_value=0, max_value=6, value=0)
games_jogador2_set1 = st.number_input("Games do Jogador 2 - Set 1", min_value=0, max_value=6, value=0)

st.subheader("Segundo Set")
games_jogador1_set2 = st.number_input("Games do Jogador 1 - Set 2", min_value=0, max_value=6, value=0)
games_jogador2_set2 = st.number_input("Games do Jogador 2 - Set 2", min_value=0, max_value=6, value=0)

st.subheader("Supertiebreak (se necessário)")
pontos_jogador1_tiebreak = st.number_input("Pontos do Jogador 1 - Supertiebreak", min_value=0, max_value=20, value=0)
pontos_jogador2_tiebreak = st.number_input("Pontos do Jogador 2 - Supertiebreak", min_value=0, max_value=20, value=0)

# Botão para registrar os resultados
if st.button("Registrar Resultados"):
    vencedor_set1 = calcular_vencedor_set(games_jogador1_set1, games_jogador2_set1)
    vencedor_set2 = calcular_vencedor_set(games_jogador1_set2, games_jogador2_set2)
    
    if vencedor_set1 == "Tiebreak" or vencedor_set2 == "Tiebreak":
        st.warning("Tiebreak no set detectado. Por favor, insira os pontos do tiebreak.")
    
    if vencedor_set1 == vencedor_set2:
        vencedor_supertiebreak = calcular_vencedor_supertiebreak(pontos_jogador1_tiebreak, pontos_jogador2_tiebreak)
        if vencedor_supertiebreak == "Jogador 1":
            st.success(f"{jogador1} venceu o supertiebreak e a partida!")
        elif vencedor_supertiebreak == "Jogador 2":
            st.success(f"{jogador2} venceu o supertiebreak e a partida!")
        else:
            st.error("Supertiebreak ainda em andamento ou inválido.")
    else:
        if vencedor_set1 == "Jogador 1" and vencedor_set2 == "Jogador 1":
            st.success(f"{jogador1} venceu a partida!")
        elif vencedor_set1 == "Jogador 2" and vencedor_set2 == "Jogador 2":
            st.success(f"{jogador2} venceu a partida!")
        else:
            st.error("Partida ainda em andamento ou inválida.")

    # Atualizar estatísticas
    if classe == "B":
        pontos_vitoria = 30
    elif classe == "C":
        pontos_vitoria = 15
    elif classe == "D":
        pontos_vitoria = 8

    if vencedor_set1 == "Jogador 1" and vencedor_set2 == "Jogador 1":
        atualizar_estatisticas(jogador1, 1, 0, 2, games_jogador1_set1 + games_jogador1_set2, 0, pontos_vitoria)
        atualizar_estatisticas(jogador2, 0, 1, 0, games_jogador2_set1 + games_jogador2_set2, 0, 0)
    elif vencedor_set1 == "Jogador 2" and vencedor_set2 == "Jogador 2":
        atualizar_estatisticas(jogador2, 1, 0, 2, games_jogador2_set1 + games_jogador2_set2, 0, pontos_vitoria)
        atualizar_estatisticas(jogador1, 0, 1, 0, games_jogador1_set1 + games_jogador1_set2, 0, 0)
    elif vencedor_set1 == vencedor_set2:
        if vencedor_supertiebreak == "Jogador 1":
            atualizar_estatisticas(jogador1, 1, 0, 1, games_jogador1_set1 + games_jogador1_set2, 1, pontos_vitoria)
            atualizar_estatisticas(jogador2, 0, 1, 1, games_jogador2_set1 + games_jogador2_set2, 1, 0)
        elif vencedor_supertiebreak == "Jogador 2":
            atualizar_estatisticas(jogador2, 1, 0, 1, games_jogador2_set1 + games_jogador2_set2, 1, pontos_vitoria)
            atualizar_estatisticas(jogador1, 0, 1, 1, games_jogador1_set1 + games_jogador1_set2, 1, 0)

# Exibição da tabela de estatísticas
st.header("Estatísticas por Grupo")
df_estatisticas = pd.DataFrame.from_dict(estatisticas, orient='index')
df_estatisticas = df_estatisticas.reset_index().rename(columns={'index': 'Jogador'})
st.dataframe(df_estatisticas)
