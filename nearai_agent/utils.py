import enum
import json
import re
from decimal import Decimal, getcontext, ROUND_DOWN

import base58
import ed25519
import requests
from nearai.agents.environment import Environment
from py_near.account import Account
from py_near.dapps.core import NEAR
from datetime import datetime

STATE_FILE = "state.json"


def convert_from_decimals_to_string(number: float, decimals: int, round_digits: int = 6) -> str:
    getcontext().prec = decimals + 20
    decimal_number = Decimal(number)
    scaled_number = decimal_number / Decimal(10) ** decimals
    rounded_number = scaled_number.quantize(Decimal('1.' + '0' * round_digits), rounding=ROUND_DOWN)

    return str(rounded_number)


class State:
    def __init__(self, **entries):
        self.action = ""
        self.amount = None
        self.receiver_id = None

        self.all_available_tokens = None

        self.__dict__.update(entries)

    def to_dict(self):
        return {k: (v.name if isinstance(v, enum.Enum) else v) for k, v in self.__dict__.items()}

    def to_json(self):
        return json.dumps(self.to_dict())

    def remove_attribute(self, key):
        if key in self.__dict__:
            del self.__dict__[key]  # Use del to remove the attribute
        else:
            print(f"Attribute '{key}' not found in State.")


class AiUtils(object):
    def __init__(self, _env: Environment, _agent):
        self.env = _env
        self.agent = _agent
        self.api_base_url = "https://api.nearblocks.io"

    def get_public_key(self, extended_private_key):
        private_key_base58 = extended_private_key.replace("ed25519:", "")

        decoded = base58.b58decode(private_key_base58)
        secret_key = decoded[:32]

        signing_key = ed25519.SigningKey(secret_key)
        verifying_key = signing_key.get_verifying_key()

        base58_public_key = base58.b58encode(verifying_key.to_bytes()).decode()

        return base58_public_key

    async def get_account_balance(self, account_id):
        """Get account balance using NearBlocks API"""
        url = f"{self.api_base_url}/v1/account/{account_id}"
        # print("URL", url)
        response = requests.get(url)
        # print("RESPONSE", response)
        response.raise_for_status()
        content = response.json()
        # print("CONTENT", content)
        
        # Extract balance from the account data
        account_data = content.get("account", {})[0]
        # print("ACCOUNT DATA", account_data)
        if account_data:
            amount = account_data.get("amount", "0")
            # print("AMOUNT", amount)
            # Convert yoctoNEAR to NEAR (1 NEAR = 10^24 yoctoNEAR)
            balance = float(amount) / 10**24
            return balance
        return 0

    async def get_nearblocks_account_balance(self, account_id):
        """Get account balance using NearBlocks API"""
        url = f"https://api.nearblocks.io/v1/account/{account_id}/balance"
        response = requests.get(url)
        response.raise_for_status()
        content = response.json()
        balance = content.get("balance", 0) / NEAR
        return balance

    def get_nearblocks_account_fts(self, state, account_id):
        """Get fungible tokens using NearBlocks API"""
        url = f"https://api.nearblocks.io/v1/account/{account_id}/ft"
        response = requests.get(url)
        response.raise_for_status()
        content = response.json()
        tokens = content.get("tokens", [])

        print("tokens", tokens)

        if len((state.all_available_tokens or [])) == 0:
            self.get_all_tokens(state)

        for token in tokens:
            token_contract_id = token["contract_id"]
            token_decimals = state.all_available_tokens[token_contract_id]["decimal"] or 0
            token_balance_full = token["balance"] or 0
            if token_decimals and token_balance_full:
                token["balance_hr"] = convert_from_decimals_to_string(token_balance_full, token_decimals)

        return tokens

    def get_account_staking_pools(self, state, account_id):
        url = f"https://api.fastnear.com/v1/account/{account_id}/staking"
        response = requests.get(url)
        response.raise_for_status()
        content = response.json()
        pools = content.get("pools", [])

        print("staking_pools", pools)

        return pools

    def get_nearblocks_staking_info(self, account_id):
        """Get staking information using NearBlocks API"""
        url = f"https://api.nearblocks.io/v1/account/{account_id}/staking"
        response = requests.get(url)
        response.raise_for_status()
        content = response.json()
        staking_info = content.get("staking_info", [])
        
        print("staking_info", staking_info)
        
        return staking_info

    def get_user_message(self, state):
        last_message = self.env.get_last_message()["content"]
        reminder = "Always follow INSTRUCTIONS and produce valid JSON only as explained in OUTPUT format."
        user_message = {"message": f"{last_message}\n{reminder}", "amount": state.amount,
                        "receiver_id": state.receiver_id}

        return {"role": "user", "content": json.dumps(user_message)}

    def get_messages(self, state):
        system_prompt = self.get_data_prompt(state)
        list_messages = self.env.list_messages()
        last_message = list_messages[-1]
        if last_message["role"] == "user":
            list_messages[-1] = self.get_user_message(state)

        messages = [{"role": "system", "content": system_prompt}] + list_messages

        print("PROMPT messages:", messages)

        return messages

    def fetch_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            return data

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
        except json.JSONDecodeError as json_err:
            print(f"JSON decode error: {json_err}")

    def get_all_tokens(self, state: State):
        if not state.all_available_tokens:
            state.all_available_tokens = self.fetch_url("https://api.ref.finance/list-token-price")

        return state.all_available_tokens

    def parse_response(self, response):
        try:
            print("Parsing response", response)
            parsed_response = json.loads(response)
            return parsed_response

        except Exception as err:
            markdown_json_match = re.match(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
            if markdown_json_match:
                response = markdown_json_match.group(1)

            else:
                markdown_match = re.search(r'```(.*?)```', response, re.DOTALL)
                if markdown_match:
                    response = markdown_match.group(1).replace('\n', '').strip()
                else:
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        response = json_match.group(0).replace('\n', '').strip()
            try:
                print("Parsing response", response)
                parsed_response = json.loads(response)
                return parsed_response
            except json.JSONDecodeError:
                try:
                    response = response.replace(";", "")
                    print("Parsing response", response)
                    parsed_response = json.loads(response)
                    return parsed_response
                except json.JSONDecodeError:
                    print(f"JSON decode error: {response}")
                    return {"message": "JSON decode error"}

    def get_state(self):
        all_files = self.env.list_files(self.env.get_agent_temp_path())
        if STATE_FILE in all_files:
            try:
                _state = self.env.read_file(STATE_FILE)
                parsed_dict = json.loads(_state)
                return parsed_dict
            except json.JSONDecodeError:
                return {}
        else:
            return {}

    def save_state(self, state):
        state.remove_attribute('all_available_tokens')
        print("Saving state", state.to_json())
        self.env.write_file(STATE_FILE, state.to_json())

    def get_list_token_prompt(self, state):
        prompt = f"""Below you will find  a list of all available tokens. Format of every entry: 
        NEAR_CONTRACT_ID:{{"price":PRICE_IN_USD_STRING,"symbol":"TOKEN_TICKER","decimal":NUMBER}}


        {self.get_all_tokens(state)}

        """

        return prompt

    
    def get_account_transactions(self, account_id, limit=5):
        """Fetch recent transactions for an account using NearBlocks API"""
        # print("Fetching transactions for account", account_id)
        url = f"{self.api_base_url}/v1/account/{account_id}/txns"
        params = {
            "limit": limit,
            "order": "desc"  # Get most recent transactions
        }
        response = requests.get(url, params=params)
        # print("RESPONSE", response)
        response.raise_for_status()
        content = response.json()
        # print("CONTENT", content)
        
        transactions = content.get("txns", [])
        # print("TRANSACTIONS", transactions)
        return transactions

    def analyze_transactions(self, transactions):
        """Analyze transaction history to determine patterns"""
        if not transactions:
            return {
                "activity_level": "inactive",
                "transaction_types": {},
                "recent_activity": False
            }
        
        # Count transaction types
        tx_types = {}
        recent_timestamp = 0
        
        print("Transactions", transactions)
        for tx in transactions:
            print("TX", tx)
            # Analyze transaction types
            actions = tx.get("actions", [])
            print("Actions", actions)
            for action in actions:
                action_kind = action.get("action", "unknown")
                print("Action Kind", action_kind)
                tx_types[action_kind] = tx_types.get(action_kind, 0) + 1
                print("TX Types", tx_types)
            
            # Check timestamp of most recent transaction
            block_timestamp = int(tx.get("block_timestamp", 0))
            if block_timestamp > recent_timestamp:
                recent_timestamp = block_timestamp
        
        # Determine if there was recent activity (within last 7 days)
        current_time = datetime.now().timestamp() * 1000000000  # Convert to nanoseconds
        recent_activity = (current_time - recent_timestamp) < (7 * 24 * 60 * 60 * 1000000000)
        print("Recent Activity", recent_activity)
        
        # Determine activity level
        if len(transactions) >= 5:
            activity_level = "highly active"
        elif len(transactions) >= 3:
            activity_level = "moderately active"
        elif len(transactions) > 0:
            activity_level = "minimally active"
        else:
            activity_level = "inactive"
            
        return {
            "activity_level": activity_level,
            "transaction_types": tx_types,
            "recent_activity": recent_activity
        }
    
    def make_staking_recommendation(self, balance, transaction_analysis):
        """Determine if staking is recommended based on account activity and balance"""
        # Check for minimum balance requirement (at least 1 NEAR)
        if balance < 1:
            return {
                "recommendation": "not_recommended",
                "reason": "Insufficient balance for staking. A minimum of 1 NEAR is recommended.",
                "confidence": "high"
            }
        
        # Check account activity
        activity_level = transaction_analysis.get("activity_level", "inactive")
        recent_activity = transaction_analysis.get("recent_activity", False)
        tx_types = transaction_analysis.get("transaction_types", {})
        
        # If account is highly active with recent transactions, probably not a good idea to stake all funds
        if activity_level == "highly active" and recent_activity:
            # Check if they have enough balance to stake some and keep some liquid
            if balance > 10:
                return {
                    "recommendation": "partial_stake",
                    "reason": "Your account is very active with recent transactions. Consider staking only a portion of your balance to maintain liquidity for continued activity.",
                    "confidence": "medium",
                    "suggested_amount": round(balance * 0.7, 2)  # Stake 70% of balance
                }
            else:
                return {
                    "recommendation": "not_recommended",
                    "reason": "Your account is very active with recent transactions, and your balance suggests you may need liquidity for continued activity.",
                    "confidence": "medium"
                }
        
        # If account has moderate activity but not recently, good candidate for staking
        if activity_level in ["moderately active", "minimally active"] and not recent_activity:
            return {
                "recommendation": "recommended",
                "reason": "Your account shows some historical activity but has been quiet recently. Staking would be a good way to earn rewards on your idle NEAR.",
                "confidence": "high",
                "suggested_amount": round(balance * 0.9, 2)  # Stake 90% of balance
            }
        
        # If account is inactive or has very little activity, excellent staking candidate
        if activity_level == "inactive" or (activity_level == "minimally active" and not recent_activity):
            return {
                "recommendation": "highly_recommended",
                "reason": "Your account shows minimal activity, making it an excellent candidate for staking to earn rewards on your NEAR.",
                "confidence": "high",
                "suggested_amount": round(balance * 0.95, 2)  # Stake 95% of balance
            }
        
        print("reached here at 371")
        
        # Default recommendation for cases not covered above
        return {
            "recommendation": "recommended",
            "reason": "Based on your balance and account activity, staking appears to be a reasonable option.",
            "confidence": "medium",
            "suggested_amount": round(balance * 0.8, 2)  # Stake 80% of balance
        }
    
    def format_transactions_as_markdown(self, transactions):
        """Format transactions as markdown for display"""
        print("Starting format_transactions_as_markdown")
        print(f"Transactions to format: {len(transactions) if transactions else 0}")
        
        if not transactions:
            print("No transactions to format")
            return "\n\n**No recent transactions found**"
        
        markdown_list = []
        
        for i, tx in enumerate(transactions):
            print(f"Processing transaction {i+1}/{len(transactions)}")
            try:
                # Get transaction hash
                tx_hash = tx.get("transaction_hash", tx.get("hash", "Unknown"))
                print(f"Transaction hash: {tx_hash}")
                
                # Get block timestamp and format it
                block_timestamp = tx.get("block_timestamp", "Unknown")
                if block_timestamp != "Unknown":
                    timestamp = datetime.fromtimestamp(int(block_timestamp) / 1000000000).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    timestamp = "Unknown"
                print(f"Transaction timestamp: {timestamp}")
                
                # Extract transaction details
                actions = tx.get("actions", [])
                print(f"Actions: {actions}")
                action_details = []
                
                if not actions:
                    action_details.append("Unknown action")
                    print("No actions found in transaction")
                
                for action in actions:
                    try:
                        kind = action.get("action", "Unknown")
                        print(f"Action kind: {kind}")
                        args = action.get("args", {})
                        
                        if kind == "TRANSFER":
                            deposit = args.get("deposit", "0")
                            # Convert yoctoNEAR to NEAR
                            amount = float(deposit) / 10**24
                            action_details.append(f"Transfer: {amount} NEAR")
                        elif kind == "FUNCTION_CALL":
                            method_name = args.get("method_name", "Unknown")
                            action_details.append(f"Function: {method_name}")
                        else:
                            action_details.append(kind)
                    except Exception as e:
                        print(f"Error processing action: {e}")
                        action_details.append("Error processing action")
                
                actions_str = ", ".join(action_details) or "No actions"
                print(f"Action string: {actions_str}")
                
                # Get status
                status = tx.get("outcomes", {}).get("status", "Unknown")
                print(f"Status: {status}")
                
                # Build markdown line
                try:
                    markdown_line = (
                        f"- **[{tx_hash[:8]}...](https://nearblocks.io/txns/{tx_hash})** | "
                        f"{actions_str} | "
                        f"Status: {status} | {timestamp}\n"
                    )
                    print(f"Markdown line: {markdown_line}")
                    markdown_list.append(markdown_line)
                except Exception as e:
                    print(f"Error creating markdown line: {e}")
                    markdown_list.append(f"- Error formatting transaction {tx_hash[:8] if tx_hash != 'Unknown' else 'Unknown'}\n")
            
            except Exception as e:
                print(f"Error processing transaction: {e}")
                markdown_list.append("- Error processing transaction\n")
        
        result = "\n" + "\n".join(markdown_list)
        print(f"Final markdown length: {len(result)}")
        return result
    
    def format_recommendation_as_markdown(self, account_id, balance, recommendation):
        """Format the staking recommendation as markdown"""
        print("starting at 433")
        rec_type = recommendation.get("recommendation", "")
        reason = recommendation.get("reason", "")
        confidence = recommendation.get("confidence", "")
        suggested_amount = recommendation.get("suggested_amount", None)
        
        # Create header with appropriate emoji
        if rec_type == "highly_recommended":
            header = "# ✅ Staking is Highly Recommended"
        elif rec_type == "recommended":
            header = "# ✅ Staking is Recommended"
        elif rec_type == "partial_stake":
            header = "# ⚠️ Partial Staking Recommended"
        else:
            header = "# ❌ Staking is Not Recommended"
        
        # Build the full recommendation message
        markdown = f"{header}\n\n"
        markdown += f"**Account:** [{account_id}](https://nearblocks.io/address/{account_id})\n\n"
        markdown += f"**Current Balance:** {balance} NEAR\n\n"
        markdown += f"**Recommendation:** {reason}\n\n"
        
        if suggested_amount:
            markdown += f"**Suggested Staking Amount:** {suggested_amount} NEAR\n\n"
        
        markdown += "## Important Considerations\n\n"
        markdown += "- Staking involves locking up your NEAR tokens\n"
        markdown += "- There is a waiting period when unstaking (typically 2-3 days)\n"
        markdown += "- APY rates vary by validator, typically ranging from 8-12%\n"
        markdown += "- Choose validators carefully - consider their track record and fees\n\n"
        
        markdown += "*This recommendation is provided based on your account's transaction history and balance. Always do your own research before making financial decisions.*"
        
        return markdown
