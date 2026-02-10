# QR Code Generator

A flexible Python utility for generating QR codes for websites and contact information. Create professional QR codes with support for both interactive and command-line interfaces.

## Features

- 🌐 **Website QR Codes**: Generate QR codes that link to any URL
- 📱 **Contact QR Codes**: Create vCard QR codes with contact information (name, phone, email, website)
- 🎯 **Flexible Input**: Interactive mode or command-line arguments
- ⏰ **Auto-timestamped Files**: QR codes automatically save with timestamps or custom names
- ✅ **Well-Tested**: Comprehensive unit test suite included

## Installation

### Requirements

- Python 3.7+
- `qrcode` library
- `Pillow` (PIL) for image generation

### Setup

1. Clone or download this repository:
```bash
cd /Users/nathanaelminarik/Projects/utils/qrcode-generator
```

2. Install required dependencies:
```bash
pip install qrcode[pil]
```

## Usage

### 1. Interactive Mode (Recommended for Users)

Run the generator without arguments to enter interactive mode:

```bash
python generator.py
```

You'll see a menu:
```
=== QR Code Generator ===
Choose an option:
1. Generate Website QR Code
2. Generate Contact QR Code
3. Exit

Enter your choice (1-3): 
```

#### Example: Interactive Website QR Code

```bash
$ python generator.py

=== QR Code Generator ===
Choose an option:
1. Generate Website QR Code
2. Generate Contact QR Code
3. Exit

Enter your choice (1-3): 1
Enter website URL: https://www.nathanminarik.com
QR code saved to qrcode_20260210_124350.png
```

#### Example: Interactive Contact QR Code

```bash
$ python generator.py

=== QR Code Generator ===
Choose an option:
1. Generate Website QR Code
2. Generate Contact QR Code
3. Exit

Enter your choice (1-3): 2
--- Enter Your Contact Information ---
Full Name: Nathan Minarik
Phone Number: 703.868.7182
Email Address: nathanminarik@gmail.com
Website URL (optional, press Enter to skip): https://www.nathanminarik.com
QR code saved to contact_qrcode.png
```

### 2. Command-Line Mode (For Automation & Scripting)

Use command-line arguments for programmatic access and automation.

#### Website QR Code via Command Line

Generate a website QR code pointing to any URL:

```bash
python generator.py --type website --url "https://www.nathanminarik.com"
```

Output:
```
QR code saved to qrcode_20260210_124350.png
```

With custom output filename:

```bash
python generator.py --type website --url "https://www.nathanminarik.com" --output my_website.png
```

#### Contact QR Code via Command Line

Generate a contact QR code with complete contact information:

```bash
python generator.py --type contact \
  --name "Nathan Minarik" \
  --phone "703.868.7182" \
  --email "nathanminarik@gmail.com" \
  --website "https://www.nathanminarik.com"
```

Output:
```
QR code saved to contact_qrcode.png
```

With custom output filename:

```bash
python generator.py --type contact \
  --name "Nathan Minarik" \
  --phone "703.868.7182" \
  --email "nathanminarik@gmail.com" \
  --website "https://www.nathanminarik.com" \
  --output nathan_contact.png
```

#### Contact QR Code without Website (Optional Field)

```bash
python generator.py --type contact \
  --name "John Doe" \
  --phone "555-123-4567" \
  --email "john@example.com"
```

### 3. Programmatic Usage (Python API)

Import and use the functions directly in your Python code:

```python
from generator import generate_qr_code, generate_contact_vcard

# Generate a website QR code
generate_qr_code("https://www.example.com", "website_qr.png")

# Generate a contact QR code
vcard = generate_contact_vcard(
    name="Nathan Minarik",
    phone="703.868.7182",
    email="nathanminarik@gmail.com",
    url="https://www.nathanminarik.com"
)
generate_qr_code(vcard, "contact_qr.png")
```

## Command-Line Arguments

