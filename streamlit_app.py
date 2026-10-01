import streamlit as st
import pandas as pd
import io

# Configuração da página web
st.set_page_config(page_title="Processador Rápido de Planilhas", layout="centered")
st.title("📋 Copiar & Colar do Excel")
st.write("Selecione as células no Excel, copie (Ctrl+C) e cole na caixa abaixo.")

# 1. Área de Texto para colar os dados do Excel
dados_colados = st.text_area(
    "Cole as células do Excel aqui:", 
    height=200, 
    placeholder="Exemplo:\nColuna1\tColuna2\nDado1\tDado2"
)

# Só processa se o usuário tiver colado algo
if dados_colados.strip():
    try:
        # O Excel separa colunas por TAB (\t). O StringIO simula um arquivo de texto na memória.
        df = pd.read_csv(io.StringIO(dados_colados), sep="\t")
        
        # Mostra uma prévia para o usuário ter certeza de que colou certo
        with st.expander("🔍 Prévia dos dados identificados", expanded=False):
            st.dataframe(df)
            
        # --- SEU CÓDIGO DO COLAB ENTRA AQUI ---
        linhas_em_branco = []
        linhas = tabela.split('\n')

        for i, linha in enumerate(linhas):
            if i == 0 or i == len(linhas) - 1:
                continue
        
            campos = linha.split('\t')
            if campos and not campos[-1].strip():
                linhas_em_branco.append((i + 1, linha))
                if len(campos) > 6:
                  print("Retirada pelo:", campos[4],
                        "\nHorário da retirada:", campos[1],
                        "\nChave retirada:", campos[2],
                        "\nSIAPE/RA/RG:", campos[5],
                        "\nSetor:", campos[6],
                        "\nEntregador:", campos[7],
                        "\nDia:", campos[0],"\n")
        # --------------------------------------
        
        # 2. Exibição do Resultado
        st.subheader("✨ Texto Gerado:")
        st.text_area("Resultado (pronto para copiar):", value=texto_final, height=250)
        
        st.info("💡 Dica: Passe o mouse sobre a caixa de texto acima e clique no ícone de duas folhas no canto superior direito para copiar tudo de uma vez.")

    except Exception as e:
        st.error(f"Erro ao processar os dados colados. Certifique-se de incluir o cabeçalho (nome das colunas). Detalhes: {e}")
else:
    st.warning("Aguardando você colar os dados para iniciar o processamento.")
