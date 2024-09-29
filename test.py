import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from openai import OpenAI
import os

# OpenAI API key
client = OpenAI(
    api_key="KEY",
)

def read_requirements(file_path):
    with open(file_path, 'r') as file:
        requirements = file.readlines()
    return [req.strip() for req in requirements]

def gpt_evaluate_requirement(requirement):
    prompt = f"Evaluate the following requirement based on the criteria: \n\nRequirement: {requirement}\n\nConsistency, Clarity, Testability, Measurability, and Uniqueness.\n\nProvide a score between 1 and 10 for each criteria. Just provide the score number, don't give the result out of ten."
   
    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0,
        messages=[
          {"role": "system", "content": "You are an expert at evaluating software requirements. Use consistent criteria to evaluate the requirements objectively every time. The results should not vary between evaluations for the same requirement."},
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

    headers = ["Requirement ID", "Consistency", "Clarity", "Testability", "Measurability", "Uniqueness", "Overall"]
    

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

            overall_score = sum(scores) / len(scores) 
            overall_score_label = tk.Label(root, text=f"{overall_score:.1f}", font=('Helvetica', 10))  # Score gösterimi
            overall_score_label.grid(row=row, column=len(headers) - 1, padx=10, pady=5, sticky="w")
        else:
            label = tk.Label(root, text=req_id)
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

            for col in range(1, len(headers) - 1): 
                label = tk.Label(root, text="-")
                label.grid(row=row, column=col, padx=10, pady=5, sticky="w")

            # Overall Score
            overall_score_label = tk.Label(root, text="N/A", font=('Helvetica', 10))
            overall_score_label.grid(row=row, column=len(headers) - 1, padx=10, pady=5, sticky="w")

        # Menu creation
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menu_bar)

        headers = ["Requirement ID", "Consistency", "Clarity", "Testability", "Measurability", "Uniqueness", "Overall"]
        for i, header in enumerate(headers):
            tk.Label(root, text=header, font=('Helvetica', 10, 'bold')).grid(row=0, column=i, padx=10, pady=10, sticky="w")

        for row, (req_id, scores) in enumerate(requirements_data, start=1):
            tk.Label(root, text=req_id).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            for col, score in enumerate(scores, start=1):
                progress = ttk.Progressbar(root, orient="horizontal", length=100, mode="determinate")
                progress.grid(row=row, column=col, padx=10, pady=5, sticky="w")
                progress['value'] = score * 10
            overall_score = sum(scores) / len(scores)
            tk.Label(root, text=f"{overall_score:.1f}", font=('Helvetica', 10)).grid(row=row, column=len(headers) - 1, padx=10, pady=5, sticky="w")
    root.mainloop()


def main(input_path, output_path):
    input_path = filedialog.askopenfilename(title="Select Requirements File", filetypes=[("Text Files", "*.txt")])
    output_path = filedialog.asksaveasfilename(title="Save Evaluation Results As", filetypes=[("Text Files", "*.txt")])

    if input_path and output_path:
        requirements = read_requirements(input_path)
        requirements_data = [(req.split(':')[0], gpt_evaluate_requirement(req)) for req in requirements]
        write_evaluation_results(requirements_data, output_path)
        create_gui(requirements_data)
    
    requirements = read_requirements(input_path)
    requirements_data = [(req.split(':')[0], gpt_evaluate_requirement(req)) for req in requirements]
    write_evaluation_results(requirements_data, output_path)
    create_gui(requirements_data)

if __name__ == "__main__":
    input_path = 'requirements.txt'  
    output_path = 'evaluation_results.txt' 
    main(input_path, output_path)
