# # # # from difflib import SequenceMatcher
# # # # import fitz

# # # # def similarity(a, b):
# # # #     return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# # # # def match_filled_to_blank_fields(filled_fields, blank_pdf_path):
# # # #     doc = fitz.open(blank_pdf_path)
# # # #     blank_fields = []
# # # #     for page_num, page in enumerate(doc):
# # # #         for w in page.widgets():
# # # #             label = page.get_textbox(w.rect + (-70, -70, 70, 70)).strip()
# # # #             blank_fields.append({
# # # #                 "field_name": w.field_name,
# # # #                 "label": label,
# # # #                 "page": page_num
# # # #             })

# # # #     matched = {}
# # # #     for bf in blank_fields:
# # # #         best_score = 0
# # # #         best_value = None
# # # #         for ff in filled_fields:
# # # #             score = similarity(bf["label"], ff["label"])
# # # #             if score > best_score:
# # # #                 best_score = score
# # # #                 best_value = ff["value"]
# # # #         if best_score > 0.35:
# # # #             matched[bf["field_name"]] = best_value
# # # #             print(f"Matching '{bf['label']}' to '{ff['label']}' → score: {score}")
# # # #     return matched

# # # from difflib import SequenceMatcher
# # # import fitz

# # # def similarity(a, b):
# # #     return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# # # # def match_filled_to_blank_fields(filled_fields, blank_pdf_path):
# # # #     doc = fitz.open(blank_pdf_path)
# # # #     blank_fields = []

# # # #     # Step 1: Extract all fields in the blank form
# # # #     for page_num, page in enumerate(doc):
# # # #         for w in page.widgets():
# # # #             label = page.get_textbox(w.rect + (-70, -70, 70, 70)).strip()
# # # #             blank_fields.append({
# # # #                 "field_name": w.field_name,
# # # #                 "label": label,
# # # #                 "page": page_num
# # # #             })

# # # #     # Step 2: Match each blank field to extracted field
# # # #     matched = {}
# # # #     for bf in blank_fields:
# # # #         best_score = 0
# # # #         best_value = ""
# # # #         for ff in filled_fields:
# # # #             score = similarity(bf["label"], ff["label"])
# # # #             if score > best_score:
# # # #                 best_score = score
# # # #                 best_value = ff["value"]
# # # #         matched[bf["field_name"]] = best_value if best_score > 0.35 else ""

# # # #     return matched

# # # def match_filled_to_blank_fields(filled_fields, blank_pdf_path):
# # #     doc = fitz.open(blank_pdf_path)
# # #     blank_fields = []

# # #     for page_num, page in enumerate(doc):
# # #         for w in page.widgets():
# # #             label = page.get_textbox(w.rect + (-70, -70, 70, 70)).strip()
# # #             blank_fields.append({
# # #                 "field_name": w.field_name,
# # #                 "label": label,
# # #                 "page": page_num
# # #             })

# # #     matched = {}
# # #     used = set()

# # #     for bf in blank_fields:
# # #         best_score = 0
# # #         best_value = ""
# # #         best_idx = -1

# # #         for i, ff in enumerate(filled_fields):
# # #             if i in used:
# # #                 continue
# # #             score = similarity(bf["label"], ff["label"])
# # #             if score > best_score:
# # #                 best_score = score
# # #                 best_value = ff["value"]
# # #                 best_idx = i

# # #         if best_score > 0.35:
# # #             matched[bf["field_name"]] = best_value
# # #             used.add(best_idx)
# # #         else:
# # #             matched[bf["field_name"]] = ""

# # #     return matched

# # from difflib import SequenceMatcher
# # import fitz

# # def similarity(a, b):
# #     return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# # def match_filled_to_blank_fields(filled_fields, blank_pdf_path):
# #     doc = fitz.open(blank_pdf_path)
# #     blank_fields = []

# #     for page_num, page in enumerate(doc):
# #         for w in page.widgets():
# #             label = page.get_textbox(w.rect + (-70, -70, 70, 70)).strip()
# #             blank_fields.append({
# #                 "field_name": w.field_name,
# #                 "label": label,
# #                 "page": page_num
# #             })

# #     matched = {}
# #     used = set()

# #     print("🎯 Matching process:")
# #     for bf in blank_fields:
# #         best_score = 0
# #         best_value = ""
# #         best_idx = -1
# #         best_filled_label = ""

# #         for i, ff in enumerate(filled_fields):
# #             if i in used:
# #                 continue
# #             score = similarity(bf["label"], ff["label"])
# #             if score > best_score:
# #                 best_score = score
# #                 best_value = ff["value"]
# #                 best_idx = i
# #                 best_filled_label = ff["label"]

# #         # Lowered threshold from 0.35 to 0.2
# #         threshold = 0.2
# #         if best_score > threshold:
# #             matched[bf["field_name"]] = best_value
# #             used.add(best_idx)
# #             print(f"✅ {bf['field_name']}: '{bf['label']}' ← '{best_filled_label}' (score: {best_score:.2f})")
# #         else:
# #             matched[bf["field_name"]] = ""
# #             print(f"❌ {bf['field_name']}: '{bf['label']}' (no match, best: {best_score:.2f})")

# #     return matched

# from difflib import SequenceMatcher
# import fitz
# from langchain_ollama import OllamaLLM
# from langchain.prompts import ChatPromptTemplate

