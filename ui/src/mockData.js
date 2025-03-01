export const mockData = {
  accountId: "example.near",
  balance: 125.75,
  recommendation: {
    summary: "Based on your balance and transaction history, staking with a diversified approach is recommended.",
    stakingPercentage: 70,
    riskLevel: "Medium",
    suggestedValidators: [
      {
        name: "Staked.us",
        apr: 10.2,
        recommendedAmount: 50.3
      },
      {
        name: "Figment",
        apr: 9.8,
        recommendedAmount: 37.725
      }
    ],
    potentialMonthlyYield: 0.76,
    riskMitigationStrategy: "Split your stake between 2-3 validators to minimize risk while maintaining good returns."
  },
  transactions: [
    {
      hash: "9xnaEs5YFGBTyNfRWZQxnM5RyPwEWFLvQCjnNrZqFmZc",
      type: "transfer",
      timestamp: "2023-03-15T12:34:56Z",
      amount: 15.5,
      from: "example.near",
      to: "recipient.near",
      status: "Success"
    },
    {
      hash: "8WM5xHJEZLbJBQgVBza3KQaKPFP7gGKkE4Edp9UJ6vNC",
      type: "stake",
      timestamp: "2023-03-10T09:22:43Z",
      amount: 50,
      from: "example.near",
      to: "validator.poolv1.near",
      status: "Success"
    },
    {
      hash: "CvNnBVsA5Ktqw6GZN2JKTvU1mEE4bh5cXTgCRKGV7mRa",
      type: "unstake",
      timestamp: "2023-02-28T16:45:12Z",
      amount: 20,
      from: "validator.poolv1.near",
      to: "example.near",
      status: "Success"
    },
    {
      hash: "DMayhNoE72hPPzEdXkigC9QdtpEQQbZzzT1PFHKKtDYN",
      type: "transfer",
      timestamp: "2023-02-15T11:04:32Z",
      amount: 5.25,
      from: "friend.near",
      to: "example.near",
      status: "Success"
    },
    {
      hash: "5t6UEipvBAEGMqnGkVjKgZXS4B8ZMVPkQXAWgZUjwEvV",
      type: "swap",
      timestamp: "2023-02-01T08:23:19Z",
      details: "Swap 10 NEAR for 45.5 USDC",
      status: "Success"
    }
  ]
}; 