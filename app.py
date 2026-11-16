
import os
import streamlit as st
from groq import Groq
from groq import APIError
from dotenv import load_dotenv

# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "openai/gpt-oss-120b"

# --------------------------------------------------
# 2. Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Workout Plan Generator",
    page_icon="💪",
    layout="centered"
)

st.title("💪 AI Workout Plan Generator")

st.write(
    "Create a personalized weekly workout plan "
    "based on your fitness goals, experience and available equipment."
)


# --------------------------------------------------
# 3. Function to generate workout plan
# --------------------------------------------------

def generate_workout_plan(
    fitness_goal: str,
    experience_level: str,
    workout_days: int,
    equipment: str,
    limitations: str
) -> str:
    """
    Generate a personalized workout plan using Groq API.

    Args:
        fitness_goal: User's fitness objective.
        experience_level: User's workout experience.
        workout_days: Number of available workout days.
        equipment: Available workout equipment.
        limitations: Injuries or physical limitations.

    Returns:
        AI-generated workout plan as a string.

    Raises:
        ValueError: If inputs are invalid or response is empty.
        RuntimeError: If the Groq API request fails.
    """

    # Validate inputs
    if not fitness_goal.strip():
        raise ValueError("Please select a fitness goal.")

    if not experience_level.strip():
        raise ValueError("Please select your experience level.")

    if not 1 <= workout_days <= 7:
        raise ValueError("Workout days must be between 1 and 7.")

    if not equipment.strip():
        raise ValueError("Please select available equipment.")

     # Create the Groq client
    client = Groq(api_key=GROQ_API_KEY)

    # Build system prompt
    system_prompt = """
You are a professional fitness program designer.

Your job is to create practical, personalized weekly
workout plans based on the user's fitness profile.

IMPORTANT: Follow every user constraint strictly.

1. FITNESS GOAL
- Design exercises according to the selected fitness goal.
- Build muscle: prioritize resistance training.
- Lose fat: combine appropriate resistance and cardio.
- General fitness: balance strength and conditioning.
- Improve endurance: prioritize sustainable endurance training.

2. EXPERIENCE LEVEL
- Beginner: use simple exercises, manageable volume,
  conservative progression and clear instructions.
- Intermediate: introduce moderate training volume.
- Advanced: use appropriately challenging programming.

3. EQUIPMENT RESTRICTIONS
- Recommend ONLY the equipment explicitly selected.
- Home dumbbells means dumbbells and bodyweight only.
- No equipment means bodyweight exercises only.
- Full gym means standard gym equipment is available.
- Never assume access to additional equipment.
- Do not recommend furniture or household objects as workout
  equipment unless the user explicitly permits them.
- For home dumbbells, use only dumbbells and bodyweight.
- Do not assume the user owns an exercise bench or chair.
- Do not recommend furniture, household objects or
  improvised equipment.
- Do not recommend resistance bands unless selected.
- Do not include optional equipment alternatives.
- Every exercise must be possible using only the
  selected equipment and bodyweight.

4. WORKOUT DAYS
- Create exactly the requested number of training days.
- Clearly identify the remaining recovery days.
- Distribute training to allow adequate recovery.

5. INJURIES AND PHYSICAL LIMITATIONS
- Treat all reported limitations as strict constraints.
- Avoid movements that may aggravate reported limitations.
- Do not prescribe rehabilitation or medical treatment.
- Do not diagnose medical conditions.
- Include a brief safety disclaimer.
- Recommend professional assessment before starting
  exercise when an injury or limitation is reported.
- Advise stopping movements that cause pain.
- Do not automatically classify exercises as knee-friendly,
  back-friendly or joint-friendly.
- Do not recommend an exercise involving the affected body
  part unless its suitability is reasonably established.
- When the reported limitation is vague, prioritize exercises
  that do not load or stress the affected area.
- Do not suggest alternative exercises that introduce
  similar stress on the affected area.
- Do not use phrases such as "if pain-free" to bypass
  the restriction.
  - Never assume that low-impact exercises are automatically
  safe for a reported injury.
- For knee pain, do not automatically prescribe squats,
  lunges, glute bridges, kneeling exercises or movements
  requiring repeated knee flexion.
- Do not prescribe exercises that load the affected joint
  when the user's specific limitation is unclear.
- Avoid exercises that require kneeling or putting pressure
  on the affected joint.
- Do not claim that an exercise protects or rehabilitates
  an injured joint.
- Do not use phrases such as "if pain-free" to bypass
  an injury restriction.
- Recommend professional assessment to determine suitable
  exercises before suggesting affected-joint training.
  BACK PAIN RESTRICTIONS:

- Do not assume that machine-supported exercises are
  automatically safe for someone with back pain.
- Avoid exercises involving significant spinal loading,
  bending, twisting or sustained unsupported trunk positions.
- Do not automatically recommend squats, leg presses,
  hack squats, deadlifts or Smith machine squats.
- Avoid exercises that require the user to stabilize
  heavy loads through the lower back.
- Do not prescribe spinal mobility or rehabilitation
  exercises as treatment.
- Do not claim that an exercise is back-safe or
  lumbar-friendly without individual assessment.
- When the nature of the back pain is unclear, avoid
  programming exercises that load or stress the affected area.
- Recommend assessment by a qualified healthcare
  professional before beginning the workout.

6. WORKOUT STRUCTURE
For each training day provide:
- Workout focus.
- Exercise name.
- Sets.
- Repetitions or duration.
- Rest between sets.
- Brief exercise instructions.
For each workout day:
- Provide an estimated total session duration.
- Keep beginner sessions approximately 30-50 minutes.
- Include warm-up and cool-down in the estimated duration.

7. BEGINNER-FRIENDLY PROGRAMMING
- Keep training volume manageable.
- Prefer simple exercises.
- Include warm-up and cool-down suggestions.
- Include recovery days.
- Explain gradual progression.

8. WORKOUT QUALITY AND BALANCE

- For beginners training 2-3 days per week, prefer
  full-body workouts unless another split is more appropriate.
- Include appropriate upper-body push, upper-body pull,
  lower-body and core movements across the week.
- Avoid unnecessarily complicated exercises.
- Avoid excessive training volume for beginners.
- Do not repeat the same demanding muscle-group workout
  on consecutive training days.
- Make exercise variations appropriate to the experience level.
- Do not assume access to furniture or household objects.
- Ensure every exercise follows the selected equipment limits.
- Provide realistic rest periods and manageable session lengths.
- Progress gradually based on exercise technique and recovery.
- Never recommend pillows, chairs, tables, benches or other
  household objects as exercise equipment.
- Use only the explicitly selected equipment.
- Avoid technically demanding movements for beginners,
  including ballistic dumbbell swings.
- Avoid prescribing maximum repetitions or training to failure
  for beginners.
- Prefer controlled repetitions within a defined range.
- Balance weekly training volume across all major muscle groups.
- Avoid unnecessarily repeating lower-body exercises.
- Keep beginner sessions practical and manageable.
- Do not use "as many reps as possible" as a prescription.

9. RESPONSE FORMAT
Start with a summary of the fitness profile.

Then provide:
A. Weekly workout overview.
B. Day-by-day workout details.
C. Warm-up and cool-down suggestions.
D. Recovery recommendations.
E. Safety disclaimer when limitations are reported.

Use Markdown headings, tables and bullet points.
Do not recommend additional equipment.
Do not ignore user constraints.
Do not invent medical advice.
Make the plan realistic and practical.
"""

    # Build user prompt
    user_prompt = f"""
Create a personalized weekly workout plan using
the following information:

Fitness Goal: {fitness_goal}
Experience Level: {experience_level}
Workout Days Per Week: {workout_days}
Available Equipment: {equipment}
Injuries or Limitations: {limitations if limitations.strip() else "None reported"}

Please strictly follow all the constraints.
"""

    try:
        # Call Groq API
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.5,
            max_completion_tokens=4000
        )

        # Extract response
        workout_plan = response.choices[0].message.content

        if not workout_plan or not workout_plan.strip():
            raise ValueError(
                "The AI returned an empty response. Please try again."
            )

        return workout_plan

    except ValueError:
        raise

    except APIError as error:
        raise RuntimeError(
            "Unable to generate your workout plan due to an API error. "
            "Please check your Groq API key, account limits and try again."
        ) from error

    except Exception as error:
        raise RuntimeError(
            "Something went wrong while generating your workout plan. "
            "Please try again later."
        ) from error


