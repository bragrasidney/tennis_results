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

# Função para calcular o vencedor de um set
def calcular_vencedor_set(games_jogador1, games_jogador2, pontos_tiebreak_jogador1=None, pontos_tiebreak_jogador2=None):
    if games_jogador1 >= 6 and games_jogador1 >= games_jogador2 + 2:
        return "Jogador 1"
    elif games_jogador2 >= 6 and games_jogador2 >= games_jogador1 + 2:
        return "Jogador 2"
    elif games_jogador1 == 6 and games_jogador2 == 6:
        if pontos_tiebreak_jogador1 is not None and pontos_tiebreak_jogador2 is not None:
            if pontos_tiebreak_jogador1 > pontos_tiebreak_jogador2:
                return "Jogador 1"
            else:
                return "Jogador 2"
        return "Tiebreak"
    return None

# Função para calcular o vencedor de um supertiebreak
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

# Função para reverter as estatísticas de uma partida
def reverter_estatisticas(classe, grupo, jogador1, jogador2, vencedor, games_jogador1, games_jogador2, saldo_tiebreaks, pontos_vitoria):
    if vencedor == jogador1:
        st.session_state.estatisticas[classe][grupo][jogador1]["Vitórias"] -= 1
        st.session_state.estatisticas[classe][grupo][jogador2]["Derrotas"] -= 1
    else:
        st.session_state.estatisticas[classe][grupo][jogador2]["Vitórias"] -= 1
        st.session_state.estatisticas[classe][grupo][jogador1]["Derrotas"] -= 1
    st.session_state.estatisticas[classe][grupo][jogador1]["Jogos"] -= 1
    st.session_state.estatisticas[classe][grupo][jogador2]["Jogos"] -= 1
    st.session_state.estatisticas[classe][grupo][jogador1]["Sets"] -= 2 if vencedor == jogador1 else 0
    st.session_state.estatisticas[classe][grupo][jogador2]["Sets"] -= 2 if vencedor == jogador2 else 0
    st.session_state.estatisticas[classe][grupo][jogador1]["Games"] -= games_jogador1
    st.session_state.estatisticas[classe][grupo][jogador2]["Games"] -= games_jogador2
    st.session_state.estatisticas[classe][grupo][jogador1]["Tiebreaks"] -= saldo_tiebreaks if vencedor == jogador1 else 0
    st.session_state.estatisticas[classe][grupo][jogador2]["Tiebreaks"] -= saldo_tiebreaks if vencedor == jogador2 else 0
    st.session_state.estatisticas[classe][grupo][jogador1]["Pontos"] -= pontos_vitoria if vencedor == jogador1 else 0
    st.session_state.estatisticas[classe][grupo][jogador2]["Pontos"] -= pontos_vitoria if vencedor == jogador2 else 0

# Inicialização do Session State
if "estatisticas" not in st.session_state:
    st.session_state.estatisticas = {}
if "partidas" not in st.session_state:
    st.session_state.partidas = []

# Interface do Streamlit
st.title("Registro de Resultados de Tênis")

# Seleção de classe e grupo
classe = st.selectbox("Selecione a Classe", ["B", "C", "D"])
grupo = st.selectbox("Selecione o Grupo", ["Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4"])

# Seleção de jogadores
st.header("Selecionar Jogadores")
jogador1 = st.selectbox("Jogador 1", tenistas)
jogador2 = st.selectbox("Jogador 2", tenistas)

# Verificar se os jogadores são iguais
if jogador1 == jogador2:
    st.error("Os jogadores devem ser diferentes. Por favor, selecione jogadores distintos.")

# Entrada de resultados
st.header("Registrar Resultados")
st.subheader("Primeiro Set")
games_jogador1_set1 = st.number_input("Games do Jogador 1 - Set 1", min_value=0, max_value=4, value=0)
games_jogador2_set1 = st.number_input("Games do Jogador 2 - Set 1", min_value=0, max_value=4, value=0)

# Verifica se é necessário um tiebreak no primeiro set
if games_jogador1_set1 >= 3 and games_jogador2_set1 >= 3:
    st.subheader("Tiebreak do Primeiro Set")
    pontos_tiebreak_jogador1_set1 = st.number_input("Pontos do Jogador 1 - Tiebreak Set 1", min_value=0, max_value=20, value=0)
    pontos_tiebreak_jogador2_set1 = st.number_input("Pontos do Jogador 2 - Tiebreak Set 1", min_value=0, max_value=20, value=0)
