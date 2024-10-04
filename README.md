# D-chat - USDA AI Challenge Winners

D-chat is a cutting-edge decentralized chat application that combines the power of AWS cloud services with decentralized technologies to provide a secure, scalable, and intelligent communication platform.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Key Features](#key-features)
3. [Technologies Used](#technologies-used)
4. [Getting Started](#getting-started)
5. [Demo](#demo)
6. [Contact](#contact)

## Architecture Overview

D-chat's architecture is designed for scalability, security, and performance:

![Screenshot 2024-09-29 044955](https://github.com/user-attachments/assets/93da5494-571c-485f-aa15-af81fe40c41f)

1. **Data Collection**
   - Utilizes Selenium, BeautifulSoup (BSoup), and Python for web scraping
   - Targets USDA data sources for agricultural insights
   - Processes and prepares data for decentralized storage

2. **Decentralized Storage**
   - Implements Pinata IPFS for data pinning and decentralized storage
   - Ensures data availability and integrity

3. **AWS Infrastructure**
   - **EC2 Instances**: Host the main application components
   - **Frontend**:
     - Built with Next.js and React
     - Containerized using Docker for consistency and easy deployment
   - **Backend**:
     - Implemented in Python
     - Dockerized for scalability and isolation
   - **Amazon Bedrock**: Provides AI/ML capabilities
   - **Claude AI**: Integrated for advanced natural language processing
   - **Amazon S3**: Used for additional storage needs and data backups

4. **Knowledge Base**
   - Stores and manages RAG (Retrieval-Augmented Generation) data
   - Enhances chat capabilities with context-aware responses

## Key Features

- Decentralized data storage using IPFS technology
- AI-powered chat functionality leveraging Claude AI
- Scalable and resilient AWS-based infrastructure
- Integration of USDA agricultural data for informed discussions
- Real-time communication with end-to-end encryption
- Multi-platform support (web, mobile, desktop)
- User authentication and authorization
- Chat history and message search capabilities

## Technologies Used

- Frontend: Next.js, React, Docker
- Backend: Python, Docker
- Data Scraping: Selenium, BeautifulSoup
- Decentralized Storage: Pinata IPFS
- Cloud Services: AWS EC2, S3, Bedrock
- AI/ML: Claude AI, Amazon Bedrock
- Version Control: Git

## Getting Started

To get started with D-chat, ensure you have the following prerequisites:

- Node.js (v14 or later)
- Python (v3.8 or later)
- Docker and Docker Compose
- AWS CLI configured with appropriate permissions
- IPFS node (for local development)

## Demo

![WhatsApp Image 2024-10-01 at 10 39 20 PM](https://github.com/user-attachments/assets/5fe71c3b-d242-48fd-8b38-d35078fd8383)

![WhatsApp Image 2024-10-01 at 10 40 20 PM](https://github.com/user-attachments/assets/d9b6755e-9c0b-404a-8fe7-3cd86e362c75)


## Contact

For support or inquiries, please open an issue on GitHub.

---
