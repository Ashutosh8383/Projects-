Secure Messaging System Using AES Encryption, HMAC Integrity Verification, and User Authentication
Project Overview
This project is a Secure Messaging System developed in Python to demonstrate the core principles of software security:
•	Confidentiality
•	Integrity
•	Authentication

The system allows registered users to securely exchange encrypted messages while ensuring message integrity and protecting against unauthorized access.
Features
User Authentication
•	User Registration
•	User Login
•	SHA-256 Password Hashing
•	Brute Force Protection (Account Locking)

Secure Messaging
•	AES Encryption using Fernet
•	Secure Message Storage
•	Message Decryption for Authorized Users

Integrity Verification
•	HMAC-SHA256 Message Verification
•	Detection of Message Tampering

Attack Simulation
•	Man-in-the-Middle (MITM) Attack Demonstration
•	Replay Attack Demonstration

Logging
•	Login Logs
•	Registration Logs
•	Message Logs
•	Security Event Logs

Technologies Used
•	Python 3.x
•	Tkinter
•	SQLite
•	Cryptography Library
•	hashlib
•	hmac

Project Structure
SecureMessagingSystem/
•	app.py
•	auth.py
•	crypto_utils.py
•	database.py
•	messaging.py
•	attack_simulation.py
•	logger_util.py
•	requirements.txt
•	README.md
data/
•	users.db
•	secret.key
•	logs.txt

Installation
1.	Install Python
2.	Install required package
3.  pip install cryptography
4.	Run the application
python app.py

Security Mechanisms
Confidentiality
Messages are encrypted using AES encryption through the Fernet module.

Integrity
HMAC-SHA256 is used to verify message integrity and detect unauthorized modifications.

Authentication
Passwords are hashed using SHA-256 before storage.

Secure Key Management
Encryption keys are generated dynamically and stored securely in a key file.

Future Enhancements
•	Multi-user communication
•	Digital signatures
•	Email notifications
•	Cloud deployment
•	Advanced intrusion detection

Author
Ashutosh Patil 
Software Security Project
