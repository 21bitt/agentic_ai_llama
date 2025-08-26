# agentic_ai_llama
i think....i made an agentic ai...?


folder structure

your_agent_project/
├── agent_terminal.py 

├── .env      

├── storage/                 

├── data_input/ 

├── processed/                 

└── utils/

    └── file_utils.py       

used .env to hide openai api key used for this .py

it takes a bit of time to load because it was hitting openai rate limit. (using free openai account api key)


tried to set the file size limit and validate files with few criterias for input sanitization. (set as 200 mb for now because i was trying to have it work with rockyou.txt file and pull passwords. but just this size is slowing down the agent significantly...)
after indexing, the files are moved to processed folder so it doesn't end up duplicating and reprocessed again.
some error messages to print if i have issues with API key and index issue. 
and it reads/writes only inside dedicated directories. 
tried to limit the rate but still getting 429 error
and tried to harden so it wouldn't output api key.
