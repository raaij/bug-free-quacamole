from google.adk.agents import Agent

from draw_dash.tool import execute_sql

root_agent = Agent(
    name="query_execution_agent",
    model="gemini-2.5-flash",
    description="Agent that executes queries and provides a text description of results..",
    instruction=(
        """
You execute queries against a database and provide the user with the result.
The database engine in use is DuckDB.
"""
        +  # TODO: Replace this with metadata extracted by metadata agent.
        """
You have access to the `marketing` table.

This has the following columns:
<csv>
"Column","Description"
"CUST_ID","Unique identifier for each customer."
"BALANCE","The current balance in the customer's account."
"BALANCE_FREQUENCY","How frequently the balance is updated (a value closer to 1 indicates more frequent updates)."
"PURCHASES","The total amount of purchases made by the customer."
"ONEOFF_PURCHASES","The total amount of one-off (non-installment) purchases."
"INSTALLMENTS_PURCHASES","The total amount of purchases made in installments."
"CASH_ADVANCE","The amount of cash withdrawn from the credit card."
"PURCHASES_FREQUENCY","How frequently purchases are made (a value closer to 1 indicates more frequent purchases)."
"ONEOFF_PURCHASES_FREQUENCY","How frequently one-off purchases are made."
"PURCHASES_INSTALLMENTS_FREQUENCY","How frequently installment purchases are made."
"CASH_ADVANCE_FREQUENCY","How frequently cash advances are made."
"CASH_ADVANCE_TRX","The number of cash advance transactions."
"PURCHASES_TRX","The number of purchase transactions."
"CREDIT_LIMIT","The credit limit for the customer."
"PAYMENTS","The total amount of payments made by the customer."
"MINIMUM_PAYMENTS","The minimum payment amount due from the customer."
"PRC_FULL_PAYMENT","The percentage of time the customer has paid the full balance."
"TENURE","The duration of the customer's account tenure, in months."
</csv>
"""
    ),
    tools=[execute_sql],
)
