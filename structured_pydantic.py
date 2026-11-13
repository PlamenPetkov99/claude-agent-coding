from pydantic import BaseModel, Field
import anthropic
from typing import Literal

client = anthropic.Anthropic()

# job_text = """
# Junior Machine Learning Engineer at HFT Architecture. Fully remote, from anywhere
# in the world. USD 125,000-155,000 per year. You'll write Python daily including
# tests, and should be able to explain why ordinary cross-validation breaks on time
# series. A personal project to show is required.
# """

# job_text_salary_null = """
# Junior Machine Learning Engineer at HFT Architecture. Fully remote, from anywhere
# in the world. You'll write Python daily including tests, and should be able to explain why ordinary cross-validation breaks on time
# series. A personal project to show is required.
# """

JOB_TEXTS = [
    # 1. fully remote, USD per year
    """Junior ML Engineer at HFT Architecture. Fully remote, from anywhere in the
    world. USD 125,000-155,000 per year. Python and testing required.""",

    # 2. hybrid, BGN per month, only "up to"
    """Mid-level Backend Developer (Python/Django) at SoftCraft Ltd. Hybrid: 2 days per
    week in our Sofia office. Salary up to 5,000 BGN per month. Must have Django,
    PostgreSQL, Docker. Nice to have: AWS, Celery.""",

    # 3. on-site, no salary
    """Senior Python Developer at Bank of Plovdiv. Work from our Plovdiv office,
    5 days a week. Requirements: 7+ years Python, FastAPI, Kafka.""",

    # 4. "remote" but restricted to a region, EUR per year
    """Python Engineer at EuroTech GmbH. Remote within the EU only.
    EUR 55,000-70,000 annually. Django, Celery, Redis.""",

    # 5. vague wording, "home office"
    """Data Engineer at DataFlow. Home office possible most days, occasional visits
    to Berlin HQ. 4,500 EUR/month gross. Python, Airflow, SQL.""",

    # 6. almost no information
    """We're hiring a Python dev! Great team, free coffee. Apply now.""",
]


class JobPosting(BaseModel):
    title: str = Field(description="Only  the title of the job exclude the seniority level")
    company: str | None
    work_mode: Literal["Remote", "Hybrid", "On-site"] | None = Field(description="Whether the job is remote or some other type like for example Hybrid")
    work_mode_details: str | None = Field(description="Additional information about the work mode")
    salary_min: float | None = Field(description=(
    "Lowest salary stated in the posting. Rules: "
    "'X-Y' -> X; 'up to X' -> null; 'from X' -> X; "
    "single exact number X -> X; no salary -> null."
))
    salary_max: float | None = Field(description=(
    "Highest salary stated in the posting. Rules: "
    "'X-Y' -> Y; 'up to X' -> X; 'from X' -> null; "
    "single exact number X -> X; no salary -> null."
))
    required_skills: list[str] = Field(description="List of required skills for the job")
    additional_skills: list[str] | None = Field(description="List of additional skills for the job most of the times they mark it with Nice to have")
    seniority: Literal["junior", "mid", "senior"]| None = Field(description="The seniority level of the job")
    currency: str|None = Field(description="The currency of the salary , please use the ISO 4217 code like 'USD', 'EUR' or 'BGN'")
    salary_period: Literal["Per month","Per year","Per hour"] | None = Field(description="The period of the salary")

for text in JOB_TEXTS:

    response = client.messages.parse(
        model="claude-haiku-5-5",
        max_tokens=500,
        messages=[{"role": "user", "content": f"Extract the job details:\n\n{text}"}],
        output_format=JobPosting,
    )

    job = response.parsed_output
    print(job)
    # print(JobPosting.model_json_schema())




