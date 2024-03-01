import streamlit as st
from app.postgres import Postgres
from app.gemini import Gemini

gemini = Gemini()
postgres = Postgres()
postgres.connect()


st.title('Generative SQL Data')
st.write('This app uses gemini to generate SQL queries based on user input')
list_tables = postgres.list_tables()
result_array = [item[0] for item in list_tables]
selected_table = st.multiselect(
    label='Select your tables',
    options=result_array
    )
table_infos = []
query_scheme = """
Given an input question, use sqlite syntax to generate a sql query by choosing 
one or multiple of the following tables. Write query in between <SQL></SQL>.\n
"""
for index, table in enumerate(selected_table):
    table_infos.append(postgres.get_table_info(table))
    query_scheme += f"""
Table Name : {table}
For this Problem you can use the following table Schema:
<table_schema>
{table_infos[index]}
</table_schema>\n
"""
question = st.text_area('Enter your question')
query_scheme += f"""
Please provide the SQL query using LOWER in column and LIKE for this question: 
Question:{question}
Query: 
"""
if st.button('Generate Query'):
    result = gemini.fetch(query_scheme)
    query = gemini.parse_response(result)
    print("Query : "+query)
    result = postgres.get_data(query)
    print("Result : "+str(result))

    st.header("Dataframe")
    st.dataframe(result ,hide_index=True, use_container_width=True)
