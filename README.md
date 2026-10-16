# 💸 Budget Buddy

> *Small savings every day. Big progress over time.*

## 📖 About Budget Buddy

Ever wonder where your money went, even when you feel like you barely spent anything? Sometimes, it's not the big purchases that drain our wallets, but the little expenses that pile up day after day. A snack here, a drink there, or an unnecessary purchase might seem harmless on its own, but together, they can take a bigger bite out of our budget than we realize.

**Budget Buddy** is a simple personal finance dashboard designed to help users track their income, monitor their expenses, and visualize where their money goes. By making small expenses easier to recognize, the application encourages better budgeting habits and more mindful financial decisions.

This project was developed as part of the course requirements for **EEE 111: Python Programming**. It applies fundamental Python programming concepts to a practical, real-world application, using **Streamlit** for the web-based user interface, **Matplotlib** for data visualization, and **CSV files** for storing and loading financial data.

---

## 🚀 Setup and Installation

Follow these steps to set up and run Budget Buddy on your local machine using a Python virtual environment.

### 1. Clone the Repository

Clone the repository to your computer. Replace the example URL with your actual GitHub repository URL.

```bash
git clone https://github.com/your-username/budget-buddy-your-lastname-your-student-number.git
```

Navigate to the project directory:

```bash
cd budget-buddy-your-lastname-your-student-number
```

### 2. Create a Virtual Environment

Create a virtual environment to keep the project's dependencies separate from other Python projects.

```bash
python -m venv name_of_your_env
```

### 3. Activate the Virtual Environment

Activate the virtual environment before installing dependencies or running the application.

**Windows (Command Prompt):**

```bat
name_of_your_env\Scripts\activate
```

**Windows (PowerShell):**

```powershell
.\name_of_your_env\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source name_of_your_env/bin/activate
```

To exit the virtual environment when you're finished, run:

```bash
deactivate
```

### 4. Install Dependencies

Install the required Python libraries:

```bash
pip install streamlit matplotlib
```

If the repository includes a `requirements.txt` file, you can install all listed dependencies instead:

```bash
pip install -r requirements.txt
```

### 5. Run the Application

Start the Budget Buddy dashboard by running:

```bash
streamlit run main.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`, where you can open the application in your web browser.

---

## 🛠️ Technologies Used

- **Python** – Core programming language
- **Streamlit** – Web application interface and interactive dashboard
- **Matplotlib** – Charts and data visualization
- **CSV** – Local storage for financial data

---

## ⚠️ Known Issues & Limitations

### Functional Limitations

- **No Edit or Delete Options:** Recorded expenses and their categories cannot currently be modified or deleted directly through the user interface.
- **No Recurring Transactions:** All transactions must be entered manually. Automatic recording of recurring expenses, such as monthly subscriptions, or income, such as salary, is not supported.
- **Single Currency Support:** The application uses a single currency and does not currently support multiple currencies, automatic currency conversion, or customizable currency symbols.
- **No Automated Budget Alerts:** Although users can set monthly budget targets, the application does not send email or desktop notifications when spending approaches or exceeds the budget limit.
- **Local CSV Storage Only:** Financial data is stored in local CSV files. The application does not currently support cloud synchronization, multi-user authentication, or a shared online database.

### Technical & Performance Issues

- **Re-rendering Delays:** Switching between filters, charts, and data tables may cause brief delays because Streamlit reruns the Python script when users interact with the interface.
- **Session State Limitations:** Unsaved data held in the active session may be lost if the application unexpectedly crashes or the session is interrupted before the data is saved to disk.

---

## 📌 Notes

- Make sure Python is installed on your computer before starting.
- Run all installation and application commands from the project directory.
- Keep your virtual environment activated while running the application.
- Ensure that financial data is saved properly to avoid losing unsaved changes.
- Confirm that the listed limitations accurately reflect the application's current functionality.

---

*Budget Buddy: Making personal finance tracking simple, clear, and manageable.*


