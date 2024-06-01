import openai

# OpenAI API anahtarınızı buraya ekleyin
openai.api_key = 'YOUR_API_KEY'

def read_requirements(file_path):

    with open(file_path, 'r') as file:
        requirements = file.readlines()
    return [req.strip() for req in requirements]

def gpt_evaluate_requirement(requirement):
   
    prompt = f"Evaluate the following requirement based on the criteria:\n\nRequirement: {requirement}\n\nCriteria:\n1. Consistency\n2. Clarity\n3. Testability\n4. Measurability\n5. Uniqueness\n\nProvide a score between 1 and 10 for each criterion."
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )


    scores_text = response.choices[0].text.strip().split("\n")
    scores = [int(score.split(":")[1].strip()) for score in scores]
    overall_score = sum(scores) / len(scores)
    return scores, overall_score

def write_evaluation_results(requirements, output_path):

    with open(output_path, 'w') as file:
        for requirement in requirements:
            scores, overall_score = gpt_evaluate_requirement(requirement)
            req_id = requirement.split(':')[0]
            scores_str = ','.join(map(str, scores))
            file.write(f"{req_id}: [{scores_str}] - Overall [{overall_score:.1f}]\n")

def main(input_path, output_path):

    requirements = read_requirements(input_path)
    write_evaluation_results(requirements, output_path)

if __name__ == "__main__":
    input_path = 'requirements.txt'  # Girdi dosyasının yolu
    output_path = 'evaluation_results.txt'  # Çıktı dosyasının yolu
    main(input_path, output_path)
