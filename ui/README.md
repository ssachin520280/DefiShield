# DefiShield UI

A beautiful React UI for displaying staking recommendations and transaction data from the DefiShield agent.

## Overview

This UI component visualizes the output from the DefiShield agent, presenting staking recommendations and transaction history in an easy-to-understand format. The UI is built with React and Chakra UI, providing a responsive and accessible interface.

## Features

- **Account Summary**: Displays account ID and available balance
- **Staking Recommendation**: Shows personalized staking advice, including:
  - Recommended staking percentage
  - Risk assessment
  - Potential yield
  - Suggested validators with APR rates
- **Transaction History**: Lists recent transactions with detailed information

## Data Structure

The UI expects data in the following JSON format:

```json
{
  "accountId": "example.near",
  "balance": 125.75,
  "recommendation": {
    "summary": "Based on your balance and transaction history, staking with a diversified approach is recommended.",
    "stakingPercentage": 70,
    "riskLevel": "Medium",
    "suggestedValidators": [
      {
        "name": "Validator Name",
        "apr": 10.2,
        "recommendedAmount": 50.3
      }
    ],
    "potentialMonthlyYield": 0.76,
    "riskMitigationStrategy": "Risk mitigation strategy text"
  },
  "transactions": [
    {
      "hash": "transaction-hash",
      "type": "transfer|stake|unstake|swap",
      "timestamp": "ISO timestamp",
      "amount": 15.5,
      "from": "sender.near",
      "to": "recipient.near",
      "status": "Success|Pending|Failed",
      "details": "Optional transaction details"
    }
  ]
}
```

## Integration

To integrate this UI with the actual agent output:

1. Replace the mock data in `src/mockData.js` with the actual data from the agent
2. Ensure the data follows the structure outlined above
3. Adapt the components if needed to match any additional data fields

## Future Improvements

- Add dark/light mode toggle
- Implement filtering and sorting of transactions
- Add graphs to visualize staking performance over time
- Include a dashboard view with key metrics 