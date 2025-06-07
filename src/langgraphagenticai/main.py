import streamlit as st 
import json
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLM.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisaplayResultStreamlit


def load_langgraph_agenticai_app():
    """ 
    Loads and runs the langgraph AgenticAi application with streamlit UI:
    This function intializes the UI, handles user Input, Configures the LLM model,
    sets up the graph based on the selected usecase and displays the output while 
    implementing exception handling for robustness
    """
    ## load UI
    try:
        ui = LoadStreamlitUI()
        user_input = ui.load_streamlit_ui()
        
        if not user_input:
            st.error("Error: Failed to load user input from the UI")
            return
        if st.session_state.IsFetchButtonClicked:
            user_message = st.session_state.timeframe
        #elif st.session_state.IsSDLC:
            #user_message = st.session_state.State
        else:
            user_message = st.text_input("Enter your message:")
            
        if user_message:
            try:
                obj_llm_config = GroqLLM(user_controls_input = user_input)
                model = obj_llm_config.get_llm_model()
                
                if not model:
                    st.error("Error LLM model could not be initaated.")
                    return
                
                usecase = user_input.get("selected_usecase")
                print("Usecase info",usecase)
                if not usecase:
                    st.error("Eoor No use case selected")
                    return
                ## Graph BUilder
                graphbuilder = GraphBuilder(model)
                try:
                    graph = graphbuilder.setup_graph(usecase)
                    DisaplayResultStreamlit(usecase,graph,user_message).display_results_on_ui()
                except Exception as e:
                    raise ValueException(f"Eoor occured with exception :{e}") 
                    return
                
            except Exception as e:
                raise ValueException(f"Eoor occured with exception :{e}") 
                return      
        
    except Exception as e:
        raise ValueException(f"Eoor occured with exception :{e}")
        

