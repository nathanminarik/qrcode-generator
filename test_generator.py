import unittest
import os
import tempfile
from pathlib import Path
from generator import generate_contact_vcard, generate_qr_code


class TestGenerateContactVcard(unittest.TestCase):
    """Test cases for generate_contact_vcard function"""
    
    def test_vcard_with_all_fields(self):
        """Test vCard generation with all fields including URL"""
        vcard = generate_contact_vcard(
            name="John Doe",
            phone="555-1234",
            email="john@example.com",
            url="https://example.com"
        )
        
        self.assertIn("BEGIN:VCARD", vcard)
        self.assertIn("END:VCARD", vcard)
        self.assertIn("VERSION:3.0", vcard)
        self.assertIn("FN:John Doe", vcard)
        self.assertIn("TEL:555-1234", vcard)
        self.assertIn("EMAIL:john@example.com", vcard)
        self.assertIn("URL:https://example.com", vcard)
    
    def test_vcard_without_url(self):
        """Test vCard generation without URL"""
        vcard = generate_contact_vcard(
            name="Jane Doe",
            phone="555-5678",
            email="jane@example.com"
        )
        
        self.assertIn("BEGIN:VCARD", vcard)
        self.assertIn("END:VCARD", vcard)
        self.assertIn("FN:Jane Doe", vcard)
        self.assertIn("TEL:555-5678", vcard)
        self.assertIn("EMAIL:jane@example.com", vcard)
        self.assertNotIn("URL:", vcard)
    
    def test_vcard_format_structure(self):
        """Test that vCard has correct structure"""
        vcard = generate_contact_vcard(
            name="Test User",
            phone="123-456-7890",
            email="test@example.com",
            url="https://test.com"
        )
        
        lines = vcard.strip().split('\n')
        self.assertEqual(lines[0], "BEGIN:VCARD")
        self.assertEqual(lines[-1], "END:VCARD")
    
    def test_vcard_with_special_characters(self):
        """Test vCard handles special characters in name"""
        vcard = generate_contact_vcard(
            name="José García",
            phone="555-1234",
            email="jose@example.com"
        )
        
        self.assertIn("José García", vcard)
    
    def test_nathan_contact_vcard(self):
        """Test generation of Nathan's contact vCard"""
        vcard = generate_contact_vcard(
            name="Nathan Minarik",
            phone="703.868.7182",
            email="nathanminarik@gmail.com",
            url="https://www.nathanminarik.com"
        )
        
        self.assertIn("FN:Nathan Minarik", vcard)
        self.assertIn("TEL:703.868.7182", vcard)
        self.assertIn("EMAIL:nathanminarik@gmail.com", vcard)
        self.assertIn("URL:https://www.nathanminarik.com", vcard)


class TestGenerateQRCode(unittest.TestCase):
    """Test cases for generate_qr_code function"""
    
    def setUp(self):
        """Set up temporary directory for test files"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary files"""
        for file in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_dir)
    
    def test_qr_code_with_custom_path(self):
        """Test QR code generation with custom output path"""
        output_path = os.path.join(self.temp_dir, "test_qrcode.png")
        generate_qr_code("https://example.com", output_path)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 0)
    
    def test_qr_code_with_auto_path(self):
        """Test QR code generation with auto-generated path"""
        original_dir = os.getcwd()
        try:
            os.chdir(self.temp_dir)
            generate_qr_code("https://example.com")
            
            # Check that a file matching the pattern was created
            files = [f for f in os.listdir(self.temp_dir) if f.startswith("qrcode_") and f.endswith(".png")]
            self.assertEqual(len(files), 1)
            self.assertGreater(os.path.getsize(files[0]), 0)
        finally:
            os.chdir(original_dir)
    
    def test_qr_code_with_vcard_data(self):
        """Test QR code generation with vCard data"""
        output_path = os.path.join(self.temp_dir, "contact_qrcode.png")
        vcard = generate_contact_vcard(
            name="Test User",
            phone="555-1234",
            email="test@example.com"
        )
        generate_qr_code(vcard, output_path)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 0)
    
    def test_qr_code_with_url_data(self):
        """Test QR code generation with URL data"""
        output_path = os.path.join(self.temp_dir, "url_qrcode.png")
        generate_qr_code("https://www.nathanminarik.com", output_path)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 0)
    
    def test_qr_code_file_is_png(self):
        """Test that generated QR code is a valid PNG"""
        output_path = os.path.join(self.temp_dir, "test.png")
        generate_qr_code("test data", output_path)
        
        # PNG files start with specific bytes
        with open(output_path, 'rb') as f:
            header = f.read(8)
            # PNG signature: 137 80 78 71 13 10 26 10
            self.assertEqual(header, b'\x89PNG\r\n\x1a\n')


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def setUp(self):
        """Set up temporary directory for test files"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary files"""
        for file in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_dir)
    
    def test_website_qr_code_generation(self):
        """Test generating website QR code"""
        output_path = os.path.join(self.temp_dir, "website_qr.png")
        generate_qr_code("https://www.nathanminarik.com", output_path)
        
        self.assertTrue(os.path.exists(output_path))
    
    def test_contact_qr_code_generation(self):
        """Test generating contact QR code"""
        output_path = os.path.join(self.temp_dir, "contact_qr.png")
        vcard = generate_contact_vcard(
            name="Nathan Minarik",
            phone="703.868.7182",
            email="nathanminarik@gmail.com",
            url="https://www.nathanminarik.com"
        )
        generate_qr_code(vcard, output_path)
        
        self.assertTrue(os.path.exists(output_path))


if __name__ == "__main__":
    unittest.main()
