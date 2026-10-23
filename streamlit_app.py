import streamlit as st
import pandas as pd
import urllib.parse
import io
from datetime import datetime,timezone,timedelta

# Configuração da página web
st.set_page_config(page_title="Enviador de relatórios de chaves", layout="centered")
st.title("Enviador de relatórios de chaves")
st.write("Selecione as células no Excel, tendo certeza de começar logo pela primeira coluna relevante e incluir ao menos uma coluna que é vazia nas chaves faltantes (recomendo a do horário de entrega).")
st.write("\n Então copie (Ctrl+C) e cole na caixa abaixo.")
st.write("\nPor fim aperte ctrl+Enter (ou clique fora da caixa).\n\n")

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
        with st.expander("Definir colunas", expanded=False):
            st.write("Definir em qual coluna está a informação desejada. Se precisar, use a prévia acima para referência!")
            st.write("Obs: A coluna “Entregue” deve ficar em branco caso a chave não tenha sido entregue.")
            NOME = st.number_input("Entregador", min_value=0, value= 4, width= 200)
            HORARIO = st.number_input("Horário", min_value=0, value= 1, width= 200)
            CHAVE = st.number_input("Chave", min_value=0, value= 2, width= 200)
            MATRICULA = st.number_input("Matricula", min_value=0, value= 5, width= 200)
            SETOR = st.number_input("Setor", min_value=0, value= 6, width= 200)
            ENTREGADOR = st.number_input("Entregador", min_value=0, value= 7, width= 200)
            DIA = st.number_input("Dia", min_value=0, value= 0, width= 200)
            FOI_ENTREGUE = st.number_input("Entregue", min_value=0, value= 9, width= 200)

        singular = 0
        chaves = ''
        chave_atual = ''
        chaves_bloco = ''
        texto_inicio_p = 's:'
        texto_inicio_s = 'Boa Noite.\nEu, xxx RE: venho através deste e-mail informar que todas as chaves foram entregues, com exceção da'
        texto_meio_p = ' que não foram entregues dentro do horário!\n'
        texto_meio_s = ' que não foi entregue dentro do horário!\n'
        for i in range(len(df)):
          if (df[CHAVE][i] == df[CHAVE][i]) and (df[FOI_ENTREGUE][i] != df[FOI_ENTREGUE][i]):
            singular += 1
            if singular == 1:
                pass
            elif singular == 2:
                chaves += f" {chave_atual}"
            else:
                chaves += f", {chave_atual}"
            chave_atual = df[CHAVE][i]
            chaves_bloco += f"\nRetirada pelo: {df[NOME][i]}\nHorário da retirada: {df[HORARIO][i]}\nChave retirada: {df[CHAVE][i]}\nSIAPE/RA/RG: {df[MATRICULA][i]}\nSetor: {df[SETOR][i]}\nEntregador: {df[ENTREGADOR][i]}\nDia: {df[DIA][i]}\n"
        
        if singular >= 2:
            texto_final = texto_inicio_s + texto_inicio_p + chaves + f" e {chave_atual}," + texto_meio_p + chaves_bloco
        else:
            texto_final = texto_inicio_s + f" {chave_atual}" + texto_meio_s + chaves_bloco
        

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
    except KeyError as e:
            st.error(f"Tenha certeza que a coluna “Entregue” está dentro do intervalo.\n Atualmente ela está marcada como coluna {e}, e sua tabela vai até a coluna {len(df[0])}.")
        
    except Exception as e:
            st.error(f"Erro ao processar os dados colados. Detalhes: {e}")
else:
    st.warning("Aguardando você colar os dados para iniciar o processamento.")
