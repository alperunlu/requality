import tkinter as tk
from tkinter import ttk
from openai import OpenAI
import os

# OpenAI API key
client = OpenAI(
    api_key="APIKEY",
)

def read_requirements(file_path):
    with open(file_path, 'r') as file:
        requirements = file.readlines()
    return [req.strip() for req in requirements]

def gpt_evaluate_requirement(requirement):
    prompt = f"Evaluate the following requirement based on the criteria: \n\nRequirement: {requirement}\n\nConsistency, Clarity, Testability, Measurability, and Uniqueness.\n\nProvide a score between 1 and 10 for each criteria. Just provide the score number, don't give the result out of ten."
   
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
          {"role": "system", "content": "You are an expert at evaluating software requirements."},
          {"role": "user", "content": prompt},
        ]
    )

    response_text = response.choices[0].message.content.strip()
    print("OpenAI Response:", response_text) 
    scores_text = response_text.split("\n")
    scores = []
    for score in scores_text:
        if ":" in score:
            parts = score.split(":")
            if len(parts) == 2 and parts[1].strip().isdigit():  # Check response
                scores.append(int(parts[1].strip()))
    
    return scores


def write_evaluation_results(requirements_data, output_path):
    with open(output_path, 'w') as file:
        for req_id, scores in requirements_data:
            if scores: 
                scores_str = ','.join(map(str, scores))
                overall_score = sum(scores) / len(scores)
                file.write(f"{req_id}: [{scores_str}] - Overall [{overall_score:.1f}]\n")
            else:  # If null
                file.write(f"{req_id}: No valid scores could be generated.\n")


def create_gui(requirements_data):
    root = tk.Tk()
    root.title("Requirement Evaluations")

    headers = ["Requirement ID", "Consistency", "Clarity", "Testability", "Measurability", "Uniqueness"]
    for i, header in enumerate(headers):
        label = tk.Label(root, text=header, font=('Helvetica', 10, 'bold'))
        label.grid(row=0, column=i, padx=10, pady=10, sticky="w")

    for row, (req_id, scores) in enumerate(requirements_data, start=1):
        print(f"Processing: {req_id} with scores {scores}")  # Debug
        if scores:  
            label = tk.Label(root, text=req_id)
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
         
            for col, score in enumerate(scores, start=1):
                progress = ttk.Progressbar(root, orient="horizontal", length=100, mode="determinate")
                progress.grid(row=row, column=col, padx=10, pady=5, sticky="w")
                progress['value'] = score * 10  # Max value 100, scale 0-10

    root.mainloop()


def main(input_path, output_path):
    requirements = read_requirements(input_path)
    requirements_data = [(req.split(':')[0], gpt_evaluate_requirement(req)) for req in requirements]
    write_evaluation_results(requirements_data, output_path)
    create_gui(requirements_data)

if __name__ == "__main__":
    input_path = 'requirements.txt'  
    output_path = 'evaluation_results.txt' 
    main(input_path, output_path)
