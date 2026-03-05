import sqlparse
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class SQLQuery(BaseModel):
    """A SQL query generated from natural language."""
    sql: str = Field(description="The executable PostgreSQL query.")
    explanation: str = Field(description="Brief explanation of why this query was generated.")

class DataRetrievalAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.sql_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Senior Data Engineer.
            Convert natural language requests into efficient PostgreSQL queries.
            Schema reference:
            - products(product_id, product_category_name, ...)
            - order_items(order_id, product_id, price, ...)
            - orders(order_id, customer_id, order_purchase_timestamp, ...)
            - inventory(product_id, current_stock_level, warehouse_id)
            
            Strictly avoid DELETE, DROP, or UPDATE operations."""),
            ("human", "Request: {request}")
        ])

    def validate_sql(self, sql: str) -> bool:
        """Performs safety checks on the generated SQL."""
        parsed = sqlparse.parse(sql)
        for statement in parsed:
            # Check for destructive keywords
            for token in statement.tokens:
                if token.value.upper() in ["DROP", "DELETE", "TRUNCATE", "UPDATE"]:
                    print(f"SECURITY ALERT: Destructive SQL token found: {token.value}")
                    return False
        return True

    def generate_sql(self, request: str) -> SQLQuery:
        """Generates and validates a SQL query."""
        sql_chain = self.sql_prompt | self.llm.with_structured_output(SQLQuery)
        query_obj = sql_chain.invoke({"request": request})
        
        if self.validate_sql(query_obj.sql):
            return query_obj
        else:
            raise ValueError("Generated SQL failed safety validation.")

    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """Placeholder for actual execution via SQLAlchemy."""
        print(f"Validated SQL Execution: {sql}")
        return [{"mock_data": "record_1"}, {"mock_data": "record_2"}]

if __name__ == "__main__":
    agent = DataRetrievalAgent()
    try:
        res = agent.generate_sql("Show me the total sales by category.")
        print(res.sql)
    except Exception as e:
        print(e)
