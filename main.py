import os
import subprocess
from flask import Flask, render_template, request, send_file

# Add MiKTeX bin directory to the system PATH
os.environ["PATH"] += os.pathsep + r'C:\Users\sansk\AppData\Local\Programs\MiKTeX\miktex\bin\x64'

app = Flask(__name__, template_folder=os.path.abspath("templates"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    # Extract user input from the form
    # Extract user input from the form
    user_input = {
        'full_name': request.form.get('full_name'),
        'address': request.form.get('address'),
        'phone': request.form.get('phone'),
        'email': request.form.get('email'),
        'GitHub': request.form.get('GitHub'),  # Added GitHub field
        'objective': request.form.get('objective'),
        'education': request.form.get('education'),
        'skills': request.form.getlist('skills'),
        'experience': request.form.get('experience'),
        'projects': request.form.getlist('projects'),
        'certifications': request.form.get('certifications'),
        'references': request.form.get('references')
    }

    # Call the generative AI to get additional content based on user input
    generated_content = generate_content_with_ai(user_input)

    # Create a LaTeX template with placeholders
    # Create a LaTeX template with placeholders
    latex_template = f"""
    \\documentclass{{article}}
    \\usepackage{{titlesec}}
    \\usepackage[margin=0.5in, top=0.05in]{{geometry}}  % Adjust the top margin here

    \\title{{{user_input['full_name']}}}  % Add your document title here

    \\begin{{document}}
    \\maketitle  % Use \\maketitle to display the title

    \\titleformat{{\\section}}[block]
    {{\\normalfont\\Large\\bfseries}}{{\\thesection}}{{1em}}{{}}{{\\hrule}}  % Add a horizontal line after each section heading

    \\section*{{Contact Information}}

    \\begin{{tabular}}{{@{{}}ll@{{\\hspace{{5cm}}}}lr}}  % Adjust the spacing as needed
    Address: & {user_input['address']} & Email: & {user_input['email']} \\\\
    Phone: & {user_input['phone']} & GitHub: & {user_input['GitHub']} \\\\
    \\end{{tabular}}

    \\section*{{Education}}
    {user_input['education']}

\\section*{{Skills}}
{{% if {user_input['skills']} %}}
    \\begin{{itemize}}
    {{% for skill in {user_input['skills']} %}}
        \\item {{ skill }}
    {{% endfor %}}
    \\end{{itemize}}
{{% endif %}}


    \\section*{{Experience}}
    {user_input['experience']}

    \\section*{{Projects}}
    {{% if user_input['projects'] %}}
        \\begin{{itemize}}
        {{% for project in user_input['projects'] %}}
            \\item {{ project }}
        {{% endfor %}}
        \\end{{itemize}}
    {{% endif %}}

    \\section*{{Certifications}}
    {user_input['certifications']}

    \\section*{{References}}
    {user_input['references']}

    \\section*{{Generated Content}}
    {generated_content}

    \\end{{document}}
    """

    # Save the LaTeX template to a file
    with open('resume_template.tex', 'w') as f:
        f.write(latex_template)

    # Compile LaTeX to PDF using subprocess
    subprocess.run(["C:\\Users\\sansk\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64\pdflatex.exe", 'resume_template.tex'])

    # subprocess.run(["xelatex", 'resume_template.tex'])
    # Return the generated PDF to the user
    return send_file('resume_template.pdf', as_attachment=True)

def generate_content_with_ai(user_input):
    # Implement logic to call the generative AI service and get content based on user input
    # Replace the following line with your actual generative AI integration code
    generated_content = "This is a generated content based on user input."
    return generated_content

if __name__ == '__main__':
    app.run(debug=True)
