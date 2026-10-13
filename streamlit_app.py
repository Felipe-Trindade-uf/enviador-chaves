import streamlit as st
import pandas as pd
import urllib.parse
import io
from datetime import datetime,timezone,timedelta

# Configuração da página web
st.set_page_config(page_title="Enviador de relatórios de chaves", layout="centered")
st.title("Enviador de relatórios de chaves")
st.write("Selecione as células no Excel, tendo certeza de começar logo pela primeira coluna e terminar com uma coluna que é vazia nas chaves faltantes (recomendo a do horário de entrega).")
st.write("\n Então copie (Ctrl+C) e cole na caixa abaixo.")
st.write("\nPor fim aperte ctrl+Enter.\n\n")

# 1. Área de Texto para colar os dados do Excel
dados_colados = st.text_area(
    "Cole as células aqui:", 
    height="content", 
    placeholder="Exemplo:\n01.10.2026\t08:00\tChave12\tJuninho Silva\t111111\tMorador\tJoão\n01.10.2026\t08:10\tChave43\tGalvão Bueno\t122211\tCEO\tJoão"
)

# Só processa se o usuário tiver colado algo
if dados_colados.strip():
    try:

        NOME = 4
        HORARIO = 1
        CHAVE = 2
        MATRICULA = 5
        SETOR = 6
        ENTREGADOR = 7
        DIA = 0
        FOI_ENTREGUE = 9
        
        df = pd.read_csv(io.StringIO(dados_colados), sep="\t", header=None)
        
        # Mostra uma prévia para o usuário ter certeza de que colou certo
        with st.expander("Prévia dos dados", expanded=False):
            st.dataframe(df)

        singular = 0
        chaves = ''
        texto_inicio_p = 's:'
        texto_inicio_s = 'Boa Noite.\nEu, xxx RE: venho através deste e-mail informar que todas as chaves foram entregues, com exceção da'
        texto_meio_p = ' que não foram entregues dentro do horário!\n\n'
        texto_meio_s = ' que não foi entregue dentro do horário!\n\n'
        for i in range(len(df)):
          if df[FOI_ENTREGUE][i] != df[FOI_ENTREGUE][i]:
            singular += 1
            chaves += f" {df[CHAVE][i]},"
            texto_meio += f"Retirada pelo: {df[NOME][i]}\nHorário da retirada: {df[HORARIO][i]}\nChave retirada: {df[CHAVE][i]}\nSIAPE/RA/RG: {df[MATRICULA][i]}\nSetor: {df[SETOR][i]}\nEntregador: {df[ENTREGADOR][i]}\nDia: {df[DIA][i]}\n\n"

        if singular >= 2:
            texto_final = texto_inicio_s + texto_inicio_p + texto_meio_p
        else:
            texto_final = texto_inicio_s + texto_meio_s
        

        # --------------------------------------
        
        # 2. Exibição do Resultado
        st.subheader("Email Gerado:")
        st.text_area("Resultado (pronto para copiar):", value=texto_final, height=250)
        st.info("Clique no link abaixo para continuar o processo de enviar o e-mail:")
        data = datetime.now(timezone(timedelta(hours=-3))).strftime('%d/%m/%y')
        assunto = f"Central de chaves Bloco - X / Dia {data}"
        email_assunto = urllib.parse.quote(assunto)
        email_corpo = urllib.parse.quote(texto_final)
        url_mailto = f"https://mail.google.com/mail/u/0/?fs=1&su={email_assunto}&body={email_corpo}&tf=cm"
        st.link_button("Ir para Gmail",url_mailto)

    except Exception as e:
        st.error(f"Erro ao processar os dados colados. Detalhes: {e}")
else:
    st.warning("Aguardando você colar os dados para iniciar o processamento.")
