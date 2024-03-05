import subprocess

def run_streamlit_app(port):
    # Define the command to run the Streamlit app
    command = ["streamlit", "run", "WelcomePage.py", "--server.port", str(port)]  # Replace "your_app.py" with the path to your Streamlit app script
    
    # Run the Streamlit app using subprocess
    subprocess.run(command)

if __name__ == "__main__":
    port = 8080
    run_streamlit_app(port)
