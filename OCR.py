import streamlit as st
import ollama
from PIL import Image
import base64

# Configuração inicial da página
st.set_page_config(
    page_title="OCR com Gemma-3",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para carregar e converter imagem do logo em base64
def carregar_logo(path_imagem):
    with open(path_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Exibir título customizado com logo
logo_base64 = carregar_logo("C:/Users/giovana.carmazio/Desktop/gemma3.png")
st.markdown(
    f"""
    <h1><img src="data:image/png;base64,{logo_base64}" width="50" style="vertical-align: -12px;"> OCR Inteligente</h1>
    """,
    unsafe_allow_html=True
)

st.write("Extraia textos de imagens utilizando a tecnologia do modelo **Gemma-3 Vision**.")
st.divider()

# Sidebar com upload e botões
with st.sidebar:
    st.subheader("📤 Envie sua imagem")
    imagem_upada = st.file_uploader("Selecione uma imagem (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

    if imagem_upada:
        st.image(imagem_upada, caption="Imagem carregada", use_column_width=True)
        iniciar_ocr = st.button("🔍 Iniciar OCR")

        if st.button("🗑️ Limpar Resultado"):
            st.session_state.pop('resultado_ocr', None)
            st.experimental_rerun()

# Processamento do OCR se botão for clicado
if imagem_upada and iniciar_ocr:
    with st.spinner("🔄 Analisando imagem, aguarde..."):
        resposta = ollama.chat(
            model="gemma3:12b",
            messages=[{
                "role": "user",
                "content": """Analise o texto da imagem enviada e extraia todas as informações legíveis.
                              Apresente o conteúdo de forma estruturada em Markdown, com títulos, listas 
                              ou blocos de código quando necessário.""",
                "images": [imagem_upada.getvalue()]
            }]
        )
        st.session_state['resultado_ocr'] = resposta.message.content

# Exibição dos resultados
st.subheader("📄 Resultado do OCR")
if 'resultado_ocr' in st.session_state:
    st.markdown(st.session_state['resultado_ocr'], unsafe_allow_html=True)
else:
    st.info("Envie uma imagem e clique em 'Iniciar OCR' para ver o resultado aqui.")

# Rodapé simplificado
st.divider()
st.caption("🚀 Desenvolvido com ❤️ utilizando o modelo Gemma-3 Vision")
