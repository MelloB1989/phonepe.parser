const transactions = require("./transactions.json");

//console.log(transactions);

const calculate = (transactions) => {
  const per_month = {};
  const per_transaction_detail = {};

  transactions.forEach((transaction) => {
    const month = transaction.Date.split(" ")[0];
    const transaction_str = transaction["Transaction Details"];

    const transaction_detail =
      transaction.Type === "DEBIT"
        ? transaction_str?.replace("Paid to ", "")
        : transaction_str?.replace("Received from ", "");

    // Initialize the month in per_month if it doesn't exist
    if (!per_month[month]) {
      per_month[month] = { spent: 0, earned: 0 };
    }
    if (!per_transaction_detail[transaction_detail]) {
      per_transaction_detail[transaction_detail] = { spent: 0, earned: 0 };
    }

    // Update the spent or earned amount based on the transaction type
    if (transaction.Type === "DEBIT") {
      per_month[month].spent += transaction.Amount;
      per_transaction_detail[transaction_detail].spent += transaction.Amount;
    } else {
      per_month[month].earned += transaction.Amount;
      per_transaction_detail[transaction_detail].earned += transaction.Amount;
    }
  });

  console.log(per_month);
  const selectedKeys = [
    "Aparna AU LOTUS",
    "Rahul Tech Team Noobs ⚡",
    "Abhinav Tech Team Noobs ⚡",
    "Manas NBL CC TECH TEAM",
    "Aymaan~ NBL TECH",
  ];
  // Initialize the final result object
  const result = {};

  // Initialize totals for "Others"
  let othersSpent = 0;
  let othersEarned = 0;

  // Iterate over the keys of the original map
  for (const key in per_transaction_detail) {
    if (selectedKeys.includes(key)) {
      // If the key is in the selected keys, add it to the result as is
      result[key] = per_transaction_detail[key];
    } else {
      // If not, add the spent and earned to the totals for "Others"
      othersSpent += per_transaction_detail[key].spent;
      othersEarned += per_transaction_detail[key].earned;
    }
  }

  // Add the "Others" key to the result with the accumulated totals
  result["Others"] = { spent: othersSpent, earned: othersEarned };
  console.log(result);
};

calculate(transactions);
