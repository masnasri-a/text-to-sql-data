from app.postgres import Postgres
from app.gemini import Gemini
gemini = Gemini()
postgres = Postgres()
postgres.connect()
table = 'influencer'
table2 = 'cities'
table_info = postgres.get_table_info(table)
table_info2 = postgres.get_table_info(table2)
print("Informasi tentang tabel \n\n\n")
question = input("Masukkan pertanyaan: ")
prompt = f"""Given an input question, use sqlite syntax to generate a sql query by choosing 
one or multiple of the following tables. Write query in between <SQL></SQL>.
Table Name : {table}
For this Problem you can use the following table Schema:
<table_schema>
{table_info}
</table_schema>
Table Name : {table2}
For this Problem you can use the following table Schema:
<table_schema>
{table_info2}
</table_schema>
            
Please provide the SQL query using LOWER in column and LIKE for this question: 
Question:{question}
Query: """
# print("Prompt : "+prompt)
result = gemini.fetch(prompt)
query = gemini.parse_response(result)
print("Query : "+query)
result = postgres.get_data(query)
print("Result : "+str(result))