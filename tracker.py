from openai import OpenAI
from datatime import datetime
import json
import os

tools = [
    {
  "type": "function",
  "function": {
    "name": "create_json",
    "description": "Creates a JSON object with task details including date, task name, effect rating, time spent, and additional details if available.",
    "parameters": {
      "type": "object",
      "properties": {
        "date": {
          "type": "string",
          "description": "The date when the task was performed, in YYYY-MM-DD format. (i.e september 12th 2020 = 2020-09-12). Call access_datetime function to find day."
        },
        "task": {
          "type": "string",
          "description": "The name or description of the task performed by user."
        },
        "effect": {
          "type": "integer",
          "description": "An integer rating representing the effect of the task, -5 representing the most detrimental effect and 5 representing the most positive. (i.e coding practice = 4, play video games = -3, etc)."
        },
        "time_spent": {
          "type": "integer",
          "description": "Optional. The time spent on the task in minutes. Defaults to -1 if not specified."
        },
        "info": {
            "type": "string",
            "description": "Optional. Include additional information about the task if it exists, (i.e. learnt how to use tries, made hand detection, etc)"
        }
      },
      "required": ["date", "task", "effect"]
    }
    }
    },
    {
        "type": "function",
        "function": {
            "name": "access_datetime",
            "description": "Get current date and time",
        },
    }
    ]

def tool_use(user_responses, 
             system_message="""From the user response, use the following functions""", 
             model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    


def access_datetime():
    return datetime.now()

def create_json(date: str, task: str, effect: int, time_spent = -1, info = ""):
    
    task = {
        "date": date,
        "task": task,
        "time_spent": time_spent,
        "effect": effect,
        "info":info,

    }
    filename = f"~/Desktop/Accountabiltiy/time_spent/{date}.json"
    if os.path.exists(filename):
        with open(filename, "r+", encoding="utf-8") as file:
            try:
                data = json.load(file)  
            except json.JSONDecodeError:
                data = []  
        
           
            if not isinstance(data, list):
                data = [data]

            
            data.append(task)

            # Move cursor to the beginning and overwrite
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()  # Remove extra content if needed
    else:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([task], file, indent=4)

if __name__ == "__main__":
