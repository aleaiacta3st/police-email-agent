import re


def extract_case_id(subject):
    match = re.search(r'\[Case #([a-f0-9-]+)\]', subject)
    if match:
        return match.group(1)
    return None

def clean_subject(subject):
    cleaned = re.sub(r'\[Case #[a-f0-9-]+\]', '', subject)
    cleaned = re.sub(r'^(Re:\s*)+', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\[(assault|cybercrime|theft)\]', '', cleaned)

    return cleaned.strip() 

def extract_category(subject):
    match = re.search(r'\[(assault|cybercrime|theft)\]', subject)
    if match:
        return match.group(1)
    return None