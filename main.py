import argparse
from jobspy_mcp import jobspy_mcp_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the JobSpy MCP server.")
    parser.add_argument("-p", "--port", type=int, help="Port to host the server on", default=5566)
    parser.add_argument(
        "-t",
        "--transport",
        type=str,
        default="stdio",
        choices=["stdio", "http", "sse"],
        help="Transport method for the MCP server (default: stdio). Host using streamable-http transport on default port 5566"
    )
    args = parser.parse_args()
    transport = "streamable-http" if args.transport == "http" else args.transport

    if transport == "streamable-http" or args.transport == "sse":
        jobspy_mcp_server.settings.host = "0.0.0.0"
        jobspy_mcp_server.settings.port = args.port

    import asyncio
    try:
        jobspy_mcp_server.run(transport=transport)
    except asyncio.exceptions.CancelledError:
        print("Server stopped by user.")
    except KeyboardInterrupt:
        print("Server stopped by user.")
    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        print("Server has been shut down.")
        exit(0)
