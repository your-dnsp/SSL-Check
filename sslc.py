import ssl
import socket
from datetime import datetime
import dns.resolver
import dns.reversename
from urllib.parse import urlparse

def get_domain_from_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme:
        return parsed_url.netloc
    else:
        return parsed_url.path  # Assumes the user might input a domain without a scheme

def check_ssl_certificate(domain):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
    
    conn.settimeout(10.0)
    
    try:
        conn.connect((domain, 443))
        ssl_info = conn.getpeercert()
        
        expiration_date = datetime.strptime(ssl_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
        print(f"Certificate for {domain} expires on {expiration_date}")
        
        if expiration_date < datetime.now():
            print("The SSL certificate has expired.")
        else:
            print("The SSL certificate is valid.")
    except Exception as e:
        print(f"An error occurred while checking SSL certificate for {domain}: {e}")
    finally:
        conn.close()

def check_dns_configuration(domain):
    try:
        for qtype in ('A', 'AAAA'):
            answer = dns.resolver.resolve(domain, qtype, raise_on_no_answer=False)
            if answer.rrset is not None:
                print(f"{qtype} records for {domain}:")
                for data in answer:
                    print(f"- {data}")
            else:
                print(f"No {qtype} records found for {domain}.")
    except Exception as e:
        print(f"DNS lookup error for {domain}: {e}")

def reverse_dns_lookup(ip_address):
    try:
        addr = dns.reversename.from_address(ip_address)
        answers = dns.resolver.resolve(addr, "PTR")
        for rdata in answers:
            print(f"The reverse lookup for IP {ip_address} is: {rdata.target}")
    except Exception as e:
        print(f"Could not resolve {ip_address}: {e}")

def main():
    user_input = input("Please enter the URL of the website: ")
    domain = get_domain_from_url(user_input)
    if domain:
        print(f"\nChecking SSL certificate and DNS configuration for {domain}...")
        check_ssl_certificate(domain)
        check_dns_configuration(domain)
        
        print("\nPerforming reverse DNS lookups for the domain's IP addresses...")
        try:
            for qtype in ('A', 'AAAA'):
                answer = dns.resolver.resolve(domain, qtype, raise_on_no_answer=False)
                if answer.rrset is not None:
                    for data in answer:
                        reverse_dns_lookup(str(data))
        except Exception as e:
            print(f"Could not perform reverse DNS lookup for {domain}: {e}")
    else:
        print("Invalid URL provided.")

if __name__ == "__main__":
    main()
