import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

st.title("Semantic Search for Excel Rows")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("### Preview of Uploaded Data", df.head())
    
    # Let user select a column to search against
    columns = df.columns.tolist()
    selected_col = st.selectbox("Select column to perform semantic search on:", columns)
    
    if selected_col:
        # Fill missing values and convert to string
        df[selected_col] = df[selected_col].astype(str).fillna("")
        corpus = df[selected_col].tolist()
        
        # Compute embeddings
        st.write("Computing embeddings... please wait.")
        corpus_embeddings = model.encode(corpus, show_progress_bar=True)
        
        # Initialize FAISS Index
        dimension = corpus_embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(corpus_embeddings).astype('float32'))
        st.success("Embeddings computed and FAISS index built successfully!")
        
        # User input query
        query = st.text_input("Enter your search query:")
        top_k = st.slider("Select number of top results to display:", min_value=1, max_value=20, value=5)
        
        if query:
            query_embedding = model.encode([query])
            distances, indices = index.search(np.array(query_embedding).astype('float32'), top_k)
            
            st.write(f"### Top {top_k} Most Similar Rows:")
            
            results = []
            for idx, dist in zip(indices[0], distances[0]):
                if idx < len(df):
                    row_data = df.iloc[idx].to_dict()
                    # Calculate a simple similarity score inverted from L2 distance
                    row_data['Similarity Distance (L2)'] = round(float(dist), 4)
                    results.append(row_data)
            
            res_df = pd.DataFrame(results)
            st.dataframe(res_df)