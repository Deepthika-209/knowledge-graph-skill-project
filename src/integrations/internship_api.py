
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_URL = "https://openintern.dev/api/v1/jobs"


TECHNICAL_KEYWORDS = (
    "software",
    "developer",
    "programming",
    "java",
    "python",
    "data science",
    "data analyst",
    "machine learning",
    "artificial intelligence",
    "web development",
    "cybersecurity",
    "cloud",
)


def fetch_internships(region="other", limit=27, india_only=False):
    """Fetch public internship listings from OpenIntern."""

    params = urlencode({"region": region})
    request = Request(
        f"{API_URL}?{params}",
        headers={"User-Agent": "StudentSkillRecommendationSystem/1.0"},
    )

    try:
        with urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))

    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
        return {
            "success": False,
            "message": f"Unable to fetch internship listings: {exc}",
            "internships": [],
        }

    internships = []

    for job in data.get("jobs", []):
        company_info = job.get("company") or {}
        company = company_info.get("name", "Unknown company")
        title = job.get("title", "Untitled internship")

        for posting in job.get("postings", []):
            location = posting.get("location") or "Location not specified"
            apply_url = posting.get("apply_url", "")

            searchable_text = f"{title} {company}".lower()

            if not any(word in searchable_text for word in TECHNICAL_KEYWORDS):
                continue

            if india_only and "india" not in location.lower():
                continue

            internships.append({
                "title": title,
                "company": company,
                "location": location,
                "posted_at": posting.get("posted_at"),
                "url": apply_url,
                "source": "OpenIntern",
            })

    # Remove duplicate listings while preserving order.
    # Remove duplicate listings while preserving order.
    unique = {}

    for internship in internships:
        key = (
            internship["company"].strip().lower(),
            internship["title"].strip().lower(),
            internship["location"].strip().lower(),
        )

        if key not in unique:
            unique[key] = internship

    internships = list(unique.values())

    results = list(unique.values())[:max(1, limit)]

    return {
        "success": True,
        "message": f"Fetched {len(results)} technical internship listings.",
        "internships": results,
        "total_available": data.get("total", len(results)),
    }