# llm = OllamaLLM(model="llama3.1:8b")

# def similarity(a, b):
#     return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# def generate_blank_field_label(text, field_name):
#     """Generate semantic labels for blank form fields using AI"""
#     prompt = ChatPromptTemplate.from_template(
#         "You are analyzing a blank PDF form field to understand what information should go there.\n\n"
#         "Field name: '{field_name}'\n"
#         "Nearby text on the form: '{text}'\n\n"
#         "Based on the context, what type of information should this field contain?\n"
#         "Return a short semantic label like 'full name', 'email', 'phone number', 'street address', 'move-in date', etc.\n"
#         "Return only the label, no explanation:"
#     )
#     return llm.invoke(prompt.format(field_name=field_name, text=text)).strip().lower()

# def fuzzy_match_keywords(label1, label2):
#     """Enhanced matching using keyword overlap and fuzzy matching"""
#     # Common synonyms and variations
#     synonyms = {
#         'address': ['street', 'addr', 'location'],
#         'name': ['resident', 'tenant', 'applicant', 'client'],
#         'phone': ['telephone', 'mobile', 'cell', 'number'],
#         'email': ['e-mail', 'mail', 'electronic'],
#         'date': ['move-in', 'movein', 'start', 'lease'],
#         'suite': ['unit', 'apt', 'apartment', 'room']
#     }
    
#     # Split labels into words
#     words1 = set(label1.lower().split())
#     words2 = set(label2.lower().split())
    
#     # Direct word overlap
#     overlap = len(words1.intersection(words2))
#     if overlap > 0:
#         return 0.8 + (overlap * 0.1)
    
#     # Check synonyms
#     for word1 in words1:
#         for word2 in words2:
#             for key, syn_list in synonyms.items():
#                 if (word1 == key and word2 in syn_list) or (word2 == key and word1 in syn_list):
#                     return 0.7
#                 if word1 in syn_list and word2 in syn_list:
#                     return 0.6
    
#     # Fallback to sequence matching
#     return similarity(label1, label2)

# def match_filled_to_blank_fields(filled_fields, blank_pdf_path):
#     doc = fitz.open(blank_pdf_path)
#     blank_fields = []

#     # Extract blank fields and generate AI labels for them
#     print("🔍 Analyzing blank form fields...")
#     for page_num, page in enumerate(doc):
#         for w in page.widgets():
#             nearby_text = page.get_textbox(w.rect + (-70, -70, 70, 70)).strip()
            
#             # Generate AI label for blank field
#             ai_label = generate_blank_field_label(nearby_text, w.field_name)
            
#             blank_fields.append({
#                 "field_name": w.field_name,
#                 "original_text": nearby_text,
#                 "ai_label": ai_label,
#                 "page": page_num
#             })
#             print(f"  {w.field_name}: '{nearby_text}' → '{ai_label}'")

#     matched = {}
#     used_filled_indices = set()

#     print("\n🎯 Matching fields...")
    
#     # Match each blank field to the best filled field
#     for bf in blank_fields:
#         best_score = 0
#         best_value = ""
#         best_filled_field = None
#         best_idx = -1

#         for i, ff in enumerate(filled_fields):
#             if i in used_filled_indices:
#                 continue
            
#             # Try matching with AI-generated label
#             ai_score = fuzzy_match_keywords(bf["ai_label"], ff["label"])
            
#             # Also try matching with original text
#             text_score = fuzzy_match_keywords(bf["original_text"], ff["label"])
            
#             # Use the better score
#             score = max(ai_score, text_score)
            
#             if score > best_score:
#                 best_score = score
#                 best_value = ff["value"]
#                 best_filled_field = ff
#                 best_idx = i

#         # Lower threshold and show matching details
#         threshold = 0.25  # Reduced from 0.35
#         if best_score > threshold:
#             matched[bf["field_name"]] = best_value
#             used_filled_indices.add(best_idx)
#             print(f"  ✅ {bf['field_name']}: '{bf['ai_label']}' ← '{best_filled_field['label']}' (score: {best_score:.2f})")
#         else:
#             matched[bf["field_name"]] = ""
#             print(f"  ❌ {bf['field_name']}: '{bf['ai_label']}' (no good match, best score: {best_score:.2f})")

#     # Show unmatched filled fields
#     unmatched_filled = [ff for i, ff in enumerate(filled_fields) if i not in used_filled_indices]
#     if unmatched_filled:
#         print(f"\n⚠️  Unmatched filled fields: {[ff['label'] + ': ' + ff['value'] for ff in unmatched_filled]}")

#     return matched


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
    
    print("🔍 Categorizing extracted data by type...")
    
    for field in filled_fields:
        value = field['value']
        label = field['label'].lower()
        
        # Skip obvious company/template data
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
            # Check if it's a full name (multiple words)
            if len(value.split()) >= 2:
                data_by_type['full_names'].append(field)
            else:
                data_by_type['general_names'].append(field)
            categorized = True
        
        # If not categorized, put in other
        if not categorized:
            data_by_type['other'].append(field)
    
    # Print categorized data for debugging
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
    
    print("\n🎯 Smart matching process...")
    
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
            threshold = 0.15  # Lower threshold for better coverage
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
        print(f"\n⚠️  Unused source data: {unused_data}")
    
    return matched