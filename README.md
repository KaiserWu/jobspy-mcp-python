# JobSpy MCP Python Server

This project provides an MCP (Multi-Component Platform) server that leverages the [JobSpy](https://github.com/speedyapply/JobSpy) engine for AI-powered job searching.

## Features

- Aggregates job postings from popular job boards: LinkedIn, Indeed, Glassdoor, Google, ZipRecruiter, Bayt, and Naukri.
- Concurrent scraping for fast results.
- Returns results as a structured table.
- Proxy support to bypass blocking.
- Easily extendable via MCP tools.

## Usage

Start the server:

```bash
python server.py
```

You can specify the port and transport method:

```bash
python server.py --port 5566 --transport http
```

## Example: Search for Jobs

**Example Chatbot Prompt**

```
Search for remote Python developer parttime jobs in Berlin around 6 miles, posted in the last 48 hours, from LinkedIn and Indeed. Show me 10 results per job board.
```

**Parameters used:**

- `search_term`: "Python developer"
- `location`: "Berlin"
- `results_wanted`: 10
- `hours_old`: 48
- `site_name`: ["linkedin", "indeed"]
- `distance`: 6 miles
- `job_type`: parttime
- `is_remote`: true

## Output

Results are returned as a Markdown table for easy readability by LLMs and users.

## Docker

You can build and run the server using Docker:

### Build the Docker image

```bash
docker build -t jobspy-mcp-python .
```

### Run the server with Docker

```bash
docker run -p 5566:5566 jobspy-mcp-python
```

## Requirements

- Python 3.10+
- See `requirements.txt` for dependencies

## License

MIT License