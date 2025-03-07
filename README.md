# Build an LLM Agent in 5 minutes 
## Overview

This repository shows you how to build an LLM using Snowflake's API. 

<img width="500" alt="Screenshot 2025-03-07 at 12 04 05 AM" src="https://github.com/user-attachments/assets/889a971b-2c04-4b57-a43d-a1c626b290bf" />

## Instructions 

1. Clone this repo. 

2. Sign up for an account [here](https://signup.snowflake.com/?utm_campaign=cortex-agent-api-demo). Activate your account and you should see a welcome screen. 

3. Go to `Projects` -> `Worksheets` -> Click `Create SQL Worksheet`

4. Copy and paste the entire [setup.sql](https://github.com/annafil/cortex-agent-api-demo/blob/main/setup.sql) into the worksheet and hit run. It might take a couple of minutes for Step 9 to finish! You should see the following response: 
`Stage area MODELS successfully created.`

5. Go to `Data` -> `Add Data` -> Click `Load files into a Stage`. 

6. Upload the `sales_metrics_model.yaml` file. Make sure to select `SALES_INTELLIGENCE.DATA` as your database + schema and `MODELS` as your 'Stage'.
<img width="500" alt="Screenshot 2025-03-06 at 11 47 56 PM" src="https://github.com/user-attachments/assets/5cb78028-50a3-48a0-a324-feeb11ad0260" />

7. Create a folder called `.streamlit` and a file called `secrets.toml` inside.
  
8. Click on your name in the bottom left corner, and select `Connect a tool to Snowflake`. Use the dialog to fill out your information, replacing values in `[]` like so: 

  ```
[snowflake]
account = "[Account Identifier]"
user = "[User Name]"
password = "[Same as when you signed up. Be careful here and don't check this in to GitHub!"
role = "[Role]"
host = "[Account/Server URL]"
```

9. Run `pip install -r requirements.txt` to make sure you have all the dependencies working.

10. Run `streamlit run streamlit.app` and you should see a chat assistant ready to work with you! Try a few prompts:
- "What was the total sales volume last year?" should output a SQL query and an interpretation of your request.
- "Summarize the call with TechCorp Inc" should give you a summary of the call transcript. 
