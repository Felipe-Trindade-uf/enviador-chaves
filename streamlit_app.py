import streamlit as st
import pandas as pd
import io

# Configuração da página web
st.set_page_config(page_title="Enviador de relatórios de chaves", layout="centered")
st.title("Enviador de relatórios de chaves")
st.write("Selecione as células no Excel, tendo certeza de começar logo pela primeira coluna e terminar com uma coluna que é vazia nas chaves faltantes (recomendo a do horário de entrega).","\n Então copie (Ctrl+C) e cole na caixa abaixo.","\nPor fim aberte ctrl+Enter.\n\n")

# 1. Área de Texto para colar os dados do Excel
dados_colados = st.text_area(
    "Cole as células aqui:", 
    height="content", 
    placeholder="Exemplo:\n01.10.2026\t08:00\tChave12\tJuninho Silva\t111111\tMorador\tJoão\n01.10.2026\t08:10\tChave43\tGalvão Bueno\t122211\tCEO\tJoão"
)

# Só processa se o usuário tiver colado algo
if dados_colados.strip():
    try:
        df = pd.read_csv(io.StringIO(dados_colados), sep="\t", header=None)
        
        # Mostra uma prévia para o usuário ter certeza de que colou certo
        with st.expander("Prévia dos dados", expanded=False):
            st.dataframe(df)

        texto_inicio = 'Boa Noite\nEu, xxx RE: venho através deste e-mail informar que todas as chaves foram entregues, com exceção das:'
        texto_meio = ' que não foram entregues dentro do horário!\n\n'
        for i in range(len(df)):
          if df[9][i] != df[9][i]:
            texto_inicio += f" {df[2][i]},"
            texto_meio += f"Retirada pelo: {df[4][i]}\nHorário da retirada: {df[1][i]}\nChave retirada: {df[2][i]}\nSIAPE/RA/RG: {df[5][i]}\nSetor: {df[6][i]}\nEntregador: {df[7][i]}\nDia: {df[0][i]}\n\n"
        texto_final = texto_inicio + texto_meio

        # --------------------------------------
        
        # 2. Exibição do Resultado
        st.subheader("Email Gerado:")
        st.text_area("Resultado (pronto para copiar):", value=texto_final, height=250)
        st.info("Clique no link abaixo para continuar o processo de enviar o e-mail:")

    except Exception as e:
        st.error(f"Erro ao processar os dados colados. Certifique-se de incluir o cabeçalho (nome das colunas). Detalhes: {e}")
else:
    st.warning("Aguardando você colar os dados para iniciar o processamento.")
