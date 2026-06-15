
121. Best Time to Buy and Sell Stock
tip : normal max profit calclualation 
class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        profit = 0
        MinPrice = prices[0]
        for i in range(1, len(prices)):

            if MinPrice>=prices[i]:
                MinPrice=prices[i]
            else:
                profit = max(profit, prices[i]-MinPrice)

        return profit
        