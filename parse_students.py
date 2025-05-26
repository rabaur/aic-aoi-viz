from bs4 import BeautifulSoup
import re

def parse_student_info(html_file):
    """
    Parse the ETH AI Center doctoral students webpage and extract student names and research interests.
    
    Args:
        html_file (str): Path to the HTML file
        
    Returns:
        dict: Dictionary with student names as keys and lists of research interests as values
    """
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Initialize dictionary to store results
    student_info = {}
    
    # Find all text-image divs that contain student information
    student_divs = soup.find_all('div', class_='text-image')
    
    for div in student_divs:
        # Find the name (it's in a bold paragraph)
        name_elem = div.find('b')
        if not name_elem:
            continue
            
        name = name_elem.text.strip()
        
        # Find the research interests (it's in the last paragraph)
        paragraphs = div.find_all('p')
        if len(paragraphs) < 2:  # Need at least 2 paragraphs (name and interests)
            continue
            
        # Get the last paragraph which contains research interests
        interests_text = paragraphs[-1].text.strip()
        
        # Split interests by comma and clean up
        interests = [interest.strip() for interest in interests_text.split(',')]
        
        # Add to dictionary
        student_info[name] = interests
    
    return student_info

if __name__ == "__main__":
    # Example usage
    html_file = "data/doctoral-fellows.html"
    students = parse_student_info(html_file)
    
    # Print example for Anej Svete
    print("Example for Raphaël Baur:")
    print(students.get("Raphaël Baur", [])) 