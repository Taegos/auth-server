# auth-server
Simple auth server that can be integrated in more complex systems, written in Python with Flask.

Supports
  - Account creation
  - Authentication 
  
 On a successful authentication attempt the server responds with an 'auth-token'.
 The token can be verified using a public key provided at the index (default http://127.0.0.1:5000/)
 In other words, other systems that 'trusts' this app can verify that a successful login attempt has occured.
 