else:
    pontos_tiebreak_jogador1_set1 = None
    pontos_tiebreak_jogador2_set1 = None

st.subheader("Segundo Set")
games_jogador1_set2 = st.number_input("Games do Jogador 1 - Set 2", min_value=0, max_value=4, value=0)
games_jogador2_set2 = st.number_input("Games do Jogador 2 - Set 2", min_value=0, max_value=4, value=0)

# Verifica se é necessário um tiebreak no segundo set
if games_jogador1_set2 >= 3 and games_jogador2_set2 >= 3:
    st.subheader("Tiebreak do Segundo Set")
    pontos_tiebreak_jogador1_set2 = st.number_input("Pontos do Jogador 1 - Tiebreak Set 2", min_value=0, max_value=20, value=0)
    pontos_tiebreak_jogador2_set2 = st.number_input("Pontos do Jogador 2 - Tiebreak Set 2", min_value=0, max_value=20, value=0)
else:
    pontos_tiebreak_jogador1_set2 = None
    pontos_tiebreak_jogador2_set2 = None

# Verifica se é necessário um supertiebreak
vencedor_set1 = calcular_vencedor_set(games_jogador1_set1, games_jogador2_set1, pontos_tiebreak_jogador1_set1, pontos_tiebreak_jogador2_set1)
vencedor_set2 = calcular_vencedor_set(games_jogador1_set2, games_jogador2_set2, pontos_tiebreak_jogador1_set2, pontos_tiebreak_jogador2_set2)

if vencedor_set1 != vencedor_set2:
    st.subheader("Supertiebreak (obrigatório devido ao empate nos sets)")
    pontos_jogador1_supertiebreak = st.number_input("Pontos do Jogador 1 - Supertiebreak", min_value=0, max_value=20, value=0)
    pontos_jogador2_supertiebreak = st.number_input("Pontos do Jogador 2 - Supertiebreak", min_value=0, max_value=20, value=0)

