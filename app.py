
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Escala de Mídia - Igreja", layout="wide")

st.markdown(
    '''
    <style>
    .stApp {
        background-color: white;
        color: black;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.title("📅 Escala de Mídia - Igreja")

# Funções
def carregar_programacoes():
    try:
        return pd.read_csv('programacoes.csv')
    except:
        return pd.DataFrame(columns=["ID", "Data", "Programacao", "Categoria", "Descricao", "Status"])

def carregar_escalados():
    try:
        return pd.read_csv('escalados.csv')
    except:
        return pd.DataFrame(columns=["ID Programacao", "Nome", "Data", "Categoria", "Programacao"])

def salvar_programacoes(df):
    df.to_csv('programacoes.csv', index=False)

def salvar_escalado(dados):
    df = carregar_escalados()
    df.loc[len(df)] = dados
    df.to_csv('escalados.csv', index=False)

# Menu
menu = ["Home", "Me Escalar", "Ver Escala", "Dashboard", "Gerenciar Programações"]
escolha = st.sidebar.selectbox("Menu", menu)

if escolha == "Home":
    st.subheader("Bem-vindo à Escala de Mídia da Igreja")

if escolha == "Me Escalar":
    st.subheader("🖊️ Escolher sua Escala")

    categorias = ["Filmagem", "Câmera Fixa", "Fotografia", "Projeção/Telão", "Transmissão/Live", "Iluminação"]
    categoria = st.selectbox("Escolha a Categoria:", categorias)
    nomes = ["Gabriel", "Alex", "Matheus", "Julio Cesar", "Lucas", "Samuel"]
    nome = st.selectbox("Escolha seu nome:", nomes)

    df = carregar_programacoes()
    if not df.empty:
        df = df.sort_values(by="Data")
        programacoes = df["Programacao"] + " - " + df["Categoria"].fillna("") + " (" + df["Data"] + ")"
        selecao = st.selectbox("Escolha a Programação:", programacoes)

        indice = programacoes[programacoes == selecao].index[0]
        programacao = df.loc[indice]

        if st.button("✅ Me Escalar"):
            salvar_escalado([
                str(programacao['ID']),
                nome,
                programacao['Data'],
                programacao['Categoria'],
                programacao['Programacao']
            ])
            st.success(f"{nome} escalado com sucesso! 🎉")
    else:
        st.warning("Nenhuma programação cadastrada.")

if escolha == "Ver Escala":
    st.subheader("👥 Escalados por Programação")

    df = carregar_programacoes()
    escala = carregar_escalados()

    if not df.empty:
        for index, row in df.iterrows():
            cat = row['Categoria'] if pd.notnull(row['Categoria']) else ""
            st.markdown(f"### 📅 {row['Data']} - {row['Programacao']} {('('+cat+')') if cat else ''}")
            pessoas = escala[escala['ID Programacao'].astype(str) == str(row['ID'])]
            nomes = pessoas['Nome'].tolist()

            if nomes:
                st.success(f"👥 Escalados: {', '.join(nomes)}")
            else:
                st.warning("👥 Ninguém escalado ainda.")
    else:
        st.warning("Nenhuma programação cadastrada.")

if escolha == "Dashboard":
    st.subheader("📊 Dashboard de Escalas")

    df_programacoes = carregar_programacoes()
    df_escalados = carregar_escalados()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Escalados", len(df_escalados))
    col2.metric("Total de Programações", len(df_programacoes))
    col3.metric("Total de Categorias", len(["Filmagem", "Câmera Fixa", "Fotografia", "Projeção/Telão", "Transmissão/Live", "Iluminação"]))

if escolha == "Gerenciar Programações":
    st.subheader("🛠️ Gerenciamento de Programações")
    senha = st.text_input("🔐 Digite a senha de admin:", type="password")
    if senha == "123":
        df = carregar_programacoes()

        aba = st.radio("O que deseja fazer?", ["Adicionar Programação", "Editar Programação"])

        if aba == "Adicionar Programação":
            data = st.date_input("Data")
            programacao = st.text_input("Nome da Programação")
            categoria = st.text_input("Categoria (Opcional)")
            descricao = st.text_input("Descrição (Opcional)")

            if st.button("➕ Adicionar Programação"):
                novo_id = str(int(datetime.now().timestamp()))
                nova_linha = {
                    "ID": novo_id,
                    "Data": str(data),
                    "Programacao": programacao,
                    "Categoria": categoria,
                    "Descricao": descricao,
                    "Status": "Aberto"
                }
                df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
                salvar_programacoes(df)
                st.success("Programação adicionada com sucesso!")

        if aba == "Editar Programação":
            st.dataframe(df)
            opcoes = df["ID"].tolist()
            id_programacao = st.selectbox("Selecione o ID da Programação para editar:", opcoes)
            linha = df[df["ID"] == id_programacao].iloc[0]

            nova_data = st.date_input("Nova Data", datetime.strptime(linha["Data"], "%Y-%m-%d"))
            nova_programacao = st.text_input("Novo nome da Programação", linha["Programacao"])

            if st.button("Salvar Alterações"):
                df.loc[df["ID"] == id_programacao, "Data"] = str(nova_data)
                df.loc[df["ID"] == id_programacao, "Programacao"] = nova_programacao
                salvar_programacoes(df)
                st.success("Alterações salvas!")
    else:
        st.warning("Acesso restrito. Digite a senha correta.")
