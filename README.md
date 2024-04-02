# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).


> Path: tokenB->tokenA->tokenD->tokenC->tokenB, tokenB balance = 20.129889
> |Swap    |amountIn |amountOut |
> |----------|----------|-----------|
> |B -> A|5|5.655322|
> |A -> D|5.655322|2.458781|
> |D -> C|2.458781|5.088927|
> |C -> B|5.088927|20.129889
> 
## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

>Slippage is the difference between the expected price and the real price of a trade. There are several reasons that cause slippage in AMM. For example, high-volume trades in an illiquid pool change the ratio of two assets drastically, subsequently changing the price. Besides, transactions in AMM are not instantaneous. The price can change by the time the blockchain confirms the trade. 
> 
> In Uniswap V2, slippage is handled by "amountInMax" or "amountOutMin" in each peripheral function. A case in point is the function swapExactTokensForTokens. At the beginning, it acquires an array "amounts" that stores the amount of token after exchange in each swap. The transaction will be executed if the final amount of token someone receives is greater than the expected value. 
>

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> The value of liquidity pool will grow over time by accumulating trading fee and sending money directly (not through minting) to the pool. This can lead to the senerio that it's impossible for some people to provide liquidity because the minimum quantity of pool shares (1E-18) is too high. 
>
> The attacker can raise the value of liquidity pool share by these steps. First, an attacker initializes a new liquidity pool by providing 10000 wei ETH and 10000 USDT. The pool mints $\sqrt{10000 * 10000} = 10000$ LP tokens. Per LP token worths 1 USTD (regardless of ETH for simplicity). Secondly, the attacker transfers 2000000 USDT to the contract. The LP token now worths about 200 USTD. Thus, the attacker can manipulate the price. Moreover, he can still withdraw all tokens, including those directly transferred into the pool.
>
> To mitigate this issue, 1000 LP (MINIMUM_LIQUIDITY) is minted to zero address from the person initializing the pool, meaning that he can't withdraw all the tokens deposited. Consider the case mentioned, the attacker receive $10000 - 1000 = 9000$ LP tokens. Then he transfers 2000000 USDT to the contract. He can still manipulate the price. However, when he tries to burn LP tokens, all he receives is 1800000 USDT, losing 200000 USTD. The more he transfers into the contract, the more he loses. 

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> The formula is 
> $$
liquidity = min\{\frac{amount0}{reserve0}, \frac{amount1}{reserve1}\} * totalSupply
> $$
> The intuition is that the minting function mints the LP token based on the ratio of the amount of token provided and the reserve. The purpose of minimum function is to encourage liquidity providers to deposit two tokens without changin the proportion of them. For example, if someone only deposits one kind of token, he'll get no LP token.


## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> The procedures are as follows
> 
> 1. A user place a transaction. 
> 2. Front-running: The attacker notices the user's pending transaction due to the transparancy of blockchain. The attacker frontruns him by offering higher gas fee, so the swap can be completed at a lower price. Also, the amount the attacker buys is optimized so that the profit is maximized and the user's transaction won't be reverted. The user's transaction will push the price further.
> 3. Back-runninig: The attacker swaps the token again at a higher price. 
>
> Under such attack, slippage occurs and the user gains less. 
