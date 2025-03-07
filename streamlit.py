import json
import requests
import streamlit as st
import snowflake.connector
import sseclient 


# replace these values in your .streamlit.toml file, not here!
HOST = st.secrets["snowflake"]["host"]
ACCOUNT = st.secrets["snowflake"]["account"]
USER =st.secrets["snowflake"]["user"]
PASSWORD = st.secrets["snowflake"]["password"]
ROLE = st.secrets["snowflake"]["role"]
WAREHOUSE= "SALES_INTELLIGENCE_WH"

# variables shared across pages

AGENT_API_ENDPOINT = "/api/v2/cortex/agent:run"
API_TIMEOUT = 50000  # in milliseconds

CORTEX_SEARCH_SERVICES = "sales_intelligence.data.sales_conversation_search"
SEMANTIC_MODELS = "@sales_intelligence.data.models/sales_metrics_model.yaml" 

def run_snowflake_query(query):
    try:
        df = session.sql(query.replace(';',''))
        
        return df

    except Exception as e:
        st.error(f"Error executing SQL: {str(e)}")
        return None, None

def agent_api_call(query: str, limit: int = 10):

    text = ""
    sql = ""
    citations = []
    
    payload = {
        "model": "llama3.1-70b",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": query
                    }
                ]
            }
        ],
        "tools": [
            {
                "tool_spec": {
                    "type": "cortex_analyst_text_to_sql",
                    "name": "analyst1"
                }
            },
            {
                "tool_spec": {
                    "type": "cortex_search",
                    "name": "search1"
                }
            }
        ],
        "tool_resources": {
            "analyst1": {"semantic_model_file": SEMANTIC_MODELS},
            "search1": {
                "name": CORTEX_SEARCH_SERVICES,
                "max_results": limit
            }
        }
    }
    
    resp = requests.post(
            url=f"https://{HOST}"+AGENT_API_ENDPOINT,
            json=payload,
            headers={
                "Authorization": f'Snowflake Token="{st.session_state.CONN.rest.token}"',
                "Content-Type": "application/json",
            }
        )


    if resp.status_code < 400: 
        client = sseclient.SSEClient(resp)

        for event in client.events():
            try: 
                parsed = json.loads(event.data)

                try: 
                    if parsed['delta']['content'][0]['type'] == 'text': 
                        text = parsed['delta']['content'][0]['text']
                        yield text
     
                    elif parsed['delta']['content'][0]['type'] == 'tool_use': 
                        text = parsed['delta']['content'][1]['tool_results']['content'][0]['json']['text']
                        sql = parsed['delta']['content'][1]['tool_results']['content'][0]['json']['sql']
                        yield text
                        yield "\n\n```" + sql + "" 

                    else: 
                        text = parsed
                        yield text


                except:
                    continue
            except:
                continue

def main():

    with st.sidebar:
        if st.button("Reset Conversation", key="new_chat"):
            st.session_state.messages = []
            st.rerun()

    st.title("Intelligent Sales Assistant")

    # connection
    if 'CONN' not in st.session_state or st.session_state.CONN is None:

        try: 
            st.session_state.CONN = snowflake.connector.connect(
                user=USER,
                password=PASSWORD,
                account=ACCOUNT,
                host=HOST,
                port=443,
                role=ROLE,
                warehouse=WAREHOUSE
            )  
            st.info('Snowflake Connection established!', icon="💡")    
        except:
            st.error('Connection not established. Check that you have correctly entered your Snowflake credentials!', icon="🚨")    



    #try: 
    #  Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'].replace("•", "\n\n-"))

    if user_input := st.chat_input("What is your question?"):

            # Add user message to chat       
            with st.chat_message("user"):
                st.markdown(user_input)
                st.session_state.messages.append({"role": "user", "content": user_input})

            # Get response from API
            with st.spinner("Processing your request..."):
                
                response = agent_api_call(user_input, 1)
                text = st.write(response)

                # Add assistant response to chat
                if text:
                    st.session_state.messages.append({"role": "assistant", "content": text})

      
if __name__ == "__main__":
    main()