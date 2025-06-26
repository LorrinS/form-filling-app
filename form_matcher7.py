from difflib import SequenceMatcher
import fitz
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import re

llm = OllamaLLM(model="llama3.1:8b")

def validate_data_type(value, expected_type):
    """Validate if a value matches the expected data type"""
    value = str(value).strip()
    
    if expected_type == "name":
        # Should contain letters and possibly spaces/hyphens
        return bool(re.match(r'^[A-Za-z\s\-\.\']+$', value)) and len(value) > 1
    
    elif expected_type == "email":
        # Basic email validation
        return bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', value))
    
    elif expected_type == "phone":
        # Should contain mostly digits, possibly with separators
        digits_only = re.sub(r'[^\d]', '', value)
        return len(digits_only) >= 7 and len(digits_only) <= 15
    
    elif expected_type == "address":
        # Should contain numbers and letters
        return bool(re.search(r'\d', value)) and bool(re.search(r'[A-Za-z]', value))
    
    elif expected_type == "date":
        # Should match date patterns
        return bool(re.match(r'\d{1,2}[/\-]\d{1,2}[/\-]\d{4}', value))
    
    elif expected_type == "number":
        # Should be mostly digits
        return bool(re.match(r'^\d+$', value))
    
    elif expected_type == "city":
        # Should be letters, spaces, possibly apostrophes
        return bool(re.match(r'^[A-Za-z\s\'\.]+$', value)) and len(value) > 1
    
    elif expected_type == "postal_code":
        # Canadian postal code or US zip
        return bool(re.match(r'^[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d$|^\d{5}(-\d{4})?$', value))
    
    return True  # Default to True for unknown types

def extract_name_parts(full_name):
    """Extract first, middle, and last names from a full name"""
    if not full_name or not isinstance(full_name, str):
        return "", "", ""
    
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0], "", ""
    elif len(parts) == 2:
        return parts[0], "", parts[1]
    elif len(parts) >= 3:
        return parts[0], " ".join(parts[1:-1]), parts[-1]
    else:
        return "", "", ""

def determine_field_type_and_validate(field_description, value=""):
    """Use AI to determine what type of data a field expects"""
    prompt = ChatPromptTemplate.from_template(
        "Analyze this form field to determine what type of data it expects.\n\n"
        "Field description/context: '{field_description}'\n\n"
        "What type of data should this field contain? Choose the most specific option:\n"
        "- first_name\n"
        "- middle_name\n"
        "- last_name\n"
        "- full_name\n"
        "- email\n"
        "- phone\n"
        "- address (street address)\n"
        "- city\n"
        "- postal_code\n"
        "- occupancy_date\n"
        "- unit_number\n"
        "- name (general name field)\n"
        "- other\n\n"
        "Return only the field type (e.g., 'first_name' or 'email'):"
    )
    
    result = llm.invoke(prompt.format(field_description=field_description)).strip().lower()
    return result

def categorize_extracted_data(filled_fields):
    """Categorize extracted data by type with better organization"""
    data_by_type = {
        'first_names': [],
        'middle_names': [],
        'last_names': [],
        'full_names': [],
        'emails': [],
        'phones': [],
        'addresses': [],
        'dates': [],
        'unit_numbers': [],
        'cities': [],
        'postal_codes': [],
        'general_names': [],
        'other': []
    }
    
    print("Categorizing extracted data by type...")
    
    for field in filled_fields:
        value = field['value']
        label = field['label'].lower()
        
        # Skip obvious company/template data 
        #####################################needs to be updated################################################# *************************
        if any(skip_word in value.lower() for skip_word in ['provident', 'customerservice', 'pemi.com']):
            continue
        
        categorized = False
        
        # Email detection
        if validate_data_type(value, 'email'):
            data_by_type['emails'].append(field)
            categorized = True
        
        # Phone detection
        elif validate_data_type(value, 'phone'):
            data_by_type['phones'].append(field)
            categorized = True
        
        # Date detection
        elif validate_data_type(value, 'date'):
            data_by_type['dates'].append(field)
            categorized = True
        
        # Address detection
        elif validate_data_type(value, 'address'):
            data_by_type['addresses'].append(field)
            categorized = True
        
        # Unit number detection
        elif any(word in label for word in ['suite', 'unit']) and validate_data_type(value, 'number'):
            data_by_type['unit_numbers'].append(field)
            categorized = True
        
        # Name detection
        elif validate_data_type(value, 'name'):
            # Check if it's a full name 
            if len(value.split()) >= 2:
                data_by_type['full_names'].append(field)
            else:
                data_by_type['general_names'].append(field)
            categorized = True
        
        # If not categorized, put in other
        if not categorized:
            data_by_type['other'].append(field)
    
    # debugging
    for category, items in data_by_type.items():
        if items:
            print(f"  {category.upper()}:")
            for item in items:
                print(f"    {item['label']}: {item['value']}")
    
    return data_by_type

