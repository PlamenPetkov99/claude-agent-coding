from structured_pydantic import JobPosting, JOB_TEXTS, client

EXPECTED = [
    {   # 1. HFT
        "company": "HFT Architecture",
        "work_mode": "Remote",
        "salary_min": 125000,
        "salary_max": 155000,
        "required_skills": {"python", "testing"},
        "additional_skills": None,
        "seniority": "junior",
        "currency": "USD",
        "salary_period": "Per year",
    },
    { #2. SoftCraft Ltd
        "company":"SoftCraft Ltd",
        "work_mode":"Hybrid",
        "salary_min":None,
        "salary_max":5000.0,
        "required_skills":{'Django', 'PostgreSQL', 'Docker','Python'},
        "additional_skills":{'AWS', 'Celery'},
        "seniority":"mid",
        "currency":"BGN",
        "salary_period":"Per month"
    },
    {   #3. Bank of Plovdiv
        "company":"Bank of Plovdiv",
        "work_mode":"On-site",
        "salary_min":None,
        "salary_max":None,
        "required_skills":{'Python', 'FastAPI', 'Kafka'},
        "additional_skills":None,
        "seniority":"senior",
        "currency":None,
        "salary_period":None
    },
    {   #4. EuroTech
        "company":"EuroTech GmbH",
        "work_mode":"Remote",
        "salary_min":55000.0,
        "salary_max":70000.0,
        "required_skills":{'Django', 'Celery', 'Redis','Python'},
        "additional_skills":None,
        "seniority":None,
        "currency":"EUR",
        "salary_period":"Per year"
    },
    {   #5.DataFlow
        "company":"DataFlow",
        "work_mode":"Hybrid",
        "salary_min":4500.0,
        "salary_max":4500.0,
        "required_skills":{'Python', 'Airflow', 'SQL'},
        "additional_skills":None,
        "seniority":None,
        "currency":"EUR",
        "salary_period":"Per month"
    },
    {   #6.Unknown
        "company":None,
        "work_mode":None,
        "salary_min":None,
        "salary_max":None,
        "required_skills":{'Python'},
        "additional_skills":None,
        "seniority":None,
        "currency":None,
        "salary_period":None
    }
]

RUNS_PER_CASE = 3
SET_FIELDS = {"required_skills", "additional_skills"}


def normalize(field, value):

    if field in SET_FIELDS:
        return {s.lower() for s in (value or [])}
    return value


def check(job, expected):

    errors = []
    for field, expected_value in expected.items():
        actual = normalize(field, getattr(job, field))
        wanted = normalize(field, expected_value)
        if actual != wanted:
            errors.append(f"{field}: expected {wanted!r}, got {actual!r}")
    return errors


def extract(text):
    response = client.messages.parse(
        model="claude-haiku-5-5",
        max_tokens=500,
        messages=[{"role": "user", "content": f"Extract the job details:\n\n{text}"}],
        output_format=JobPosting,
    )
    return response.parsed_output


if __name__ == "__main__":
    passed = total = 0
    for i, (text, expected) in enumerate(zip(JOB_TEXTS, EXPECTED), start=1):
        for run in range(1, RUNS_PER_CASE + 1):
            total += 1
            errors = check(extract(text), expected)
            if errors:
                print(f"Error #{i} run {run}: " + "; ".join(errors))
            else:
                passed += 1
                print(f"Pass #{i} run {run}")
    print(f"\n{passed}/{total} passed ({passed / total:.0%})")