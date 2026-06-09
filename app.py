import streamlit as st
import os
from ibm_watsonx_ai.foundation_models import Model
import chromadb
from chromadb.utils import embedding_functions

# --- 1. STREAMLIT CONFIGURATION ---
st.set_page_config(page_title="College Admission Agent", page_icon="🎓", layout="centered")
st.title("🎓 University Admission AI Assistant")
st.caption("Powered by IBM Granite 3.0 & Retrieval-Augmented Generation (RAG)")

# --- 2. IBM CREDENTIALS SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("🔑 IBM Cloud Authentication")
    st.markdown("Enter your mandatory IBM Cloud Lite service credentials below.")
    
    # Store credentials securely in session state or inputs
    api_key = st.text_input("IBM Cloud API Key", type="password", value=os.getenv("IBM_API_KEY", ""))
    project_id = st.text_input("watsonx.ai Project ID", value=os.getenv("IBM_PROJECT_ID", ""))
    
    st.divider()
    st.info("💡 **Tip**: This agent reads raw policy data directly from `university_data.txt` to guarantee factual accuracy.")

# Verify credentials before activating the core LLM engine
if not api_key or not project_id:
    st.warning("⚠️ Please provide your IBM Cloud API Key and Project ID in the sidebar to begin.")
    st.stop()

# --- 3. INITIALIZE VECTOR DATABASE & DATA INGESTION ---
@st.cache_resource
def initialize_knowledge_base():
    """Reads institutional documents, vectorizes them, and builds a local vector store."""
    # Use a free, high-quality local embedding model matching enterprise standards
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # Setup standard ephemeral Chroma client
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(
        name="admission_policies", 
        embedding_function=embedding_func
    )
    
    # Read raw policy text file
    if not os.path.exists("university_data.txt"):
        with open("university_data.txt", "w") as f:
            f.write("[DOCUMENT: Template]\nFall 2026 application deadline is August 15, 2026.")
            
    with open("university_data.txt", "r") as file:
        raw_text = file.read()
    
    # Quick structural chunking based on our text dividers
    chunks = [c.strip() for c in raw_text.split("\n\n") if c.strip()]
    ids = [f"doc_{i}" for i in range(len(chunks))]
    
    # Upsert data chunks directly into our vector database
    collection.add(documents=chunks, ids=ids)
    return collection

try:
    vector_db_collection = initialize_knowledge_base()
except Exception as e:
    st.error(f"Failed to initialize local Vector DB: {e}")
    st.stop()

# --- 4. CONFIGURING IBM GRANITE CORE ---
@st.cache_resource
def load_ibm_granite(api_key, project_id):
    """Initializes the connection to the mandatory IBM Granite model series."""
    credentials = {
        "url": "https://us-south.ml.cloud.ibm.com", # Update map location if space cluster varies
        "apikey": api_key
    }
    
    # Greedy decoding structure used explicitly to enforce factual data anchoring
    model_params = {
        "decoding_method": "greedy",
        "max_new_tokens": 400,
        "min_new_tokens": 1,
        "temperature": 0.0
    }
    
    return Model(
        model_id="ibm/granite-8b-code-instruct",
        credentials=credentials,
        project_id=project_id,
        params=model_params
    )

granite_model = load_ibm_granite(api_key, project_id)

# --- 5. MANAGING CONVERSATIONAL HISTORY STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your official admission assistant. Ask me anything about our entry eligibility, fee scale, or upcoming deadlines."}
    ]

# Display ongoing message logs instantly on stream refreshes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. AGENT WORKFLOW INTERACTION LOOP ---
if user_query := st.chat_input("e.g., What is the deadline and fee for Computer Science?"):
    
    # 1. Display user entry immediately
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        
    # 2. Query Vector DB to get relevant admissions paragraphs
    with st.spinner("Searching official university database..."):
        retrieved_results = vector_db_collection.query(
            query_texts=[user_query], 
            n_results=3
        )
        # Extract matches into context string
        context_documents = " ".join(retrieved_results['documents'][0])
        
    # 3. Formulate strict prompt structure for IBM Granite
    rag_prompt = f"""You are the official AI Admission Assistant for the university.
Your goal is to guide prospective students accurately using ONLY the verified context documents provided below.

Strict Instruction Rules:
1. If the context documents do not contain information relevant to answer the question, say exactly: "I am sorry, I cannot find that information in our official guidelines. Please contact our central admissions office directly at admissions@university.edu." Do not invent any facts.
2. Rely strictly on explicit details, dates, and currency values found inside the text blocks below.

Verified Context Documents:
{context_documents}

Student Question: {user_query}

Official Institutional Answer:"""

    # 4. Generate prediction from IBM Granite model
    with st.chat_message("assistant"):
        with st.spinner("Generating official response via IBM Granite..."):
            try:
                response_text = granite_model.generate_text(prompt=rag_prompt)
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as model_err:
                error_msg = f"IBM watsonx.ai Service Error: {str(model_err)}"
                st.error(error_msg)




# --- 6. EVALUATOR / USER TESTING HELPER FORM ---
st.markdown("---")
with st.expander("💡 Check What You Can Ask This Bot (Sample Questions)"):
    st.markdown("""
    Aap niche diye gaye questions ko copy karke chat box me test kar sakte hain:
    
    **📅 Deadlines & Timelines**
    * `What is the last date to submit the online application form for 2026?`
    * `Is there a late application window and what is the penalty fee?`
    * `When will the first merit cutoff list be announced?`
    * `What is the deadline to withdraw admission and claim a refund?`
    * `When do first-year physical orientation and classes start?`
    
    **⚙️ Eligibility & Lateral Entry**
    * `What is the minimum aggregate percentage required for B.Tech CSE?`
    * `Are English marks included when calculating the core PCM aggregate score?`
    * `Can a commerce student apply for the BCA program?`
    * `What is the eligibility criteria for direct lateral entry into B.Tech second year?`
    * `What is the minimum aggregate score required for the MBA program?`
    
    **💰 Fees & Hostel Charges**
    * `What is the tuition fee per semester for the B.Tech Computer Science program?`
    * `Is the one-time registration admission fee refundable?`
    * `What are the annual hostel accommodation charges and does it include food?`
    * `What is the fine rate per day for late payment of semester fees?`
    * `Are there extra charges for using the campus transport/bus facility?`
    
    **🎓 Scholarships & Financial Aid**
    * `What are the criteria to qualify for the 100% tuition fee waiver scholarship?`
    * `What minimum CGPA must be maintained to renew the scholarship yearly?`
    * `Is there any tuition fee discount or concession for siblings?`
    * `What is the EWS financial assistance criteria and family income limit?`
    * `Can a student combine two different institutional scholarships concurrently?`
    
    **🏢 Placements & Campus Life**
    * `What is the average placement package offered to Computer Science graduates?`
    * `Which top recruiters visit the campus for placements?`
    * `What are the central library timings during final semester examination weeks?`
    * `Is it mandatory for first-year outstation students to stay in the hostel?`
    * `Can I change my engineering branch after completing the first year?`
    
    **⚠️ RAG Guardrail Test (Out of Context Questions - Bot should say No)**
    * `Does the campus have a swimming pool?`
    * `What is the uniform or dress code for engineering students?`
    * `Can I bring a personal car or bike to the college hostel?`
    """)