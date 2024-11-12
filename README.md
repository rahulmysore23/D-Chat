# D-chat

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

![Picture2](https://github.com/user-attachments/assets/6291c97a-5564-4937-a00c-1e7baee81169)

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

![image](https://github.com/user-attachments/assets/c7a9f5ad-5c94-4006-9b98-aac1b6911b72)

![WhatsApp Image 2024-11-11 at 22 40 08_bed29aa6](https://github.com/user-attachments/assets/bdd3774f-113b-47b9-9fe2-c2943e710609)

![WhatsApp Image 2024-11-11 at 22 40 52_bc187d6d](https://github.com/user-attachments/assets/eaca8f4c-c96e-4cdd-b8cb-5bb093a1c781)

![WhatsApp Image 2024-11-11 at 22 39 10_90900244](https://github.com/user-attachments/assets/3d294d08-7199-4f98-80f3-25e97d9b89b7)

## Contact

For support or inquiries, please open an issue on GitHub.

---
