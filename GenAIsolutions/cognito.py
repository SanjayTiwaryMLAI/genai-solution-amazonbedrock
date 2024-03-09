
import boto3
from streamlit_cognito_auth import CognitoAuthenticator
import os, base64
import streamlit as st

pool_id = os.environ["POOL_ID"]
app_client_id = os.environ["APP_CLIENT_ID"]
app_client_secret = os.environ["APP_CLIENT_SECRET"]

authenticator = CognitoAuthenticator(
    pool_id=pool_id,
    app_client_id=app_client_id,
    app_client_secret=app_client_secret,
    use_cookies=False
)

import hmac
import hashlib

def calculate_secret_hash(client_secret, username, client_id):
    message = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'), 
                   msg = str(message).encode('utf-8'), 
                   digestmod = hashlib.sha256).digest()
    return base64.b64encode(dig).decode()


# Helper functions for Cognito integration
def get_cognito_client():
    client = boto3.client(
        "cognito-idp", 
        region_name="us-east-1"
    )
    return client

def sign_up(client, username, password):
    try:
        secret_hash = calculate_secret_hash(app_client_secret, username,app_client_id)
        print(secret_hash)
        resp = client.sign_up(
            ClientId=app_client_id,
            Username=username,
            Password=password,
            SecretHash =secret_hash
        )
        print(resp)
    except Exception as e:
        print(e)
        
def createuser(client, username, password):
    try:
        secret_hash = calculate_secret_hash(app_client_secret, username,app_client_id)
        print(secret_hash)
        resp = client.sign_up(
            ClientId=app_client_id,
            Username=username,
            Password=password,
            SecretHash =secret_hash
        )
        print(resp)
    except Exception as e:
        print(e)

def confirm_sign_up(client, username, code):
    try:
        resp = client.confirm_sign_up(
            ClientId=app_client_id,
            Username=username, 
            ConfirmationCode=code,
            SecretHash =app_client_secret
        )
        print(resp)
    except Exception as e:
        print(e)  



# is_logged_in = authenticator.login()
# if not is_logged_in:
#     st.stop()
    
# Secure the entire app with Auth 
def main():

    #authenticator.login()

    # User authenticated, run app
    #authenticated_user = authenticator.get_username()
    
    # Rest of Streamlit app
    import streamlit as st

    st.title("Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Sign Up"):
        client = get_cognito_client()
        sign_up(client, username, password)
        st.success("User created! Please check your email for a confirmation code.")
  

        # ```python
        st.title("Confirm Sign Up") 
        code = st.text_input("Confirmation Code")

        if st.button("Confirm"):
            client = get_cognito_client()
            confirm_sign_up(client, username, code)
            st.success("Confirmed!")
    # ```

    # The user enters their confirmation code from the email to confirm their account.

    # 3. Add routes or logic to switch between pages:

    # ```python 
    page = st.sidebar.selectbox("Choose page", ["Sign Up", "Confirm"])
    
    if page == "Sign Up":
        st.write("Sign Up")
    
    elif page == "Confirm":
        st.write("Confirm")
if __name__ == "__main__":
    main()

