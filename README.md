# Student Cloud Portal - Secure File Sharing System 🎓☁️

A premium, student-centric file sharing system built with **Flask** and **AWS (S3 + DynamoDB)**. This portal allows students to securely upload, manage, and sync their research data with local AES-256 encryption.

## 🚀 Features
- **Cyber-Academic UI**: High-end glassmorphism design with a "Cloud Fresh" aesthetic.
- **Hybrid Cloud Security**: Files are encrypted locally using AES-256 before being synced to AWS S3.
- **Scholar Workspace**: Personalized dashboard with real-time storage metrics and research file registry.
- **High-Visibility Scholar Status**: Enhanced, glowing "Scholar Account" badge for clear status indication.
- **Auto-Dismissing Notifications**: Smart 10-second alert timers to keep your workspace clutter-free.
- **Duplicate Prevention**: Robust "Submission Lock" architecture to ensure clean file records.
- **Zero-Knowledge Architecture**: Your data is yours. Encryption happens on your machine.
- **Human-Friendly UX**: Optimized typography (16px base) and responsive layouts.

## 🛠️ Technology Stack
- **Frontend**: HTML5, Vanilla CSS (Custom Design System), Bootstrap 5, FontAwesome 6.
- **Backend**: Flask (Python).
- **Cloud Infrastructure**: 
  - **AWS S3**: Secure object storage for encrypted research blobs.
  - **AWS DynamoDB**: Scalable NoSQL database for student metadata and file registries.
- **Security**: Cryptography (AES-256), TLS 1.3 Tunneling.

## 📦 Setup & Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Shivakumar-09/file-transfering-using-Aws.git
   cd file-transfering-using-Aws
   ```
2. **Install Dependencies**:
   ```bash
   pip install flask boto3 cryptography python-dotenv
   ```
3. **Configure AWS Credentials**:
   Create a `.env` file with your AWS Academy or IAM credentials:
   ```env
   AWS_ACCESS_KEY=your_key
   AWS_SECRET_KEY=your_secret
   AWS_SESSION_TOKEN=your_token
   AWS_REGION=us-east-1
   S3_BUCKET_NAME=your_bucket
   DYNAMODB_USER_TABLE=Users
   DYNAMODB_FILE_TABLE=Files
   ```
4. **Run the Portal**:
   ```bash
   python app.py
   ```

## 📜 License
This project is developed for academic research purposes.

---
🚀 *Happy Researching!*
