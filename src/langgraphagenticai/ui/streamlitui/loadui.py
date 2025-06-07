import streamlit as st 
import os
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage
from src.langgraphagenticai.ui.uiconfig import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config() # ui config
        self.user_controls ={}
        
    def initialize_session(self):
        return {
            "current_step":"requirements",
            "requirements":"",
            "user_stories":"",
            "po_feedback":"",
            "generate_code":"",
            "review_feedback":"",
            "decision":None
        }
        
    def render_requirements(self):
        st.markdown("Requirements submission")
        st.session_state.state["requirements"] = st.text_area("Enter your requirements",height=200,key="req_input")
        if st.button("Submit Requirements",key="submit_req"):
            st.session_state.state["current_step"] ="generate_user_stories"
            st.session_state.IsSDLC = True
        
    def load_streamlit_ui(self):
        st.set_page_config(page_title= self.config.get_page_title(),layout="wide")
        st.header(self.config.get_page_title())
        st.session_state.timeframe = ""
        st.session_state.IsFetchButtonClicked = False
        st.session_state.IsSDLC = False
        
        
        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usease_options = self.config.get_usecase_options()
            self.user_controls["selected_llm"] = st.selectbox("Select LLM",llm_options)
            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Selected Model",model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API KEY",type="password")
                
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter GROQ API Key to proceed")
                
            self.user_controls["selected_usecase"] = st.selectbox("selected Usecase",usease_options)
            
            if "state" not in st.session_state:
                st.session_state.state = self.initialize_session()
            #self.render_requirements()
            
        return self.user_controls
            
        