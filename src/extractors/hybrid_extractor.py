import pandas as pd
import re
import os
import json
from datetime import datetime
import requests
from typing import Dict, Any, Optional

# Import the rule-based functions from title_focused_extractor
from title_focused_extractor import (
    classify_approval_status_from_title,
    extract_income_from_title_and_body,
    extract_credit_score_from_title_and_body,
    extract_approval_amount_from_title_and_body,
    calculate_title_quality_score,
    verify_freedom_card_mention,
    extract_features_from_text
)

def setup_ollama_client(model: str = "mistral"):
    """Setup Ollama client with local model"""
    # Test if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            print(f"Ollama is running. Using model: {model}")
            return model
        else:
            raise Exception("Ollama not responding")
    except Exception as e:
        raise Exception(f"Ollama not running or not accessible: {e}")

def llm_classify_post(title: str, body: str, card_name: str, model: str = "mistral") -> Dict[str, Any]:
    """Use Ollama LLM to classify a single post"""
    
    prompt = f"""
You are analyzing a Reddit post about credit card applications. Please classify this post and extract key information.

POST TITLE: {title}
POST BODY: {body}
CARD: {card_name}

IMPORTANT: Only classify posts that are about {card_name} (Freedom Unlimited or Freedom Flex). If the post is clearly about other cards (Capital One, Citi, Amex, etc.) and doesn't mention {card_name}, mark as "unknown".

Please respond with a JSON object containing:
1. "approval_status": "approved", "denied", "question", or "unknown"
2. "confidence": 0-10 score for your classification
3. "income": annual income if mentioned (number only, or null)
4. "credit_score": credit score if mentioned (number only, or null)
5. "approval_amount": credit limit if mentioned (number only, or null)
6. "reasoning": brief explanation of your classification

Focus on:
- Only classify if the post is about {card_name} (Freedom Unlimited/Flex)
- Approval status should be based on clear approval/denial language for {card_name}
- If post mentions {card_name} approval/denial, include it even if other cards are mentioned
- If post is clearly about other cards only, mark as "unknown"
- Only extract numbers that are clearly income, credit scores, or credit limits
- Be conservative - if uncertain, mark as "unknown"

Response format:
{{
    "approval_status": "approved",
    "confidence": 8,
    "income": 50000,
    "credit_score": 720,
    "approval_amount": 5000,
    "reasoning": "Post mentions {card_name} approval and includes specific credit limit"
}}

Respond only with valid JSON.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 300
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result_text = response.json()["response"]
            # Clean up the response to extract JSON
            result_text = result_text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            try:
                result = json.loads(result_text)
                return result
            except json.JSONDecodeError:
                # Try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                        return result
                    except:
                        pass
                
                # If all else fails, return a default response
                return {
                    "approval_status": "unknown",
                    "confidence": 0,
                    "income": None,
                    "credit_score": None,
                    "approval_amount": None,
                    "reasoning": f"Failed to parse LLM response: {result_text[:100]}"
                }
        else:
            raise Exception(f"Ollama API error: {response.status_code}")
    
    except Exception as e:
        print(f"LLM classification failed: {e}")
        return {
            "approval_status": "unknown",
            "confidence": 0,
            "income": None,
            "credit_score": None,
            "approval_amount": None,
            "reasoning": f"LLM error: {str(e)}"
        }

def validate_with_llm(df: pd.DataFrame, confidence_threshold: int = 5, model: str = "mistral") -> pd.DataFrame:
    """Use LLM to validate posts with low confidence scores"""
    
    print(f"Validating {len(df)} posts with LLM (confidence threshold: {confidence_threshold})...")
    
    # Add LLM validation columns for all posts
    df['llm_approval_status'] = ''
    df['llm_confidence'] = 0
    df['llm_income'] = None
    df['llm_credit_score'] = None
    df['llm_approval_amount'] = None
    df['llm_reasoning'] = ''
    df['used_llm'] = False
    
    llm_count = 0
    
    for idx, row in df.iterrows():
        # Use LLM for all posts to get confidence scores and validation
        print(f"Using LLM for post {idx + 1}/{len(df)}: {row['Title'][:50]}...")
        
        llm_result = llm_classify_post(
            row['Title'], 
            row['Body'], 
            row['Card_Name'],
            model
        )
        
        # Update with LLM results
        df.at[idx, 'llm_approval_status'] = llm_result['approval_status']
        df.at[idx, 'llm_confidence'] = llm_result['confidence']
        df.at[idx, 'llm_income'] = llm_result['income']
        df.at[idx, 'llm_credit_score'] = llm_result['credit_score']
        df.at[idx, 'llm_approval_amount'] = llm_result['approval_amount']
        df.at[idx, 'llm_reasoning'] = llm_result['reasoning']
        df.at[idx, 'used_llm'] = True
        
        llm_count += 1
        
        # Override rule-based classification if LLM is more confident
        if llm_result['confidence'] > row['title_quality_score']:
            df.at[idx, 'approval_status'] = llm_result['approval_status']
            df.at[idx, 'title_quality_score'] = llm_result['confidence']
            
            # Override extracted values if LLM found them
            if llm_result['income']:
                df.at[idx, 'Extracted Income'] = llm_result['income']
            if llm_result['credit_score']:
                df.at[idx, 'Extracted Credit Score'] = llm_result['credit_score']
            if llm_result['approval_amount']:
                df.at[idx, 'Extracted Approval Amount'] = llm_result['approval_amount']
        
        # If LLM says it's not about Freedom cards, mark for exclusion
        if llm_result['approval_status'] == 'unknown' and 'not about freedom' in llm_result['reasoning'].lower():
            df.at[idx, 'approval_status'] = 'exclude'
    
    print(f"LLM validation completed. Used LLM for {llm_count} posts.")
    return df

def hybrid_extract_fields(input_file: str, output_file: str = None, 
                         use_llm: bool = True, confidence_threshold: int = 5,
                         model: str = "mistral") -> str:
    """Hybrid extraction using rules first, then LLM validation for uncertain cases"""
    
    print("Starting hybrid extraction...")
    
    # Step 1: Use rule-based extraction (fast and cheap)
    print("Step 1: Rule-based extraction...")
    
    # Load dataset
    df = pd.read_csv(input_file)
    
    # Initialize new columns
    df['approval_status'] = ''
    df['title_quality_score'] = 0
    df['Extracted Income'] = ''
    df['Extracted Credit Score'] = ''
    df['Extracted Approval Amount'] = ''
    
    # Process each row with rule-based extraction
    for idx, row in df.iterrows():
        title = str(row['Title'])
        body = str(row['Body'])
        
        # Use Decision column if available, otherwise classify from title
        if 'Decision' in df.columns:
            decision = str(row['Decision']).lower()
            if decision in ['approved', 'pre-approved']:
                approval_status = 'approved'
            elif decision in ['denied', 'rejected']:
                approval_status = 'denied'
            else:
                approval_status = classify_approval_status_from_title(title)
        else:
            # Fallback to title classification
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
    
    # Step 2: Filter for high-quality posts
    print("Step 2: Filtering high-quality posts...")
    
    quality_df = df[
        (df['approval_status'].isin(['approved', 'denied'])) &
        (df['title_quality_score'] >= 1) &  # Lowered threshold to see more posts
        (df['Card_Name'].isin(['Freedom Unlimited', 'Freedom Flex', 'Freedom (Generic)'])) &
        (~df['Title'].str.contains('sapphire|preferred|reserve|csr|csp', case=False, na=False)) &
        (~df['Body'].str.contains('sapphire|preferred|reserve|csr|csp', case=False, na=False)) &
        # Exclude posts that are clearly about other cards
        (~df['Title'].str.contains('capital one|savor|citi|custom cash|amex|bce|bce', case=False, na=False)) &
        (~df['Body'].str.contains('capital one|savor|citi|custom cash|amex|bce|bce', case=False, na=False))
    ]
    
    # Additional verification: ensure the specific card is actually mentioned
    verified_posts = []
    for idx, row in quality_df.iterrows():
        if verify_freedom_card_mention(row['Title'], row['Body'], row['Card_Name']):
            verified_posts.append(idx)
    
    quality_df = quality_df.loc[verified_posts]
    
    print(f"Rule-based filtering found {len(quality_df)} high-quality posts")
    
    # Step 3: LLM validation for all posts (optional)
    if use_llm:
        print("Step 3: LLM validation for all posts...")
        try:
            setup_ollama_client(model)
            quality_df = validate_with_llm(quality_df, confidence_threshold, model)
        except Exception as e:
            print(f"LLM validation failed: {e}")
            print("Continuing with rule-based results only...")
    
    # Step 4: Final processing
    print("Step 4: Final processing...")
    
    # Remove posts that LLM marked as not about Freedom cards
    if use_llm and 'approval_status' in quality_df.columns:
        quality_df = quality_df[quality_df['approval_status'] != 'exclude']
        print(f"Removed posts that LLM identified as not about Freedom cards")
    
    # Clean and validate extracted data
    quality_df['income_clean'] = quality_df['Extracted Income'].apply(lambda x: 
        int(x) if x and str(x).isdigit() and 10000 <= int(x) <= 500000 else None)
    
    quality_df['credit_score_clean'] = quality_df['Extracted Credit Score'].apply(lambda x: 
        int(x) if x and str(x).isdigit() and 300 <= int(x) <= 850 else None)
    
    quality_df['approval_amount_clean'] = quality_df['Extracted Approval Amount'].apply(lambda x: 
        int(x) if x and str(x).isdigit() and 500 <= int(x) <= 50000 else None)
    
    # Create target variable (1 for approved, 0 for denied)
    quality_df['target'] = quality_df['approval_status'].map({'approved': 1, 'denied': 0})
    
    # Extract additional features from text
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
    
    # Add LLM columns if used
    if use_llm and 'llm_approval_status' in quality_df.columns:
        comprehensive_columns.extend([
            'llm_approval_status', 'llm_confidence', 'llm_income', 
            'llm_credit_score', 'llm_approval_amount', 'llm_reasoning', 'used_llm'
        ])
    
    # Fill missing values for display
    quality_df['income_clean'] = quality_df['income_clean'].fillna('Not extracted')
    quality_df['credit_score_clean'] = quality_df['credit_score_clean'].fillna('Not extracted')
    quality_df['approval_amount_clean'] = quality_df['approval_amount_clean'].fillna('Not extracted')
    
    # Convert boolean columns to Yes/No for readability
    boolean_columns = ['is_student', 'is_first_card', 'has_chase_account', 'mentions_income', 'mentions_credit_score']
    for col in boolean_columns:
        if col in quality_df.columns:
            quality_df[col] = quality_df[col].map({True: 'Yes', False: 'No'})
    
    # Generate output filename if not provided
    if output_file is None:
        method = 'hybrid_llm' if use_llm else 'hybrid_rules'
        output_file = f'data/processed/{method}_dataset.csv'
    
    # Create processed directory if it doesn't exist
    os.makedirs('data/processed', exist_ok=True)
    
    # Save results
    quality_df[comprehensive_columns].to_csv(output_file, index=False)
    
    print(f"Hybrid extraction completed:")
    print(f"- Total posts processed: {len(df)}")
    print(f"- High-quality posts found: {len(quality_df)}")
    print(f"- Approval status breakdown:")
    print(quality_df['approval_status'].value_counts())
    if use_llm and 'used_llm' in quality_df.columns:
        llm_used = quality_df['used_llm'].sum()
        print(f"- LLM validation used for {llm_used} posts")
    print(f"- Saved to: {output_file}")
    
    return output_file

def main():
    """Main function to run the hybrid extractor"""
    import sys
    
    # Parse command line arguments
    use_llm = '--no-llm' not in sys.argv
    confidence_threshold = 5  # Default threshold
    model = "mistral"  # Default model
    
    # Check for custom confidence threshold
    for i, arg in enumerate(sys.argv):
        if arg == '--confidence' and i + 1 < len(sys.argv):
            try:
                confidence_threshold = int(sys.argv[i + 1])
            except ValueError:
                print("Invalid confidence threshold. Using default (5)")
        elif arg == '--model' and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
    
    # Find the most recent raw data file
    raw_files = [f for f in os.listdir('data/raw') if f.endswith('.csv')]
    if not raw_files:
        print("No raw data files found in data/raw/")
        return
    
    # Use the most recent file
    latest_file = sorted(raw_files)[-1]
    input_file = f'data/raw/{latest_file}'
    
    if use_llm:
        print(f"Running hybrid extraction with Ollama LLM validation (model: {model}, confidence threshold: {confidence_threshold})...")
    else:
        print("Running hybrid extraction with rule-based filtering only...")
    
    output_file = hybrid_extract_fields(
        input_file, 
        use_llm=use_llm, 
        confidence_threshold=confidence_threshold,
        model=model
    )
    print(f"Hybrid extraction completed: {output_file}")

if __name__ == "__main__":
    main() 