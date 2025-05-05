# 🌐 Horizonite Banking Portal

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-orange.svg)](https://streamlit.io/)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Visit-92c952)](https://horizonite.streamlit.app/)

A **modern, secure**, and feature-rich banking portal built with Python and Streamlit, designed to empower users with comprehensive financial management capabilities.

---

## ✨ Key Features

### 📊 User Dashboard
- 💰 Real-time account summary and balance overview
- 📈 Interactive transaction visualizations
- ⚡ Quick-access shortcuts for common actions

### 💸 Transaction Management
- 🔄 Fund transfers between accounts
- 🔍 Filterable transaction history
- 📊 Advanced analytics and customizable reports


### ⚙️ Account Management
- 🧑 User profile customization
- 🔐 Security preference settings
- 📄 Downloadable account statements

### 🛠️ Admin Panel
- 👥 User management dashboard
- 📉 Transaction monitoring tools


### ❓ Support Center
- 📨 Contact form for customer support
- ❓ Comprehensive FAQs and user guides

---

## 🖼️ Screenshots Gallery

| 🏠 Home Page        | 🔐 Account Details     |
|---------------------|------------------------|
| ![Home Page](https://i.postimg.cc/prt8sQxv/horizone-home.png) | ![Account Details](https://i.postimg.cc/9XJF8tcB/Account-Details.png) |

| 📊 User Dashboard   | ⚙️ Admin Panel         |
|---------------------|------------------------|
| ![User Dashboard](https://i.postimg.cc/bNtHHJhp/userdashboard.png) | ![Admin Panel](https://i.postimg.cc/Fsrk1HHT/Admin-pannel.png) |

| 🧮 EMI Calculator   | 📞 Contact Us          |
|---------------------|------------------------|
| ![EMI Calculator](https://i.postimg.cc/Jh255BG7/emicalc.png) | ![Contact Us](https://i.postimg.cc/MHy0wPtX/contact-us.png) |

---

## 📥 **Installation Guide**

Get Horizonite Banking Portal up and running in just a few steps! Follow this guide to set up the project on your local machine. 🚀

### **Step 1: Clone the Repository**
Clone the Horizonite repository and navigate to the project directory:

```bash
git clone https://github.com/Arya-rani/Horizonite.git
cd Horizonite
```

### **Step 2: Install Dependencies**
Install the required Python packages using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

### **Step 3: Launch the Application**
Run the Streamlit application to start the Horizonite Banking Portal:

```bash
streamlit run Home.py
```

---

## 📋 **Technical Requirements**

The following packages are essential for running Horizonite. Ensure you have these installed with the specified versions:

| **Package**     | **Version** | **Purpose**                     |
|-----------------|-------------|---------------------------------|
| **Streamlit**   | 1.30.0      | Web framework for the app       |
| **Pandas**      | 2.1.4       | Data manipulation and analysis  |
| **Matplotlib**  | 3.8.2       | Data visualization              |
| **Plotly**      | 5.18.0      | Interactive charts and graphs   |
| **PyOTP**       | 2.9.0       | Two-factor authentication (2FA) |
| **Pillow**      | 10.2.0      | Image processing                |
| **UUID**        | 1.30        | Unique identifier generation    |

> **Note**: Ensure you have **Python 3.11+** installed before setting up the project. You can download it from [python.org](https://www.python.org/downloads/).

## 🗂️ **Project Architecture**

The Horizonite Banking Portal is structured for modularity, scalability, and maintainability. Below is the project's file and folder organization, designed to keep code clean and accessible. 🌐

```
Horizonite/
├── Home.py                 # 🚀 Main application entry point
├── main.py                 # 🧠 Core business logic
├── assets/                 # 🎨 Static resources
│   ├── css/                # 💅 Custom CSS styles
│   └── images/             # 🖼️ Visual assets (logos, icons)
├── data/                   # 💾 Persistent storage
│   ├── users/              # 🔒 Encrypted user data (JSON)
│   ├── sessions/           # ⏰ Active session records
│   └── logs/               # 📜 System activity logs
├── pages/                  # 📑 Feature-specific modules
│   ├── Admin.py            # 🛠️ Admin dashboard
│   └── Contact_us.py       # 📞 Support portal
└── utils/                  # 🛠️ Helper utilities
    ├── auth.py             # 🔐 Authentication functions
    ├── db.py               # 🗄️ Data handling logic
    └── security.py         # 🛡️ Security protocols
```

---

## 💾 **Data Architecture**

Horizonite uses a lightweight and secure data storage system to manage user information, sessions, and logs efficiently. 📊

- **User Data**: 🔒 Stored as encrypted JSON files in `data/users/` for secure user management.
- **Sessions**: ⏲️ Time-stamped session records in `data/sessions/` for robust session tracking.
- **Logs**: 📋 Activity logs with timestamps in `data/logs/` for system monitoring and debugging.

---

## 📚 **License**

This project is proudly licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details. 🗳️

---

## 🙏 **Acknowledgments**

A big thank you to the tools and communities that made Horizonite possible! 🌟

- **Streamlit**: For its intuitive web framework. 🎨
- **Plotly & Matplotlib**: For powerful data visualization capabilities. 📈
- **PyOTP**: For secure two-factor authentication (2FA). 🔐
- **Font Awesome**: For sleek and modern icons. ✨
- **Open Source Community**: For inspiration and support. 🤗

---

## 🧱 **Built With**

Horizonite is crafted with modern technologies to ensure performance, security, and a delightful user experience. 🛠️

- 🐍 **Python 3.11+**: The backbone of the application.
- 🎨 **Streamlit Framework**: For rapid and responsive UI development.
- 🗃️ **JSON File Storage**: Lightweight and secure data persistence.
- 🔐 **TOTP Authentication**: Industry-standard two-factor authentication.
- 📱 **Responsive Design**: Seamless experience across devices.

---

## 🤝 **Contributing**

We welcome contributions to make Horizonite even better! Follow these steps to get started: 🚀

1. 🍴 **Fork the Repository**: Create your own copy of the project.
2. 🌿 **Create a Feature Branch**: `git checkout -b feature/new-feature`
3. 💾 **Commit Your Changes**: `git commit -am 'Add new feature'`
4. 🚀 **Push to Your Branch**: `git push origin feature/new-feature`
5. 📬 **Submit a Pull Request**: Share your changes with us!

---

## 📬 **Contact**

Have questions or need support? Reach out to us! 💬

- 📧 **Email**: [arya.rani@example.com](mailto:arya922004@gmail.com)
- 💬 **Live Chat**: Available directly on the Horizonite App

---

## 🚀 **Future Improvements**

We’re committed to making Horizonite the best it can be! Here are some planned enhancements: 🌟

1. 🧪 **Testing Section**: Introduce unit testing guidelines and coverage reports.
2. ⚙️ **CI/CD Pipeline**: Set up GitHub Actions for automated testing and deployment.
3. 🗄️ **Database**: Transition to SQLite/PostgreSQL for production-grade scalability.
4. 🔒 **Security**: Provide detailed encryption specifications for stored data.
5. 📜 **API Docs**: Add Swagger/OpenAPI documentation for API endpoints.
6. 🎥 **Demo Video**: Embed a walkthrough video for seamless onboarding.
7. 📝 **Changelog**: Maintain a version history with release notes.
8. 🌐 **Browser Compatibility**: Include a matrix of supported browsers.

> **Want to help?** Let us know if you’d like to contribute to any of these improvements! Open an issue or reach out directly. 🙌

---
