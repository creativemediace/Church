
import streamlit as st
import pandas as pd
from datetime import datetime
import time
import os

st.set_page_config(page_title="Escala de Mídia - Igreja", layout="wide")

# Modo fixo claro
fundo = "#FFFFFF"
texto = "#111"
borda = "#CCC"
input_bg = "#F9F9F9"

st.markdown(
    f'''
    <style>
    [data-testid="stSidebar"] {{display: none;}}
    html, body, [class*="css"] {{
        font-size: 16px !important;
        background: {fundo};
        color: {texto};
    }}
    @media (max-width: 768px) {{
        html, body, [class*="css"] {{
            font-size: 13px !important;
        }}
    }}
    .topnav {{
        width: 100%;
        text-align: center;
        padding: 0.5rem;
    }}
    .topnav select {{
        padding: 0.4rem 0.8rem;
        font-size: 0.95rem;
        border-radius: 6px;
        border: 1px solid {borda};
        background: {input_bg};
        color: {texto};
        min-width: 200px;
    }}
    h1, h2, h3, h4 {{
        color: {texto};
    }}
    </style>
    ''',
    unsafe_allow_html=True
)

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

def carregar_nomes_extra():
    if os.path.exists("nomes.csv"):
        return pd.read_csv("nomes.csv")
    else:
        return pd.DataFrame(columns=["Categoria", "Nome"])

def salvar_programacoes(df):
    df.to_csv('programacoes.csv', index=False)

def salvar_escalado(dados):
    df = carregar_escalados()
    df.loc[len(df)] = dados
    df.to_csv('escalados.csv', index=False)

def salvar_nome_extra(categoria, nome):
    df = carregar_nomes_extra()
    df.loc[len(df)] = [categoria, nome]
    df.to_csv('nomes.csv', index=False)

menu = ["Home", "Ver Escala", "Me Escalar", "Gerenciar Programações"]
st.markdown('<div class="topnav">', unsafe_allow_html=True)
escolha = st.selectbox("", menu, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

if escolha == "Home":
    st.markdown("<h1 style='color:transparent;'> </h1>", unsafe_allow_html=True)
    texto_titulo = "Comunidade da Esperança"
    local = st.empty()
    for i in range(len(texto_titulo) + 1):
        local.markdown(f"<h2 style='color:{texto};'>{texto_titulo[:i]}</h2>", unsafe_allow_html=True)
        time.sleep(0.05)

if escolha == "Me Escalar":
    st.subheader("🖊️ Escolher sua Escala")

    categorias = [
        "🎬 FILMAGEM",
        "📷 CÂMERA FIXA (Live)",
        "📸 FOTOGRAFIA",
        "🖥️ PROJEÇÃO / TELÃO",
        "📡 TRANSMISSÃO / LIVE",
        "🎚️ ILUMINAÇÃO"
    ]
    categoria = st.selectbox("Escolha a Categoria:", categorias)

    nomes_por_categoria = {
        "🎬 FILMAGEM": ["Alex", "Gabriel Dantas", "Julio Cesar", "Matheus"],
        "📷 CÂMERA FIXA (Live)": ["Arthur0f", "Arthur Th", "Gabriel Dantas", "Julio Cesar", "Juninho", "Lucas Brasileiro", "Lucas", "Nilo", "Samuel Santiago", "Wesley Cardoso", "Ryan", "Matheus", "Alexandre Neto"],
        "📸 FOTOGRAFIA": ["Arthur0f", "Arthur Th", "Daniel", "Gabriel Rodrigues", "Hêloa", "Leticia Alcântara", "Lucas Brasileiro", "Samuel Santiago", "Brendoca"],
        "🖥️ PROJEÇÃO / TELÃO": ["Dayanne", "Hévelin", "Juninho", "Lucas", "Marina", "Ana Júlia", "Wesley Cardoso", "Lucas Almeida", "Matheus TI", "Alexandre Neto"],
        "📡 TRANSMISSÃO / LIVE": ["Dayanne", "Eliseu", "Luana Monteiro", "Minela", "Indy Leticia", "Erynaldo", "Matheus TI"],
        "🎚️ ILUMINAÇÃO": ["Dayanne", "Rafael", "Samyr"]
    }

    nomes_extra = carregar_nomes_extra()
    nomes_adicionais = nomes_extra[nomes_extra["Categoria"] == categoria]["Nome"].tolist()
    nomes = sorted(list(set(nomes_por_categoria.get(categoria, []) + nomes_adicionais)))

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
                categoria,
                programacao['Programacao']
            ])
            st.success(f"{nome} escalado com sucesso! 🎉")
    else:
        st.warning("Nenhuma programação cadastrada.")

    st.subheader("➕ Cadastrar Novo Integrante")
    cat_novo = st.selectbox("Escolha a Categoria para o novo integrante:", categorias)
    nome_novo = st.text_input("Digite o nome do novo integrante:")

    if st.button("Adicionar Novo Integrante"):
        if nome_novo.strip() != "":
            salvar_nome_extra(cat_novo, nome_novo.strip())
            st.success(f"{nome_novo} adicionado com sucesso à categoria {cat_novo}!")
        else:
            st.warning("Digite um nome válido.")

if escolha == "Ver Escala":
    st.subheader("👥 Escalados por Programação")

    df = carregar_programacoes()
    escala = carregar_escalados()

    if not df.empty:
        datas_unicas = df["Data"].unique().tolist()
        datas_unicas.insert(0, "Todas")

        programacoes_unicas = df["Programacao"].unique().tolist()
        programacoes_unicas.insert(0, "Todas")

        filtro_data = st.selectbox("Filtrar por Data:", datas_unicas)
        filtro_prog = st.selectbox("Filtrar por Programação:", programacoes_unicas)

        df_filtrado = df.copy()
        if filtro_data != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Data"] == filtro_data]
        if filtro_prog != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Programacao"] == filtro_prog]

        for index, row in df_filtrado.iterrows():
            cat = row['Categoria'] if pd.notnull(row['Categoria']) else ""
            st.markdown(f"### 📅 {row['Data']} - {row['Programacao']} {('('+cat+')') if cat else ''}")
            pessoas = escala[escala['ID Programacao'].astype(str) == str(row['ID'])]

            if not pessoas.empty:
                nomes_formatados = [f"{n} ({pessoas.iloc[i]['Categoria']})" for i, n in enumerate(pessoas['Nome'])]
                st.success(f"👥 Escalados: {', '.join(nomes_formatados)}")
            else:
                st.warning("👥 Ninguém escalado ainda.")
    else:
        st.warning("Nenhuma programação cadastrada.")

if escolha == "Gerenciar Programações":
    st.subheader("🛠️ Gerenciamento de Programações")
    senha = st.text_input("🔐 Digite a senha de admin:", type="password")
    if senha == "123":
        df = carregar_programacoes()

        aba = st.radio(
            "O que deseja fazer?",
            ["Adicionar Programação", "Excluir Programação"]
        )

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

        if aba == "Excluir Programação":
            st.dataframe(df)
            opcoes = df["ID"].tolist()
            id_programacao = st.selectbox("Selecione o ID da Programação para excluir:", opcoes)

            if st.button("❌ Excluir Programação"):
                df = df[df["ID"] != id_programacao]
                salvar_programacoes(df)
                st.success("Programação excluída com sucesso!")

    else:
        st.warning("Acesso restrito. Digite a senha correta.")
