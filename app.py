import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import re
import io
from typing import Tuple, Optional
import json

# Configure page settings
st.set_page_config(
    page_title="Conversational Data Analyst",
    page_icon="📊",
    layout="wide"
)

# Configure Gemini API
genai.configure(api_key="AIzaSyAdlblRJbXyDCCgKtQzCWl1QwJpacra1HA")
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_view' not in st.session_state:
    st.session_state.current_view = None

def safe_execute_code(code: str, df: pd.DataFrame) -> Tuple[Optional[str], Optional[go.Figure]]:
    """Safely execute Python code and return the output."""
    try:
        # Create a safe environment with only necessary variables
        local_vars = {
            'pd': pd,
            'plt': plt,
            'sns': sns,
            'px': px,
            'go': go,
            'df': df,
            'Figure': go.Figure
        }
        
        # Execute the code
        exec(code, {}, local_vars)
        
        # Check if a Plotly figure was created
        if 'fig' in local_vars and isinstance(local_vars['fig'], (go.Figure, px.Figure)):
            return None, local_vars['fig']
        
        # If no figure was created, check for matplotlib figures
        if plt.get_fignums():
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            return None, buf.getvalue()
        
        return None, None
    except Exception as e:
        return str(e), None

def extract_code_from_response(response: str) -> Tuple[str, Optional[str]]:
    """Extract Python code from Gemini's response."""
    code_pattern = r'```python\n(.*?)\n```'
    code_match = re.search(code_pattern, response, re.DOTALL)
    
    if code_match:
        code = code_match.group(1)
        text = response.replace(code_match.group(0), '').strip()
        return text, code
    return response, None

def generate_gemini_response(df: pd.DataFrame, question: str) -> str:
    """Generate response from Gemini API."""
    context = {
        'dataframe_info': {
            'columns': list(df.columns),
            'shape': df.shape,
            'dtypes': df.dtypes.astype(str).to_dict(),
            'sample_data': df.head(3).to_dict(orient='records')
        }
    }
    
    prompt = f"""You are a data analyst expert. Analyze the following DataFrame:

Context: {json.dumps(context, indent=2)}

User Question: {question}

Please provide:
1. A clear explanation of the analysis
2. Python code (using plotly for visualizations) to answer the question
3. Key insights from the data

Format your response with:
- Explanation in plain text
- Code in ```python``` blocks
- Insights as bullet points

Use plotly for visualizations and ensure the code is complete and executable."""
    
    response = model.generate_content(prompt)
    return response.text

def create_sidebar():
    """Create the sidebar with data insights."""
    with st.sidebar:
        st.header("📊 Data Insights")
        if st.session_state.df is not None:
            df = st.session_state.df
            st.write("Quick Stats:")
            st.write(f"- Total Records: {len(df)}")
            st.write(f"- Countries: {len(df['Country'].unique())}")
            st.write(f"- Subscription Types: {', '.join(df['Subscription_Type'].unique())}")
            
            # Show subscription distribution
            sub_dist = df['Subscription_Type'].value_counts()
            fig = px.pie(values=sub_dist.values, names=sub_dist.index, title="Subscription Distribution")
            st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("🤖 Conversational Data Analyst")
    st.markdown("---")
    
    # Create two columns for the main layout
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # File upload section
        uploaded_file = st.file_uploader("📂 Upload your data file", type=['csv', 'xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state.df = df
                st.success("✅ File uploaded successfully!")
                
                # Display data preview in an expander
                with st.expander("📋 Data Preview", expanded=True):
                    st.dataframe(df.head(), use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
    
    with col2:
        # Chat interface
        if st.session_state.df is not None:
            st.subheader("💬 Ask questions about your data")
            user_question = st.text_input("Your question:", placeholder="e.g., Show me customer distribution by country")
            
            if user_question:
                with st.spinner("🤔 Analyzing your data..."):
                    # Generate response
                    response = generate_gemini_response(st.session_state.df, user_question)
                    
                    # Extract code and text
                    text_response, code = extract_code_from_response(response)
                    
                    # Display text response
                    st.markdown("### Analysis")
                    st.write(text_response)
                    
                    # Execute code if present
                    if code:
                        with st.spinner("📊 Generating visualization..."):
                            error, figure = safe_execute_code(code, st.session_state.df)
                            if error:
                                st.error(f"❌ Error executing code: {error}")
                            elif isinstance(figure, (go.Figure, px.Figure)):
                                st.plotly_chart(figure, use_container_width=True)
                            elif figure:
                                st.image(figure)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "question": user_question,
                        "response": response
                    })
            
            # Display chat history in an expander
            with st.expander("📜 Chat History", expanded=False):
                for chat in reversed(st.session_state.chat_history):
                    st.markdown(f"**Q:** {chat['question']}")
                    st.markdown(f"**A:** {chat['response']}")
                    st.markdown("---")
    
    # Create sidebar
    create_sidebar()

if __name__ == "__main__":
    main() 