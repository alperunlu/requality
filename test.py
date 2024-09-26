import tkinter as tk
from tkinter import ttk
import openai

# OpenAI API key
openai.api_key = 'YOUR_API_KEY'

def read_requirements(file_path):
    with open(file_path, 'r') as file:
        requirements = file.readlines()
    return [req.strip() for req in requirements]

def gpt_evaluate_requirement(requirement):
    prompt = f"Evaluate the following requirement based on the criteria:\n\nRequirement: {requirement}\n\nCriteria:\n1. Consistency\n2. Clarity\n3. Testability\n4. Measurability\n5. Uniqueness\n\nProvide a score between 1 and 10 for each criterion."
    response = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=prompt,
        max_tokens=1500
    )
    scores_text = response.choices[0].text.strip().split("\n")
    scores = [int(score.split(":")[1].strip()) for score in scores_text]
    return scores

def write_evaluation_results(requirements_data, output_path):
    with open(output_path, 'w') as file:
        for req_id, scores in requirements_data:
            scores_str = ','.join(map(str, scores))
            overall_score = sum(scores) / len(scores)
            file.write(f"{req_id}: [{scores_str}] - Overall [{overall_score:.1f}]\n")

def create_gui(requirements_data):
    root = tk.Tk()
    root.title("Requirement Evaluations")

    headers = ["Requirement ID", "Consistency", "Clarity", "Testability", "Measurability", "Uniqueness"]
    for i, header in enumerate(headers):
        label = tk.Label(root, text=header, font=('Helvetica', 10, 'bold'))
        label.grid(row=0, column=i, padx=10, pady=10, sticky="w")

    for row, (req_id, scores) in enumerate(requirements_data, start=1):
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
