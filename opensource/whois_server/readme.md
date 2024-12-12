# WHOIS Server
A simple and lightweight WHOIS server

For example, in an RFC 1036 client, you can query a domain name using the command `whois -h whois.us.kg "domainname"`, provided that `whois.us.kg` points to a WHOIS server and port 43 is open. This is just a basic code (we use this)—you’ll need to implement your own database and related functionality.

In the provided code, the `get_whois` function is used to retrieve WHOIS data as plain text from the server. You’ll need to implement this function yourself.