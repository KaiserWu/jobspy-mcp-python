# server.py
import argparse
from mcp.server.fastmcp import FastMCP
from jobspy import scrape_jobs
from typing import Optional, List
import pandas as pd

instructions = """
This is a MCP server using JobSpy engine for AI job searching.

JobSpy is a job scraping library with the goal of aggregating all the jobs from popular job boards with one tool.
Scrapes job postings from LinkedIn, Indeed, Glassdoor, Google, ZipRecruiter, Bayt & Naukri concurrently
Aggregates the job postings in a dataframe
Proxies support to bypass blocking
"""

# Create an MCP server
mcp = FastMCP("jobspy-mcp-python", instructions=instructions, stateless_http=True)

@mcp.tool(
    name="search_jobs",
    description="Searches various job boards for job postings. Returns the results as a table.",
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

):
    """Searches job boards for job postings and returns the results as a DataFrame.
        parameters={
        "search_term": {"type": "string", "description": "Search term for the job, e.g. 'software engineer'"},
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
    jobs = scrape_jobs(
        site_name=site_name,
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
        distance=distance,
        job_type=job_type,
        is_remote=is_remote,
    )
    if isinstance(jobs, pd.DataFrame):
        return jobs.head().to_markdown()
    return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the JobSpy MCP server.")
    parser.add_argument("-p", "--port", type=int, help="Port to host the server on", default=5566)
    parser.add_argument(
        "-t",
        "--transport",
        type=str,
        default="stdio",
        choices=["stdio", "http"],
        help="Transport method for the MCP server (default: stdio). Host using streamable-http transport on default port 5566"
    )
    args = parser.parse_args()
    transport = "stdio" if args.transport == "stdio" else "streamable-http"

    if args.transport == "http":
        mcp.settings.port = args.port

    import asyncio
    try:
        mcp.run(transport=transport)
    except asyncio.exceptions.CancelledError:
        print("Server stopped by user.")
    except KeyboardInterrupt:
        print("Server stopped by user.")
    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        print("Server has been shut down.")
        exit(0)