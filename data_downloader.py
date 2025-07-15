#!/usr/bin/env python3
"""
Data Downloader for DeFi Credit Scoring System
==============================================

This script helps download the transaction data from Google Drive.
Since direct Google Drive downloads can be tricky, this provides
helper functions and instructions.

Usage:
    python download_data.py
"""

import os
import requests
import zipfile
import json

def download_google_drive_file(file_id, destination):
    """
    Download a file from Google Drive using the file ID.
    
    Args:
        file_id (str): The Google Drive file ID
        destination (str): Local path to save the file
    """
    
    # Google Drive direct download URL
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    
    print(f"Downloading file to {destination}...")
    
    session = requests.Session()
    response = session.get(url, stream=True)
    
    # Handle the download confirmation for large files
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            params = {'id': file_id, 'confirm': value}
            response = session.get(url, params=params, stream=True)
            break
    
    # Save the file
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)
    
    print(f"Download completed: {destination}")

def extract_zip_file(zip_path, extract_to):
    """
    Extract a zip file to a specified directory.
    
    Args:
        zip_path (str): Path to the zip file
        extract_to (str): Directory to extract to
    """
    
    print(f"Extracting {zip_path} to {extract_to}...")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    
    print("Extraction completed")

def validate_json_file(json_path):
    """
    Validate that the JSON file is properly formatted and contains expected data.
    
    Args:
        json_path (str): Path to the JSON file
    
    Returns:
        bool: True if valid, False otherwise
    """
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("Error: JSON should contain a list of transactions")
            return False
        
        if len(data) == 0:
            print("Error: JSON file is empty")
            return False
        
        # Check required fields in first transaction
        required_fields = ['from', 'functionName', 'timeStamp', 'value', 'blockNumber']
        first_tx = data[0]
        
        missing_fields = [field for field in required_fields if field not in first_tx]
        if missing_fields:
            print(f"Error: Missing required fields: {missing_fields}")
            return False
        
        print(f"JSON file validated successfully!")
        print(f"- Total transactions: {len(data)}")
        print(f"- Unique wallets: {len(set(tx['from'] for tx in data))}")
        print(f"- Unique functions: {len(set(tx['functionName'] for tx in data))}")
        
        return True
        
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return False
    except Exception as e:
        print(f"Error validating JSON: {str(e)}")
        return False

def main():
    """
    Main function to download and prepare the data.
    """
    
    print("DeFi Credit Scoring - Data Downloader")
    print("=" * 50)
    
    # File IDs from the Google Drive links
    files = {
        "raw_json": {
            "id": "1ISFbAXxadMrt7Zl96rmzzZmEKZnyW7FS",
            "name": "user_transactions.json",
            "size": "~87MB"
        },
        "compressed": {
            "id": "14ceBCLQ-BTcydDrFJauVA_PKAZ7VtDor",
            "name": "user_transactions.zip",
            "size": "~10MB"
        }
    }
    
    print("Available files:")
    for key, info in files.items():
        print(f"  {key}: {info['name']} ({info['size']})")
    
    # Ask user which file to download
    choice = input("\nWhich file would you like to download? (raw_json/compressed): ").strip().lower()
    
    if choice not in files:
        print("Invalid choice. Please select 'raw_json' or 'compressed'")
        return
    
    file_info = files[choice]
    file_id = file_info["id"]
    filename = file_info["name"]
    
    # Download the file
    try:
        download_google_drive_file(file_id, filename)
        
        # If it's a zip file, extract it
        if filename.endswith('.zip'):
            extract_zip_file(filename, '.')
            json_filename = filename.replace('.zip', '.json')
        else:
            json_filename = filename
        
        # Validate the JSON file
        if os.path.exists(json_filename):
            if validate_json_file(json_filename):
                print(f"\n✅ Data ready! You can now run:")
                print(f"python credit_scorer.py {json_filename}")
            else:
                print("\n❌ Data validation failed. Please check the file.")
        else:
            print(f"\n❌ JSON file not found: {json_filename}")
            
    except Exception as e:
        print(f"\n❌ Download failed: {str(e)}")
        print("\nManual download instructions:")
        print("1. Go to the Google Drive link provided in the challenge")
        print("2. Download the file manually")
        print("3. Save it as 'user_transactions.json' in this directory")
        print("4. Run: python credit_scorer.py user_transactions.json")

if __name__ == "__main__":
    main()
