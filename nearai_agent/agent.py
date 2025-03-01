import asyncio
import re
import traceback
from nearai.agents.environment import Environment
from utils import AiUtils

# Initialize utility helper with environment and agent references
utils = None

async def agent(env: Environment):
    global utils
    print("Starting agent execution")
    if utils is None:
        print("Initializing AiUtils")
        utils = AiUtils(env, agent)
    
    # Get the user's message
    user_message = env.get_last_message()["content"]
    print(f"User message: {user_message}")
    
    # Check if the message contains an account ID (looking for .near or valid account ID format)
    account_id = extract_account_id(user_message)
    print(f"Extracted account_id: {account_id}")
    
    if not account_id:
        # If no account ID is found, ask the user to provide one
        print("No account ID found, asking user to provide one")
        env.add_reply("To provide a staking recommendation, I need your NEAR account ID. Please provide a valid account ID (e.g., 'example.near').")
        return
    
    # Let the user know we're analyzing their account
    print(f"Starting analysis for account: {account_id}")
    env.add_reply(f"Analyzing account {account_id}...\n\nRetrieving balance and recent transactions...")
    
    try:
        # Get account balance
        print("Fetching account balance")
        balance = await utils.get_account_balance(account_id)
        print(f"Account balance: {balance} NEAR")
        
        # Get recent transactions (last 5)
        print("Fetching recent transactions")
        transactions = utils.get_account_transactions(account_id, limit=5)
        print(f"Found {len(transactions)} transactions")
        
        if len(transactions) == 0:
            print("WARNING: No transactions found")
        else:
            print(f"First transaction hash: {transactions[0].get('transaction_hash', 'Unknown')}")
        
        # Analyze transaction patterns
        print("Analyzing transaction patterns")
        transaction_analysis = utils.analyze_transactions(transactions)
        print(f"Transaction analysis: {transaction_analysis}")
        
        # Make staking recommendation based on analysis
        print("Generating staking recommendation")
        recommendation = utils.make_staking_recommendation(balance, transaction_analysis)
        print(f"Recommendation: {recommendation}")
        
        # Format transactions for display
        print("Formatting transactions as markdown")
        tx_markdown = utils.format_transactions_as_markdown(transactions)
        print("Transactions formatted successfully")
        
        # Format the recommendation as markdown
        print("Formatting recommendation as markdown")
        recommendation_markdown = utils.format_recommendation_as_markdown(account_id, balance, recommendation)
        print("Recommendation formatted successfully")
        
        # Add recent transactions section
        print("Building full response")
        full_response = recommendation_markdown + "\n\n## Recent Transactions" + tx_markdown
        print("Full response built successfully")
        
        # Reply to the user with the recommendation
        print("Sending reply to user")
        env.add_reply(full_response)
        print("Reply sent successfully")
        
    except Exception as e:
        print(f"ERROR: Exception occurred: {str(e)}")
        print(traceback.format_exc())
        # Handle any errors that might occur during processing
        env.add_reply(f"Error analyzing account {account_id}: {str(e)}\n\nPlease verify the account ID and try again.")


def extract_account_id(message):
    """Extract NEAR account ID from user message"""
    print(f"Extracting account ID from: {message}")
    
    # Look for .near accounts
    near_pattern = r'([a-zA-Z0-9_-]+\.near)'
    near_match = re.search(near_pattern, message)
    if near_match:
        print(f"Found .near account: {near_match.group(1)}")
        return near_match.group(1)
    
    # Look for account IDs that might be mentioned explicitly
    account_pattern = r'account[:\s]+([a-zA-Z0-9_.-]+)'
    account_match = re.search(account_pattern, message, re.IGNORECASE)
    if account_match:
        print(f"Found explicitly mentioned account: {account_match.group(1)}")
        return account_match.group(1)
    
    # Look for phrases like "analyze xyz" or "check xyz"
    analyze_pattern = r'(?:analyze|check|assess|evaluate|for)[:\s]+([a-zA-Z0-9_.-]+)'
    analyze_match = re.search(analyze_pattern, message, re.IGNORECASE)
    if analyze_match:
        print(f"Found account in analyze pattern: {analyze_match.group(1)}")
        return analyze_match.group(1)
    
    print("No account ID pattern matched")
    return None


print("Script loaded, running agent")
# Run the agent asynchronously
asyncio.run(agent(env))