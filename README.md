# 💬 Chat with SQL Database using LangChain

Interact with your SQL database using natural language instead of writing complex SQL queries.

This project uses LLMs to convert user questions into SQL queries, execute them, and return meaningful responses.

---

## 🚀 Features

- 🔍 Ask questions in plain English  
- 🧠 Converts natural language → SQL queries  
- ⚡ Fast responses using Groq API  
- 🗄️ Supports MySQL and SQLite  
- 📊 Clean and readable output  
- 🧩 Built with LangChain  

---

## 🛠️ Tech Stack

- Python  
- LangChain  
- Groq API  
- SQLAlchemy  
- MySQL / SQLite  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/chat-with-sql-db.git
cd chat-with-sql-db
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Add API Key

Create a `.env` file in the root directory and add:

```
GROQ_API_KEY=your_api_key_here
```

---

### 4️⃣ Run the Project

```bash
python app.py
```

---

## 💡 Example Queries

- "Show all students with marks above 80"  
- "How many users are registered?"  
- "List top 5 products by sales"  

---

## 🧠 How It Works

1. User enters a question in natural language  
2. LangChain converts it into an SQL query  
3. Query is executed on the database  
4. Results are returned in a human-readable format  

---

## ⚠️ Notes

- Make sure your database is running  
- Verify your database credentials  
- Avoid destructive queries like `DELETE` or `DROP`  

---

## 🔮 Future Improvements

- Add Streamlit UI  
- Support multiple databases  
- Improve query accuracy  
- Add authentication  

---

## ⭐ Support

If you found this project helpful, give it a ⭐ on GitHub!