def find_best_match(target_field_type, nearby_text, data_by_type, used_indices):
    """Find the best matching data for a target field"""
    best_match = None
    best_score = 0
    best_category = None
    best_index = -1
    
    # Define search strategy based on target field type
    search_strategy = {
        'first_name': [('full_names', 'extract_first'), ('general_names', 'direct'), ('other', 'direct')],
        'middle_name': [('full_names', 'extract_middle'), ('general_names', 'direct')],
        'last_name': [('full_names', 'extract_last'), ('general_names', 'direct')],
        'full_name': [('full_names', 'direct'), ('general_names', 'direct')],
        'email': [('emails', 'direct')],
        'phone': [('phones', 'direct')],
        'address': [('addresses', 'direct')],
        'city': [('cities', 'direct'), ('other', 'direct')],
        'postal_code': [('postal_codes', 'direct'), ('other', 'direct')],
        'occupancy_date': [('dates', 'direct')],
        'unit_number': [('unit_numbers', 'direct'), ('other', 'direct')],
        'name': [('full_names', 'direct'), ('general_names', 'direct')],
        'other': [('other', 'direct'), ('full_names', 'direct'), ('general_names', 'direct')]
    }
    
    categories_to_search = search_strategy.get(target_field_type, [('other', 'direct')])
    
    for category, extraction_method in categories_to_search:
        if category not in data_by_type:
            continue
            
        for i, field in enumerate(data_by_type[category]):
            field_key = f"{category}_{i}"
            if field_key in used_indices:
                continue
            
            # Calculate semantic similarity
            score = SequenceMatcher(None, nearby_text.lower(), field['label'].lower()).ratio()
            
            # Boost score for exact category matches
            if category in ['emails', 'phones', 'addresses', 'dates', 'unit_numbers']:
                score += 0.4
            
            # Additional boost for high-priority matches
            if target_field_type == 'email' and category == 'emails':
                score += 0.5
            elif target_field_type == 'phone' and category == 'phones':
                score += 0.5
            elif target_field_type == 'address' and category == 'addresses':
                score += 0.5
            
            if score > best_score:
                best_score = score
                best_match = field
                best_category = category
                best_index = i
    
    return best_match, best_score, best_category, best_index

def extract_value_by_method(field, extraction_method):
    """Extract the appropriate value based on the extraction method"""
    if extraction_method == 'direct':
        return field['value']
    elif extraction_method == 'extract_first':
        first, _, _ = extract_name_parts(field['value'])
        return first
    elif extraction_method == 'extract_middle':
        _, middle, _ = extract_name_parts(field['value'])
        return middle
    elif extraction_method == 'extract_last':
        _, _, last = extract_name_parts(field['value'])
        return last
    else:
        return field['value']

def match_filled_to_blank_fields(filled_fields, blank_pdf_path):
    """Enhanced matching with semantic understanding and validation"""
    doc = fitz.open(blank_pdf_path)
    matched = {}
    
    # Categorize extracted data
    data_by_type = categorize_extracted_data(filled_fields)
    used_indices = set()
    
    print("\n Smart matching process...")
    
    # Process each field in the blank form
    for page in doc:
        for w in page.widgets():
            field_name = w.field_name
            nearby_text = page.get_textbox(w.rect + (-100, -100, 100, 100)).strip()
            
            # Determine what this field needs
            target_field_type = determine_field_type_and_validate(nearby_text)
            
            # Find the best match
            best_match, best_score, best_category, best_index = find_best_match(
                target_field_type, nearby_text, data_by_type, used_indices
            )
            
            # Assign the best match if score is reasonable
            threshold = 0.15 
            if best_match and best_score > threshold:
                # Determine extraction method
                search_strategy = {
                    'first_name': [('full_names', 'extract_first'), ('general_names', 'direct')],
                    'middle_name': [('full_names', 'extract_middle')],
                    'last_name': [('full_names', 'extract_last'), ('general_names', 'direct')],
                    'full_name': [('full_names', 'direct'), ('general_names', 'direct')],
                }
                
                extraction_method = 'direct'
                if target_field_type in search_strategy:
                    for cat, method in search_strategy[target_field_type]:
                        if best_category == cat:
                            extraction_method = method
                            break
                
                # Extract the value
                final_value = extract_value_by_method(best_match, extraction_method)
                
                matched[field_name] = final_value
                used_indices.add(f"{best_category}_{best_index}")
                
                print(f"  ✅ {field_name}: '{nearby_text[:30]}...' → '{target_field_type}' = '{final_value}' (score: {best_score:.2f})")
            else:
                matched[field_name] = ""
                print(f"  ❌ {field_name}: '{nearby_text[:30]}...' → '{target_field_type}' (no suitable match)")
    
    # Show unused data
    unused_data = []
    for category, items in data_by_type.items():
        for i, item in enumerate(items):
            if f"{category}_{i}" not in used_indices:
                unused_data.append(f"{item['label']}: {item['value']}")
    
    if unused_data:
        print(f"\n Unused source data: {unused_data}")
    
    return matched