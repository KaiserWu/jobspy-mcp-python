# server.py
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from jobspy import scrape_jobs
from typing import Optional, List
import pandas as pd
import logging

instructions = """
This is a MCP server using JobSpy engine for AI job searching.

JobSpy is a job scraping library with the goal of aggregating all the jobs from popular job boards with one tool.
Scrapes job postings from LinkedIn, Indeed, Glassdoor, Google, ZipRecruiter, Bayt & Naukri concurrently
Aggregates the job postings in a dataframe
Proxies support to bypass blocking
"""

# Create an MCP server
jobspy_mcp_server = FastMCP("jobspy-mcp-python", instructions=instructions, stateless_http=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False))

@jobspy_mcp_server.tool(
    name="search_jobs",
    description="""Searches various job boards for job postings. Returns the results as a markdown table.
    parameters={
        "search_term": {"type": "string", "description": "Search term for the job, e.g. 'software engineer', 'data scientist'"},
        "location": {"type": "string", "description": "Location, e.g. 'Berlin, Germany'", "default": None},
        "results_wanted": {"type": "integer", "description": "Number of desired results per job board", "default": 20},
        "hours_old": {"type": "integer", "description": "Only jobs posted in the last X hours", "default": 72},
        "site_name": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of job boards, e.g. ['indeed', 'linkedin', 'zip_recruiter', 'glassdoor', 'google', 'bayt', 'naukri']",
            "default": ["indeed", "linkedin", "zip_recruiter", "glassdoor", "google", "bayt", "naukri"]
        },
        "distance": {"type": "integer", "description": "Search radius in miles, e.g. 50", "default": None},
        "job_type": {
            "type": "string",
            "description": "Type of job, e.g. fulltime, parttime, internship, contract",
            "default": None
        },
        "is_remote": {"type": "boolean", "description": "Whether the job is remote", "default": False}
    }""" 
)
def search_jobs(
    search_term: str,
    location: Optional[str] = None,
    results_wanted: int = 20,
    hours_old: int = 72,
    site_name: List[str] = ["indeed", "linkedin", "zip_recruiter", "glassdoor", "google", "bayt", "naukri"],
    distance: Optional[int] = None,
    job_type: Optional[str] = None,
    is_remote: bool = False,
) -> str:
    """Searches job boards for job postings and returns the results as a json array of job URLs."""
    logging.info(f"Searching jobs for term: {search_term} at location: {location} on sites: {site_name}")
    fetch_description = False
    distance_km = None
    site_name_lower = to_lowercase(site_name)
    if "linkedin" in site_name:
        fetch_description = True
    if distance is not None:
        distance_km = int(distance * 1.60934)  # Convert miles to kilometers
    try:
        jobs = scrape_jobs(
            site_name=site_name_lower,
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            hours_old=hours_old,
            distance=distance_km,
            job_type=job_type,
            is_remote=is_remote,
            linkedin_fetch_description=fetch_description,
        )
        if isinstance(jobs, pd.DataFrame):
            return jobs.head().to_json(orient="records")
        return str(jobs)
    except Exception as e:
        logging.error(f"Error occurred while searching jobs: {e}")
        return str(e)

def to_lowercase(s: List[str]) -> List[str]:
    """Converts a string to lowercase."""
    return [item.lower() for item in s]