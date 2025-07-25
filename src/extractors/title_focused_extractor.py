import pandas as pd
import re
import os
from datetime import datetime

def classify_approval_status_from_title(title):
    """Classify approval status primarily from title"""
    title_lower = title.lower()
    
    # Strong approval indicators in titles
    approval_indicators = [
        'approved', 'got approved', 'was approved', 'instant approval',
        'approved for', 'got the card', 'received the card', 'successful',
        'approval success', 'got it', 'accepted'
    ]
    
    # Strong denial indicators in titles
    denial_indicators = [
        'denied', 'got denied', 'was denied', 'rejected', 'rejection',
        'application denied', 'not approved', 'declined', 'denial',
        'got rejected', 'was rejected'
    ]
    
    # Question/uncertainty indicators in titles
    question_indicators = [
        'approval odds', 'chances of approval', 'should i apply',
        'will i get approved', 'approval likelihood', 'recommendations',
        'help', 'advice', 'what card', 'which card', 'next card',
        'approval question', 'odds', 'chances'
    ]
    
    # Check for strong signals in title first
    for phrase in approval_indicators:
        if phrase in title_lower:
            return 'approved'
    
    for phrase in denial_indicators:
        if phrase in title_lower:
            return 'denied'
    
    for phrase in question_indicators:
        if phrase in title_lower:
            return 'question'
    
    return 'unknown'

