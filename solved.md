
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

3. Longest Substring Without Repeating Characters
tip : hashmap of string in inout and therir updated index
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        has = {}
        start=0
        max_len=0
        
        for i in range(len(s)):
            if s[i] in has and has[s[i]] >=start:
                start = has[s[i]]+1
            has[s[i]] = i
            max_len = max(max_len, i-start+1)
        return max_len        Use a separate solved.html — I can generate it from solved.md automatically every time you add a question (you rejected this, but it's the only way to get a true button-on-same-line behavior)