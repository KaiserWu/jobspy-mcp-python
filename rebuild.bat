@echo off
docker stop jobspy-mcp
docker rm jobspy-mcp
docker rmi jobspy-mcp-python:latest
docker build -t jobspy-mcp-python:latest .
docker run --restart unless-stopped -d --name jobspy-mcp -p 5566:5566 jobspy-mcp-python:latest