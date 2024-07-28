# This is a simple demo made for educational purposes
# Please note that BlazeInferno64 is not responsible for any misuse of this file!
import zipfile
import logging
import os
import urllib.parse
import requests
import time

logging.basicConfig(level=logging.INFO)

def get_input(prompt: str, check_func: callable) -> str:
    while True:
        user_input = input(prompt)
        if check_func(user_input):
            return user_input
        else:
            logging.error("Error: Invalid Input!")

def check_for_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
def download_password_list(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open("password_lists.txt", "w", encoding="utf-8") as file:
            file.write(response.text)
        logging.info(f"\nSuccessfully downloaded the password list from url: {url} and saved it to the current working directory as 'password_lists.txt'\n")
        return "password_lists.txt"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading password list from {url}: {e}\n")
        return None
    
def download_zip_file(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open("zipfile.zip", "wb") as file:
            file.write(response.content)
        logging.info(f"\nSuccessfully downloaded the password list from url: {url} and saved it to the current working directory as 'password_lists.txt'\n")
        return "password_lists.txt"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading password list from {url}: {e}\n")
        return None
        

def check_zip_file(zip_file: str) -> bool:
    if check_for_url(zip_file):
        return True
    else:
        return os.path.exists(zip_file) and zipfile.is_zipfile(zip_file)

def check_password_list(password_list: str) -> bool:
    if(check_for_url(password_list)):
        return True
    else:
        return os.path.exists(password_list) and os.path.isfile(password_list)

def check_extraction_dir(extract_dir: str) -> bool:
    return os.path.exists(extract_dir) and os.path.isdir(extract_dir) and os.access(extract_dir, os.W_OK)

def create_extraction_dir(extract_dir: str) -> bool:
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

def crack_zip_password(zip_file: str, password_list: str, extract_dir: str, encoding: str = "utf-8") -> str:
    try:
        with zipfile.ZipFile(zip_file) as zip_ref:
            with open(password_list, "r", encoding=encoding) as f:
                for line_num, password in enumerate(f, start=1):
                    password = password.strip()
                    if not password:
                        logging.warning(f"Skipping empty password on line: {line_num}!")
                        continue
                    try:
                        zip_ref.extractall(extract_dir, pwd=password.encode())
                        return password
                    except RuntimeError as e:
                        logging.error(f"Error checking password '{password}' on line {line_num}: {e}")
                    except Exception as e:
                        logging.error(f"Error on line ${line_num}: ${e}")
    except zipfile.BadZipFile as e:
        logging.error(f"Error: Bad zip file - {e}!")
    except zipfile.LargeZipFile as e:
        logging.error(f"Error: Zip file is too large - {e}!")
    except FileNotFoundError:
        logging.error("Error: File not found!")
    except PermissionError:
        logging.error(f"Error: Permission denied!")
    except Exception as e:
        logging.error(f"Error: {e}")
    return None

def main():
    zip_file = get_input("Enter the zip file location: ", check_zip_file)
    password_list_input = get_input("Enter the password list location: ", check_password_list)

    if check_for_url(zip_file):
        zipFile = download_zip_file(zip_file)
        if zipFile is None:
            return
    else:
        zipFile = zip_file
    
    if check_for_url(password_list_input):
        password_list = download_password_list(password_list_input)
        if password_list is None:
            return
    else:
        password_list = password_list_input

    extract_dir = input("Enter the extraction directory (default: current working directory): ")
    if not extract_dir:
        extract_dir = os.getcwd()
    
    create_extraction_dir(extract_dir)

    if not check_extraction_dir(extract_dir):
        logging.error("Error: Extraction directory is writable!")
        return
    
    cracked_password = crack_zip_password(zipFile, password_list, extract_dir)
    if cracked_password is not None:
        print(f"\nPassword cracked: {cracked_password}\n")
        print("Finishing up everything...")
        time.sleep(5)
    else:
        logging.error("Failed to crack password!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.error(f"\nError: Keyboard Interrupt error!\n")