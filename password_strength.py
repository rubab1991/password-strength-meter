import streamlit as st
import re
import random
import string

# Common weak passwords blacklist
BLACKLIST = {"password123", "123456", "qwerty", "admin", "letmein", "welcome", "password"}

def generate_strong_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))

def check_password_strength(password):
    score = 0
    feedback = []
    
    if password in BLACKLIST:
        return 0, ["This password is too common. Please choose a more secure one."]
    
    # Custom scoring weights
    length_weight = 2 if len(password) >= 12 else 1 if len(password) >= 8 else 0
    uppercase_weight = 1 if re.search(r'[A-Z]', password) else 0
    lowercase_weight = 1 if re.search(r'[a-z]', password) else 0
    digit_weight = 1 if re.search(r'\d', password) else 0
    special_weight = 2 if re.search(r'[!@#$%^&*]', password) else 0
    
    score = length_weight + uppercase_weight + lowercase_weight + digit_weight + special_weight
    
    if length_weight == 0:
        feedback.append("Increase the length to at least 8 characters.")
    if uppercase_weight == 0:
        feedback.append("Add at least one uppercase letter.")
    if lowercase_weight == 0:
        feedback.append("Add at least one lowercase letter.")
    if digit_weight == 0:
        feedback.append("Include at least one number (0-9).")
    if special_weight == 0:
        feedback.append("Use at least one special character (!@#$%^&*).")
    
    return score, feedback

def main():
    st.title("🔐 Password Strength Meter & Generator")
    
    password = st.text_input("Enter your password:", type="password")
    
    if password:
        score, feedback = check_password_strength(password)
        
        if score <= 2:
            st.error("Password Strength: Weak 🔴")
        elif score <= 4:
            st.warning("Password Strength: Moderate 🟡")
        else:
            st.success("Password Strength: Strong 🟢")
        
        if feedback:
            st.subheader("Suggestions to Improve:")
            for tip in feedback:
                st.write(f"- {tip}")
    
    if st.button("Generate Strong Password"):
        strong_password = generate_strong_password()
        st.text_input("Suggested Strong Password:", strong_password, type="default")

if __name__ == "__main__":
    main()