```
usage: generator.py [-h] [--type {website,contact}] [--url URL] [--name NAME]
                    [--phone PHONE] [--email EMAIL] [--website WEBSITE]
                    [--output OUTPUT]

Generate QR codes for websites and contact information

optional arguments:
  -h, --help            Show help message and exit
  --type {website,contact}
                        Type of QR code to generate
  --url URL             Website URL (for website QR codes)
  --name NAME           Full name (for contact QR codes)
  --phone PHONE         Phone number (for contact QR codes)
  --email EMAIL         Email address (for contact QR codes)
  --website WEBSITE     Website URL (for contact QR codes, optional)
  --output OUTPUT       Output file path (optional, auto-generated if not provided)
```

## API Reference

### `generate_qr_code(data: str, output_path: str = None) -> None`

Generate a QR code from data and save it to a file.

**Parameters:**
- `data` (str): The data to encode in the QR code (URL or vCard string)
- `output_path` (str, optional): File path where the QR code will be saved. If not provided, auto-generates filename with timestamp

**Example:**
```python
generate_qr_code("https://example.com", "my_qr.png")
```

### `generate_contact_vcard(name: str, phone: str, email: str, url: str = None) -> str`

Generate a vCard format string for contact information.

**Parameters:**
- `name` (str): Full name
- `phone` (str): Phone number (e.g., "703.868.7182" or "+1-555-123-4567")
- `email` (str): Email address
- `url` (str, optional): Website URL

**Returns:** vCard formatted string suitable for QR encoding

**Example:**
```python
vcard = generate_contact_vcard(
    name="Nathan Minarik",
    phone="703.868.7182",
    email="nathanminarik@gmail.com",
    url="https://www.nathanminarik.com"
)
print(vcard)
```

## Testing

Run the comprehensive unit test suite:

```bash
python -m unittest test_generator -v
```

The test suite includes:
- **vCard tests**: Format validation, field handling, special characters
- **QR code tests**: File generation, custom paths, auto-timestamp paths, PNG validation
- **Integration tests**: Real-world workflows

Expected output:
```
Ran 12 tests in 0.162s
OK
```

## Output Files

### Website QR Codes
- Default name: `qrcode_YYYYMMDD_HHMMSS.png`
- Custom name: Specify with `--output` flag
- When scanned, directs users to the specified URL

### Contact QR Codes
- Default name: `contact_qrcode.png`
- Custom name: Specify with `--output` flag
- When scanned on a smartphone, prompts user to add contact with all provided information

## Example Workflows

### Batch Generate Multiple Contact QR Codes

```bash
# Create QR codes for a team
python generator.py --type contact --name "Alice Smith" --phone "555-0001" --email "alice@company.com" --output alice_contact.png
python generator.py --type contact --name "Bob Johnson" --phone "555-0002" --email "bob@company.com" --output bob_contact.png
python generator.py --type contact --name "Carol White" --phone "555-0003" --email "carol@company.com" --output carol_contact.png
```

### Create QR Codes for Multiple Projects

```bash
# Generate QR codes for multiple websites
python generator.py --type website --url "https://project1.com" --output project1_qr.png
python generator.py --type website --url "https://project2.com" --output project2_qr.png
python generator.py --type website --url "https://project3.com" --output project3_qr.png
```

### Generate Your Personal Card QR Code

```bash
python generator.py --type contact \
  --name "Nathan Minarik" \
  --phone "703.868.7182" \
  --email "nathanminarik@gmail.com" \
  --website "https://www.nathanminarik.com" \
  --output nathanminarik_contact.png
```

Then print or display `nathanminarik_contact.png` on business cards or marketing materials!

## File Structure

```
qrcode-generator/
├── generator.py           # Main QR code generator module
├── test_generator.py      # Unit tests
├── README.md             # This file
└── *.png                 # Generated QR code files
```

## Use Cases

- **Business Cards**: Print contact QR codes on business cards
- **Networking Events**: Share your contact information instantly
- **Marketing**: Link QR codes on flyers/posters to websites
- **Automation**: Generate QR codes programmatically for large batches
- **Event Management**: Create attendee QR codes
- **Product Packaging**: Link to product information pages

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions:
1. Check that all dependencies are installed: `pip install qrcode[pil]`
2. Run the test suite to ensure everything works: `python -m unittest test_generator -v`
3. Verify your input data (URLs should include protocol, phone format should be valid)
