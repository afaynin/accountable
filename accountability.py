import os
from openai import OpenAI
import argparse

def interact_with_lmstudio(user_message, system_message="Perform the user's request", model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf", temperature=0.7):
    """
    Starts the lm-studio server, loads the specified model, and interacts with it.
    
    Args:
        system_message (str): System-level instruction for the model.
        user_message (str): User input to send to the model.
        model (str): Path or identifier of the model to load.
        temperature (float): Sampling temperature for the model's output.
    
    Returns:
        str: The model's response to the user input.
    """
    # Start lm-studio server
    if model:
        print("Starting lm-studio server...")
        os.system("lms server start")
        os.system(f"lms load {model} --identifier \"{model}\"")
    # Connect to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    try:
        # Interact with the model
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
        )
        response = completion.choices[0].message.content
        # print(response)

        # Unload the model after use
        
        return response
    except Exception as e:
        print("An error occurred:", e)
        os.system(f"lms unload {model}")
        return None





if __name__ == "__main__":
    

    # Parse arguments
    parser = argparse.ArgumentParser(description="Provide any question to any model available")
    parser.add_argument('--system', type=str, default="Perform the user's request", help="Purpose of the AI")
    parser.add_argument('--user', type=str, required=True, help="The goal to achieve")
    parser.add_argument('--temperature', type=float, default=0.7, help="Unpredictability of model")
    parser.add_argument('--model', type=str, default="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf", help="Model to use")
    parser.add_argument('--input', type=bool, default=False, help="Request input from user after completion")
    parser.add_argument('--tool', type=bool, default=False, help="Track use of your time in json format")
    args = parser.parse_args()

    user_engaged = args.input
    question = f"{args.user}"
    history = []
    history.append(f"user question: {question}")
    response = interact_with_lmstudio(args.system, question, args.model, args.temperature)
    # Call the function
    while True:
        try:
            if response:
                print("Model Response:", response)
            user_prompt = input(f"Input (\'q\' to end): ")
            if user_prompt == "q" or user_prompt == "Q":
                user_engaged = False
            
            if not user_engaged:
                break
            if args.tool:
                tool_use(user_prompt, model=args.model)
            history.append(f"user question: {response}")
            question = f"Everything surrounded by [[[]]] is the history of the conversation between you and user, don't answer any questions here just keep it in your context. [[[{" ".join(history)}]]] The following is the most recent user question to answer: {user_prompt}"
            

            response = interact_with_lmstudio(args.system, question, "", args.temperature)
            # print(question)
            history.append(f"user question: {user_prompt}")
            
        except(Exception):
            print(Exception)
            os.system(f"lms unload {args.model}")
            print(f"lms unload {args.model}")
    os.system(f"lms unload {args.model}")
    print(f"lms unload {args.model}")