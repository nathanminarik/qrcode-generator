import qrcode
from pathlib import Path
from datetime import datetime
import argparse


def generate_contact_vcard(
    name: str,
    phone: str,
    email: str,
    url: str = None
) -> str:
    """
    Generate a vCard format string for contact information.
    
    Args:
        name: Full name
        phone: Phone number (format: XXX.XXX.XXXX or +1XXXXXXXXXX)
        email: Email address
        url: Website URL (optional)
    
    Returns:
        vCard formatted string
    """
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL:{phone}
EMAIL:{email}"""
    
    if url:
        vcard += f"\nURL:{url}"
    
    vcard += "\nEND:VCARD"
    return vcard


def generate_qr_code(data: str, output_path: str = None) -> None:
    """
    Generate a QR code from the given data and save it to a file.
    
    Args:
        data: The data to encode in the QR code
        output_path: The file path where the QR code image will be saved
    """
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"qrcode_{timestamp}.png"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    print(f"QR code saved to {output_path}")


def get_user_input_interactive() -> dict:
    """
    Interactively prompt the user for contact information.
    
    Returns:
        Dictionary containing user information
    """
    print("\n=== QR Code Generator ===")
    print("Choose an option:")
    print("1. Generate Website QR Code")
    print("2. Generate Contact QR Code")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        url = input("Enter website URL: ").strip()
        return {"type": "website", "url": url}
    
    elif choice == "2":
        print("\n--- Enter Your Contact Information ---")
        name = input("Full Name: ").strip()
        phone = input("Phone Number: ").strip()
        email = input("Email Address: ").strip()
        url = input("Website URL (optional, press Enter to skip): ").strip()
        
        return {
            "type": "contact",
            "name": name,
            "phone": phone,
            "email": email,
            "url": url if url else None
        }
    
    elif choice == "3":
        print("Exiting...")
        exit(0)
    
    else:
        print("Invalid choice. Please try again.")
        return get_user_input_interactive()


def main():
    """Main entry point for the QR code generator"""
    parser = argparse.ArgumentParser(
        description="Generate QR codes for websites and contact information"
    )
    parser.add_argument(
        "--type",
        choices=["website", "contact"],
        help="Type of QR code to generate"
    )
    parser.add_argument(
        "--url",
        help="Website URL (for website QR codes)"
    )
    parser.add_argument(
        "--name",
        help="Full name (for contact QR codes)"
    )
    parser.add_argument(
        "--phone",
        help="Phone number (for contact QR codes)"
    )
    parser.add_argument(
        "--email",
        help="Email address (for contact QR codes)"
    )
    parser.add_argument(
        "--website",
        help="Website URL (for contact QR codes, optional)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (optional, auto-generated if not provided)"
    )
    
    args = parser.parse_args()
    
    # If command-line arguments provided, use them
    if args.type:
        if args.type == "website":
            if not args.url:
                print("Error: --url is required for website QR codes")
                return
            generate_qr_code(args.url, args.output)
        
        elif args.type == "contact":
            if not all([args.name, args.phone, args.email]):
                print("Error: --name, --phone, and --email are required for contact QR codes")
                return
            contact_vcard = generate_contact_vcard(
                name=args.name,
                phone=args.phone,
                email=args.email,
                url=args.website
            )
            output_path = args.output if args.output else "contact_qrcode.png"
            generate_qr_code(contact_vcard, output_path)
    
    # Otherwise, use interactive mode
    else:
        user_data = get_user_input_interactive()
        
        if user_data["type"] == "website":
            generate_qr_code(user_data["url"], user_data.get("output"))
        
        elif user_data["type"] == "contact":
            contact_vcard = generate_contact_vcard(
                name=user_data["name"],
                phone=user_data["phone"],
                email=user_data["email"],
                url=user_data["url"]
            )
            output_path = user_data.get("output", "contact_qrcode.png")
            generate_qr_code(contact_vcard, output_path)


if __name__ == "__main__":
    main()
