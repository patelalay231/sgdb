# sgdb: AI-powered GDB Extension
## Simplified Setup

The `sgdb` script has been updated to handle all setup tasks automatically. You no longer need to manually create or activate the Python virtual environment or install dependencies. The script will take care of everything for you.

### Steps:
1. **Set the env file:**
   - rename file .env.example with .env 
   - get and set the API keys 
2. **Run the `sgdb` script:**
   ```bash
   ./sgdb <executable> [gdb options]
   ```

This script will automatically:
- Create the Python virtual environment if it doesn't exist.
- Activate the virtual environment.
- Install the required Python packages.
- Launch the application with the AI extension loaded.

You can also add `sgdb` to your PATH for global access:
```bash
sudo cp sgdb /usr/local/bin/
```

Once added to your PATH, you can run `sgdb` from anywhere:
```bash
sgdb <executable> [gdb options]
```

## Getting Started

To set up the project manually for development or testing, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd sgdb
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the project:**
   ```bash
   ./sgdb <executable> [gdb options]
   ```

## Project Structure
- `sgdb` — Launcher script
- `env/` — Python virtual environment
- `requirements.txt` — Python dependencies
- `src/gdb_ai.py` — Main GDB AI extension

## Contributing

We welcome contributions! To contribute, follow these steps:

1. **Fork the repository** and clone your fork.
2. **Set up the project** using the steps in the "Getting Started" section.
3. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b my-feature-branch
   ```

4. **Make your changes** and commit them:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

5. **Push your branch** to your fork:
   ```bash
   git push origin my-feature-branch
   ```

6. **Submit a pull request** to the main repository.


## Notes
- The `sgdb` script will automatically handle the setup tasks before launching GDB.

