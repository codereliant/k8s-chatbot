import json
import subprocess

from colorama import Back, init, Fore
from openai import OpenAI

def execute_kubectl_cmd(cmd):
    # add kubectl prefix if it's not already there
    if not cmd.startswith("kubectl"):
        cmd = f"kubectl {cmd}"

    if cmd.startswith("kubectl delete"):
        return "I'm sorry, Deleting resources is disabled."
    
    try:
        output = subprocess.check_output(cmd, shell=True)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error executing kubectl command: {e}"

client = OpenAI()
model_name = "gpt-3.5-turbo-0125"

tools = [
    {
        "type": "function",
        "function": {
            "name": "execute_kubectl_cmd",
            "description": "execute the kubeclt command against the current kubernetes cluster",
            "parameters": {
                "type": "object",
                    "properties": {
                        "cmd": {
                            "type": "string",
                            "description": "the kubectl command to execute",
                        },
                    },
                    "required": ["cmd"],
            },
        },
    }
]

def chat_completion(user_input):
    messages = [{"role": "user", "content": user_input}]
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "execute_kubectl_cmd": execute_kubectl_cmd,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                cmd=function_args.get("cmd"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model=model_name,
            messages=messages,
        )
        return second_response.choices[0].message.content
    else:
        return response_message
    

def run_conversation():
    print("Welcome to the Kubernetes chatbot!")
    print("You can ask me anything about your Kubernetes cluster.")
    while True:
        print(Back.CYAN + Fore.BLACK + " You: ", end="")
        print(" > ", end="")
        user_input = input()
        if user_input.lower() == "exit" or user_input.lower() == "q":
            print("Goodbye!")
            break
        else:
            resp = chat_completion(user_input)
            print("")
            print(Back.GREEN + Fore.BLACK + " Assitant: ", end="")
            print(" > ", end="")
            print(f"{resp}")
            print("")




def main():
    init(autoreset=True)
    run_conversation()


if __name__ == "__main__":
    main()