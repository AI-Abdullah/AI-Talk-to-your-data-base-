import streamlit as st
import os 
import sqlite3
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def get_sql_query(user_query):
    sys_prompt = ChatPromptTemplate.from_template("""
                    You are an expert in converting English questions to SQL query!
                    The SQL database has the name STUDENT and has the following columns - NAME, COURSE, 
                    SECTION and MARKS. 
                    CRITICAL RULE: When the question asks about "student" (like "name the student", "who has", 
                    "show me the student"), always use SELECT * to return ALL COLUMNS (NAME, COURSE, SECTION, MARKS).
                    Only use specific columns (like SELECT COURSE or SELECT MARKS) when the question specifically 
                    asks for just that field.
                                                  For example, 
                    Example 1 - How many entries of records are present?, 
                        the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
                    Example 2 - Tell me all the students studying in Data Science COURSE?, 
                        the SQL command will be something like this SELECT * FROM STUDENT 
                        where COURSE="Data Science"; 
                    Example 3 - Who has the highest marks?,
                        the SQL command will be something like this SELECT * FROM STUDENT WHERE MARKS = (SELECT MAX(MARKS) FROM STUDENT);
                    Example 4 - Which course is Abdullah studying?,
                        the SQL command will be something like this SELECT COURSE FROM STUDENT WHERE NAME="Abdullah";
                    Example 5 - What are the marks of Student3?,
                        the SQL command will be something like this SELECT MARKS FROM STUDENT WHERE NAME="Student3";
                    also the sql code should not have ``` in beginning or end and sql word in output.
                    Now convert the following question in English to a valid SQL Query: {user_query}. 
                    No preamble, only valid SQL please
                                                       """)
    llm = ChatOpenAI(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        model="gpt-3.5-turbo"
    )

    chain = sys_prompt | llm | StrOutputParser()
    response = chain.invoke({"user_query": user_query})
    return response

def return_sql_response(sql_query):
    database = "student.db"
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        return cursor.fetchall()
    
def main():
    st.set_page_config(page_title="Text TO SQL")
    st.header("Talk to your Database !")

    user_query = st.text_input("Input your question:")
    submit = st.button("Enter")
    
    if submit and user_query:
        try:
            sql_query = get_sql_query(user_query)
            st.write(f"Generated SQL: `{sql_query}`")
            
            retrieved_data = return_sql_response(sql_query)
            st.subheader(f"Retrieved {len(retrieved_data)} records:")
            
            # Display data in a better format
            if retrieved_data:
                # Create headers for the table
                st.table(retrieved_data)
            else:
                st.info("No data found for this query.")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Please try rephrasing your question.")



if __name__ == "__main__":
    main()