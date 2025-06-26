import os
import pandas as pd
from sqlalchemy import create_engine, text
from openai import OpenAI

class NLToSQL:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API Key is required.")
        self.client = OpenAI(api_key=self.api_key)
        self.db = None
        self.df = None
        self.table_name = None

    def load_excel_to_db(self, file_path, table_name):
        self.df = pd.read_excel(file_path, skiprows=range(1, 5), header=0)
        self.db = create_engine('sqlite:///:memory:', echo=False)
        self.df.to_sql(name=table_name, con=self.db, index=False, if_exists='replace')
        self.table_name = table_name
        return self.df

    def get_table_prompt(self):
        if self.df is None or self.table_name is None:
            raise ValueError("DataFrame or table name is not set.")
        return f'''Given sqlite SQL table definition and natural language requests,
write accurate SQL queries. 
### sqlite SQL table definition 
# {self.table_name} ({", ".join(str(col) for col in self.df.columns)})
'''

    def query_from_nl(self, user_prompt):
        table_prompt = self.get_table_prompt()
        system_prompt = """You are an Expert SQLite Query generator.
Generate SQLite queries based on table definition and natural language requests.
Return only SQL query, nothing else. Query should start with SELECT and end with semicolon(;)."""
        full_prompt = table_prompt + "\n### Request:\n" + user_prompt

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    def refine_query(self, query):
        query = query.strip()
        if not query.upper().startswith("SELECT"):
            query = "SELECT " + query
        if not query.endswith(";"):
            query += ";"
        return query

    def run_query(self, query):
        if self.db is None:
            raise ValueError("Database is not initialized.")
        with self.db.connect() as conn:
            result = conn.execute(text(query))
            return result.fetchall()

    def interactive_loop(self):
        while True:
            user_input = input("SQL로 조회하고 싶은 내용을 적어주세요. 예) 테이블에서 월간 평균 매출액을 알고싶어. 나가려면 q를 입력하세요\n")
            if user_input.lower() == 'q':
                break
            sql = self.refine_query(self.query_from_nl(user_input))
            print("Generated SQL:", sql)
            results = self.run_query(sql)
            print("Query Result:")
            for row in results:
                print(row)
