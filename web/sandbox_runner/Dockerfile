FROM python:3.13-slim

# Non-root user for test execution inside the container.
RUN useradd --create-home --uid 10001 runner

WORKDIR /workspace
USER runner