# --------------------------------------------------
# 4. User input section
# --------------------------------------------------

st.subheader("Tell us about yourself")

with st.form("workout_form"):

    fitness_goal = st.selectbox(
        "What is your fitness goal?",
        [
            "Build muscle",
            "Lose fat",
            "General fitness",
            "Improve endurance"
        ]
    )

    experience_level = st.selectbox(
        "What is your experience level?",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    workout_days = st.slider(
        "How many days can you work out per week?",
        min_value=1,
        max_value=7,
        value=4
    )

    equipment = st.selectbox(
        "What equipment do you have access to?",
        [
            "No equipment",
            "Home dumbbells",
            "Full gym"
        ]
    )

    limitations = st.text_area(
        "Any injuries or physical limitations? (Optional)",
        placeholder="Example: Bad knees, back pain, no overhead pressing..."
    )

    generate_button = st.form_submit_button(
        "Generate Workout Plan",
        use_container_width=True
    )


# --------------------------------------------------
# 5. Generate, regenerate and display workout plan
# --------------------------------------------------

# Save the user's inputs when Generate is clicked
if generate_button:

    st.session_state["workout_inputs"] = {
        "fitness_goal": fitness_goal,
        "experience_level": experience_level,
        "workout_days": workout_days,
        "equipment": equipment,
        "limitations": limitations
    }

    st.session_state["generation_requested"] = True


# Generate or regenerate the workout plan
if st.session_state.get("generation_requested", False):

    st.session_state["generation_requested"] = False

    if not GROQ_API_KEY:
        st.error(
            "Groq API key not found. Please configure "
            "GROQ_API_KEY in your .env file."
        )

    else:
        inputs = st.session_state["workout_inputs"]

        with st.spinner(
            "Your AI fitness coach is preparing your workout plan..."
        ):
            try:
                workout_plan = generate_workout_plan(
                    fitness_goal=inputs["fitness_goal"],
                    experience_level=inputs["experience_level"],
                    workout_days=inputs["workout_days"],
                    equipment=inputs["equipment"],
                    limitations=inputs["limitations"]
                )

                st.session_state["workout_plan"] = workout_plan

                # Count successful generations
                st.session_state["generation_count"] = (
                    st.session_state.get("generation_count", 0) + 1
                )

            except ValueError as error:
                st.error(str(error))

            except RuntimeError as error:
                st.error(str(error))


# Display the plan whenever it exists in session state
if "workout_plan" in st.session_state:

    st.success("Your personalized workout plan is ready!")

    st.markdown("---")
    st.subheader("Your Personalized Workout Plan")

    st.markdown(st.session_state["workout_plan"])

    st.markdown("---")

    st.caption(
        "Disclaimer: This AI-generated workout plan "
        "is for general fitness information only. "
        "Consult a qualified healthcare professional "
        "before exercising with an injury or medical condition."
    )


    # Download workout plan
    download_content = st.session_state["workout_plan"]

    st.download_button(
        label="Download Workout Plan",
        data=download_content.encode("utf-8"),
        file_name="my_workout_plan.md",
        mime="text/markdown",
        use_container_width=True
    )
    # Regenerate workout plan
    if st.button(
        "🔄 Regenerate Workout Plan",
        use_container_width=True
    ):
        st.session_state["generation_requested"] = True
        st.rerun()
