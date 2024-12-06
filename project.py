import pyttsx3
import pyfiglet
import PyPDF2
import emoji
from tabulate import tabulate
  
# Initialize the text-to-speech engine
engine = pyttsx3.init()

def read_single_page(pdf_reader):
    while True:  # Start an infinite loop to keep asking for input until a valid page number is entered
        try:
            # Prompt the user to enter a page number
            page_number = int(input("\nEnter page number you want to read: "))
            
            # Check if the entered page number is within the valid range of pages in the PDF
            if page_number < 1 or page_number > len(pdf_reader.pages):
                print(f"\033[91mThe page number {page_number} is not in this PDF.\033[0m\n")
                continue  # Continue the loop to ask for input again
            
            else:
                # Get the specific page (adjusting for zero-based indexing)
                nth_page = pdf_reader.pages[page_number - 1]
                
                # Print a message indicating which page is being read
                print(f"reading the PDF Page {page_number}...", end="", flush=True)
                
                # Extract text from the specified page
                text = nth_page.extract_text()
                
                # Use the text-to-speech engine to read the extracted text aloud
                engine.say(text)
                engine.runAndWait()
                
                # Print a message indicating the page was read successfully
                print("read successfully.\n")
                
                break  # Exit the loop after successfully reading the page

        except ValueError:
            # Handle the case where the input is not a valid integer
            print("\033[91mInvalid input. Please enter a valid page number.\033[0m\n")
            continue  # Continue the loop to ask for input again


def read_all_pages(pdf_reader):
    print("reading the PDF...", end="", flush=True)  # Print the initial message without a newline, flush the output buffer to ensure the message is displayed immediately
    
    counter = 0  # Initialize a counter to keep track of the current page number
    
    for page in pdf_reader.pages:  # Iterate through all the pages in the PDF
        text = page.extract_text()  # Extract text from the current page
        
        counter = counter + 1  # Increment the page counter
        print(f"Page {counter}...", end="", flush=True)  # Print the current page number, without a newline, and flush the output buffer
        
        engine.say(text)  # Use the text-to-speech engine to read the extracted text aloud
        engine.runAndWait()  # Wait for the text-to-speech engine to finish reading the current page before moving on to the next one
    
    print("read successfully.\n")  # Print a message indicating that all pages have been read successfully


def read_custom_page(pdf_reader):
    while True:  # Start an infinite loop to repeatedly prompt the user for input until valid pages are provided
        try:
            # Prompt the user to enter the start and end pages
            start_page = int(input("\nEnter the page you want to start reading: "))
            end_page = int(input("Enter the page you want to end reading: "))

            # Check if the entered page numbers are within the valid range of pages in the PDF
            if start_page < 1 or end_page < 1 or start_page > len(pdf_reader.pages) or end_page > len(pdf_reader.pages):
                print(f"\033[91mThe page number {start_page} or {end_page} is not in this PDF.\033[0m\n")
                continue  # Continue the loop to ask for input again

            # Check if the start page is greater than the end page
            if start_page > end_page:
                print("\033[91mStart page cannot be greater than end page.\033[0m\n")
                continue  # Continue the loop to ask for input again

            print("reading the PDF...", end="", flush=True)  # Print the initial message without a newline, flush the output buffer to ensure the message is displayed immediately
            
            # Iterate through the range of pages specified by the user
            for page_index in range(start_page - 1, end_page):
                page = pdf_reader.pages[page_index]  # Get the specific page (adjusting for zero-based indexing)
                text = page.extract_text()  # Extract text from the current page
                
                print(f"Page {page_index + 1}...", end="", flush=True)  # Print the current page number, without a newline, and flush the output buffer
                
                engine.say(text)  # Use the text-to-speech engine to read the extracted text aloud
                engine.runAndWait()  # Wait for the text-to-speech engine to finish reading the current page before moving on to the next one

            print("read successfully.\n")  # Print a message indicating that all pages in the specified range have been read successfully
            break  # Exit the loop after successfully reading the pages

        except ValueError:
            # Handle the case where the input is not a valid integer
            print("\033[91mInvalid input. Please enter a valid page number.\033[0m\n")
            continue  # Continue the loop to ask for input again



def main():
    # Display the program title using pyfiglet
    print(pyfiglet.figlet_format("PyPDF Reader 1.0"))

    # Start an infinite loop to repeatedly prompt for PDF file path
    while True:
        try:
            # Path to the PDF file
            pdf_path = input("Enter PDF(name/path) or 'exit' to quit: ")

            if pdf_path.endswith(".pdf"):
                # Open the PDF file
                with open(pdf_path, "rb") as file:
                    # Initialize the PDF reader
                    pdf_reader = PyPDF2.PdfReader(file)

                    # Define the menu options
                    menu = [[1, "Read Full PDF"],
                            [2, "Read Single PDF Page"],
                            [3, "Read Custom PDF page(m to n)"]]
                    # Print the menu using the tabulate module
                    print("\n" + tabulate(menu, headers=["#", "Functionalities"], tablefmt="outline") + "\n")

                    # Start an inner loop to handle user menu selection
                    while True:
                        button = input(f"\nEnter button(ex. Press 1 {emoji.emojize(':right_arrow_curving_left:')}  for reading full page) or 'exit' to go back: ")

                        if button.lower() == "exit":  # Exit option to break out of the loop
                            print("You have returned to main. Enter a name or path of a PDF or 'exit' to exit the program")
                            break  # Exit the program

                        try:
                            button = int(button)  # Convert the input to an integer

                            if button == 1:
                                # Call the function to read all pages of the PDF
                                read_all_pages(pdf_reader)
                                break

                            elif button == 2:
                                # Call the function to read a single page of the PDF
                                read_single_page(pdf_reader)
                                break

                            elif button == 3:
                                # Call the function to read a custom range of pages from the PDF
                                read_custom_page(pdf_reader)
                                break

                            else:
                                # If the input is not a valid menu option, prompt the user again
                                print("Please enter option from the menu only (1, 2 or 3)")
                                continue

                        except ValueError:
                            # Handle the case where the input is not a valid integer
                            print("\033[91mInvalid input. Please enter a number from the menu or 'exit'.\033[0m\n")
                            continue
            
            elif pdf_path.lower() == "exit": 
                #breaking the main while loop
                print(f"Sayonara. See you soon {emoji.emojize(':wave:', language='alias')}\n")
                break

            else:
                # If the provided file is not a PDF, prompt the user again
                print("\033[91mPlease enter a PDF file\033[0m\n")

        except FileNotFoundError:
            # Handle the case where the PDF file is not found
            print(f"\033[91mFile does not exist. Try to run the file copying to this folder. Peace {emoji.emojize(':relieved_face:')}\033[0m\n")
            continue

    
if __name__ == "__main__":
    main()