SECURE MESSAGING SYSTEM USING AES ENCRYPTION, HMAC INTEGRITY VERIFICATION, AND USER AUTHENTICATION
ABSTRACT
The Secure Messaging System is designed to provide secure communication between users while maintaining confidentiality, integrity, and authentication. The system uses AES encryption for message confidentiality, HMAC-SHA256 for integrity verification, and SHA-256 password hashing for secure authentication. The application includes user registration, login functionality, encrypted messaging, attack simulation, and logging mechanisms. The project demonstrates practical implementation of software security principles and protection against common cyber attacks.
Keywords: AES, HMAC, SHA-256, Authentication, Confidentiality, Integrity, Secure Messaging.
________________________________________
1. INTRODUCTION
With the rapid growth of digital communication, securing sensitive information has become essential. Cyber threats such as unauthorized access, message tampering, and identity theft pose significant risks to communication systems.
This project implements a secure messaging application that ensures:
•	Confidentiality
•	Integrity
•	Authentication
The system allows users to exchange encrypted messages while preventing unauthorized modifications.
________________________________________
2. OBJECTIVES
The primary objectives of the project are:
•	Develop a secure messaging platform.
•	Implement user authentication.
•	Encrypt messages using AES.
•	Verify message integrity using HMAC.
•	Demonstrate attack detection mechanisms.
•	Maintain security logs.
________________________________________
3. SYSTEM REQUIREMENTS
Hardware Requirements
•	Processor: Intel Core i3 or above
•	RAM: 4 GB or above
•	Storage: 500 MB free space
Software Requirements
•	Python 3.x
•	VS Code
•	SQLite
•	Cryptography Library
•	Tkinter
________________________________________
4. SYSTEM DESIGN
The system consists of the following modules:
User Authentication Module
Handles registration and login.
Encryption Module
Encrypts messages before storage.
Integrity Verification Module
Generates and verifies HMAC values.
Messaging Module
Manages sending and receiving messages.
Attack Simulation Module
Demonstrates MITM and replay attacks.
Logging Module
Records security events and activities.
________________________________________
5. IMPLEMENTATION
Password Hashing
Passwords are converted into SHA-256 hashes before storage.
AES Encryption
Messages are encrypted using Fernet, which provides AES-based encryption.
HMAC Verification
HMAC-SHA256 verifies message authenticity and detects tampering.
Logging
All important security events are stored in logs.txt.
________________________________________
6. ATTACK SIMULATION
Man-in-the-Middle Attack
An attacker modifies a message during transmission.
Result: The HMAC verification fails, and the system detects tampering.
Replay Attack
An attacker resends a previously transmitted message.
Result: The system identifies duplicate communication attempts.
Brute Force Attack
Multiple incorrect login attempts are performed.
Result: The account is temporarily locked after exceeding the maximum allowed attempts.
________________________________________
7. RESULTS
The system successfully:
•	Registered users securely.
•	Authenticated users.
•	Encrypted messages.
•	Verified message integrity.
•	Detected attack attempts.
•	Generated security logs.
________________________________________
8. ADVANTAGES
•	Secure communication.
•	Strong encryption.
•	Integrity protection.
•	User authentication.
•	Easy-to-use interface.
________________________________________
9. LIMITATIONS
•	Local deployment only.
•	No digital signatures.
•	Single-device operation.
________________________________________
10. FUTURE ENHANCEMENTS
•	Cloud deployment.
•	Multi-factor authentication.
•	Digital signatures.
•	Blockchain-based logging.
•	Mobile application support.
________________________________________
11. CONCLUSION
The Secure Messaging System successfully demonstrates the implementation of software security concepts. By integrating AES encryption, HMAC verification, user authentication, and attack simulation, the project provides a practical approach to securing digital communications. The developed system meets the fundamental requirements of confidentiality, integrity, and authentication and serves as a useful educational model for secure software development.
________________________________________
REFERENCES
1.	Python Documentation
2.	Cryptography Library Documentation
3.	NIST Cryptographic Standards
4.	OWASP Security Guidelines
5.	Software Security Principles and Practices