def extract_income_from_title_and_body(title, body):
    """Extract income, prioritizing title but checking body if needed"""
    combined_text = f"{title} {body}"
    
    # First try to find income in title
    title_patterns = [
        r'income.*?(\$?\d{1,3}[,]?\d{3})',
        r'make.*?(\$?\d{1,3}[,]?\d{3}).*?(annually|yearly|per year)',
        r'(\$?\d{1,3}[,]?\d{3}).*?(income|salary)'
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            amount = int(match.group(1).replace(',', '').replace('$', ''))
            if 10000 <= amount <= 500000:
                return amount
    
    # If not found in title, check body
    body_patterns = [
        r'income.*?(\$?\d{1,3}[,]?\d{3})',
        r'annual income.*?(\$?\d{1,3}[,]?\d{3})',
        r'make.*?(\$?\d{1,3}[,]?\d{3}).*?(annually|yearly|per year)',
        r'salary.*?(\$?\d{1,3}[,]?\d{3})'
    ]
    
    for pattern in body_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            amount = int(match.group(1).replace(',', '').replace('$', ''))
            if 10000 <= amount <= 500000:
                return amount
    
    return None

def extract_credit_score_from_title_and_body(title, body):
    """Extract credit score, prioritizing title but checking body if needed"""
    combined_text = f"{title} {body}"
    
    # First try to find credit score in title
    title_patterns = [
        r'(credit score|fico).*?(\d{3})',
        r'score.*?(\d{3})',
        r'(\d{3}).*?(credit score|fico)'
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            # Extract the numeric part (group 2 for patterns with 2 groups, group 1 for single group)
            if len(match.groups()) > 1:
                score_str = match.group(2)
            else:
                score_str = match.group(1)
            
            # Make sure it's actually a number
            if score_str.isdigit():
                score = int(score_str)
                if 300 <= score <= 850:
                    return score
    
    # If not found in title, check body
    body_patterns = [
        r'(credit score|fico).*?(\d{3})',
        r'score.*?(\d{3})',
        r'(\d{3}).*?(credit score|fico)',
        r'fico.*?(\d{3})'
    ]
    
    for pattern in body_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            # Extract the numeric part (group 2 for patterns with 2 groups, group 1 for single group)
            if len(match.groups()) > 1:
                score_str = match.group(2)
            else:
                score_str = match.group(1)
            
            # Make sure it's actually a number
            if score_str.isdigit():
                score = int(score_str)
                if 300 <= score <= 850:
                    return score
    
    return None

def extract_approval_amount_from_title_and_body(title, body):
    """Extract approval amount, prioritizing title but checking body if needed"""
    combined_text = f"{title} {body}"
    
    # Look for approval-specific language in title first
    title_patterns = [
        r'approved.*?(\$?\d{1,3}[,]?\d{3,4})',
        r'got.*?(\$?\d{1,3}[,]?\d{3,4}).*?limit',
        r'limit.*?(\$?\d{1,3}[,]?\d{3,4})'
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            amount = int(match.group(1).replace(',', '').replace('$', ''))
            if 500 <= amount <= 50000:
                return amount
    
    # If not found in title, check body
    body_patterns = [
        r'approved.*?(\$?\d{1,3}[,]?\d{3,4})',
        r'got.*?(\$?\d{1,3}[,]?\d{3,4}).*?limit',
        r'credit limit.*?(\$?\d{1,3}[,]?\d{3,4})',
        r'starting limit.*?(\$?\d{1,3}[,]?\d{3,4})'
    ]
    
    for pattern in body_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            amount = int(match.group(1).replace(',', '').replace('$', ''))
            if 500 <= amount <= 50000:
                return amount
    
    return None

def calculate_title_quality_score(title):
    """Score how clear the title is about approval/denial status"""
    title_lower = title.lower()
    score = 0
    
    # High confidence indicators
    if any(phrase in title_lower for phrase in ['approved', 'denied', 'rejected']):
        score += 5
    
    # Medium confidence indicators
    if any(phrase in title_lower for phrase in ['got approved', 'got denied', 'was approved', 'was denied']):
        score += 4
    
    # Question indicators (lower score)
    if any(phrase in title_lower for phrase in ['odds', 'chances', 'should i', 'help', 'advice']):
        score += 1
    
    # Chase-specific language
    if any(phrase in title_lower for phrase in ['chase', 'freedom unlimited', 'freedom flex', 'cfu', 'cff', 'chase cfu', 'chase cff']):
        score += 2
    
    return score

def verify_freedom_card_mention(title, body, card_name):
    """Verify that the specific Freedom card is mentioned in the content"""
    combined_text = f"{title} {body}".lower()
    
    if card_name == 'Freedom Unlimited':
        # Check for Freedom Unlimited specific mentions
        unlimited_indicators = [
            'freedom unlimited', 'cfu', 'chase freedom unlimited',
            'freedom unlimited card', 'cfu card', 'chase cfu'
        ]
        return any(indicator in combined_text for indicator in unlimited_indicators)
    
    elif card_name == 'Freedom Flex':
        # Check for Freedom Flex specific mentions
        flex_indicators = [
            'freedom flex', 'cff', 'chase freedom flex',
            'freedom flex card', 'cff card', 'chase cff'
        ]
        return any(indicator in combined_text for indicator in flex_indicators)
    
    return False

def extract_features_from_text(text):
    """Extract binary features from text"""
    text_lower = str(text).lower()
    
    features = {
        'is_student': any(phrase in text_lower for phrase in ['student', 'college', 'university', 'school']),
        'is_first_card': any(phrase in text_lower for phrase in ['first card', 'first credit card', 'first cc', 'first time']),
        'has_chase_account': any(phrase in text_lower for phrase in ['chase account', 'chase checking', 'chase savings', 'chase relationship']),
        'mentions_income': any(phrase in text_lower for phrase in ['income', 'salary', 'make', 'earn', 'annual']),
        'mentions_credit_score': any(phrase in text_lower for phrase in ['credit score', 'fico', 'score']),
        'text_length': len(text)
    }
    
    return features

def extract_fields_title_focused(input_file, output_file=None, comprehensive=False):
    """Extract structured fields using title-focused approach"""
    
    # Load dataset
    df = pd.read_csv(input_file)
    
    # Initialize new columns
    df['approval_status'] = ''
    df['title_quality_score'] = 0
    df['Extracted Income'] = ''
    df['Extracted Credit Score'] = ''
    df['Extracted Approval Amount'] = ''
    
    # Process each row
    for idx, row in df.iterrows():
        title = str(row['Title'])
        body = str(row['Body'])
        
        # Classify approval status from title
        approval_status = classify_approval_status_from_title(title)
        df.at[idx, 'approval_status'] = approval_status
        
        # Calculate title quality score
        quality_score = calculate_title_quality_score(title)
        df.at[idx, 'title_quality_score'] = quality_score
        
        # Extract other fields (title first, then body)
        income = extract_income_from_title_and_body(title, body)
        if income:
            df.at[idx, 'Extracted Income'] = income
        
        credit_score = extract_credit_score_from_title_and_body(title, body)
        if credit_score:
            df.at[idx, 'Extracted Credit Score'] = credit_score
        
        approval_amount = extract_approval_amount_from_title_and_body(title, body)
        if approval_amount:
            df.at[idx, 'Extracted Approval Amount'] = approval_amount
    
    # Filter for high-quality posts with clear approval/denial status
    # Only include Freedom Unlimited and Freedom Flex (exclude Sapphire, etc.)
    # Check both title and body for specific card mentions
    quality_df = df[
        (df['approval_status'].isin(['approved', 'denied'])) &
        (df['title_quality_score'] >= 3) &
        (df['Card_Name'].isin(['Freedom Unlimited', 'Freedom Flex'])) &
        (~df['Title'].str.contains('sapphire|preferred|reserve|csr|csp', case=False, na=False)) &
        (~df['Body'].str.contains('sapphire|preferred|reserve|csr|csp', case=False, na=False))
    ]
    
    # Additional verification: ensure the specific card is actually mentioned in the content
    verified_posts = []
    for idx, row in quality_df.iterrows():
        if verify_freedom_card_mention(row['Title'], row['Body'], row['Card_Name']):
            verified_posts.append(idx)
    
    quality_df = quality_df.loc[verified_posts]
    
    # Clean and validate extracted data
    quality_df['income_clean'] = quality_df['Extracted Income'].apply(lambda x: 
        int(x) if x and str(x).isdigit() and 10000 <= int(x) <= 500000 else None)
    
    quality_df['credit_score_clean'] = quality_df['Extracted Credit Score'].apply(lambda x: 
        int(x) if x and str(x).isdigit() and 300 <= int(x) <= 850 else None)
    
    quality_df['approval_amount_clean'] = quality_df['Extracted Approval Amount'].apply(lambda x: 
        int(x) if x and str(x).isdigit() and 500 <= int(x) <= 50000 else None)
    
    # Create target variable (1 for approved, 0 for denied)
    quality_df['target'] = quality_df['approval_status'].map({'approved': 1, 'denied': 0})
    
    # Extract additional features from text if comprehensive mode
    if comprehensive:
        for idx, row in quality_df.iterrows():
            combined_text = f"{row['Title']} {row['Body']}"
            features = extract_features_from_text(combined_text)
            
            for feature_name, feature_value in features.items():
                quality_df.at[idx, feature_name] = feature_value
        
        # Select comprehensive set of columns for output
        comprehensive_columns = [
            'Title', 'URL', 'Body', 'Source', 'Card_Name', 'Scraped_At',
            'approval_status', 'title_quality_score',
            'Extracted Income', 'Extracted Credit Score', 'Extracted Approval Amount',
            'income_clean', 'credit_score_clean', 'approval_amount_clean',
            'target', 'is_student', 'is_first_card', 'has_chase_account',
            'mentions_income', 'mentions_credit_score', 'text_length'
        ]
        
        # Fill missing values for display
        quality_df['income_clean'] = quality_df['income_clean'].fillna('Not extracted')
        quality_df['credit_score_clean'] = quality_df['credit_score_clean'].fillna('Not extracted')
        quality_df['approval_amount_clean'] = quality_df['approval_amount_clean'].fillna('Not extracted')
        
        # Convert boolean columns to Yes/No for readability
        boolean_columns = ['is_student', 'is_first_card', 'has_chase_account', 'mentions_income', 'mentions_credit_score']
        for col in boolean_columns:
            quality_df[col] = quality_df[col].map({True: 'Yes', False: 'No'})
        
        quality_df = quality_df[comprehensive_columns]
    
    # Generate output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if comprehensive:
            output_file = f'data/processed/title_focused_comprehensive_dataset_{timestamp}.csv'
        else:
            output_file = f'data/processed/title_focused_extracted_data_{timestamp}.csv'
    
    # Create processed directory if it doesn't exist
    os.makedirs('data/processed', exist_ok=True)
    
    # Save results
    quality_df.to_csv(output_file, index=False)
    
    print(f"Title-focused extraction completed:")
    print(f"- Total posts processed: {len(df)}")
    print(f"- High-quality posts found: {len(quality_df)}")
    print(f"- Approval status breakdown:")
    print(quality_df['approval_status'].value_counts())
    if comprehensive:
        print(f"- Card distribution:")
        print(quality_df['Card_Name'].value_counts())
    print(f"- Saved to: {output_file}")
    
    return output_file

def main():
    """Main function to run the title-focused extractor"""
    import sys
    
    # Check if comprehensive mode is requested
    comprehensive = '--comprehensive' in sys.argv
    
    # Find the most recent raw data file
    raw_files = [f for f in os.listdir('data/raw') if f.endswith('.csv')]
    if not raw_files:
        print("No raw data files found in data/raw/")
        return
    
    # Use the most recent file
    latest_file = sorted(raw_files)[-1]
    input_file = f'data/raw/{latest_file}'
    
    if comprehensive:
        print(f"Creating comprehensive dataset from {input_file} with title-focused approach...")
    else:
        print(f"Processing {input_file} with title-focused extraction...")
    
    output_file = extract_fields_title_focused(input_file, comprehensive=comprehensive)
    print(f"Title-focused extraction completed: {output_file}")

if __name__ == "__main__":
    main() 