# Botão para registrar os resultados
if st.button("Registrar Resultados"):
    if jogador1 == jogador2:
        st.error("Os jogadores devem ser diferentes. Por favor, selecione jogadores distintos.")
    else:
        if vencedor_set1 != vencedor_set2:
            vencedor_supertiebreak = calcular_vencedor_supertiebreak(pontos_jogador1_supertiebreak, pontos_jogador2_supertiebreak)
            if vencedor_supertiebreak == "Jogador 1":
                st.success(f"{jogador1} venceu o supertiebreak e a partida!")
                atualizar_estatisticas(classe, grupo, jogador1, 1, 0, 1, games_jogador1_set1 + games_jogador1_set2, 1, 30 if classe == "B" else 15 if classe == "C" else 8)
                atualizar_estatisticas(classe, grupo, jogador2, 0, 1, 1, games_jogador2_set1 + games_jogador2_set2, -1, 0)
                st.session_state.partidas.append({
                    "Classe": classe,
                    "Grupo": grupo,
                    "Jogador 1": jogador1,
                    "Jogador 2": jogador2,
                    "Vencedor": jogador1,
                    "Games Jogador 1": games_jogador1_set1 + games_jogador1_set2,
                    "Games Jogador 2": games_jogador2_set1 + games_jogador2_set2,
                    "Tiebreaks": 1,
                    "Pontos": 30 if classe == "B" else 15 if classe == "C" else 8
                })
            elif vencedor_supertiebreak == "Jogador 2":
                st.success(f"{jogador2} venceu o supertiebreak e a partida!")
                atualizar_estatisticas(classe, grupo, jogador2, 1, 0, 1, games_jogador2_set1 + games_jogador2_set2, 1, 30 if classe == "B" else 15 if classe == "C" else 8)
                atualizar_estatisticas(classe, grupo, jogador1, 0, 1, 1, games_jogador1_set1 + games_jogador1_set2, -1, 0)
                st.session_state.partidas.append({
                    "Classe": classe,
                    "Grupo": grupo,
                    "Jogador 1": jogador1,
                    "Jogador 2": jogador2,
                    "Vencedor": jogador2,
                    "Games Jogador 1": games_jogador1_set1 + games_jogador1_set2,
                    "Games Jogador 2": games_jogador2_set1 + games_jogador2_set2,
                    "Tiebreaks": 1,
                    "Pontos": 30 if classe == "B" else 15 if classe == "C" else 8
                })
            else:
                st.error("Supertiebreak ainda em andamento ou inválido.")
        else:
            if vencedor_set1 == "Jogador 1" and vencedor_set2 == "Jogador 1":
                st.success(f"{jogador1} venceu a partida!")
                atualizar_estatisticas(classe, grupo, jogador1, 1, 0, 2, games_jogador1_set1 + games_jogador1_set2, 0, 30 if classe == "B" else 15 if classe == "C" else 8)
                atualizar_estatisticas(classe, grupo, jogador2, 0, 1, 0, games_jogador2_set1 + games_jogador2_set2, 0, 0)
                st.session_state.partidas.append({
                    "Classe": classe,
                    "Grupo": grupo,
                    "Jogador 1": jogador1,
                    "Jogador 2": jogador2,
                    "Vencedor": jogador1,
                    "Games Jogador 1": games_jogador1_set1 + games_jogador1_set2,
                    "Games Jogador 2": games_jogador2_set1 + games_jogador2_set2,
                    "Tiebreaks": 0,
                    "Pontos": 30 if classe == "B" else 15 if classe == "C" else 8
                })
            elif vencedor_set1 == "Jogador 2" and vencedor_set2 == "Jogador 2":
                st.success(f"{jogador2} venceu a partida!")
                atualizar_estatisticas(classe, grupo, jogador2, 1, 0, 2, games_jogador2_set1 + games_jogador2_set2, 0, 30 if classe == "B" else 15 if classe == "C" else 8)
                atualizar_estatisticas(classe, grupo, jogador1, 0, 1, 0, games_jogador1_set1 + games_jogador1_set2, 0, 0)
                st.session_state.partidas.append({
                    "Classe": classe,
                    "Grupo": grupo,
                    "Jogador 1": jogador1,
                    "Jogador 2": jogador2,
                    "Vencedor": jogador2,
                    "Games Jogador 1": games_jogador1_set1 + games_jogador1_set2,
                    "Games Jogador 2": games_jogador2_set1 + games_jogador2_set2,
                    "Tiebreaks": 0,
                    "Pontos": 30 if classe == "B" else 15 if classe == "C" else 8
                })
            else:
                st.error("Partida ainda em andamento ou inválida.")

# Exibir partidas registradas
st.header("Partidas Registradas")
if st.session_state.partidas:
    df_partidas = pd.DataFrame(st.session_state.partidas)
    st.dataframe(df_partidas)

    # Selecionar partida para exclusão
    partida_para_excluir = st.selectbox("Selecione uma partida para excluir", df_partidas.index)
    if st.button("Excluir Partida"):
        partida = st.session_state.partidas.pop(partida_para_excluir)
        reverter_estatisticas(
            partida["Classe"], partida["Grupo"], partida["Jogador 1"], partida["Jogador 2"],
            partida["Vencedor"], partida["Games Jogador 1"], partida["Games Jogador 2"],
            partida["Tiebreaks"], partida["Pontos"]
        )
        st.success(f"Partida entre {partida['Jogador 1']} e {partida['Jogador 2']} excluída com sucesso!")
else:
    st.write("Nenhuma partida registrada ainda.")

# Exibição das tabelas por classe e grupo
st.header("Estatísticas por Classe e Grupo")

# Ordenar as classes em ordem alfabética
classes_ordenadas = sorted(st.session_state.estatisticas.keys())

for classe in classes_ordenadas:
    st.subheader(f"Classe {classe}")
    
    # Ordenar os grupos em ordem numérica
    grupos_ordenados = sorted(st.session_state.estatisticas[classe].keys(), key=lambda x: int(x.split()[-1]))
    
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

# Exportar estatísticas para Excel
if st.button("Exportar Estatísticas para Excel"):
    df_export = pd.concat([
        pd.DataFrame(st.session_state.estatisticas[classe][grupo]).assign(Classe=classe, Grupo=grupo)
        for classe in st.session_state.estatisticas
        for grupo in st.session_state.estatisticas[classe]
    ])
    df_export.to_excel("estatisticas_tenis.xlsx", index=False)
    st.success("Estatísticas exportadas para 'estatisticas_tenis.xlsx'.")
