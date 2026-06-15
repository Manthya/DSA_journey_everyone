
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


122. Best Time to Buy and Sell Stock II

class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        profit = 0
        n = len(prices)

        for i in range(1, n):
            if prices[i]>prices[i-1]:
                profit+=prices[i]-prices[i-1]
        return profit


