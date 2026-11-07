FROM python:3.12-slim
RUN pip install --no-cache-dir 'numpy>=1.26,<3' 'matplotlib>=3.8,<4' 'pytest>=8,<10'
ENV PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/matplotlib HOME=/tmp PYTHONPATH=/work
WORKDIR /work
USER 65534:65534
