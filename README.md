
# AI Workout Plan Generator 💪

An AI-powered workout plan generator built using Python, Streamlit and the Groq API.

The application generates personalized weekly workout plans based on fitness goals, experience level, workout frequency, available equipment and physical limitations.

## Features

- **Personalized Workout Plans:** Generate workout plans based on individual fitness goals.
- **Fitness Goals:** Build muscle, lose fat, general fitness and improve endurance.
- **Experience Levels:** Beginner, intermediate and advanced.
- **Flexible Scheduling:** Select between 1 and 7 workout days per week.
- **Equipment Selection:** No equipment, home dumbbells or full gym.
- **Physical Limitations:** Specify injuries or exercise restrictions.
- **AI-powered Generation:** Uses the Groq API to generate workout plans.
- **Regenerate Plans:** Generate a different workout plan using the same inputs.
- **Download Plans:** Download the generated workout plan in Markdown format.
- **Error Handling:** Handles API errors and invalid inputs.

## Technology Stack

- Python
- Streamlit
- Groq API
- LLM: OpenAI GPT-OSS 120B (via Groq)
- Python-dotenv

## Project Structure

```text
workout-plan-generator/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

Note: The `.env` file is stored locally and must not be committed to GitHub.

## Prerequisites

- Python 3.10 or later
- Git
- Groq API key

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd workout-plan-generator
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Groq API key

Create a `.env` file in the project root directory.

Add your API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your actual Groq API key.

Never share or commit your API key.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## How to Use

1. Select your fitness goal.
2. Choose your experience level.
3. Select the number of workout days per week.
4. Select your available equipment.
5. Enter any injuries or physical limitations, if applicable.
6. Click **Generate Workout Plan**.
7. Regenerate the plan if you want another variation.
8. Download your workout plan as a Markdown file.

## Disclaimer

The generated workout plans are intended for general fitness information only and do not replace professional medical advice.

Consult a qualified healthcare professional before beginning an exercise program, especially if you have an injury or medical condition.

## Author

Developed as part of the Codebasics AI Engineering Cohort assignment.
