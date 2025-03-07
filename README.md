# Build an LLM Agent in 5 minutes 
## Overview

This repository shows you how to build an LLM using Snowflake's API. 

## Instructions 

1. Clone this repo. 

2. Sign up for an account [here](https://signup.snowflake.com/). Activate your account and you should see a welcome screen. 

3. Go to Projects -> Worksheets -> Click "Create SQL Worksheet" 

4. Copy and paste the entire [setup.sql](https://github.com/annafil/cortex-agent-api-demo/blob/main/setup.sql) into the worksheet and hit run. It might take a couple of minutes for Step 9 to finish! You should see the following response: 
`Stage area MODELS successfully created.`

5. Go to Databases -> Add Data -> Click Load files into a Stage. 

6. Upload the `sales_metrics.yaml file. Make sure to select SALES_INTELLIGENCE.DATA schema and MODELS under 'Stage'.

7. Click on your name in the bottom left corner, and select "Connect a tool to Snowflake". Find your: 
- Account Name
- 