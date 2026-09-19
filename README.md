# 🤖 AI Autonomous Code Review Agent

> AI-powered autonomous code review system that analyzes source code from GitHub repositories and generates structured reviews for bugs, security vulnerabilities, performance issues, code quality, and recommended improvements.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![GitHub API](https://img.shields.io/badge/GitHub-API-black?logo=github)](https://docs.github.com/en/rest)
[![Gemini](https://img.shields.io/badge/Google-Gemini%20AI-4285F4?logo=google)](https://ai.google.dev/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20Workflow-orange)](https://www.langchain.com/langgraph)

## 🔗 Project Links

- *GitHub Repository:* https://github.com/vvarmaaddanki/ai-autonomous-code-review-agent
- *Live API:* Coming soon
- *API Documentation:* Available through FastAPI Swagger UI after running the application locally

> *Note:* The live deployment URL will be added after deploying the FastAPI backend.

---

## 📌 Overview

The *AI Autonomous Code Review Agent* is a Python-based backend application that connects the *GitHub API* with *Generative AI* to automate source-code review.

The system can retrieve files from a GitHub repository, analyze source code using a Gemini-powered AI reviewer, and return structured feedback covering:

- 🐛 Bugs
- 🔐 Security vulnerabilities
- ⚡ Performance issues
- 🧹 Code quality
- 💡 Recommended improvements

The project demonstrates practical experience with *Python backend development, REST APIs, GitHub API integration, Generative AI, LLM-based code analysis, FastAPI, and agentic AI workflows*.

---

## 🎯 Key Features

### 🔍 GitHub Repository Integration

- Fetch GitHub repository metadata
- Retrieve repository file trees
- Fetch individual source files
- Analyze Python source code directly from GitHub

### 🤖 AI-Powered Code Review

Uses Google's Gemini API to analyze source code and generate developer-focused feedback.

The AI review checks for:

1. Bugs and potential runtime issues
2. Security vulnerabilities
3. Performance bottlenecks
4. Code quality and maintainability
5. Recommended improvements

### 🚀 REST API Backend

Built with *FastAPI* and exposes documented REST endpoints through Swagger/OpenAPI.

### 📄 File-Level Code Review

Review a specific source file from a GitHub repository.

### 📦 Repository-Level Code Review

Automatically discovers Python files in a repository and submits the collected source code for AI-assisted review.

### 🔐 Environment-Based Configuration

API credentials are loaded through environment variables rather than hard-coded into the source code.

---

## 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │   GitHub Repository  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     GitHub API       │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    FastAPI Backend   │
                 └──────────┬───────────┘
                            │
                 ┌──────────┴───────────┐
                 │                      │
                 ▼                      ▼
        Repository Scanner       File Extraction
                 │                      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     Gemini LLM       │
                 │   AI Code Analysis   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Structured Code      │
                 │ Review & Suggestions │
                 └──────────────────────┘
🛠️ Technology Stack
Backend
Python
FastAPI
Uvicorn
REST API
Swagger / OpenAPI
AI / LLM
Google Gemini API
google-genai
Large Language Model (LLM)
Generative AI
AI-assisted code analysis
GitHub Integration
GitHub REST API
Repository metadata
Repository file tree
Source-code retrieval
Agent / Workflow Concepts
LangGraph
Agentic AI
Autonomous workflow orchestration
LLM-powered automation
Development Tools
Git
GitHub
VS Code
Python Virtual Environment
📂 Project Structure
ai-autonomous-code-review-agent/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── services/
│   │   │   ├── github_service.py
│   │   │   └── review_service.py
│   │   │
│   │   └── schemas/
│   │       └── review_schema.py
│   │
│   └── requirements.txt
│
├── .gitignore
├── README.md
└── LICENSE
🔌 API Endpoints
Method
Endpoint
Description
GET
/health
Health check
GET
/github/{owner}/{repo}
Get repository information
GET
/github/{owner}/{repo}/files
List repository files
GET
/github/{owner}/{repo}/file
Retrieve a specific file
POST
/review
Review source code directly
POST
/github/{owner}/{repo}/review-file
AI review of a GitHub file
POST
/github/{owner}/{repo}/review
AI review of a GitHub repository
