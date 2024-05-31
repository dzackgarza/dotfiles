#!/usr/bin/python

import os
import subprocess
import requests
import sys

anki_url = "http://localhost:8765"
apkg_output_dir = "/home/dzack/flashcards"


def search_flashcard(directory):
    try:
        with open(directory, 'r') as file:
            for line in file:
                if 'flashcard:' in line:
                    return True
        return False
    except FileNotFoundError:
        print("File not found.")
        return False

def list_files(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths

def change_extension_to_apkg(file_path):
    # print("Changing " + file_path)
    # Split the file path into directory and filename
    directory, filename = os.path.split(file_path)
    # Split the filename into name and extension
    name, extension = os.path.splitext(filename)
    # Change the extension to 'apkg'
    new_extension = '.apkg'
    # Construct the new file path
    new_file_path = os.path.join(apkg_output_dir, name + new_extension)
    # print("New path: " + new_file_path)
    return new_file_path

def run_external_program(arg1, arg2):
    print(arg1 + " ----> " + arg2)
    try:
        # Replace 'program_name' with the name of the external program you want to run
        subprocess.run(['lists_to_anki.py', arg1, arg2], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def walk_dir_for_flashcards(directory_path):
    all_file_paths = list_files(directory_path)
    markdown_files = filter(lambda name: ".md" in name, all_file_paths)
    flashcard_files = filter(lambda name: search_flashcard(name), markdown_files)
    in_out_name_tuples = []
    for file_path in flashcard_files:
        apkg_out = change_extension_to_apkg(file_path)
        in_out_name_tuples.append( (file_path, apkg_out) )
    return in_out_name_tuples


# def import_deck() -> None:
def import_deck(deck_name):
    deck_path = apkg_output_dir + "/" + deck_name
    payload = {
        "action": "importPackage",
        "version": 6,
        "params": {
            "path": deck_path
        }
    }

    try:
        response = requests.post(anki_url, json=payload)
        response.raise_for_status()
        print("Deck imported successfully: " + deck_name)
        # print(response.json())
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        sys.exit(1)

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python program_name.py directory")
        sys.exit(1)

    # Extract the directory argument
    directory = sys.argv[1]

    # Print the directory argument
    print("Directory:", directory)
    in_outs = walk_dir_for_flashcards(directory)
    for a,b in in_outs:
        run_external_program(a, b)

    apkg_files = [file for file in os.listdir(apkg_output_dir) if file.endswith(".apkg")]
    # print(apkg_files)
    for pkg in apkg_files:
        import_deck(pkg)
    
if __name__ == "__main__":
    main()
