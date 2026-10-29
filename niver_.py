import streamlit as st
import json
import os

# Configuração da página
st.set_page_config(
    page_title="Feliz Aniversário! 🎉",
    page_icon="🎂",
    layout="centered"
)

# Efeitos visuais iniciais
st.balloons()
st.snow()

# --- FUNÇÕES PARA SALVAR E CARREGAR DADOS ---
ARQUIVO_COMENTARIOS = "comentarios.json"
PASTA_UPLOADS = "uploads"

# Cria a pasta de uploads se ela não existir
if not os.path.exists(PASTA_UPLOADS):
    os.makedirs(PASTA_UPLOADS)

def carregar_comentarios():
    if os.path.exists(ARQUIVO_COMENTARIOS):
        with open(ARQUIVO_COMENTARIOS, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def salvar_comentario(nome, texto):
    comentarios = carregar_comentarios()
    comentarios.append({"nome": nome, "texto": texto})
    with open(ARQUIVO_COMENTARIOS, "w", encoding="utf-8") as f:
        json.dump(comentarios, f, ensure_ascii=False, indent=4)

def listar_fotos_salvas():
    if os.path.exists(PASTA_UPLOADS):
        return [os.path.join(PASTA_UPLOADS, f) for f in os.listdir(PASTA_UPLOADS) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]
    return []

# Criando as Abas
aba1, aba2, aba3 = st.tabs(["🎂 Início", "📸 Galeria & Memórias", "💬 Seção de Comentários"])

with aba1:
    st.title("Feliz Aniversário! 🥳")
    st.subheader("Seja bem-vindo(a) à nossa comemoração especial!")
    
    # Exibindo a imagem principal
    try:
        st.image(
            "cake.jpg", 
            caption="Happy Birthday! 🎉", 
            use_container_width=True
        )
    except Exception as e:
        st.error("Não foi possível carregar a imagem principal. Verifique se o arquivo está na mesma pasta.")

    # Inserindo um GIF divertido
    st.markdown("### Um toque especial:")
    st.image("https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif", width=400)

with aba2:
    st.header("📸 Nossas Memórias")
    st.write("Envie fotos para a nossa galeria especial!")
    
    # Botão para carregar novas fotos
    fotos_enviadas = st.file_uploader(
        "Escolha as fotos para adicionar à galeria:", 
        type=["jpg", "jpeg", "png", "webp"], 
        accept_multiple_files=True
    )
    
    if fotos_enviadas:
        for foto in fotos_enviadas:  # <- Corrigido aqui (removido o ']')
            caminho_arquivo = os.path.join(PASTA_UPLOADS, foto.name)
            # Salva o arquivo fisicamente na pasta uploads
            with open(caminho_arquivo, "wb") as f:
                f.write(foto.getbuffer())
        st.success("Foto(s) salva(s) com sucesso na galeria! 💖")
        st.rerun() # Atualiza a tela para mostrar a foto nova na hora

    # Exibindo todas as fotos salvas na pasta
    fotos_salvas = listar_fotos_salvas()
    if fotos_salvas:
        st.markdown("---")
        st.subheader("🖼️ Galeria de Momentos")
        cols = st.columns(2)
        for i, caminho_foto in enumerate(fotos_salvas):
            with cols[i % 2]:
                st.image(caminho_foto, caption=f"Memória {i+1}", use_container_width=True)
    else:
        st.info("A galeria está vazia. Seja o primeiro a enviar uma foto!")

with aba3:
    st.header("Seção de Comentários")
    st.write("Deixe seu comentário, felicitação ou história marcante!")
    
    # Formulário para enviar o comentário
    with st.form("form_comentario", clear_on_submit=True):
        nome = st.text_input("Seu nome:")
        comentario = st.text_area("Seu comentário:")
        botao_enviar = st.form_submit_button("Publicar Comentário")
        
        if botao_enviar:
            if nome and comentario:
                salvar_comentario(nome, comentario)
                st.success("Comentário publicado.")
            else:
                st.warning("Por favor, preencha o seu nome e o comentário.")

    st.markdown("---")
    st.subheader("Mural de Comentários")
    
    # Carrega e exibe os comentários salvos no arquivo JSON
    comentarios_salvos = carregar_comentarios()
    if comentarios_salvos:
        for c in reversed(comentarios_salvos):
            st.markdown(f"**👤 {c['nome']}** disse:")
            st.info(c['texto'])
    else:
        st.write("Nenhum comentário ainda. Seja o primeiro a comentar!")
