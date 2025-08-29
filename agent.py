#Import OpenAI models 

import openai 

# Add parent directory to path to import apikey
import sys
import os

# Get the parent directory (root of the project)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import openai_api_key
from openai import OpenAI

#Import asyncio
import asyncio

#Import json to work with outputs 
import json 

#Import markdown and HTML sanitization libraries
import markdown
import bleach 

#Define the filepath for this research file. We must later create a file for each agentic loop. 
file_path = "test_research.txt"



#Define the agent 
class Agent: 
    def __init__(self, client, id):
        self.client = client 
        self.id = id  
        # to be added at a later point. For now, we will just test basic agent functionality
        #self.main_ag_loop = main_ag_loop 

    
    #This function breaks down each question into a set of n questions that make sense based on the prompt. 

    def break_down_question_with_llm(self, prompt):
         
        response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """You are a component of a research assistant that breaks 
                     down questions into multiple parts. Break down this question into simpler questions for you to answer.

                     Your response should be in json format as follows. 
                     Example research question: "how do computers work?"
                     Example breakdown output json string:

                     [
                     {"question": {"question-number": 1, "question-value": "How does the CPU work"}},
                     {"question": {"question-number": 2, "question-value": "How does memory work"}},
                     {"question": {"question-number": 3, "question-value": "How does the computer display data?"}}
                     ]

                     After you output the string, you are done!
                     """},
                    {"role": "user", "content": f"{prompt}"}
                ]
            )
        return response.choices[0].message.content
    
    import json 

    def break_down_formatter(self, llm_question_breakdown_ouput): 
        
        #Strip the triple quotes
        clean_output = llm_question_breakdown_ouput.strip().strip("'''").strip()
        #Parse the json and convert to a list of dictionaries 
        try:
            questions_data = json.loads(clean_output)
        except json.JSONDecodeError as e: 
            print(f"Error parsing JSON: {e}")
            return 

        #Loop through each question in the parsed data 
        #Extract questions first 

        with open (file_path, 'a') as file: 
            
            #enumerate() takes a list and returns pairs of (index, item)
            #instead of getting each item, you also get its position number 
            for index, question_obj in enumerate(questions_data): 
                try: 
                    #This accesses one layer down into question, and then within that layer goes to question_value 
                    question = question_obj["question"] ["question-value"]
                    #Prompt the model with the question
                    response = self.prompt_model(question)

                     #Uses + 1 because index starts at zero
                    print(f"Question {index +1}: {question}")
                    print(f"Response: {response}\n")

                    #Write each question and response to the file
                    file.write(f"Question {index +1}: {question}\n")
                    file.write(f"Response: {response}\n\n")

                    # Ensure data is written immediatley to the disk 
                    file.flush()


                #Uses + 1 because index starts at zero
                except (KeyError, IndexError) as e: 
                    print(f"Error processing question {index + 1}: {e}")
                    continue 

    #This is the async version of this function 
    async def break_down_formatter_async(self, llm_question_breakdown_ouput): 

        import time 

        start = time.perf_counter()
        
        #Strip the triple quotes
        clean_output = llm_question_breakdown_ouput.strip().strip("'''").strip()
        #Parse the json and convert to a list of dictionaries 
        try:
            questions_data = json.loads(clean_output)
        except json.JSONDecodeError as e: 
            print(f"Error parsing JSON: {e}")
            return 

        #Loop through each question in the parsed data 
        #Extract questions first 


        """
        I need to write some kind of loop 
        I need to prompt the model 5 times concurrently 
        I need each async function call to have the right parameters 
        I can only extract the right parameters one at a time 

        The goal is to grab all of the values in question async, assign them and gather them. 

        """

        questions = [q["question"]["question-value"] for q in questions_data]

        #Run all prompts concurrently 

        results = await asyncio.gather(
            *[self.prompt_model_async(question) for question in questions]
        )


        # We use * to access each part of the list simultaneously 

        #need to figure out how t loop through this. 
        #assign the values, go from there. 

        
        with open (file_path, 'a') as file: 
            for i, (question, response) in enumerate(zip(questions, results)): 
                file.write(f"Question {i+1}: {question}\n")
                file.write(f"Response: {response}\n\n")
            file.flush()
        
        end = time.perf_counter()

        elapsed = end - start

        print(f"Elapsed time: {elapsed:.3f} seconds")

  


    #This function will answer each prompt. This is the base answering function. 
    def prompt_model(self, prompt): 

        #Add error checking here. 
        response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{prompt}"}
                ]
            )
        #data_to_write = response.choices[0].message.content

        # Removed for now. 
        #with open(file_path, 'a') as file:
        #    file.write(data_to_write)  # This writes the raw response!

        return response.choices[0].message.content
    
    #Compile the research done by each agent 

    def compile_research(self):
        content = ""
        try:
            with open(file_path, 'r') as file:
                content = file.read()  # Reads the entire content of the file as a single string
                #print("File content:")
                #print(content)
    
        #error checking 
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system", "content": "You are a master researcher that is in charge of multiple agents. They are going to give you output and it is your job to turn meaningful connections into a cohesive and logical output."},
                {"role":"user", "content": f"{content}"}
            ]
        )
        with open ("compiled_research.txt", 'w') as file: 
            file.write(response.choices[0].message.content)

        return response.choices[0].message.content 

    #Convert research output to HTML with proper sanitization
    def compile_research_html(self):
        # Get the markdown content
        markdown_content = self.compile_research()
        
        # Configure markdown processor with useful extensions
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',      # Tables, footnotes, def lists
            'markdown.extensions.codehilite', # Syntax highlighting for code
            'markdown.extensions.toc',        # Table of contents
            'markdown.extensions.nl2br',      # Convert newlines to <br>
        ])
        
        # Convert markdown to HTML
        html_content = md.convert(markdown_content)
        
        # Sanitize HTML to prevent XSS attacks
        allowed_tags = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'p', 'br', 'ul', 'ol', 'li', 
            'strong', 'em', 'code', 'pre', 
            'blockquote', 'a', 'table', 'thead', 
            'tbody', 'tr', 'th', 'td'
        ]
        
        allowed_attributes = {
            'a': ['href', 'title'],
            'code': ['class'],
            'pre': ['class'],
            'th': ['align'],
            'td': ['align']
        }
        
        clean_html = bleach.clean(
            html_content, 
            tags=allowed_tags, 
            attributes=allowed_attributes,
            strip=True
        )
        
        # Save HTML version to file as well
        with open("compiled_research.html", 'w', encoding='utf-8') as file: 
            file.write(clean_html)
            
        return clean_html

    
    #This function judges the final output and determines if there is a final loop that needs to be done. The answer is a simple yes or no. 

    def judge_text_from_file(self, content):
        content = ""

        try:
            with open(file_path, 'r') as file:
                content = file.read()  # Reads the entire content of the file as a single string
                print("File content:")
                print(content)
    
        #error checking 
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")

        except Exception as e:
            print(f"An error occurred: {e}") 
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system", "content": """
                 You are a research judge judging when the output of research agents is useful enough.
                 Your output will be the text 'YES' or 'NO'. 
                 """},
                {"role": "user", "content": f"{content}"}
            ]
        )
        return response.choices[0].message.content 





    #This is the async version of this function
   #This function will answer each prompt. This is the base answering function. 
    async def prompt_model_async(self, prompt): 
        import httpx 


        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {openai_api_key}", # Bearer token auth 
            "Content-Type": "application/json" # Tell server we're sending JSON
        }

        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a deep researcher who answers questions with poise and concision."},
                {"role": "user", "content": f"{prompt}"}
            ]
        }

            # Configure timeout - this is the key fix!
        timeout = httpx.Timeout(
            connect=10.0,    # Time to establish connection
            read=60.0,       # Time to read the response 
            write=10.0,      # Time to send the request
            pool=10.0        # Time to get connection from pool
        )

        async with httpx.AsyncClient(timeout=timeout) as client: 
            try: 
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"]
            
            except httpx.RequestError as e: 
                print(f"Request error: {e}")
                raise
            except httpx.HTTPStatusError as e: 
                print(f"HTTP error: {e.response.status_code}")
                raise
            except KeyError as e:
                print(f"Unexpected response structure {e}")
                raise 


    