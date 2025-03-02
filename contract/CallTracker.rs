// Find all our documentation at https://docs.near.org
use near_sdk::store::LookupMap;
use near_sdk::{env, near, log, require, AccountId, NearToken};

// Define the contract structure
#[near(contract_state)]
pub struct CallTracker {
    call_counts: LookupMap<AccountId, u32>, // Stores the number of calls per user
    fee_per_extra_call: NearToken, // Fee in NEAR for calls beyond 3
}

impl Default for CallTracker {
    fn default() -> Self {
        Self {
            call_counts: LookupMap::new(b"c"),
            fee_per_extra_call: NearToken::from_millinear(10), // 0.01 NEAR
        }
    }
}

#[near]
impl CallTracker {
    // Function to record a user's call
    #[payable] // Allows users to attach NEAR tokens
    pub fn record_call(&mut self) -> String {
        let account_id = env::predecessor_account_id(); // Get the caller's account ID
        let count = self.call_counts.get(&account_id).copied().unwrap_or(0);
        let new_count = count + 1;
        self.call_counts.insert(account_id.clone(), new_count);

        // If user exceeds 3 calls, charge a fee
        if new_count > 3 {
            let attached_deposit = env::attached_deposit();
            require!(
                attached_deposit >= self.fee_per_extra_call,
                format!("Insufficient attached deposit. You must pay {} NEAR after 3 calls.", self.fee_per_extra_call)
            );
        }

        log!("Call recorded for {}. Total calls: {}", account_id, new_count);
        format!("Call recorded. You have called this function {} times.", new_count)
    }

    // View function to check the call count for a given user
    pub fn get_call_count(&self, account_id: AccountId) -> u32 {
        self.call_counts.get(&account_id).copied().unwrap_or(0)
    }
}

/*
 * The rest of this file holds the inline tests for the code above
 * Learn more about Rust tests: https://doc.rust-lang.org/book/ch11-01-writing-tests.html
 */
#[cfg(test)]
mod tests {
    use super::*;
    use near_sdk::test_utils::{accounts, VMContextBuilder};
    use near_sdk::testing_env;

    #[test]
    fn test_record_call() {
        // Setup testing context
        let mut context = VMContextBuilder::new();
        testing_env!(context.predecessor_account_id(accounts(0)).build());
        
        // Create a contract instance
        let mut contract = CallTracker::default();
        
        // First call
        let result = contract.record_call();
        assert!(result.contains("1 times"));
        assert_eq!(contract.get_call_count(accounts(0)), 1);
        
        // Second call
        let result = contract.record_call();
        assert!(result.contains("2 times"));
        assert_eq!(contract.get_call_count(accounts(0)), 2);
    }
}
